# Repo Blueprint & Publishing Runbook — Checklist

Use this to mark off implementation tasks from `docs/Repo Blueprint and Publishing Runbook.md`.

## Repo structure

- [x] `archetypes/` exists
- [x] `content/` exists
- [x] `content/posts/` uses page bundles
- [x] `config/_default/` exists
- [ ] `docs/` contains: content-model.md, image-workflow.md, theme-notes.md *(optional per blueprint)*
- [ ] `scripts/` convenience scripts (optional)

## Content model (front matter schema)

- [x] Post front matter includes required Phase 1 fields: title/date/draft/summary/featured_image/tags/categories
- [x] Optional Phase 2 fields supported: social.excerpt/social.hashtags/location
- [ ] Confirm we’re consistently using **YAML** front matter across repo (posts + pages)

## Naming conventions

- [x] Posts named as `YYYY-MM-DD-short-slug/`
- [x] Featured image convention: `featured.jpg`
- [ ] Decide inline image naming convention (numbered vs descriptive)

## Image workflow standards

- [x] Rule: no RAW originals in git
- [ ] Document export presets (sizes/quality) in a dedicated doc
- [ ] Add an optional image optimisation script (or a manual checklist)

## Git workflow

- [x] Branch model: main + feat/*
- [x] PR template exists
- [ ] Confirm Cloudflare preview deployments appear on PRs (end-to-end)

## Cloudflare deployment

- [x] Repo connected and deploy works
- [x] Submodules handled in build command
- [x] Hugo version pinned (`HUGO_VERSION=0.154.5`)
- [ ] Custom domain fully active + HTTPS green (phishbyhannah.com)

## Quality gates (pre-merge)

- [ ] Local build check documented and used
- [ ] Image size/optimisation check consistently applied
- [ ] Link check pass (manual for now)
- [ ] Mobile review pass (preview deployment)

## Publishing runbook (operational)

- [x] Runbook exists
- [ ] Add a short “Definition of Ready” section to the website authoring docs (optional)
