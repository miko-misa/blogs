# Blogs (TypMark .tmd)

This repo stores TypMark `.tmd` sources for the portfolio blog.
On every push to `main`, GitHub Actions renders `.tmd` files to HTML
and publishes them into the `portfolio` repo at `public/blogs/`.

## URL mapping

The path is preserved from the repo root:

- `tests/a.tmd` -> `/blogs/tests/a/`
- `notes/2025/intro.tmd` -> `/blogs/notes/2025/intro/`

Each page is generated as `public/blogs/<path>/index.html`.

## Assets

Place shared assets under `assets/`. They are copied to
`portfolio/public/blogs/assets/`.

Refer to them in HTML via `/blogs/assets/...`.

## Required GitHub secret

Add this secret to the **blogs** repository:

- `PORTFOLIO_PUSH_TOKEN`: a PAT with write access to
  `https://github.com/miko-misa/portfolio.git`

Recommended: a classic PAT with `repo` scope.

## Local render (optional)

If you have `typmark-cli` installed:

```
./typmark-cli --render --theme dark input.tmd > output.html
```
