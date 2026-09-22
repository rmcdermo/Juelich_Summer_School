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
