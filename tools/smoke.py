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
        # UI review 1: original toolbar placement, consistent icons, real tooltips.
        assert page.locator(".toolbar #selectTool").count() == 1
        assert page.locator(".toolbar #nxStudioBtn svg").count() == 1
        assert "Ctrl/Cmd+G" in page.locator("#groupBtn").get_attribute("title")
        assert "Ctrl/Cmd+Shift+G" in page.locator("#ungroupBtn").get_attribute("title")
        page.locator("#textTool").click()
        assert page.evaluate("activeTool") == "text"
        page.locator("#selectTool").click()
        page.locator("#shapePaletteBtn").click()
        assert page.locator("#shapePalette").is_visible()
        page.locator("#shapePalette [data-shape-choice]").first.click()
        assert page.evaluate("activeTool") == "box"
        assert page.locator("#shapePaletteBtn svg").count() == 1
        page.locator("#scifiLinePaletteBtn").click()
        assert page.locator("#shapePalette").is_visible()
        page.locator("#scifiLinePaletteBtn").click()
        assert not page.locator("#shapePalette").is_visible()
        page.locator("#selectTool").click()
        page.evaluate("nxSnapBadge()")
        assert page.locator("#nxSnapBtn svg").count() == 1
        # v23: preserve rich styles while overriding text color via the inspector.
        page.evaluate("""() => {
            const o=txt('Mixed',10,10,20,'#000000',500);
            o.richRuns=[{start:0,end:2,style:{color:'#ff0000',italic:true}}];
            objects.push(o);selectOnly(o.id);render();
        }""")
        page.locator("#customColor").evaluate("(el) => {el.value='#007700';el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));}")
        assert page.evaluate("selectedObj().color") == "#007700"
        assert page.evaluate("selectedObj().richRuns[0].style.italic")
        assert page.evaluate("!('color' in selectedObj().richRuns[0].style)")
        page.evaluate("canvasSizeDialog()")
        page.locator("#pagePreset").select_option("A4")
        page.locator("#pageOrientation").select_option("portrait")
        page.locator("#pageUnit").select_option("cm")
        page.locator("#applyCanvasSize").click()
        assert page.evaluate("canvasSize()") == {"width":794,"height":1123,"unit":"cm"}
        assert page.evaluate("pngExportSize(300)") == {"width":2481,"height":3509,"dpi":300}
        # Large-format pages must fit below the old 25% zoom minimum.
        page.evaluate("setCanvasSize(3179,4494); nxFitAvailable()")
        assert page.evaluate("zoom") < .25
        assert page.evaluate("""() => {
            const shell=$('#canvasShell'),m=stage.getScreenCTM();
            return canvasWidth*m.a <= shell.clientWidth && canvasHeight*m.d <= shell.clientHeight;
        }""")
        page.evaluate("setZoom(.05)")
        page.locator("#zoomOut").click()
        assert page.evaluate("zoom") == .04
        page.locator("#zoomIn").click()
        assert page.evaluate("zoom") == .05
        page.evaluate("setZoom(0)")
        assert page.evaluate("zoom") == .01
        assert page.locator("#zoomOut").is_disabled()
        page.evaluate("setZoom(4)")
        assert page.evaluate("zoom") == 3
        assert page.locator("#zoomIn").is_disabled()
        # Test real PNG metadata and dimensions with a smaller image.
        page.evaluate("setCanvasSize(96,96)")
        with page.expect_download() as exported:
            page.evaluate("exportPNG(300)")
        import struct, zlib
        raw = Path(exported.value.path()).read_bytes()
        assert struct.unpack_from(">II",raw,16) == (300,300)
        pos=8; chunks=[]
        while pos<len(raw):
            n,kind=struct.unpack_from(">I4s",raw,pos)
            data=raw[pos+8:pos+8+n]
            assert zlib.crc32(kind+data)==struct.unpack_from(">I",raw,pos+8+n)[0]
            if kind==b"pHYs": chunks.append(struct.unpack(">IIB",data))
            pos+=12+n
        assert chunks==[(11811,11811,1)]
        assert not errors, errors
        page.close()
    browser.close()
print("Chromium startup, library categories and search passed.")
