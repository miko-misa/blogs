# Blogs (TypMark `.tmd`)

This repository is the canonical source for the TypMark articles published on the Hacnosuke portfolio.

During the Vercel/Cloudflare coexistence phase, every push to `main`:

1. downloads the pinned TypMark CLI;
2. validates and renders every listed article;
3. generates the folder/article index;
4. publishes the generated handoff to the private `portfolio` repository;
5. lets the portfolio host build the static SEO routes and React UI.

Generated HTML is not the source of truth. Edit `.tmd`, `info.json`, and `assets/` here.

## Folder manifest

Every folder containing articles must include `info.json`. Only listed articles are rendered and published.

```json
{
  "display": "Machine Learning",
  "description": "Folder description used by listings and SEO.",
  "articles": {
    "intro": {
      "title": "Introduction",
      "description": "Article summary shown in cards and search metadata."
    }
  }
}
```

| Field | Purpose |
| --- | --- |
| `display` | Folder title shown in listings |
| Folder `description` | Category summary and SEO description |
| `articles` key | Slug matching `<slug>.tmd` in the same folder |
| Article `title` | Listing and article title |
| Article `description` | Listing card summary and page metadata |

An omitted description is filled from article content by the portfolio build when possible.

## URL mapping

Repository paths are preserved below `/blogs/`:

```text
tests/hello.tmd -> /blogs/tests/hello/
notes/intro.tmd -> /blogs/notes/intro/
```

## Assets

Place shared assets under `assets/` and reference them with an absolute URL:

```text
/blogs/assets/your-image.png
```

## Local rendering

Install or download the pinned TypMark CLI, then run the same renderer used by GitHub Actions:

```bash
python3 scripts/render_site.py --typmark /path/to/typmark-cli
```

Output is written to the ignored `site/` directory:

```text
site/blogs-content/
site/blogs/assets/
site/blogs-index.json
```

Run the renderer self-check with:

```bash
python3 -m unittest scripts/test_render_site.py
```

## Current publishing credential

The coexistence workflow currently needs this GitHub Actions secret:

- `PORTFOLIO_PUSH_TOKEN`: write access limited to `miko-misa/portfolio`

A fine-grained token is preferred over a classic `repo` token. Generated portfolio commits remain temporarily necessary to keep Vercel and Cloudflare synchronized during canary testing.

After the Cloudflare production gate passes, this push credential will be replaced with a dispatch-only credential and generated portfolio commits will stop. The authoritative migration and retirement procedure is maintained in the private portfolio repository at `docs/hosting-migration.md`.
