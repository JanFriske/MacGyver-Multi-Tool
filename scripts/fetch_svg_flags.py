"""
Script to download high-quality SVG flags for a list of country/language codes.

Usage:
    python scripts/fetch_svg_flags.py en_GB en_US de fr gd sco

By default this script will try the following sources in order:
 1) FlagCDN: https://flagcdn.com/{size}/{cc}.svg or https://flagcdn.com/{cc}.svg (cc lower-case)
 2) Wikimedia Commons: a set of known file URLs (fallback mapping)

Notes:
- For subnational flags (e.g. Scotland) we try Wikimedia-known urls.
- This script requires `requests` to be installed in your environment.
- Run from project root. Downloads are saved to `assets/flags/svg/{code}.svg`.

This tool does network I/O. Run only if you agree to download files.
"""
from pathlib import Path
import sys
import requests

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assets" / "flags" / "svg"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Fallback mapping for language codes -> country ISO or specific SVG URL
SPECIAL_MAP = {
    "en_GB": ("gb", None),
    "en_US": ("us", None),
    "de": ("de", None),
    "fr": ("fr", None),
    "gd": (None, "https://upload.wikimedia.org/wikipedia/commons/1/10/Flag_of_Scotland.svg"),
    "sco": (None, "https://upload.wikimedia.org/wikipedia/commons/1/10/Flag_of_Scotland.svg"),
}

FLAGCDN_BASE = "https://flagcdn.com"

HEADERS = {
    "User-Agent": "MacGyver-Multi-Tool/1.0 (+https://example.invalid)"
}


def try_download_svg(cc: str, out_path: Path) -> bool:
    """Try to download an SVG from flagcdn (lowercase cc)."""
    urls = [f"{FLAGCDN_BASE}/w320/{cc}.png", f"{FLAGCDN_BASE}/32x24/{cc}.png", f"{FLAGCDN_BASE}/{cc}.svg"]
    for url in urls:
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code == 200 and r.content:
                out_path.write_bytes(r.content)
                print(f"Downloaded {url} -> {out_path}")
                return True
        except Exception as e:
            # continue trying other urls
            pass
    return False


def try_download_url(url: str, out_path: Path) -> bool:
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200 and r.content:
            out_path.write_bytes(r.content)
            print(f"Downloaded {url} -> {out_path}")
            return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
    return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide one or more language/country codes. Example: en_GB en_US gd sco")
        sys.exit(1)

    codes = sys.argv[1:]
    for code in codes:
        out = OUT_DIR / f"{code}.svg"
        # If already exists, skip
        if out.exists():
            print(f"Skipping {code}: {out} already exists")
            continue

        mapped = SPECIAL_MAP.get(code)
        if mapped:
            cc, url = mapped
        else:
            # Heuristic: try first two letters lowercased as cc
            cc = code.split('_')[0].lower()
            url = None

        downloaded = False
        if cc:
            downloaded = try_download_svg(cc, out)
        if not downloaded and url:
            downloaded = try_download_url(url, out)
        if not downloaded:
            print(f"Could not download flag for {code}. Consider adding custom SVG to assets/flags/svg/{code}.svg")

    print("Done.")
