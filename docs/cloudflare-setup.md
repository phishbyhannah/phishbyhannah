# Cloudflare deploy notes (phishbyhannah)

Cloudflare's dashboard UI may route you through a unified "Projects" flow that still uses Wrangler for the final deploy step.

## Known-good settings

### Repository
- `phishbyhannah/phishbyhannah`
- Branch: `main`

### Build command
```bash
git submodule update --init --recursive && hugo --gc --minify
```

Rationale:
- Theme is a git submodule (`themes/blowfish`), so we must initialise submodules in CI.
- Hugo builds static output to `./public`.

### Deploy command
```bash
npx wrangler deploy --assets=./public --compatibility-date=2026-01-26 --name=phishbyhannah
```

Notes:
- This is effectively deploying a static asset directory via Wrangler.
- Keep `--assets=./public` aligned with Hugo's output directory.

### Root directory
- `/`

### Environment variables
- `HUGO_VERSION=0.154.5`

## Troubleshooting

- Error about missing theme / `blowfish` not found:
  - Ensure the build command includes `git submodule update --init --recursive`.

- Hugo not found / wrong version:
  - Set `HUGO_VERSION` in project env vars.

- Assets directory errors:
  - Confirm Hugo output directory is `public` and deploy command includes `--assets=./public`.
