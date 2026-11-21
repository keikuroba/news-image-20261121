#!/usr/bin/env python3
"""news-image-20261121: write the bundled front page to the output path.

The artwork lives in the repository at assets/entry.png. This program
checks it is a well-formed PNG of the size the competition asks for
(1024 by 1024, at most 1 MiB), copies it to /output/entry.png (or the
directory named by MAKEFUN_OUTPUT_DIR / ENTRY_OUTPUT_DIR), and then
reads the copy back to confirm its SHA-256 is unchanged.

Only the standard library is used. There is no network access, no
clock and no randomness anywhere in this program, so running it twice
produces exactly the same bytes.
"""
from pathlib import Path
import hashlib
import os
import struct
import sys
import zlib

HERE = Path(__file__).resolve().parent
ARTWORK = HERE / "assets" / "entry.png"
LIMIT_BYTES = 1_048_576
SIZE = (1024, 1024)
MAGIC = b"\x89PNG\r\n\x1a\n"
# PNG colour type -> channels per pixel
CHANNELS = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}


def reject(reason):
    print(f"reject: {reason}", file=sys.stderr)
    raise SystemExit(1)


def iter_chunks(blob):
    """Yield (kind, payload) for each chunk in blob, checking CRCs."""
    pos = len(MAGIC)
    while pos < len(blob):
        if pos + 8 > len(blob):
            reject("chunk header cut off")
        size, kind = struct.unpack(">I4s", blob[pos:pos + 8])
        stop = pos + 8 + size + 4
        if stop > len(blob):
            reject(f"chunk {kind!r} cut off")
        payload = blob[pos + 8:pos + 8 + size]
        stored, = struct.unpack(">I", blob[pos + 8 + size:stop])
        if zlib.crc32(kind + payload) & 0xFFFFFFFF != stored:
            reject(f"chunk {kind!r} has a bad CRC")
        yield kind, payload
        pos = stop
        if kind == b"IEND":
            if pos != len(blob):
                reject(f"{len(blob) - pos} byte(s) past IEND")
            return
    reject("image ends without an IEND chunk")


def validate(blob):
    """Check the artwork; return (width, height)."""
    if len(blob) > LIMIT_BYTES:
        reject(f"artwork is {len(blob)} bytes, over the 1 MiB limit")
    if blob[:8] != MAGIC:
        reject("not a PNG: bad signature")
    width = height = None
    depth = ctype = None
    seen_header = False
    saw_pixels = False
    for kind, payload in iter_chunks(blob):
        if kind == b"IHDR":
            if seen_header:
                reject("two IHDR chunks")
            if len(payload) != 13:
                reject("IHDR is the wrong length")
            width, height, depth, ctype = struct.unpack(">IIBB",
                                                       payload[:10])
            if (width, height) != SIZE:
                reject(f"artwork is {width}x{height}, want "
                       f"{SIZE[0]}x{SIZE[1]}")
            seen_header = True
        elif kind == b"IDAT":
            saw_pixels = True
        elif kind == b"IEND":
            if len(payload) != 0:
                reject("IEND carries payload")
    if not seen_header:
        reject("no IHDR chunk")
    if not saw_pixels:
        reject("no IDAT chunk")
    if ctype not in CHANNELS:
        reject(f"colour type {ctype} is not supported")
    return width, height


def main():
    if not ARTWORK.is_file():
        reject(f"bundled artwork missing: {ARTWORK}")
    blob = ARTWORK.read_bytes()
    width, height = validate(blob)
    digest = hashlib.sha256(blob).hexdigest()
    outdir = (os.environ.get("MAKEFUN_OUTPUT_DIR")
              or os.environ.get("ENTRY_OUTPUT_DIR")
              or "/output")
    Path(outdir).mkdir(parents=True, exist_ok=True)
    target = Path(outdir) / "entry.png"
    target.write_bytes(blob)
    if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
        reject("copy on disk differs from the bundled artwork")
    print(f"wrote {target} ({width}x{height}, {len(blob)} bytes, "
          f"sha256 {digest[:16]}...)")


if __name__ == "__main__":
    main()
