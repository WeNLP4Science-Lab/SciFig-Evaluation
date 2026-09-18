# Program Chairs — Editorial Note

**Posted:** 31 Aug 2026, 16:38

> Dear authors,
>
> We were made aware that in your submission the font size in multiple figures is too small to be readable, including but not limited to Figures 2 and 5 through 11. Your submission will not be desk rejected for that, but please make sure to fix it according to the formatting guidelines at https://acl-org.github.io/ACLPUB/formatting.html in the camera-ready or a resubmission.
>
> Yours Sincerely, ARR Editors

## What this means

- **Not blocking** — no desk rejection this round.
- **Must be fixed** for camera-ready OR any resubmission.
- **Explicitly named:** Figures 2, 5, 6, 7, 8, 9, 10, 11.
- **"including but not limited to"** — expect the whole appendix pipeline block (Figs 6–11 are the UML pipeline diagrams).
- Reviewer YLTQ also flagged the pipeline figures independently: "font size very small, unreadable" and appear "directly AI-generated."

## ACL formatting reference

https://acl-org.github.io/ACLPUB/formatting.html — key figure rules:
- All text in figures should be **at least the same size as figure captions** (typically 9pt).
- Figures should be **legible in both print and screen**.
- Vector formats (PDF/SVG) preferred over raster.

## Action items

1. **Figure 2** (main results overview / degradation) — likely too-small axis labels or model-name legends. Regenerate with min 9pt text.
2. **Figures 5–11** (appendix UML pipelines) — YLTQ says they look AI-generated with unreadable fonts. Re-render at higher DPI OR redraw manually as TikZ/vector.
3. Reference each pipeline figure from the main text at least once so readers understand GPT-4o's dual role (YLTQ's suggestion).
