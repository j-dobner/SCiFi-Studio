# SCiFi Studio

**Free, open-source scientific illustration and figure editor.**

v22.1 public preview · 27 November 2026

[**Download the standalone editor (.html)**](https://github.com/j-dobner/SCiFi-Studio/releases/download/public-preview/SCiFi-Studio.html) · [Software license](LICENSE) · [Artwork license](artwork/LICENSE.md)

## Get started

1. Click the download link above to save `SCiFi-Studio.html` directly as a GitHub Release attachment. Alternatively, use the [repository file](SCiFi-Studio.html) and its Download raw file button.
2. Open it in a current desktop browser. No installation, account or server is required.
3. Draw, edit and assemble figures; save editable projects locally or export SVG/PNG. Save project (Ctrl/Cmd+S) opens a native Save As dialog where supported; otherwise enter a filename and use the browser's download settings to choose a folder. Each workspace panel has a labeled Collapse / Expand button.

The preview contains vector drawing and layout tools, editable paths and shapes, text and arrows, an icon editor, synthetic plot tools, local project import/export and 471 editable scientific illustrations: 329 molecular biology, 13 human organoids, 36 expanded cell atlas, 19 early progenitors, 17 original lineage illustrations, 34 embryogenesis illustrations and all 23 Carnegie stages. Molecular variants are grouped into families by default; enable **Show individual variants** for the complete count. Other unresolved private artwork, including laboratory essentials, branded instruments and legacy drawings, is excluded.

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
