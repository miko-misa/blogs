# Blogs (TypMark .tmd)

This repo stores TypMark `.tmd` sources for the portfolio blog.
On every push to `main`, GitHub Actions renders `.tmd` files to HTML
and publishes them into the `portfolio` repo under `public/blogs-content/`.

The portfolio app fetches the rendered HTML and wraps it with React/Tailwind
when visiting `/blogs/<slug>`.

## Folder info manifest (required)

Each folder that contains `.tmd` files **must** include an `info.json` file.
Only files listed in `info.json` are rendered and published.

Example format:

```
{
  "display": "Folder A",
  "articles": {
    "a": {"title": "Math 1"},
    "b": {"title": "Math 2"}
  }
}
```

- `display`: the folder display name shown in listings
- `articles`: keys are slugs and must match `<slug>.tmd` in the same folder
- `title`: title shown in folder listings

## URL mapping

The path is preserved from the repo root, using each slug:

- `tests/hello.tmd` -> `/blogs/tests/hello`
- `notes/2025/intro.tmd` -> `/blogs/notes/2025/intro`

## Folder listing

Accessing a folder shows a list of pages in that folder and any child folders
that also have `info.json`.

- `/blogs/` shows items listed in `/info.json`
- `/blogs/tests` shows items listed in `tests/info.json`

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
