# Module III: Flame Extinction — slide and asset inventory

The editable slides are in [`../../03_flame_extinction.qmd`](../../03_flame_extinction.qmd), included by [`../../combustion.qmd`](../../combustion.qmd); layouts are in [`../../custom.css`](../../custom.css).

Source numbers below refer to `08_Combustion/Lecture_UNTRACKED/Combustion_lecture_McDermott.pptx`, slides 93–114, and the corresponding original PNGs in `figs/reference-slides/`. Those originals are references, not runtime dependencies of the updated module.

| Source slide | Slide | Figures / implementation | Example links |
|---|---|---|---|
| 93 | Fire Suppression versus Flame Extinction | `oxygen-dilution-flames.png`; native lists and White et al. (2015) citation | — |
| 94 | Binary Flame Extinction for EDC | Native transport, source-term, and binary-factor equations; “Flame Extinction Factor (FEF)” label; Vilfayeau et al. (2016) citation | — |
| 95 | Continuous Flame Extinction for EDC | `flame-islands.svg`; native source-term equation and proposed-model wording | Generator linked on slide |
| 96 | Mechanisms of Flame Extinction | Native list; Vaari, Floyd, and McDermott (2011) citation, verified from the supplied paper | [Paper DOI](https://doi.org/10.3801/IAFSS.FSS.10-781) |
| 97 | Oxygen Criterion: Mowrer's Model | Native list | — |
| 98 | Oxygen Criterion: Derivation | Native aligned equations and blue result box | — |
| 99 | Simple Models of Flame Extinction | `extinction_1.png`, `extinction_2.png`; 400 dpi page renders with separate native text boxes and straight CSS arrows | [FDS manuals](https://pages.nist.gov/fds-smv/manuals.html) |
| 100 | Example: Simple Extinction Model | Native exercise | [`Qs=1_RI=05.fds`](../../examples/extinction_example/Qs=1_RI=05.fds) |
| 101 | FDS Thermal Extinction Model | Native mass and enthalpy balances | — |
| 102 | Defining the Stoichiometric Pocket | `stoichiometric-pocket-field.png` with restored original red ink annotations; native equations and pocket underbrace | — |
| 103 | FDS Thermal Extinction Model: Dilution | `dilution-cells.svg`; native heat-release and sensible-enthalpy balance | — |
| 104 | FDS Thermal Extinction Model: Criterion | `dilution-cells.svg`; native criterion and green box | — |
| 105 | Example: FDS Thermal Extinction | Native exercise; physical temperatures and FDS input values | [`Qs=1_RI=05.fds`](../../examples/extinction_example/Qs=1_RI=05.fds) |
| 106 | Simple Ignition Model (AIT) | `piloted-ignition-zone.png`; native list and White et al. (2017) citation | — |
| 107 | Example: Cup Burner | Native exercise using available files and pilot-zone syntax | [`Cup_methane_n2.fds`](../../examples/cup_burner_example/Cup_methane_n2.fds), [`Cup_methane_n2_pilot.fds`](../../examples/cup_burner_example/Cup_methane_n2_pilot.fds) |
| 108 | Pilot Ignition Model | `pilot-fuel-volume-fraction.png`; native instructions and AIT unit conversion | — |
| 109 | Example: Pilot Fuel Ignition | Native exercise | [`test_pilot.fds`](../../examples/pilot_fuel_example/test_pilot.fds) |
| 110 | Aerodynamic Quenching | `aerodynamic-quenching.svg`, `opposed-jet.svg`; qualitative diagrams | Generator linked on slide |
| 111 | Steady Laminar Flamelet | `opposed-jet.svg`; native species, mixture-fraction, and coordinate equations | OPPDIFF is the source label, not an available linked example |
| 112 | Steady Laminar Flamelet: Equations | Native aligned derivation, mixture-fraction cancellation, and scalar-dissipation definition | — |
| 113 | Damköhler Number | Native time-scale ratio | — |
| 114 | Borghi Diagram | `borghi-diagram.png`; original regime diagram | — |

## Updated comparison plots (2026-09-24)

`extinction_1.png` and `extinction_2.png` are full-page, 400 dpi renders of the user-supplied FDS-6.11.1-259-gb136b54-nightly verification PDFs. The slide uses ordinary QMD image syntax. Only the PNG figures are intended for version control; `extinction_1.pdf` and `extinction_2.pdf` are retained locally and excluded by `.gitignore`. There is no PDF viewer or custom rendering JavaScript.

To regenerate a PNG from its local source, run `pdftoppm -f 1 -singlefile -r 400 -png extinction_1.pdf extinction_1` in this directory, and repeat for `extinction_2`.

Native QMD labels and straight CSS arrows are overlaid separately. `FREE_BURN_TEMPERATURE` points to the foot of Model 1's vertical cutoff; `CRITICAL_FLAME_TEMPERATURE` points to Model 2's temperature-axis intercept. The overlay styles are in `../../custom.css` under `.ext-plot-overlay` and `.ext-temperature-arrow`.

Both labels are independent white text boxes with 24 px blue type, positioned above and to the right of their axis values. Straight arrows point down from the boxes to the corresponding temperature thresholds. Arrow coordinates assume the supplied 432 × 432 pt PDF pages displayed at 560 × 560 px. The column headings are centered over the plot axes (x = 81–405 pt). Rebuild with `quarto render 08_Combustion/combustion.qmd`.

## Figure provenance

Embedded-media paths refer to the source PPTX ZIP archive. Extracted plots are preserved lecture results; no numerical data have been inferred from their pixels.

| File | Origin and changes |
|---|---|
| `oxygen-dilution-flames.png` | `ppt/media/image224.png`, crop `(0, 0, 406, 406)` to retain the flame photographs; citation and direction caption are native slide content. |
| `simple-extinction-comparison-a.png` | `ppt/media/image230.png`, unchanged original verification plot. |
| `simple-extinction-comparison-b.png` | `ppt/media/image231.png`, unchanged original verification plot. |
| `piloted-ignition-zone.png` | `ppt/media/image254.png`, unchanged original annotated Smokeview figure. |
| `pilot-fuel-volume-fraction.png` | `ppt/media/image255.png`, unchanged original Smokeview figure. |
| `stoichiometric-pocket-field.png` | Source slide 102, Group 18: `ppt/media/image237.png` with the original red ink images `image238.png`–`image246.png` (nine overlays), composited in source order at their original DrawingML positions into an 800 × 800 PNG. The red markings are the original hand-drawn annotations, not computed contours; the pocket expression remains native math. |
| `turbulent-composition-field.png` | `ppt/media/image144.png`, source field used as input to the flame-island schematic. |
| `borghi-diagram.png` | `ppt/media/image15.tif`, converted to RGB PNG. The source deck does not supply the original diagram attribution. |
| `flame-islands.svg` | Generated from the turbulent field and illustrative flame-island markers. |
| `dilution-cells.svg` | Generated square-cell schematic of fuel/air pockets, following source slides 103–104. |
| `opposed-jet.svg` | Generated opposed-jet schematic, following source slides 110–112. |
| `aerodynamic-quenching.svg` | Generated qualitative CFT/strain boundary, following source slide 110; no quantitative curve data are claimed. |

## Regenerate the schematics

Requires Python, NumPy, Matplotlib, and Pillow. From the repository root:

```sh
python3 08_Combustion/figs/flame_extinction/draw-extinction-diagrams.py
quarto render 08_Combustion/combustion.qmd
```

The script resolves its input and output paths relative to itself and writes the four SVG files above. Keep the script and `turbulent-composition-field.png` with the generated figures. The source PPTX is not needed to rebuild these schematics or the updated slides.

## Review notes (2026-09-23)

- All 22 content slides retain their sequence and source topic. Text, equations, exercise prompts, boxes, and slide headings are editable QMD/CSS. Full-slide screenshot dependencies were removed from this module.
- The thermal-model exercise now explicitly selects `EXTINCTION_MODEL='EXTINCTION 2'`; the supplied example initially selects Model 1.
- Physical critical flame temperatures of 1700 K and 1800 K correspond to FDS `CRITICAL_FLAME_TEMPERATURE` inputs 1426.85 °C and 1526.85 °C. The original slide mixed the physical temperatures with the input keyword. Pilot AIT of 0 K is likewise identified as −273.15 °C in FDS input.
- The missing `Cup_CH4_N2.fds` reference was replaced by the available methane cup-burner case. Pilot instructions use `AIT_EXCLUSION_ZONE` on `REAC`, matching the supplied pilot variant and the local FDS User Guide, instead of the legacy INIT/AIT wording.
- Simple-extinction and cup-burner exercises note settings that are already present in their supplied input files. The input files themselves were not changed or simulated during this slide update.
- FDS syntax and units were checked against the local `fds/Manuals/FDS_User_Guide/FDS_User_Guide.tex` sections “Extinction” and “Ignition,” plus the linked example inputs.
- The original comparison plots, Smokeview images, and Borghi diagram were retained. Their original numerical datasets were not available for regeneration. The newly drawn CFT/strain curve is explicitly qualitative.
- Comparison headings were centered over the legacy plot axes; the updated PDF alignment is documented above.
- Verification: Quarto rebuild, native-content and local-link checks, equation delimiter checks, deterministic schematic regeneration, visual inspection of all module figure assets, and `git diff --check`. Browser layout review remains pending because automatic approval review rejected browser access with an HTTP 404 service error.
