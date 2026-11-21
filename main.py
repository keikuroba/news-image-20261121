#!/usr/bin/env python3
"""news-image-20261121 entrypoint.

Copies the bundled front page (assets/entry.png) to /output/entry.png
after fully validating the PNG: magic, every chunk CRC, IHDR size,
IDAT data inflating to exactly the size the header promises, and
nothing after the IEND chunk. Then reads the written file back and
checks its SHA-256 matches the source, so a bad write is never silent.

Standard library only. No network, no clock, no randomness: two runs
write byte-identical output.
"""
import hashlib
import os
import struct
import sys
import zlib

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "entry.png")
MAX_BYTES = 1048576
EXPECT_W, EXPECT_H = 1024, 1024


def fail(msg):
    print(f"entry: error: {msg}", file=sys.stderr)
    raise SystemExit(1)


def check_png(data):
    if len(data) > MAX_BYTES:
        fail(f"image is {len(data)} bytes, over the 1 MiB limit")
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("not a PNG (bad magic)")
    pos = 8
    seen_ihdr = False
    seen_iend = False
    idat = bytearray()
    width = height = None
    bit_depth = color_type = None
    while pos < len(data):
        if pos + 8 > len(data):
            fail("truncated chunk header")
        length, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        end = pos + 8 + length + 4
        if end > len(data):
            fail(f"truncated {ctype!r} chunk")
        payload = data[pos + 8:pos + 8 + length]
        crc_stored, = struct.unpack(">I", data[pos + 8 + length:end])
        crc_real = zlib.crc32(ctype + payload) & 0xFFFFFFFF
        if crc_real != crc_stored:
            fail(f"{ctype!r} chunk CRC mismatch")
        if ctype == b"IHDR":
            if seen_ihdr:
                fail("duplicate IHDR")
            if length != 13:
                fail("IHDR has wrong length")
            width, height, bit_depth, color_type = struct.unpack(
                ">IIBB", payload[:10])
            if (width, height) != (EXPECT_W, EXPECT_H):
                fail(f"image is {width}x{height}, expected "
                     f"{EXPECT_W}x{EXPECT_H}")
            seen_ihdr = True
        elif ctype == b"IDAT":
            idat += payload
        elif ctype == b"IEND":
            if length != 0:
                fail("IEND carries data")
            seen_iend = True
            pos = end
            break
        pos = end
    if not seen_ihdr:
        fail("no IHDR chunk")
    if not seen_iend:
        fail("no IEND chunk")
    if pos != len(data):
        fail(f"{len(data) - pos} trailing byte(s) after IEND")
    if not idat:
        fail("no IDAT data")
    try:
        raw = zlib.decompress(bytes(idat))
    except zlib.error as exc:
        fail(f"IDAT does not inflate: {exc}")
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}.get(color_type)
    if channels is None:
        fail(f"unsupported PNG colour type {color_type}")
    bits = bit_depth * channels
    row_bits = width * bits
    row_bytes = (row_bits + 7) // 8
    if len(raw) != height * (row_bytes + 1):
        fail(f"inflated pixel data is {len(raw)} bytes, expected "
             f"{height * (row_bytes + 1)}")
    return width, height


def main():
    if not os.path.isfile(SOURCE):
        fail(f"bundled image missing: {SOURCE}")
    with open(SOURCE, "rb") as fh:
        data = fh.read()
    width, height = check_png(data)
    outdir = (os.environ.get("MAKEFUN_OUTPUT_DIR")
              or os.environ.get("ENTRY_OUTPUT_DIR")
              or "/output")
    os.makedirs(outdir, exist_ok=True)
    target = os.path.join(outdir, "entry.png")
    with open(target, "wb") as fh:
        fh.write(data)
    with open(target, "rb") as fh:
        written = fh.read()
    if hashlib.sha256(written).hexdigest() != \
            hashlib.sha256(data).hexdigest():
        fail("written file digest differs from source")
    print(f"entry: wrote {target} ({width}x{height}, "
          f"{len(data)} bytes, sha256 "
          f"{hashlib.sha256(data).hexdigest()[:16]}...)")


if __name__ == "__main__":
    main()
