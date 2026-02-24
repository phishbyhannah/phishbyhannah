# phishbyhannah

Photo-forward dark theme site + blog built with Hugo and deployed via Cloudflare Pages.

## Local dev

```bash
hugo server -D
```

Then open http://localhost:1313

## Publishing (high level)

1. Create a new post: `hugo new content posts/<slug>/index.md`
2. Add images under the post folder.
3. Preview locally: `hugo server -D`
4. Commit + push; open a PR.
5. Preview deploy runs on the PR (Cloudflare Pages).
6. Merge to deploy to production.

Docs: see `docs/`.

## Image workflow

- Optimize committed images:
  - `bash scripts/optimize-images.sh`
  - Defaults are quality-first (high quality, minimal downsampling). Override with env vars if needed.
- Validate policy locally:
  - `python3 scripts/image_policy_check.py`
- Optional pre-commit hook:
  - `git config core.hooksPath .githooks`
