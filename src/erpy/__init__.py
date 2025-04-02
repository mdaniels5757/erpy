from term import codec
from term.basetypes import Term
from typing import Generator

import struct
# import sys


def _mailbox_gen() -> Generator[Term, None, None]:
    input_stream = open(3, "rb")
    while True:
        len_bin = input_stream.read(4)
        if len(len_bin) != 4:
            return None
        (length,) = struct.unpack("!I", len_bin)
        (term, rest) = codec.decode(input_stream.read(length))
        yield term


def _port_gen() -> Generator[None, Term, None]:
    output_stream = open(4, "wb")
    while True:
        term = codec.encode((yield))
        output_stream.write(struct.pack("!I", len(term)))
        output_stream.write(term)


def stdio_port_connection() -> (
    tuple[Generator[Term, None, None], Generator[None, Term, None]]
):
    port = _port_gen()
    next(port)
    return _mailbox_gen(), port
