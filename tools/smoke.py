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
        # UI review 4: drag widths, keyboard accessibility and collapse/restore.
        page.set_viewport_size({"width": 1440, "height": 900})
        initial_left=page.evaluate("uiResizePanelWidth('left')")
        initial_right=page.evaluate("uiResizePanelWidth('right')")
        left_grip=page.locator("#uiResize-left")
        right_grip=page.locator("#uiResize-right")
        box=left_grip.bounding_box()
        page.mouse.move(box["x"]+box["width"]/2,box["y"]+box["height"]/2)
        page.mouse.down()
        page.mouse.move(box["x"]+box["width"]/2+80,box["y"]+box["height"]/2,steps=6)
        page.mouse.up()
        assert page.evaluate("uiResizePanelWidth('left')") == initial_left+80
        right_grip.focus()
        right_grip.press("ArrowLeft")
        assert page.evaluate("uiResizePanelWidth('right')") == initial_right+10
        page.locator("#nxToggle-left").click()
        assert not left_grip.is_visible()
        page.locator("#nxToggle-left").click()
        assert page.evaluate("uiResizePanelWidth('left')") == initial_left+80
        page.locator("#nxFocusCanvas").click()
        assert not left_grip.is_visible() and not right_grip.is_visible()
        page.locator("#nxFocusCanvas").click()
        assert page.evaluate("uiResizePanelWidth('right')") == initial_right+10
        left_grip.dblclick()
        assert page.evaluate("uiResizePanelWidth('left')") == 180
        left_grip.dblclick()
        assert page.evaluate("uiResizePanelWidth('left')") == initial_left+80
        left_grip.focus()
        left_grip.press("Home")
        assert page.evaluate("uiResizePanelWidth('left')") == initial_left
        right_grip.focus()
        right_grip.press("Home")
        assert page.evaluate("uiResizePanelWidth('right')") == initial_right
        page.set_viewport_size({"width": 800, "height": 900})
        assert not left_grip.is_visible() and not right_grip.is_visible()
        page.set_viewport_size({"width": 1280, "height": 720})
        # UI review 3: favorite, filter, exact-variant insertion, thumbnail sizes.
        assert page.locator("#uiLibAll").get_attribute("aria-pressed") == "true"
        page.locator("#assetSearch").fill("")
        page.locator("#assets .ui-lib-star").first.click()
        assert page.locator("#assets .ui-lib-star").first.get_attribute("aria-pressed") == "true"
        page.locator("#uiLibFavorites").click()
        assert page.locator("#assets [data-asset]").count() == 1
        favorite_id=page.locator("#assets [data-asset]").first.get_attribute("data-asset")
        page.locator("#assets [data-asset]").first.click()
        page.locator("#uiLibRecent").click()
        assert page.locator("#assets [data-asset]").first.get_attribute("data-asset") == favorite_id
        page.locator("#uiLibSize").select_option("large")
        assert page.locator("#assets").get_attribute("data-thumbnail-size") == "large"
        page.locator("#uiLibSize").select_option("normal")
        page.locator("#uiLibFavorites").click()
        page.locator("#assets .ui-lib-star").first.click()
        assert page.locator("#assets [data-asset]").count() == 0
        page.locator("#uiLibAll").click()
        page.evaluate("selectOnly(objects.find(o=>o.type==='text').id);render()")
        # UI review 5: shared HEX palette, recent colors and mocked native eyedropper.
        page.locator("#customColor + .ui-color-more").click()
        page.locator("#uiColorHex").fill("bad!")
        assert page.locator("#uiColorApply").is_disabled()
        page.locator("#uiColorHex").fill("369")
        page.locator("#uiColorApply").click()
        assert page.evaluate("selectedObj().color.toLowerCase()") == "#336699"
        assert page.evaluate("uiColorRecent[0]") == "#336699"
        page.locator("#customColor + .ui-color-more").click()
        assert page.locator("#uiColorPopup [aria-label='Apply #336699']").count() == 1
        page.locator("#uiColorHex").fill("#ABCDEF")
        page.locator("#uiColorHex").press("Escape")
        assert page.evaluate("selectedObj().color.toLowerCase()") == "#336699"
        # Use a function body: a bare assignment evaluates to the class itself,
        # which Playwright may attempt to invoke as an evaluation callback.
        page.evaluate("() => { window.EyeDropper = class { async open(){return {sRGBHex:'#6699cc'}} }; }")
        page.locator("#customColor + .ui-color-more").click()
        page.locator("#uiColorEye").click()
        page.wait_for_function("() => selectedObj().color.toLowerCase() === '#6699cc'")
        assert page.evaluate("selectedObj().color.toLowerCase()") == "#6699cc"
        # UI review 2: sections open initially and keep their state across rendering.
        assert page.locator("#inspector .ui-props-toggle").count() >= 5
        assert page.locator("#inspector .ui-props-toggle[aria-expanded=false]").count() == 0
        assert page.locator("#inspector .ui-props-section").filter(has=page.locator("#singleFontFamily")).count() == 1
        assert page.locator("#inspector .ui-props-toggle").filter(has_text="Typography").count() == 1
        appearance = page.locator("#inspector .ui-props-toggle").filter(has_text="Appearance")
        appearance.click()
        assert appearance.get_attribute("aria-expanded") == "false"
        assert not page.locator("#customColor").is_visible()
        page.evaluate("render()")
        assert appearance.get_attribute("aria-expanded") == "false"
        appearance.click()
        assert page.locator("#customColor").is_visible()
        page.locator("#fontSize").fill("24")
        page.locator("#fontSize").press("Tab")
        assert page.evaluate("selectedObj().fontSize") == 24
        page.locator("#nxLayersTab").click()
        assert page.locator("#nxLayerPanel").is_visible()
        page.locator("#nxPropsTab").click()
        assert page.locator("#inspector").is_visible()
        page.evaluate("canvasSizeDialog()")
        page.locator("#pagePreset").select_option("A4")
        page.locator("#pageOrientation").select_option("portrait")
        page.locator("#pageUnit").select_option("cm")
        page.locator("#applyCanvasSize").click()
        assert page.evaluate("canvasSize()") == {"width":794,"height":1123,"unit":"cm"}
        assert page.evaluate("pngExportSize(300)") == {"width":2481,"height":3509,"dpi":300}
        # UI review 6: optional unit-aware rulers, actual ruler drag and non-exported page guides.
        assert not page.locator("#uiRulerTop").is_visible()
        page.locator("#uiRulerToggle").click()
        assert page.locator("#uiRulerTop").is_visible()
        page.evaluate("nxFitAvailable();uiRulerDraw()")
        assert page.locator("#uiRulerCorner").inner_text() == "cm"
        page.locator("#uiGuideButton").click()
        page.locator("#uiGuideAxis").select_option("x")
        page.locator("#uiGuideValue").fill("5")
        page.locator("#uiGuideAdd").click()
        page.evaluate("closeModal();uiRulerDraw()")
        assert abs(page.evaluate("uiGuideList()[0].v")-96*5/2.54) < .001
        assert page.evaluate("currentProjectData().pages[0].guides.length") == 1
        assert page.evaluate("window.scifiGuideTargets('x').length") == 1
        assert page.locator("#uiGuideOverlay line").count() == 1
        assert page.evaluate("!svgDocument(true).includes('uiGuideOverlay')")
        # Drag from top ruler into canvas, using actual screen coordinates.
        top=page.locator("#uiRulerTop").bounding_box()
        target=page.evaluate("""() => {const m=stage.getScreenCTM();return {x:m.e+canvasWidth*m.a/2,y:m.f+canvasHeight*m.d/2}}""")
        page.mouse.move(top["x"]+top["width"]/2,top["y"]+top["height"]/2)
        page.mouse.down()
        page.mouse.move(target["x"],target["y"],steps=8)
        page.mouse.up()
        assert page.evaluate("uiGuideList().some(g=>g.axis==='y')")
        page.locator("#uiRulerToggle").click()
        assert not page.locator("#uiRulerTop").is_visible()
        assert page.evaluate("window.scifiGuideTargets('x').length") == 0
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
        # UI review 7: workspace persistence and reset without changing project data.
        assert page.evaluate("uiWorkspaceStorageAvailable()")
        page.evaluate("uiResizeSet('left',340);uiWorkspaceSave()")
        page.locator("#gridBtn").click()
        page.locator("#uiRulerToggle").click()
        page.locator("#scifiRepeatMode").select_option("repeat")
        page.locator("#uiLibSize").select_option("large")
        page.locator("#nxToggle-pages").click()
        page.locator("#nxFocusCanvas").click()
        assert page.evaluate("uiWorkspaceRead().panels.left") is False
        assert page.evaluate("uiWorkspaceRead().panels.pages") is True
        page.locator("#nxFocusCanvas").click()
        page.reload()
        page.wait_for_selector("[data-asset]")
        assert page.evaluate("uiResizeDesired.left") == 340
        assert page.evaluate("grid") is True
        assert page.locator("#uiRulerTop").is_visible()
        assert page.locator("#scifiRepeatMode").input_value() == "repeat"
        assert page.locator("#uiLibSize").input_value() == "large"
        assert page.locator("#nxToggle-pages").get_attribute("aria-expanded") == "false"
        assert page.locator("#nxToggle-left").get_attribute("aria-expanded") == "true"
        page.evaluate("uiGuideAdd('x',10)")
        before=page.evaluate("JSON.stringify(currentProjectData())")
        page.locator("#uiWorkspacePrefs").click()
        page.locator("#uiPrefReset").click()
        assert page.evaluate("JSON.stringify(currentProjectData())") == before
        assert page.evaluate("uiResizeDesired.left") is None
        assert page.evaluate("grid") is False
        assert not page.locator("#uiRulerTop").is_visible()
        assert page.locator("#scifiRepeatMode").input_value() == "auto"
        assert page.locator("#uiLibSize").input_value() == "normal"
        assert page.locator("#nxToggle-pages").get_attribute("aria-expanded") == "true"
        # Publication tools: native formatting, panel labels, lossless export and recovery.
        page.wait_for_function("() => uiRecoveryReady")
        if page.evaluate("!!uiRecoveryPending"):
            page.locator("#uiRecoveryBtn").click()
            page.once("dialog", lambda dialog: dialog.accept())
            page.locator("#uiRecDiscard").click()
            page.wait_for_function("() => !uiRecoveryPending")
        page.evaluate("setCanvasSize(480,320); objects=[]; selectOnly(null); render()")
        page.evaluate("uiPubPanelGrid({cols:2,rows:2,margin:10,gap:10,fontPx:16,arrange:false})")
        assert page.evaluate("objects.filter(o=>o.publicationPanelLabel).map(o=>o.text)") == ["A","B","C","D"]
        page.evaluate("uiPubFormatApply({fontPx:20,strokePx:1},'page')")
        assert page.evaluate("objects.filter(o=>o.type==='text').every(o=>o.fontSize===20)")
        page.evaluate("selectOnly(objects.find(o=>o.type==='text').id);render();uiPubCopyStyle()")
        page.evaluate("selectOnly(objects.filter(o=>o.type==='text')[1].id);render();uiPubApplyStyle()")
        assert page.evaluate("selectedObj().fontSize") == 20
        page.evaluate("uiPubPhysicalDialog()")
        page.locator("#uiPosUnit").select_option("mm")
        page.locator("#uiPosX").fill("10")
        page.locator("#uiPosApply").click()
        assert abs(page.evaluate("selectedObj().x")-96*10/25.4)<.001
        assert page.evaluate("uiPubPreflight({dpi:300,font:20,stroke:.5}).some(v=>v.message.includes('Text'))")
        page.evaluate("setCanvasSize(96,96)")
        import struct
        with page.expect_download() as exported:
            page.evaluate("uiPubExport('tiff',96)")
        data=Path(exported.value.path()).read_bytes()
        assert data[:4] == bytes([73,73,42,0])
        ifd=struct.unpack_from("<I",data,4)[0]
        tags={struct.unpack_from("<H",data,ifd+2+i*12)[0]:struct.unpack_from("<HHII",data,ifd+2+i*12)[1:] for i in range(struct.unpack_from("<H",data,ifd)[0])}
        assert tags[256][2] == tags[257][2] == 96
        assert struct.unpack_from("<II",data,tags[282][2]) == (96,1)
        assert tags[279][2] == 96*96*3
        with page.expect_download() as exported:
            page.evaluate("uiPubExport('pdf',96)")
        data=Path(exported.value.path()).read_bytes()
        assert data.startswith(b"%PDF-1.4") and b"/MediaBox [0 0 72 72]" in data
        start=int(data.split(b"startxref"+bytes([10]))[-1].splitlines()[0])
        assert data[start:start+4] == b"xref"
        # Use a real local raster asset and verify the source survives editing and recovery.
        page.evaluate("""async () => {
            const c=document.createElement('canvas');c.width=40;c.height=20;
            const ctx=c.getContext('2d');ctx.fillStyle='#7799bb';ctx.fillRect(0,0,40,20);
            const blob=await new Promise(r=>c.toBlob(r,'image/png'));
            const a=await readCustomIcon(new File([blob],'test-image.png',{type:'image/png'}));
            registerCustomAsset(a);addAsset(a.id,48,48);
            const o=selectedObj();window.testOriginalImage=a.source;
            transact(()=>uiPubImageApply(o,a,{x:4,y:2,w:20,h:10,brightness:0,contrast:1,umPerPixel:1,barUm:5,barColor:'white'}));
        }""")
        assert page.evaluate("selectedObj().imageView.w") == 20
        assert page.evaluate("byId[selectedObj().type].source === window.testOriginalImage")
        assert page.evaluate("svgDocument(true).includes('ui-microscopy-bar')")
        assert page.evaluate("uiPubPreflight({dpi:300,font:8,stroke:.5}).some(v=>v.message.includes('effective DPI'))")
        page.wait_for_function("() => uiRecoveryReady && !uiRecoveryBusy")
        assert page.evaluate("uiRecoverySave(true)")
        assert page.evaluate("async () => (await uiRecoveryStore('readonly',s=>s.get(uiRecoveryKey))).project.pages.length") == 1
        page.reload()
        page.wait_for_function("() => uiRecoveryReady && !!uiRecoveryPending")
        page.locator("#uiRecoveryBtn").click()
        page.once("dialog", lambda dialog: dialog.accept())
        page.locator("#uiRecRestore").click()
        page.wait_for_function("() => !uiRecoveryPending")
        assert page.evaluate("objects.some(o=>o.imageView?.w===20 && !!byId[o.type]?.source)")
        assert not errors, errors
        page.close()
    browser.close()
print("Chromium startup, library categories and search passed.")
