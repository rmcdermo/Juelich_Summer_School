# Combustion lecture assets

The assets in this directory were derived from `Lecture_UNTRACKED/Combustion_lecture_McDermott.pptx`; that PowerPoint file remains untracked.

- `pptx-media/` contains the 277 raster images extracted verbatim from the original deck (262 PNG and 15 TIFF images). The embedded videos are excluded from this bulk extraction.
- `reference-slides/` contains 118 rasterized source slides. The modular QMD deck uses these as an accurate, complete baseline while individual slides are progressively rebuilt as native Markdown and MathJax.

- `thermochemistry/` contains locally generated figures and a selective `source/` extraction used by the native Thermochemistry section. The source extraction is provisional, derived from the untracked PowerPoint, and must be reviewed for provenance before public distribution. See its README for the source-visual replacement list and licensing status.

- `thermochemistry/video/fire-tests-real-materials.mp4` is the 33.8 s video used on the “Fire tests with real materials” slide. It was extracted from slide 20 of the original deck and is kept locally until it can be distributed as a GitHub release asset.

The QMD sources preserve the original slide numbers through their `reference-slides/slide-NNN.png` paths. This makes it straightforward to replace a reference slide with the corresponding extracted figure assets without losing the original lecture sequence.
