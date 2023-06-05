"""This example demonstrates how to invoke an auth contract with [Stellar Account] authrization.

See https://soroban.stellar.org/docs/how-to-guides/auth
See https://soroban.stellar.org/docs/learn/authorization#stellar-account
"""

import time

from stellar_sdk import (
    Network,
    Keypair,
    TransactionBuilder,
)
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.soroban import SorobanServer, ContractAuth, AuthorizedInvocation
from stellar_sdk.soroban.soroban_rpc import GetTransactionStatus
from stellar_sdk.soroban.types import Uint32, Address

rpc_server_url = "https://rpc-futurenet.stellar.org:443/"
soroban_server = SorobanServer(rpc_server_url)
network_passphrase = Network.FUTURENET_NETWORK_PASSPHRASE

# https://github.com/stellar/soroban-examples/tree/v0.6.0/auth
contract_id = "56478cfb5fc59c132706ff088c96753a8710604e2a9c852783721646db7222e4"
tx_submitter_kp = Keypair.from_secret(
    "SAAPYAPTTRZMCUZFPG3G66V4ZMHTK4TWA6NS7U4F7Z3IMUD52EK4DDEV"
)
# If tx_submitter_kp and op_invoker_kp use the same account, the submission will fail, a bug?
op_invoker_kp = Keypair.from_secret(
    "SAEZSI6DY7AXJFIYA4PM6SIBNEYYXIEM2MSOTHFGKHDW32MBQ7KVO6EN"
)

nonce = soroban_server.get_nonce(contract_id, op_invoker_kp.public_key)
func_name = "increment"
args = [Address(op_invoker_kp.public_key), Uint32(10)]

invocation = AuthorizedInvocation(
    contract_id=contract_id,
    function_name=func_name,
    args=args,
    sub_invocations=[],
)

contract_auth = ContractAuth(
    address=Address(op_invoker_kp.public_key),
    nonce=nonce,
    root_invocation=invocation,
)

contract_auth.sign(op_invoker_kp, network_passphrase)

source = soroban_server.load_account(tx_submitter_kp.public_key)
tx = (
    TransactionBuilder(source, network_passphrase)
    .add_time_bounds(0, 0)
    .append_invoke_contract_function_op(
        contract_id=contract_id,
        function_name=func_name,
        parameters=args,
        auth=[contract_auth],
    )
    .build()
)

tx = soroban_server.prepare_transaction(tx)
tx.sign(tx_submitter_kp)
print(f"Signed XDR:\n{tx.to_xdr()}")

send_transaction_data = soroban_server.send_transaction(tx)
print(f"sent transaction: {send_transaction_data}")

while True:
    print("waiting for transaction to be confirmed...")
    get_transaction_data = soroban_server.get_transaction(send_transaction_data.hash)
    if get_transaction_data.status != GetTransactionStatus.NOT_FOUND:
        break
    time.sleep(3)

print(f"transaction: {get_transaction_data}")

if get_transaction_data.status == GetTransactionStatus.SUCCESS:
    assert get_transaction_data.result_meta_xdr is not None
    transaction_meta = stellar_xdr.TransactionMeta.from_xdr(
        get_transaction_data.result_meta_xdr
    )
    result = transaction_meta.v3.tx_result.result.results[0].tr.invoke_host_function_result.success[0]  # type: ignore
    print(f"Function result: {result}")
