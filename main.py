"""The World Today — news-image-20261124.

Entry program for the make.fun competition "Sum up 24 November's world
news in one image". The finished one-page front page lives in this repo
as entry.png; this program copies it byte-for-byte to /output/entry.png
so the grader gets exactly the image that was built and reviewed.

Standard library only. No network, no randomness, no timestamps: running
it twice produces identical bytes.
"""

import hashlib
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
DESTINATION = Path("/output/entry.png")
MAX_BYTES = 1_048_576  # competition cap: entry.png must be at most 1 MiB


PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
EXPECTED_SHA256 = "5437f958e531dc0ba86e8539766fd07b50f3d1cbbfc2de5adf41a19e3bb4f481"  # the reviewed front page


def main() -> None:
    data = SOURCE.read_bytes()
    if not data.startswith(PNG_MAGIC):
        raise SystemExit("entry.png is not a whole PNG file")
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        raise SystemExit("entry.png is not the reviewed front page")
    if len(data) > MAX_BYTES:
        raise SystemExit(
            f"entry.png is {len(data)} bytes, over the {MAX_BYTES} byte cap"
        )
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_bytes(data)
    if DESTINATION.read_bytes() != data:
        raise SystemExit(f"{DESTINATION} does not match {SOURCE}")
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {DESTINATION} ({len(data)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
