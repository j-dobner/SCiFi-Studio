# SCiFi Studio

**Free, open-source scientific illustration and figure editor.**

v22.0 public preview · 27 November 2026

[Download the standalone editor](https://raw.githubusercontent.com/j-dobner/SCiFi-Studio/main/SCiFi-Studio.html) · [Software license](LICENSE) · [Artwork license](artwork/LICENSE.md)

## Get started

1. Download `SCiFi-Studio.html` (use Save Link As or GitHub's download raw file button).
2. Open it in a current desktop browser. No installation, account or server is required.
3. Draw, edit and assemble figures; save editable projects locally or export SVG/PNG.

The preview contains vector drawing and layout tools, editable paths and shapes, text and arrows, an icon editor, synthetic plot tools, local project import/export and 57 editable developmental biology illustrations: 34 embryogenesis illustrations and all 23 Carnegie stages. Other private development artwork collections are not included in this preview while their rights review continues.

## Source and build

Open `index.html` from a local checkout, keeping the `artwork/` folder beside it. Run `python tools/build.py` to recreate the single-file offline editor. The generated standalone is committed for convenient download.

## Licensing and credit

Software: [MIT](LICENSE). Original developmental artwork listed in [the provenance manifest](artwork/PROVENANCE.json): [CC0 1.0 Universal](artwork/LICENSE.md). Interface glyphs retain their [third-party license notices](THIRD-PARTY-NOTICES.md). User-imported materials and other third-party rights are not covered by the artwork dedication.

Project creator, scientific direction and AI-assisted development: **Jochen Dobner**.

Rights holder: IUF - Leibniz-Institut für umweltmedizinische Forschung GmbH. See [CITATION.cff](CITATION.cff) for citation information.

## Preview status

Validated by automated geometry checks, JavaScript syntax checks and a Chromium smoke test. Not a complete cross-browser, accessibility or scientific validation. Illustrations are schematic, not diagnostic; check accuracy and suitability for your use. Please report issues through GitHub.
