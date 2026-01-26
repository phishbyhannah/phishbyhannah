# Development Action Items (phishbyhannah)

A working checklist for building, polishing, and operating the phishbyhannah website.

## Site information architecture & content

- [ ] Finalise site positioning copy for homepage (1–2 sentence hero + supporting bullets)
- [ ] Replace any remaining theme/demo content and defaults
- [ ] Ensure first-person voice is consistent across Home/About/Services pages
- [ ] Build an initial portfolio / gallery approach (optional)

## Services packaging (structure + clarity)

- [ ] Decide the long-term services structure (audience pages vs ocean-tier packages) and make naming consistent across all pages
- [x] Social Media packages page exists (no public pricing)
- [x] Brands packages page exists (no public pricing)
- [x] Resorts packages page exists (no public pricing)
- [ ] Add consistent “Best for” + “How it works” sections across Brands/Resorts/Social Media
- [ ] Add an FAQ section answering common scope questions (revisions, approvals, turnaround, what the client provides)

## Taxonomy (blog categories)

- [ ] Add broad starter categories (from blueprint):
  - Ocean Experiences
  - Travel Comms
  - Lifestyle Content
- [ ] Decide tag conventions (descriptive vs numbered image naming; stable category set vs flexible tags)

## Image workflow & performance

- [ ] Write `docs/image-workflow.md` with export presets (sizes/quality) and naming conventions
- [ ] Add an optional helper script (e.g., `scripts/optimize-images.sh`) or a manual optimisation checklist
- [ ] Define a hard file-size budget per image (e.g., <=800KB) and a max width (e.g., 2400px)

## Cloudflare deployment & domain

- [ ] Confirm custom domain is fully active + HTTPS green (phishbyhannah.com)
- [ ] Confirm preview deployments appear on PRs and are used for review
- [ ] Document the exact Cloudflare build/deploy settings (already captured in `docs/cloudflare-setup.md`)

## Quality gates (pre-merge)

- [ ] Local preview check before PR (hugo server)
- [ ] Mobile review check on preview deployment
- [ ] Link check (manual for now)
- [ ] Image optimisation check (manual for now)

## Copy & packaging improvements (from PDF analysis)

- [ ] Clarify engagement scope (what “basic engagement” includes/excludes; comment vs DM handling; response expectations)
- [ ] Remove ambiguity in deliverables where ranges exist (e.g., 12–15 posts) OR explain the range clearly
- [ ] Tighten the reel/value explanation: focus on outcomes + what Hannah actually produces (shoot/edit/post), not just “algorithm talk”
- [ ] Fix any layout/typo issues present in exported PDFs (spacing/word-joins like “PERWEEK”, “MOREEXTRA”) and ensure web copy is clean
- [ ] Add a short “Best for…” line to every package/tier and ensure it’s consistent across services
- [ ] Add a “What you need to provide” section (brand assets, access, approvals window, shoot logistics)
- [ ] Add turnaround + cadence details (planning call cadence, scheduling rhythm, approvals timing)
- [ ] Clarify whether photography is included in each package tier and what’s assumed vs supplied

---

Last updated: 2026-01-26
