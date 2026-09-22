# Combustion lecture

This directory contains the Quarto/revealjs version of the Jülich Summer School combustion lecture.

## Render the presentation

From this directory, run:

```bash
quarto render combustion.qmd
```

This creates `combustion.html`, which can be opened in a web browser.

For a live preview while editing, run:

```bash
quarto preview combustion.qmd
```

Quarto 1.x is required. The deck uses revealjs and loads MathJax from the configured CDN when mathematical typesetting is needed.

## Source layout

- `combustion.qmd` is the presentation entry point.
- `examples/` contains the Python examples and FDS input cases, grouped by topic. Run each example from its own subfolder so relative data paths resolve correctly.
- `00_overview.qmd` contains the rubric, outline, and reading list.
- `01_thermochemistry.qmd`, `02_eddy_dissipation_concept.qmd`, `03_flame_extinction.qmd`, and `04_review.qmd` are the lecture sections.
- `figs/` contains the extracted PPTX raster assets and reference-slide images. See `figs/ASSETS.md` for details.

`Lecture_UNTRACKED/` contains the source PowerPoint decks and remains outside version control. The Quarto lecture uses the McDermott deck as its baseline.
