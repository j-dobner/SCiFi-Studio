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
        # v23.2: selective native formatting, geometry preservation, and undo.
        page.evaluate("""() => {
            const source=rect(10,20,60,40,'#123456',5);
            source.strokeColor='#234567';source.strokeWidth=4;source.dashStyle='dashed';
            source.fillGradient={kind:'linear',angle:45,stops:[{offset:0,color:'#123456',opacity:1},{offset:1,color:'#ffffff',opacity:1}]};
            const target={...rect(120,50,80,30,'#abcdef',8),type:'shape',shapeKind:'ellipse',rotation:20,opacity:.6,strokeColor:'#654321',strokeWidth:1};
            objects=[source,target];selectOnly(source.id);render();
        }""")
        page.locator("#uiPainterBtn").click()
        page.locator("#uiPainterCopy").click()
        assert page.locator("[data-paint-attr=fill]").is_checked()
        page.locator("[data-paint-attr=stroke]").uncheck()
        page.locator("[data-paint-attr=line]").uncheck()
        page.evaluate("closeModal();selectOnly(objects[1].id);render()")
        page.locator("#uiPainterBtn").click()
        page.locator("#uiPainterApply").click()
        assert page.evaluate("objects[1].color") == "#123456"
        assert page.evaluate("objects[1].fillGradient.stops[0].color") == "#123456"
        assert page.evaluate("[objects[1].x,objects[1].y,objects[1].w,objects[1].h,objects[1].rotation,objects[1].opacity,objects[1].strokeWidth]") == [120,50,80,30,20,.6,1]
        assert page.evaluate("objects[1].strokeColor") == "#654321"
        page.evaluate("undo()")
        assert page.evaluate("objects[1].color") == "#abcdef"
        page.evaluate("""() => {
            const s=txt('Source',10,10,24,'#abcdef',700);
            const t=txt('H2O',150,70,12,'#112233',400);
            t.textBoxMode='fixed';t.w=100;t.h=60;
            t.richRuns=[{start:1,end:2,style:{script:'sub',color:'#ff0000',italic:true}}];
            objects=[s,t];selectOnly(s.id);render();uiPainterCapture(s);
            uiPainterApply([t],uiPainterSource,new Set(['textColor','size']));
        }""")
        assert page.evaluate("objects[1].text") == "H2O"
        assert page.evaluate("objects[1].fontSize") == 24
        assert page.evaluate("[objects[1].w,objects[1].h]") == [100,60]
        assert page.evaluate("objects[1].richRuns[0].style.script") == "sub"
        assert page.evaluate("objects[1].richRuns[0].style.italic") is True
        assert page.evaluate("!('color' in objects[1].richRuns[0].style)")
        page.evaluate("uiPainterStart()")
        assert page.locator("#uiPainterBtn").get_attribute("aria-pressed") == "true"
        page.keyboard.press("Escape")
        assert page.locator("#uiPainterBtn").get_attribute("aria-pressed") == "false"
        # v23.3: actual native color inventory, simultaneous replacement and clone-only preview.
        page.evaluate("""() => {
            const a=rect(30,40,50,40,'#112233',4);a.strokeColor='#445566';
            const b=rect(90,40,50,40,'#445566',4);b.strokeColor='#112233';
            const g=rect(150,40,50,40,'#778899',4);
            g.fillGradient={kind:'linear',angle:45,stops:[{offset:0,color:'#112233',opacity:1},{offset:1,color:'#445566',opacity:1}]};
            const tx=txt('H2O',20,90,20,'#445566');
            tx.richRuns=[{start:1,end:2,style:{script:'sub',color:'#112233',highlight:'#aabbcc'}}];
            const nested={id:uid(),type:'symbol',name:'Native test',x:10,y:10,w:100,h:100,sourceW:200,sourceH:160,children:[a,b,g,tx],color:'#deadde',opacity:1};
            const locked=rect(220,20,50,40,'#112233',4);locked.locked=true;
            objects=[nested,locked];selectOnly(nested.id);render();
            window.figColorBefore=JSON.stringify(objects);
        }""")
        page.locator("#uiFigureColorsBtn").click()
        assert page.locator("[data-source-color='#112233']").count() == 1
        assert page.locator("[data-source-color='#DEADDE']").count() == 0
        assert page.locator("[data-source-color='#778899']").count() == 0
        page.locator("#uiFigColor-112233").fill("#445566")
        page.locator("#uiFigColor-445566").fill("#112233")
        page.wait_for_function("() => document.querySelector('#uiFigColorPreview').innerHTML.includes('#445566')")
        assert page.evaluate("JSON.stringify(objects)===window.figColorBefore")
        page.locator("#uiFigColorBefore").click()
        page.locator("#uiFigColorAfter").click()
        page.locator("#uiFigColorCancel").click()
        assert page.evaluate("JSON.stringify(objects)===window.figColorBefore")
        page.locator("#uiFigureColorsBtn").click()
        page.locator("#uiFigColor-112233").fill("#445566")
        page.locator("#uiFigColor-445566").fill("#112233")
        page.locator("#uiFigColorApply").click()
        assert page.evaluate("objects[0].children[0].fill") == "#445566"
        assert page.evaluate("objects[0].children[1].fill") == "#112233"
        assert page.evaluate("objects[0].children[0].strokeColor") == "#112233"
        assert page.evaluate("objects[0].children[2].fillGradient.stops[0].color") == "#445566"
        assert page.evaluate("objects[0].children[3].richRuns[0].style.color") == "#445566"
        assert page.evaluate("objects[0].children[3].richRuns[0].style.script") == "sub"
        assert page.evaluate("objects[1].fill") == "#112233"
        page.evaluate("undo()")
        assert page.evaluate("JSON.stringify(objects)===window.figColorBefore")
        # All-page replacements preserve page-local undo and leave library assets untouched.
        page.evaluate("""() => {
            const asset=assets.find(a=>a.kind==='group'&&a.elements?.length);
            window.figLibraryBefore=JSON.stringify(asset.elements);
            window.figLibraryId=asset.id;
            makeCompoundIcon(asset,60,60);
            const row=uiFigureColorInventory('selection',new Set(['fill']))[0];
            if(!row)throw Error('Native icon has no editable fills');
            window.figRealColor=row.color;
            uiFigureColorApply('selection',new Set(['fill']),new Map([[row.color,'#ABCDEF']]));
            if(JSON.stringify(byId[asset.id].elements)!==window.figLibraryBefore)throw Error('Library artwork was modified');
            undo();
            appendPage(false);objects=[rect(20,20,30,30,'#112233',0)];render();
            uiFigureColorApply('all',new Set(['fill']),new Map([['#112233','#FEDCBA']]));
        }""")
        assert page.evaluate("objects[0].fill") == "#FEDCBA"
        assert page.evaluate("pages[0].elements[0].children[0].fill") == "#FEDCBA"
        page.evaluate("activatePage(pages[0].id);undo()")
        assert page.evaluate("objects[0].children[0].fill") == "#112233"
        # Reset the test fixture to a single page without invoking the delete-page dialog.
        page.evaluate("pages=pages.filter(p=>p.id===activePageId);render()")
        # v23.4: Combine diagnostics, filled open closure, multi-shape union, preserved cubic spans.
        page.evaluate("""() => {
            const a=pathElem([{x:10,y:20,outX:25,outY:0},{x:70,y:20,inX:55,inY:0},{x:70,y:70},{x:10,y:70}],'#b88aad',2,'#e6c1d8',false);
            const b=rect(60,40,45,20,'#e6c1d8',0);b.strokeColor='#b88aad';
            const c=rect(95,40,25,20,'#e6c1d8',0);
            objects=[a,b,c];selection(objects.map(o=>o.id));render();window.boolOriginal=JSON.stringify(objects);
        }""")
        page.locator("#nxBooleanBtn").click()
        assert page.locator("[data-bool=union]").is_disabled()
        assert "Filled open path" in page.locator("#nxBoolSelection").inner_text()
        page.locator("#nxBoolCloseOpen").check()
        assert page.locator("[data-bool=union]").is_enabled()
        page.locator("[data-bool=union]").click()
        assert page.evaluate("objects.length") == 1
        assert page.evaluate("objects[0].closed") is True
        assert page.evaluate("objects[0].nodes.some(n=>Number.isFinite(n.outX))")
        assert page.evaluate("nxInside({x:115,y:50},nxBoolNativeContours(objects[0],false).loops)")
        page.evaluate("undo()")
        assert page.evaluate("JSON.stringify(objects)===window.boolOriginal")
        # Keep originals is opt-in and creates one independent, editable result.
        page.evaluate("selection(objects.map(o=>o.id));render()")
        page.locator("#nxBooleanBtn").click()
        assert not page.locator("#nxBoolKeepOriginals").is_checked()
        page.locator("#nxBoolCloseOpen").check()
        page.locator("#nxBoolKeepOriginals").check()
        page.locator("[data-bool=union]").click()
        assert page.evaluate("objects.length") == 4
        assert page.evaluate("JSON.stringify(objects.slice(0,3))===window.boolOriginal")
        assert page.evaluate("selectedObj().id===objects[3].id && objects[3].closed && !objects[3].groupId")
        page.evaluate("undo()")
        assert page.evaluate("JSON.stringify(objects)===window.boolOriginal")
        page.evaluate("selection(objects.map(o=>o.id));render()")
        page.locator("#nxBooleanBtn").click()
        assert not page.locator("#nxBoolKeepOriginals").is_checked()
        page.evaluate("closeModal()")
        # Incompatible objects are named and no operation is permitted.
        page.evaluate("objects.push(txt('Label',5,5));selection(objects.map(o=>o.id));render()")
        page.locator("#nxBooleanBtn").click()
        assert "Not a native closed shape" in page.locator("#nxBoolSelection").inner_text()
        assert page.locator("[data-bool=union]").is_disabled()
        page.evaluate("closeModal()")
        # Multiple subtractors, disjoint results and intersection use the same validated engine.
        page.evaluate("""() => {
            const a=rect(0,0,100,100,'#abcdef',0);
            const b=rect(20,20,20,20,'#abcdef',0);
            const c=rect(60,60,20,20,'#abcdef',0);
            const out=nxBoolCombine('subtract',[a,b,c]);
            const l=nxBoolNativeContours(out,false).loops;
            if(!nxInside({x:10,y:10},l)||nxInside({x:30,y:30},l)||nxInside({x:70,y:70},l))throw Error('Subtract holes incorrect');
            const inter=nxBoolCombine('intersect',[a,rect(10,10,80,80,'#abcdef',0),rect(20,20,20,20,'#abcdef',0)]);
            if(!nxInside({x:30,y:30},nxBoolNativeContours(inter,false).loops))throw Error('Intersection missing');
        }""")
        # v23.1: recovery preserves multiple pages, guides and native objects across reloads.
        page.wait_for_function("() => uiRecReady && !uiRecBusy")
        page.evaluate("""() => {
            objects=[txt('Recovery test',20,30,18,'#123456')];selectOnly(null);
            projectName='Recovery test project';$('#projectName').value=projectName;
            uiGuideList().splice(0);uiGuideAdd('x',10);
            appendPage(false);
            objects=[txt('Second page',15,15,16,'#654321')];render();
        }""")
        page.wait_for_function("() => !uiRecBusy")
        draft_id=page.evaluate("uiRecId")
        assert page.evaluate("uiRecSave(true)")
        assert page.evaluate("async id => (await uiRecRead(id)).project.pages.length",draft_id) == 2
        page.reload()
        page.wait_for_function("() => uiRecReady")
        assert page.evaluate("id => uiRecList.some(d=>d.id===id)",draft_id)
        assert page.evaluate("projectName") != "Recovery test project"
        page.locator("#uiRecButton").click()
        row=page.locator("[data-recovery-id='"+draft_id+"']")
        page.once("dialog", lambda dialog: dialog.accept())
        row.locator(".ui-rec-restore").click()
        page.wait_for_function("() => projectName==='Recovery test project'")
        assert page.evaluate("pages.length") == 2
        assert page.evaluate("objects[0].text") == "Second page"
        assert page.evaluate("pages[0].guides[0].v") == 10
        assert page.evaluate("async id => !!(await uiRecRead(id))",draft_id)
        # Deleting a checkpoint never changes document data.
        page.locator("#uiRecButton").click()
        page.once("dialog", lambda dialog: dialog.accept())
        row.locator(".ui-rec-delete").click()
        page.wait_for_function("id => !uiRecList.some(d=>d.id===id)",arg=draft_id)
        assert page.evaluate("objects[0].text") == "Second page"
        assert not errors, errors
        page.close()
    browser.close()
print("Chromium startup, library categories and search passed.")
