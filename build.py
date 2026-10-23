"""Build artifact.html and index.html from src/holmerud.html by inlining the HOLMERUD oak texture.

Usage: python3 build.py [--local DIR]
  --local DIR  also write DIR/test.html with three.js served from DIR/node_modules (for offline checks)
"""
import base64
import pathlib
import sys

ROOT = pathlib.Path(__file__).parent
CDN = "https://cdn.jsdelivr.net/npm/three@0.160.0/"


def build():
    html = (ROOT / "src" / "holmerud.html").read_text(encoding="utf-8")
    oak = base64.b64encode((ROOT / "src" / "holmerud-oak.jpg").read_bytes()).decode()
    out = html.replace("__OAK__", oak)
    # artifact.html is the page body the Artifact viewer wraps; index.html opens standalone in any browser.
    (ROOT / "artifact.html").write_text(out, encoding="utf-8")
    page = '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n</head>\n<body>\n' + out + '\n</body>\n</html>\n'
    (ROOT / "index.html").write_text(page, encoding="utf-8")
    print(f"index.html: {len(page) / 1024:.0f} KB")
    if "--local" in sys.argv:
        local_dir = pathlib.Path(sys.argv[sys.argv.index("--local") + 1])
        test = page.replace(CDN, "./node_modules/three/")
        (local_dir / "test.html").write_text(test, encoding="utf-8")
        print(f"{local_dir / 'test.html'} written")


if __name__ == "__main__":
    build()
