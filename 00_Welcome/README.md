# Welcome: History of Fire Modeling

Quarto/revealjs conversion of `History_of_Fire_Modeling_4.pptx`, preserving
its 64-slide sequence and 4:3 format. Historical wording, affiliations, image
credits, and source speaker notes are retained. PowerPoint animations become
static slide content; embedded movies use browser video controls.

## Preview and render

From the repository root:

```bash
quarto preview 00_Welcome/welcome.qmd
```

If a project preview is already running, keep using it. After changing an
included section, touch `00_Welcome/welcome.qmd` to trigger its watcher.

To render only this talk:

```bash
quarto render 00_Welcome/welcome.qmd
```

The output is `_site/00_Welcome/welcome.html`. The course start page links to it.

## Source layout

- `welcome.qmd`: entry point and slide settings.
- `00_nist_history.qmd`: NIST history (slides 1–4).
- `01_fire_resistance.qmd`: fire resistance (slides 5–7).
- `02_correlations.qmd`: dimensionless scaling and correlations (slides 8–12).
- `03_zone_models.qmd`: compartment fires and zone models (slides 13–19).
- `04_cfd.qmd`: CFD, ALOFT, and Smokeview (slides 20–33).
- `05_practical_les.qmd`: practical LES and WTC modeling (slides 34–45).
- `06_under_ventilated_fires.qmd`: ventilation, validation, and wildland fires (slides 46–54).
- `07_flame_spread.qmd`: flame spread, applications, and HPC (slides 55–64).
- `custom.css`: slide typography and media placement.
- `figs/`: figures and video posters, with provenance in `ASSETS.md`.
- `videos/`: 17 local MP4 files ready for Release upload, with `manifest.csv`.

Most slides use editable HTML text and individual images inside a fixed canvas
to retain the original arrangements. Edit the text directly in the section
files; positions are percentages of the slide canvas. Equations on the scaling,
MQH, and puffing-frequency slides use LaTeX. There is no conversion tool needed
to edit or render this talk.

## Video release assets

The slides already reference:

`https://github.com/rmcdermo/Juelich_Summer_School/releases/download/2026/`

Upload the 17 `welcome-*.mp4` files with their existing names to the `2026`
Release. The local videos are ignored by Git, and this conversion does not
upload them. Until upload, slides display their poster images but playback
will not work. Poster files are explicitly included in `_quarto.yml`.

From the repository root, after reviewing `videos/manifest.csv`:

```bash
gh release upload 2026 00_Welcome/videos/welcome-*.mp4 --repo rmcdermo/Juelich_Summer_School
```

The manifest records the source slide, original embedded filename, target
Release filename, poster, size, and SHA-256. The original MPG and ProRes MOV
were converted to H.264 MP4. The line-burner clip was also converted to H.264,
and PCM audio in the full-scale experiment was converted to AAC. Other
original MP4 clips were preserved.
