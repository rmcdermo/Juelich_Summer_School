# Repository instructions

## Git staging

- Never use or recommend `git add -A` (including with a path restriction).
- Stage only explicitly named files with `git add -- <file> ...`; do not use
  directory-wide staging or `git add .`.
- For a deletion or move, inspect the index and handle the specific old path
  explicitly rather than staging all changes in a directory.

## Figure quality

- Prefer true vector SVG for generated plots and diagrams. Do not embed raster
  screenshots in an SVG and treat that as vector output.
- When PNG is necessary, export enough pixels for the displayed size (at least
  twice the intended display width and height; typically 300 dpi for plots).
  Do not enlarge low-resolution images.
- Check figures at their actual slide size. Labels, equations, and lines must
  be sharp and comfortably readable, with typography appropriate to the slide.
  A vector file alone does not excuse tiny labels or a cramped layout.

## Notebook files and Git cleanup

- Do not add ignore rules for `*.ipynb` or `*.quarto_ipynb` in this repository,
  including nested `.gitignore` files. The user explicitly wants untracked
  notebook files eligible for ordinary `git clean` removal.
- Quarto 1.10.18 automatically adds `**/*.quarto_ipynb` to `.gitignore` during
  project renders, including renders performed by a live preview. This is an
  unwanted tool side effect, not permission to retain the rule.
- After any render or preview work, check the repository's `.gitignore` files
  and remove notebook ignore rules that Quarto added. Preserve other user edits.
  Do not commit these generated ignore rules or run `git clean` unless asked.

## Existing live previews

- When the user already has a Quarto preview running, leave it running and edit
  the source files. Do not start a duplicate preview or rebuild the full website
  unless requested or necessary to diagnose a stale preview.
- Edits to included section `.qmd` files may not trigger the running preview.
  After editing a section, touch the corresponding main talk `.qmd` file to
  trigger its watcher, then verify that the changed text appears in `_site/`.
  Do not assume that saving an included file refreshed the rendered slide.
