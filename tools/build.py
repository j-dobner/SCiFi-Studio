"""Build the offline standalone from the public editor and its two artwork scripts."""
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text(encoding="utf-8")
def inline(match):
    js = (ROOT / match.group(1)).read_text(encoding="utf-8")
    if re.search(r"</script", js, re.I):
        raise ValueError("Unexpected closing script tag")
    return "<script>\n" + js + "</script>"
html, count = re.subn(r'<script src="(artwork/(?:embryogenesis|carnegie)\.js)"></script>', inline, html)
if count != 2 or re.search(r"<script\b[^>]*\bsrc\s*=", html):
    raise ValueError("Unexpected external script")
(ROOT / "SCiFi-Studio.html").write_text(html, encoding="utf-8")
print("Built SCiFi-Studio.html")
