# Alloy optics bench: build

The widget is one self-contained HTML file (`../index.html`). The data is baked in, so it works offline, and inside a Confluence HTML macro.

## Rebuild or add metals

```
pip install colour-science pyyaml numpy
python fetch_data.py raw_data              # downloads the n,k files (refractiveindex.info, CC0)
python build_data.py raw_data data.json    # spectra, colour tables, ACEScg matrix
python inject.py data.json                 # writes ../index.html
```

To add a metal: add its file to `FILES` in `fetch_data.py`, add a line to the list `M` in `build_data.py` (plus `COMP` if it's an alloy you want in the mixing test), then rerun the three steps.

## What the numbers are

- Colours: CIE 1931 2° observer, D65 daylight, 5 nm steps, 380–780 nm.
- ACEScg: XYZ → ACEScg with Bradford white-point adaptation, so a perfect white is (1, 1, 1).
- Fitted edge tint: reflectivity from the full-spectrum colour at 0°; edge tint fitted per channel so the Gulbrandsen (2014) n,k match the full-spectrum colour at every angle.
- Querry's zinc is excluded (n ≈ 13 in the visible); Werner's zinc is used.
