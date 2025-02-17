"""
This example shows how to parse xdr string into an `TransactionEnvelope` or `FeeBumpTransactionEnvelope` object.
"""

from stellar_sdk import Network, parse_transaction_envelope_from_xdr

envelope_xdr = "AAAAAgAAAAA/45aQQk1+d6IL7bNNkcp+RozuoMdKlt/9wEQfoDof5wAAJxMCGnPkAA2u7QAAAAEAAAAAAAAAAAAAAABhdLGrAAAAAAAAAAEAAAAAAAAAAwAAAAAAAAABTlVDAAAAAABHvhbThHM7avImj3g6LQVSzQochVCKxGel70Vauq+6ZAAAAAAAQVaQCOBySxCQbi4AAAAAMZEL/AAAAAAAAAABoDof5wAAAEBdCGhS739T8xDpDbeuXZhvRFUMjviADruYhqY+AhDsvpQ32Gpj7arUvPx07OPCXjEfpZHdPi+18WuK1mJ0MSUM"
transaction_envelope = parse_transaction_envelope_from_xdr(
    envelope_xdr, Network.PUBLIC_NETWORK_PASSPHRASE
)
print(transaction_envelope)
