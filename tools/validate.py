"""Validate public asset inventory and the reproducible standalone."""
import json, re, subprocess, tempfile, shutil
from pathlib import Path
from build import ROOT, build
html = (ROOT / "index.html").read_text(encoding="utf-8")
assets = []
for path in re.findall(r'<script src="(artwork/[^"]+\.js)"></script>', html):
    data = (ROOT / path).read_text(encoding="utf-8")
    match = re.search(r'(?:=\s*|\.push\(\.\.\.)(\[[\s\S]*\])\)?;\s*$', data)
    assert match, path
    assets.extend(json.loads(match.group(1)))
records = json.loads((ROOT / "artwork/PROVENANCE.json").read_text(encoding="utf-8"))["assets"]
by_id = {a["id"]: a for a in assets}
assert len(assets) == len(by_id) == len(records) == 471
assert set(by_id) == {a["id"] for a in records}
assert len({a["id"] for a in records}) == 471
for r in records:
    a = by_id[r["id"]]
    assert a["name"] == r["name"] and a["kind"] == "group"
    assert len(a["elements"]) == r["elementCount"] and r["license"] == "CC0-1.0"
    assert a["width"] > 0 and a["height"] > 0 and a["license"] == "CC0-1.0"
assert sum(a["category"] == "Molecular Biology Essentials" for a in assets) == 329
standalone = build()
assert standalone == (ROOT / "SCiFi-Studio.html").read_text(encoding="utf-8")
if shutil.which("node"):
    with tempfile.TemporaryDirectory() as tmp:
        for i, script in enumerate(re.findall(r"<script>([\s\S]*?)</script>", standalone)):
            path = Path(tmp) / f"script-{i}.js"
            path.write_text(script, encoding="utf-8")
            subprocess.run(["node", "--check", str(path)], check=True)
print("Validated 471 unique native icons, CC0 manifest, and standalone consistency.")
