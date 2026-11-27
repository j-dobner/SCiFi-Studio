"""Chromium smoke test of both public editor entry points."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for name in ("index.html", "SCiFi-Studio.html"):
        page = browser.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto((ROOT / name).as_uri())
        page.wait_for_selector("[data-asset]")
        assert page.evaluate("assets.length") == 471
        assert page.evaluate("SCIFI_BUILTIN_MOLECULAR_V71.length") == 329
        for category, count in (("Human Organoids", 13), ("Molecular Biology Essentials", 329)):
            page.locator("#categoryFilter").select_option(category)
            assert page.evaluate("(c) => assets.filter(a=>categoryMatch(a,c)).length", category) == count
            assert page.locator("[data-asset]").count() > 0
        page.locator("#categoryFilter").select_option("All")
        page.locator("#assetSearch").fill("DNA double helix")
        assert page.locator("[data-asset]").count() > 0
        assert not errors, errors
        page.close()
    browser.close()
print("Chromium startup, library categories and search passed.")
