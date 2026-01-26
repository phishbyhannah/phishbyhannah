# Publishing runbook (phishbyhannah)

## One-time setup

- Install Hugo (extended): `hugo version`
- Clone the repo with submodules:

```bash
git clone --recurse-submodules <repo-url>
```

If you already cloned without submodules:

```bash
git submodule update --init --recursive
```

## Local preview

```bash
hugo server -D
```

## Create a new post

```bash
hugo new content posts/<slug>/index.md
```

Add images into the same folder:

```
content/posts/<slug>/
  index.md
  featured.jpg
  gallery-1.jpg
```

## Publish workflow (GitHub)

1. Create a branch:

```bash
git checkout -b post/<slug>
```

2. Write/edit content, preview locally.
3. Commit and push:

```bash
git add -A
git commit -m "Add post: <title>"
git push -u origin HEAD
```

4. Open a Pull Request on GitHub.
5. Review the Cloudflare Pages **preview deployment**.
6. Merge PR to deploy to production.

## Image rules (keep the repo fast)

- Do not commit RAW originals.
- Target sizes (starting point):
  - Featured image: <= 2400px wide, <= ~600KB
  - In-post images: <= 2400px wide (or smaller), <= ~600KB each
  - Prefer JPG for photos, PNG only when necessary.
