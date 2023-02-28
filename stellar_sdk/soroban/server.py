from __future__ import annotations

import uuid
from typing import Type, TYPE_CHECKING

from .exceptions import RequestException
from .jsonrpc import *
from .soroban_rpc import *
from .. import xdr as stellar_xdr
from ..account import Account
from ..client.base_sync_client import BaseSyncClient
from ..client.requests_client import RequestsClient

if TYPE_CHECKING:
    from ..transaction_envelope import TransactionEnvelope

__all__ = ["SorobanServer"]

V = TypeVar("V")


class SorobanServer:
    """Server handles the network connection to a Soroban RPC instance and
    exposes an interface for requests to that instance.

    :param server_url: Soroban RPC server URL. (ex. ``https://horizon-futurenet.stellar.org:443/soroban/rpc``)
    :param client: A client instance that will be used to make requests.
    """

    def __init__(
        self,
        server_url: str = "https://horizon-futurenet.stellar.org:443/soroban/rpc",
        client: Optional[BaseSyncClient] = None,
    ) -> None:
        self.server_url: str = server_url

        if not client:
            client = RequestsClient()
        self._client: BaseSyncClient = client

    def get_health(self) -> GetHealthResponse:
        """General node health check.

        See `Soroban Documentation - getHealth <https://soroban.stellar.org/api/methods/getHealth>`_

        :return: A :class:`GetHealthResponse <stellar_sdk.soroban_rpc.get_health.GetHealthResponse>` object.
        """
        request: Request = Request(
            id=_generate_unique_request_id(),
            method="getHealth",
        )
        return self._post(request, GetHealthResponse)

    def get_account(self, account_id: str) -> GetAccountResponse:
        """Fetch a minimal set of current info about a Stellar account.

        See `Soroban Documentation - getAccount <https://soroban.stellar.org/api/methods/getAccount>`_

        :return: A :class:`GetAccountResponse <stellar_sdk.soroban_rpc.get_account.GetAccountResponse>` object.
        """
        request = Request[GetAccountRequest](
            id=_generate_unique_request_id(),
            method="getAccount",
            params=GetAccountRequest(address=account_id),
        )
        return self._post(request, GetAccountResponse)

    def get_events(
        self,
        start_ledger: int,
        end_ledger: int,
        filters: Sequence[EventFilter] = None,
        cursor: str = None,
        limit: int = None,
    ) -> GetEventsResponse:
        """Fetch a list of events that occurred in the ledger range.

        See `Soroban Documentation - getEvents <https://soroban.stellar.org/api/methods/getEvents>`_

        :param start_ledger: The first ledger to include in the results.
        :param end_ledger: The last ledger to include in the results.
        :param filters: A list of filters to apply to the results.
        :param cursor: A cursor value for use in pagination.
        :param limit: The maximum number of records to return.
        :return: A :class:`GetEventsResponse <stellar_sdk.soroban_rpc.get_events.GetEventsResponse>` object.
        """
        pagination = PaginationOptions(cursor=cursor, limit=limit)
        data = GetEventsRequest(
            startLedger=start_ledger,
            endLedger=end_ledger,
            filters=filters,
            pagination=pagination,
        )
        request: Request = Request[GetEventsRequest](
            id=_generate_unique_request_id(), method="getEvents", params=data
        )
        return self._post(request, GetEventsResponse)

    def get_network(self) -> GetNetworkResponse:
        """General info about the currently configured network.

        :return: A :class:`GetNetworkResponse <stellar_sdk.soroban_rpc.get_network.GetNetworkResponse>` object.
        """
        request: Request = Request(
            id=_generate_unique_request_id(),
            method="getNetwork",
        )
        return self._post(request, GetNetworkResponse)

    def get_ledger_entry(self, key: stellar_xdr.LedgerKey) -> GetLedgerEntryResponse:
        """For reading the current value of ledger entries directly.
        Allows you to directly inspect the current state of a contract, a contract's code,
        or any other ledger entry. This is a backup way to access your contract data
        which may not be available via events or simulateTransaction.

        See `Soroban Documentation - getLedgerEntry <https://soroban.stellar.org/api/methods/getLedgerEntry>`_

        :param key: The ledger key to fetch.
        :return: A :class:`GetLedgerEntryResponse <stellar_sdk.soroban_rpc.get_ledger_entry.GetLedgerEntryResponse>` object.
        """
        # TODO: Split it into multiple points
        request = Request[GetLedgerEntryRequest](
            id=_generate_unique_request_id(),
            method="getLedgerEntry",
            params=GetLedgerEntryRequest(key=key.to_xdr()),
        )
        return self._post(request, GetLedgerEntryResponse)

    def get_transaction_status(
        self, transaction_hash: str
    ) -> GetTransactionStatusResponse:
        """Fetch the status of a transaction.

        See `Soroban Documentation - getTransactionStatus <https://soroban.stellar.org/api/methods/getTransactionStatus>`_

        :param transaction_hash: The hash of the transaction to fetch.
        :return: A :class:`GetTransactionStatusResponse <stellar_sdk.soroban_rpc.get_transaction_status.GetTransactionStatusResponse>` object.
        """
        request = Request[GetTransactionStatusRequest](
            id=_generate_unique_request_id(),
            method="getTransactionStatus",
            params=GetTransactionStatusRequest(hash=transaction_hash),
        )
        return self._post(request, GetTransactionStatusResponse)

    def simulate_transaction(
        self, transaction_envelope: Union[TransactionEnvelope, str]
    ) -> SimulateTransactionResponse:
        """Submit a trial contract invocation to get back return values, expected ledger footprint, and expected costs.

        See `Soroban Documentation - simulateTransaction <https://soroban.stellar.org/api/methods/simulateTransaction>`_

        :param transaction_envelope: The transaction to simulate.
        :return: A :class:`SimulateTransactionResponse <stellar_sdk.soroban_rpc.simulate_transaction.SimulateTransactionResponse>` object.
        """
        xdr = (
            transaction_envelope
            if isinstance(transaction_envelope, str)
            else transaction_envelope.to_xdr()
        )
        request = Request[SimulateTransactionRequest](
            id=_generate_unique_request_id(),
            method="simulateTransaction",
            params=SimulateTransactionRequest(transaction=xdr),
        )
        # TODO: error? request.error is None, request.result.error is not None
        return self._post(request, SimulateTransactionResponse)

    def send_transaction(
        self, transaction_envelope: Union[TransactionEnvelope, str]
    ) -> SendTransactionResponse:
        """Submit a real transaction to the Stellar network. This is the only way to make changes "on-chain".

        See `Soroban Documentation - sendTransaction <https://soroban.stellar.org/api/methods/sendTransaction>`_

        :param transaction_envelope: The transaction to send.
        :return: A :class:`SendTransactionResponse <stellar_sdk.soroban_rpc.send_transaction.SendTransactionResponse>` object.
        """
        xdr = (
            transaction_envelope
            if isinstance(transaction_envelope, str)
            else transaction_envelope.to_xdr()
        )
        request = Request[SendTransactionRequest](
            id=_generate_unique_request_id(),
            method="sendTransaction",
            params=SendTransactionRequest(transaction=xdr),
        )
        return self._post(request, SendTransactionResponse)

    def load_account(self, account_id: str) -> Account:
        """Load an account from the server, you can use the returned account
        object as source account for transactions.

        :param account_id: The account ID.
        :return: An :class:`Account <stellar_sdk.account.Account>` object.
        """
        data = self.get_account(account_id)
        return Account(account_id, data.sequence)

    def close(self) -> None:
        """Close underlying connector, and release all acquired resources."""
        self._client.close()

    def _post(self, request_body: Request, response_body_type: Type[V]) -> V:
        json_data = request_body.dict(by_alias=True)
        data = self._client.post(
            self.server_url,
            json_data=json_data,
        )
        response = Response[response_body_type, str].parse_obj(data.json())  # type: ignore[valid-type]
        if response.error:
            raise RequestException(response.error.code, response.error.message)
        return response.result  # type: ignore[return-value]

    def __enter__(self) -> "SorobanServer":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __str__(self):
        return f"<SorobanServer [server_url={self.server_url}, client={self._client}]>"


def _generate_unique_request_id() -> str:
    return uuid.uuid4().hex
