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
        assert page.locator("#projectName").input_value() == "Untitled figure"
        assert page.evaluate("projectName") == "Untitled figure"
        for panel in ("left", "right", "pages", "tools"):
            button = page.locator("#nxToggle-" + panel)
            assert button.get_attribute("aria-expanded") == "true"
            assert "Collapse" in button.inner_text()
            button.click()
            assert button.get_attribute("aria-expanded") == "false"
            assert "Expand" in button.inner_text()
            button.click()
            assert button.get_attribute("aria-expanded") == "true"
        page.locator("#nxFocusCanvas").click()
        assert page.locator("#nxFocusCanvas").inner_text() == "Restore panels"
        page.locator("#nxFocusCanvas").click()
        assert page.locator("#nxFocusCanvas").inner_text() == "Focus canvas"
        page.evaluate("""() => {
            window.testSaved = null;
            window.showSaveFilePicker = async (options) => {
                window.testSuggested = options.suggestedName;
                return {name: 'Test figure.json', createWritable: async () => ({
                    write: async (content) => { window.testSaved = JSON.parse(content); },
                    close: async () => {}
                })};
            };
        }""")
        page.evaluate("saveProject()")
        assert page.evaluate("window.testSuggested") == "Untitled figure.json"
        assert page.evaluate("window.testSaved.name") == "Test figure"
        assert page.locator("#projectName").input_value() == "Test figure"
        page.evaluate("""() => {window.showSaveFilePicker = async () => {
            throw new DOMException('Cancelled', 'AbortError');
        }}""")
        page.evaluate("saveProject()")
        assert page.locator("#projectName").input_value() == "Test figure"
        page.evaluate("window.showSaveFilePicker = undefined")
        page.once("dialog", lambda dialog: dialog.accept("Fallback figure"))
        with page.expect_download() as download:
            page.evaluate("saveProject()")
        assert download.value.suggested_filename == "Fallback figure.json"
        assert page.locator("#projectName").input_value() == "Fallback figure"
        assert not errors, errors
        page.close()
    browser.close()
print("Chromium startup, library categories and search passed.")
