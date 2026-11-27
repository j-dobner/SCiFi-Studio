# SCiFi Studio

**Free, open-source scientific illustration and figure editor.**

v22.1 public preview · 27 November 2026

[**Download the standalone editor (.html)**](https://github.com/j-dobner/SCiFi-Studio/releases/download/public-preview/SCiFi-Studio.html) · [Software license](LICENSE) · [Artwork license](artwork/LICENSE.md)

## Get started

1. Click the download link above to save `SCiFi-Studio.html` directly as a GitHub Release attachment. Alternatively, use the [repository file](SCiFi-Studio.html) and its Download raw file button.
2. Open it in a current desktop browser. No installation, account or server is required.
3. Draw, edit and assemble figures; save editable projects locally or export SVG/PNG. Save project (Ctrl/Cmd+S) opens a native Save As dialog where supported; otherwise enter a filename and use the browser's download settings to choose a folder. Each workspace panel has a labeled Collapse / Expand button.

The preview contains vector drawing and layout tools, editable paths and shapes, text and arrows, an icon editor, synthetic plot tools, local project import/export and 471 editable scientific illustrations: 329 molecular biology, 13 human organoids, 36 expanded cell atlas, 19 early progenitors, 17 original lineage illustrations, 34 embryogenesis illustrations and all 23 Carnegie stages. Molecular variants are grouped into families by default; enable **Show individual variants** for the complete count. Other unresolved private artwork, including laboratory essentials, branded instruments and legacy drawings, is excluded.

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
