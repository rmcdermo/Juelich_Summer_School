# Repository instructions

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
