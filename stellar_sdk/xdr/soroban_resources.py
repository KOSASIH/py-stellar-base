# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .ledger_footprint import LedgerFootprint
from .uint32 import Uint32

__all__ = ["SorobanResources"]


class SorobanResources:
    """
    XDR Source Code::

        struct SorobanResources
        {
            // The ledger footprint of the transaction.
            LedgerFootprint footprint;
            // The maximum number of instructions this transaction can use
            uint32 instructions;

            // The maximum number of bytes this transaction can read from ledger
            uint32 readBytes;
            // The maximum number of bytes this transaction can write to ledger
            uint32 writeBytes;

            // Maximum size of dynamic metadata produced by this contract (
            // currently only includes the events).
            uint32 extendedMetaDataSizeBytes;
        };
    """

    def __init__(
        self,
        footprint: LedgerFootprint,
        instructions: Uint32,
        read_bytes: Uint32,
        write_bytes: Uint32,
        extended_meta_data_size_bytes: Uint32,
    ) -> None:
        self.footprint = footprint
        self.instructions = instructions
        self.read_bytes = read_bytes
        self.write_bytes = write_bytes
        self.extended_meta_data_size_bytes = extended_meta_data_size_bytes

    def pack(self, packer: Packer) -> None:
        self.footprint.pack(packer)
        self.instructions.pack(packer)
        self.read_bytes.pack(packer)
        self.write_bytes.pack(packer)
        self.extended_meta_data_size_bytes.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SorobanResources:
        footprint = LedgerFootprint.unpack(unpacker)
        instructions = Uint32.unpack(unpacker)
        read_bytes = Uint32.unpack(unpacker)
        write_bytes = Uint32.unpack(unpacker)
        extended_meta_data_size_bytes = Uint32.unpack(unpacker)
        return cls(
            footprint=footprint,
            instructions=instructions,
            read_bytes=read_bytes,
            write_bytes=write_bytes,
            extended_meta_data_size_bytes=extended_meta_data_size_bytes,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanResources:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SorobanResources:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.footprint == other.footprint
            and self.instructions == other.instructions
            and self.read_bytes == other.read_bytes
            and self.write_bytes == other.write_bytes
            and self.extended_meta_data_size_bytes
            == other.extended_meta_data_size_bytes
        )

    def __str__(self):
        out = [
            f"footprint={self.footprint}",
            f"instructions={self.instructions}",
            f"read_bytes={self.read_bytes}",
            f"write_bytes={self.write_bytes}",
            f"extended_meta_data_size_bytes={self.extended_meta_data_size_bytes}",
        ]
        return f"<SorobanResources [{', '.join(out)}]>"
