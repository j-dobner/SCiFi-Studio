# SCiFi Studio

**Free, open-source scientific illustration and figure editor.**

v22.1 public preview · 27 November 2026

[**Download the standalone editor (.html)**](https://github.com/j-dobner/SCiFi-Studio/releases/download/public-preview/SCiFi-Studio.html) · [Software license](LICENSE) · [Artwork license](artwork/LICENSE.md)

## Get started

1. Click the download link above to save `SCiFi-Studio.html` directly as a GitHub Release attachment. Alternatively, use the [repository file](SCiFi-Studio.html) and its Download raw file button.
2. Open it in a current desktop browser. No installation, account or server is required.
3. Draw, edit and assemble figures; save editable projects locally or export SVG/PNG. Save project (Ctrl/Cmd+S) opens a native Save As dialog where supported; otherwise enter a filename and use the browser's download settings to choose a folder. Each workspace panel has a labeled Collapse / Expand button.

The preview contains vector drawing and layout tools, editable paths and shapes, text and arrows, an icon editor, synthetic plot tools, local project import/export and 471 editable scientific illustrations: 329 molecular biology, 13 human organoids, 36 expanded cell atlas, 19 early progenitors, 17 original lineage illustrations, 34 embryogenesis illustrations and all 23 Carnegie stages. Molecular variants are grouped into families by default; enable **Show individual variants** for the complete count. Other unresolved private artwork, including laboratory essentials, branded instruments and legacy drawings, is excluded.

## v23.9 — Extended export formats review

The existing Export dialog adds current-page baseline TIFF (uncompressed lossless 8-bit RGB, DPI metadata), JPEG (lossy, quality 95%, JFIF density) and lossless raster PDF (RGB image at the selected DPI and physical page size in PDF points). All three flatten transparent artwork onto white, honor the existing 1–2400 DPI and 40-megapixel / 16,384 px limits, and omit nonprinting guides. PDF is a raster document, not a vector or editable-text export; use SVG for editable vectors. PNG transparency and existing SVG/project options remain unchanged. No external dependencies, server or project-schema changes. TIFF files can be large; CMYK, vector PDF, EPS and multipage PDF are not included in this increment.

## v23.8 — Publication panels review

Panel layout… adds a page-owned nonprinting planning layer. Generate an equal grid (up to 6 × 6), edit individual panel labels and rectangular frames in physical units, show/hide boundaries, and optionally snap to visible panel edges using Smart Snap. Existing artwork is never automatically moved, cropped or resized. Insert editable native text labels explicitly; they are independent objects, not linked to the guide frames. Layouts are saved with projects, duplicated with pages and undoable. Guides are excluded from exports; inserted text labels export normally. Page resizing does not rescale panels. Overlap is allowed for inset layouts. This initial increment uses numerical frame editing; direct drag handles and content assignment are deferred.

## v23.7 — Precise transform review

The existing Properties panel offers **Precise transform…** for selected native objects, symbols and supported groups. Set frame dimensions and anchor positions in px, mm, cm or inches (96 design pixels/inch), choose one of nine reference anchors, optionally unlock proportions for individual objects, and preview before applying. Groups preserve proportions; unattached single arrows use exact endpoints. Native paths scale all anchors, Bézier handles and compound contours. Fixed text-box frames resize independently of their fonts; auto-size labels scale font and glyph width within native limits. Native outline scaling is opt-in; internal symbol/plot strokes inherently scale with their frame. Frame sizes are not visible ink bounds. Locked/hidden objects and attached connector networks are protected; the latter still use existing connector tools. Undo restores the previous geometry. No project schema change.

## v23.6 — Figure line widths review

Line widths inventories positive visible native outline, path, arrow and fixed text-box border widths. Select replacements in nominal physical points and filter by stroke role. The selection, current page and all-page scopes have clone-only before/after previews; all-page undo is separate on each page. Uniformly scaled native symbols account for their cumulative scale; nonuniformly stretched symbols are flagged with approximate area-equivalent widths. Hidden/locked artwork, absent outlines, zero-width outlines, imported SVG/raster, plots and QC cards are excluded. Colors, dash styles, geometry and arrowhead types remain unchanged; arrowhead dimensions follow the existing width-dependent rendering rule. Native width limits are validated before applying. Existing project format and public library are unchanged.

## v23.5 — Figure typography review

The Typography tool lists base font-family/size entries and explicit rich-text overrides. Replace individual existing families or nominal vertical point sizes, with a clone-only before/after preview for the selection, current page or all pages. Nominal size accounts for cumulative vertical scaling inside editable symbols (96 design pixels per inch); superscript/subscript rendering retains its relative scaling. Replacements outside the native 6–160 design-pixel range are rejected before applying. Bold, italic, text colors and other rich-text attributes are preserved. Auto-size labels may reflow; fixed frames remain unchanged, with approximate overflow warnings. Shape labels support family replacement only; imported artwork, plots and hidden/locked parts are excluded. Font availability depends on the system. All-page undo is separate per page. Line-width standardization is available separately in v23.6.

## v23.4 — Combine shapes review

Combine accepts 2–16 native paths or simple geometric shapes, with a per-object compatibility report and explicit opt-in closure for filled open paths. Union, sequential subtraction from the backmost shape, common intersection and odd-coverage exclusion produce native editable compound contours. The backmost object supplies style. Complete surviving Bézier spans retain their handles; clipped intersections remain polygonal approximations. The engine is bounded by segment and contour limits and rejects unsafe/empty results without modifying originals. Embedded shape labels are not carried over; compound illustrations must be opened for component editing. Undo restores the original objects. The optional **Keep original objects** checkbox (unchecked by default) inserts an independent editable result directly above the frontmost selected input while retaining the source objects, their groups and stacking order. Undo removes just the new result. The preserved inputs remain visible; move the result or hide the inputs to inspect it separately.

## v23.3 — Figure colors review

Figure colors inventories editable native paint slots in the selected artwork, current page or all pages. It supports nested native icon parts, solid fills, outlines, line colors, gradient stops, text/rich-text colors and highlights, fixed text-box colors and opt-in page backgrounds. Replace selected HEX colors simultaneously, filter by role, search source HEX, and compare before/after on a cloned page preview without touching live artwork. Locked/hidden objects, imported raster/SVG, plot/QC palettes and shared library originals are excluded. All-page replacements use separate undo history per affected page. This increment is color-only; global typography and line-width standardization are deferred.

## v23.2 — Format painter review

Copy a native object's appearance using Format painter, choose individual attributes, then apply to a selection or click compatible objects repeatedly (Esc exits). Native text, shapes, rectangles, paths and arrows are supported. Fill/gradient, stroke, line width/dash, opacity, text attributes, fixed-box background/border and arrowheads are individually selectable; opacity, arrowheads and text-box styling are opt-in. Auto-size text can reflow. Fixed text-box geometry, path geometry, object positions, text content and connector attachments are preserved. Unrelated rich-text attributes survive; selected base attributes replace their overrides. Biological symbols, plots and uploaded SVG/raster objects are deliberately excluded. Each application is undoable. Recovery remains available from v23.1.

## v23.1 — Recovery review

This version restores the approved v23 UI baseline and adds only local recovery checkpoints. The Recovery button provides automatic checkpoint controls, manual checkpointing, recovery, JSON download and explicit deletion. IndexedDB stores up to eight editing-session drafts (60 MB per draft); previous drafts are not silently replaced or evicted. Checkpoints run after committed edits (three-second debounce and 15-second periodic check). Unfinished editing sessions are skipped. Project files and SVG/PNG export are unchanged. Browser-local recovery is best effort, not a substitute for manual project saving. Browser storage may be unavailable, cleared, or different after moving a standalone file.

## v23 UI review 7 — Workspace preferences

Workspace preferences remember normal panel collapse states, widths, minimized-width restore values, Properties section states, ruler and grid visibility, snapping options, tool behavior and library display options locally in the browser. The Preferences button in the Edit tools header offers common settings and a reset to defaults. Focus canvas does not overwrite the usual panel configuration. Reset preserves current document data, page guides, favorites and recent colors/illustrations. Storage is browser-dependent, especially for renamed or moved standalone HTML files; if unavailable, preferences work for the current session only.

## v23 UI review 6 — Rulers and guides

Optional rulers follow the current canvas unit (px, mm, cm, in), page origin, pan and zoom. Drag from a ruler to create a guide, then drag its blue marker to adjust it or double-click the marker to remove it. Guides… allows precise numeric positioning and removal. Visible guides participate in existing smart snapping; they are stored per page in project JSON, copied when duplicating a page, and omitted from figure exports. Rulers are off by default. Existing projects without guide records open normally.

## v23 UI review 5 — Color controls

A shared HEX palette is available beside native color pickers, including outline, background, text and gradient controls. It accepts three- and six-digit HEX, stores up to 16 recent colors locally where browser storage permits, and uses the browser-native screen eyedropper where supported. Original color change handlers remain responsible for editing and undo. Double-clicking sidebar handles now toggles minimum/previous width; Home resets to the responsive default.

## v23 UI review 4 — Resizable sidebars

Drag the inner edge of the illustration library or Properties panel to adjust its width. Double-click the resize handle to toggle minimum and previous width. Press Home when focused to restore the original responsive width. Arrow keys resize by 10 px, Shift by 40 px. Widths remain available across panel collapse and Focus canvas locally in the browser; narrow screens retain the original layout. No document dimensions or artwork are changed.

## v23 UI review 3 — Illustration library

Adds local favorites of individual variants, a newest-first recent-insertions view, three thumbnail sizes, exact-variant favorites inside the family chooser, and selected scientific search synonyms. All original categories, variant grouping, multi-selection and import/export tools remain available. Preferences are stored in the browser when local storage is available; they are not added to project files.

## v23 UI review 2 — Properties

The existing Properties panel now has individually collapsible, icon-labeled sections, all expanded by default, with browser-local collapse state. Text and layout, appearance and typography have separate headings. Existing controls, layer tab, artwork and project format remain unchanged.

## v23 UI review 1 — toolbar

Incremental review: consistent outline icons, clearer toolbar group labels and descriptive native tooltips with existing shortcuts. Original panel layout, bluish v23 theme and editor functions remain in place. No additional UI/UX work is included in this iteration.

## v23 experimental branch

This branch explores a cleaner workspace, whole-object text-color overrides, DIN A0–A6 page formats and px/mm/cm/in sizing. Design coordinates use 96 units per inch; physical sizes are rounded to the nearest design pixel. PNG exports support configurable DPI with embedded PNG physical-resolution metadata, up to 40 megapixels / 16,384 pixels per side. SVG remains vector with physical dimensions. This is a development branch, not the public release.

## Source and build

Open `index.html` from a local checkout, keeping the `artwork/` folder beside it. Run `python tools/build.py` to recreate the single-file offline editor. The generated standalone is committed for convenient download.

## Licensing and credit

Software: [MIT](LICENSE). Original scientific artwork listed in [the provenance manifest](artwork/PROVENANCE.json): [CC0 1.0 Universal](artwork/LICENSE.md). Interface glyphs retain their [third-party license notices](THIRD-PARTY-NOTICES.md). User-imported materials and other third-party rights are not covered by the artwork dedication.

Project creator, scientific direction and AI-assisted development: **Jochen Dobner**.

Rights holder: IUF - Leibniz-Institut für umweltmedizinische Forschung GmbH. See [CITATION.cff](CITATION.cff) for citation information.

## Preview status

v22.1 restores artwork against its audited source blobs and verifies IDs, native geometry and counts. See the repository validation workflow for build and Chromium checks. Not a complete cross-browser, accessibility or scientific validation. Illustrations are schematic, not diagnostic; check accuracy and suitability for your use. Please report issues through GitHub.
