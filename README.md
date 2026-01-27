# Blogs (TypMark .tmd)

This repo stores TypMark `.tmd` sources for the portfolio blog.
On every push to `main`, GitHub Actions renders `.tmd` files to HTML
and publishes them into the `portfolio` repo under `public/blogs-content/`.

The portfolio app fetches the rendered HTML and wraps it with React/Tailwind
when visiting `/blogs/<slug>`.

## URL mapping

The path is preserved from the repo root:

- `tests/a.tmd` -> `/blogs/tests/a`
- `notes/2025/intro.tmd` -> `/blogs/notes/2025/intro`

Each page is generated as `public/blogs-content/<path>.html`.

## Assets

Place shared assets under `assets/`. They are copied to
`portfolio/public/blogs/assets/`.

Use absolute paths in your Markdown so they work from any blog route:

- `/blogs/assets/your-image.png`

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
