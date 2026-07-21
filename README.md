# Business Information Systems — Open Textbook

This is a Quarto "book" project. Chapters live in `chapters/`, downloadable
companion workbooks live in `assets/starter-files/`, and screenshots (once
captured) live in `assets/images/`.

## Rendering locally

You'll need Quarto installed (https://quarto.org/docs/get-started/), a free,
one-time install, unrelated to any course software. Once installed:

    quarto render        # builds the static site into _book/
    quarto preview        # live-reloading local preview while you write

## Publishing to GitHub Pages

The included `.github/workflows/publish.yml` renders and deploys the book
automatically on every push to `main`, using GitHub Actions (also free). In
the repo's Settings > Pages, set the source to the `gh-pages` branch after
the first successful workflow run, and the book will be live at
`https://<username>.github.io/<repo-name>/`.

## Adding a new chapter

1. Add a new `.qmd` file under `chapters/`.
2. List it in `_quarto.yml` under `book: chapters:`, in the order it should appear.
3. Drop any companion workbook into `assets/starter-files/` and link to it
   from the chapter, the way Chapter 1 links to its starter file.

## Adding an appendix

Same idea as a chapter, but list the `.qmd` under `book: appendices:` in
`_quarto.yml` instead of `chapters:`. Quarto groups appendices separately in
the sidebar and gives them letter labels (Appendix A, B, ...) instead of
chapter numbers.

## Status

Chapter 1 is the first full draft, alongside Appendix A (an Excel quick
reference covering the whole Excel unit, Chapters 1-3, in one dense page).
This repo is a working model of the structure, not a finished book, more
chapters get added the same way.
