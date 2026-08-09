#!/usr/bin/env python3
"""The UID format the wall units' built-in reader produces.

The wall unit has an RFID-to-keyboard-wedge that types a **decimal** number,
not hex. The digits are the UID's bytes read least-significant-byte first:

    card UID bytes   A1 B2 C3 D4        (as an ACR122U returns them)
    reversed         D4 C3 B2 A1
    as an integer    0xD4C3B2A1
    typed            3569595041

wallet/services/cards.py decodes it by exactly reversing that, so a bench tool
that types plain hex produces a different string from the one the wall reader
would produce for the same card. Both are accepted by the search box, but a
card enrolled from one form and presented in the other has bitten us before,
so the bench tools now emit what the wall units emit.

Kept import-free so it can be unit tested without a reader or pyscard.
"""


def uid_bytes_to_wedge_decimal(uid_bytes):
    """Bytes from a GET UID response -> the decimal string a wall reader types.

    Little-endian on purpose: it is the byte order the wall readers use, and
    getting it backwards yields a plausible-looking number that resolves to a
    completely different card.
    """
    raw = bytes(bytearray(uid_bytes))
    if not raw:
        raise ValueError("Empty UID")
    total = 0
    for index, byte in enumerate(bytearray(raw)):
        total |= byte << (8 * index)
    return str(total)


def uid_bytes_to_hex(uid_bytes):
    """The same UID as the hex string the wallet stores, e.g. A1B2C3D4."""
    return "".join("{:02X}".format(byte) for byte in bytearray(bytes(bytearray(uid_bytes))))


def format_uid(uid_bytes, style="decimal"):
    if style == "hex":
        return uid_bytes_to_hex(uid_bytes)
    if style == "decimal":
        return uid_bytes_to_wedge_decimal(uid_bytes)
    raise ValueError("Unknown UID format: {}".format(style))


if __name__ == "__main__":
    # A quick self-check without a reader:
    #   python3 linux-host/wedge_uid.py
    for hex_uid, expected in (
        ("A1B2C3D4", "3569595041"),
        ("DEADC0DE01", "8032136670"),
        ("0BADBEEF", "4022250763"),
    ):
        raw = bytearray.fromhex(hex_uid)
        got = uid_bytes_to_wedge_decimal(raw)
        print("{:<12} -> {:<14} {}".format(hex_uid, got, "OK" if got == expected else "MISMATCH"))
