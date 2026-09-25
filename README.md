# Jülich Summer School on Fire Dynamics Modeling

Documentation repository for the [Jülich Summer School on Fire Dynamics Modeling](https://www.fz-juelich.de/en/ias/ias-7/research-1/divisions/fire-dynamics/intro/3rd-summer-school-on-fire-dynamics-modeling-2022)

## Lecture Team

Simo Hostikka (Aalto University, Finland)  
Bjarne Husted (DTU - Technical University of Denmark)  
Kevin McGrattan (NIST)  
Randall McDermott (NIST)    
Marcos Vanella (NIST)  
Jason Floyd (Fire Safety Research Institute, UL Research Institutes)  
Lukas Arnold (Forschungszentrum Jülich GmbH)  
Alexander Belt (Forschungszentrum Jülich GmbH)  
Emanuele Gissi (Corpo Nazionale dei Vigili del Fuoco)  

## Quarto Presentations

Presentations are written in [Quarto](https://quarto.org/) Markdown (`.qmd`) and rendered as reveal.js slides for viewing in a web browser. Use an existing lecture, such as [Combustion](08_Combustion/README.md), as a starting point for preparing talks.

### Install Quarto

Download and install the [Quarto CLI](https://quarto.org/docs/get-started/) for Windows, macOS, or Linux. Then open a terminal and verify the installation:

```bash
quarto --version
```

### Preview a presentation

From the repository root, change to the lecture directory and preview its main `.qmd` file. For example:

```bash
cd 08_Combustion
quarto preview combustion.qmd
```

Quarto opens the presentation in your browser and refreshes it as you save changes. Keep the terminal running during editing; press `Ctrl+C` to stop the preview. For modular lectures, preview the main file (such as `combustion.qmd`), which includes the individual section files.

To generate the HTML presentation without starting a preview:

```bash
quarto render combustion.qmd
```

## Published talks (GitHub Pages)

The talks website is deployed to
[rmcdermo.github.io/Juelich_Summer_School](https://rmcdermo.github.io/Juelich_Summer_School/).
The landing page links to the five current Quarto presentations. Other course
materials remain available in this repository.

The [Pages workflow](.github/workflows/pages.yml) builds the website on pull
requests and deploys it on pushes to `main`. Once the workflow is on `main`, it
can also be started from **Actions → Deploy talks to GitHub Pages → Run workflow**.
Deployment status and the published URL appear in that workflow run.

### GitHub configuration

- Set **Settings → Pages → Build and deployment → Source** to **GitHub Actions**
  (already configured).
- GitHub Actions must be enabled. If **Settings → Actions → General** restricts
  allowed actions, allow the `actions/*` actions and
  `quarto-dev/quarto-actions/setup` used by the workflow.
- The deployment uses the `github-pages` environment. If its protection rules
  restrict deployment branches, allow `main`; if required reviewers are enabled,
  approve the deployment when prompted.
- No personal access token, repository secrets, `gh-pages` branch, or custom
  domain is required. The workflow grants its deployment job the necessary
  permissions; the repository's default workflow permissions can remain read-only.

Commit and push these files to `main` (or merge a pull request) to trigger the
first deployment. No further settings are normally needed.

### Build the website locally

The workflow uses Quarto **1.10.18**. From the repository root:

```bash
quarto render
quarto preview
```

The rendered website is written to `_site/`, which is excluded from Git. The
explicit render list in `_quarto.yml` includes only the landing page and lecture
entry points, not individual section files. To publish another Quarto talk, add
its entry point to that list and add a link in `index.qmd`.

Only files committed to Git are available during deployment. Videos excluded by
`.gitignore` must be hosted separately (for example, as GitHub Release assets)
and referenced by URL, as the Combustion lecture already does. MathJax and
externally hosted videos require an internet connection when viewing the talks.

Currently, three referenced videos are not in Git and will not play on the site:

- `04_Pressure/Section_1_assets/video/compartment-oxygen-deflagration.mp4`
- `04_Pressure/Section_1_assets/video/ceiling-board-heat-soot.mp4`
- `05_Turbulence/figs/small_compartment_demo.mp4`

Upload these clips to a suitable host and update their slide references to the
published URLs to make them available online. Video poster images are explicitly
listed in `_quarto.yml` because Quarto does not automatically copy every poster;
add new poster images to that resource list as needed.
