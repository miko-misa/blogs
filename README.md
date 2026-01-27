# Blogs (TypMark .tmd)

This repo stores TypMark `.tmd` sources for the portfolio blog.
On every push to `main`, GitHub Actions renders `.tmd` files to HTML
and publishes them into the `portfolio` repo under `public/blogs-content/`.

The portfolio app fetches the rendered HTML and wraps it with React/Tailwind
when visiting `/blogs/<slug>`.

## Articles manifest (required)

Each folder that contains `.tmd` files **must** include an `articles.xml` file.
Only files listed in `articles.xml` are rendered and published.

Example format:

```
<articles>
  <article file="a.tmd" slug="a" title="My Article" />
  <article file="b.tmd" slug="b" title="Another One" />
</articles>
```

- `file`: the `.tmd` filename in the same folder
- `slug`: output slug (used in URL)
- `title`: title shown in folder listings

## URL mapping

The path is preserved from the repo root, using each `slug`:

- `tests/a.tmd` with slug `hello` -> `/blogs/tests/hello`
- `notes/2025/intro.tmd` with slug `intro` -> `/blogs/notes/2025/intro`

## Folder listing

Accessing a folder shows a list of pages in that folder and any child folders
that also have `articles.xml`.

- `/blogs/` shows items listed in `/articles.xml`
- `/blogs/tests` shows items listed in `tests/articles.xml`

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
