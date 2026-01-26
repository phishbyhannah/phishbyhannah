# Project Charter and Backlog

## Project name

Ocean/Lifestyle Consulting Website Platform (Hugo + Git + Cloudflare)

## 1. Purpose

Create a cost-controlled, high-performance public website consisting of:

* A business landing site (services, positioning, portfolio highlights, contact).
* A blog (markdown-authored posts with strong visual storytelling).
* A foundational content-and-process core that later enables centralized and automated social distribution.

## 2. Business context

The business is a digital production and communications consulting company serving lifestyle, travel, and experience brands. Differentiation is anchored in underwater photography, ocean experiences, and beach lifestyle activities.

## 3. Objectives

### MVP objectives (Phase 1)

1. Launch a professional landing page and blog, hosted on Cloudflare Pages, built with Hugo.
2. Establish repeatable publishing operations: local authoring → Git push → Cloudflare build/deploy.

### Foundation objectives (Phase 2+)

1. Standardize content structure and metadata so every post is distribution-ready.
2. Enable later automation for social distribution without re-architecting the website.

## 4. Non-goals (explicitly out of scope for MVP)

* GUI-based CMS and editorial workflow tooling beyond Markdown + Git.
* E-commerce, bookings, memberships, personalization.
* Complex backend systems; any dynamic functionality to be considered later via optional serverless components.

## 5. Stakeholders and roles

* Content Owner (Daughter): brand voice, photography selection, editorial calendar, final approval.
* Platform Owner (You): Hugo scaffolding, theme, Git processes, Cloudflare Pages configuration, automation later.
* Optional Reviewer (Trusted third party): pre-launch QA review of copy, UX, and links.

## 6. Constraints and guiding principles

* Cost control: remain within free tiers wherever possible (Git hosting + Cloudflare Pages).
* Git is the source of truth: content, configuration, and presentation are versioned.
* Static-first architecture: keep the public site static for speed, simplicity, and low operational burden.
* Image discipline: originals stay local/off-repo; only web-optimized assets are committed.
* Operational simplicity: documented steps that can be executed consistently by a non-developer.

## 7. Deliverables

### Phase 1 (MVP)

* Hugo site repository with theme and minimal customizations.
* Landing page, about/services, portfolio highlights page (optional), and contact page.
* Blog list and blog post templates (archetypes) with consistent metadata.
* Cloudflare Pages project connected to the Git repo with automatic deploys.
* Preview deployments on pull requests for safe review before production.
* Publishing Runbook (authoring to production process).

### Phase 2 (Foundation for distribution)

* Standardized metadata for social distribution (summary, featured image, tags, social excerpt).
* RSS feed and OpenGraph/Twitter card metadata validated.
* Content taxonomy (categories/tags) aligned with target market and services.

## 8. Acceptance criteria

MVP is considered complete when:

1. Site builds locally and deploys via Cloudflare Pages from the main branch.
2. A pull request triggers a preview deployment and can be reviewed before merging.
3. A new blog post can be created using a template, populated, previewed locally, and published end-to-end in under 30 minutes.
4. Images appear correctly, are appropriately optimized for web, and do not bloat the repository.
5. Basic SEO is present: page titles/descriptions, sitemap, RSS, and social cards.

## 9. Risks and mitigations

* Risk: Repository grows quickly due to photos.

  * Mitigation: commit web derivatives only; enforce file size guidelines; consider external image hosting later if needed.
* Risk: Theme complexity slows progress.

  * Mitigation: start with minimal customization; iterate after content workflow stabilizes.
* Risk: Build limits/timeouts on free tiers.

  * Mitigation: batch changes, avoid rapid-fire commits; keep build steps lean; pin Hugo version.
* Risk: Process is too technical for content owner.

  * Mitigation: provide runbook, checklists, and simple scripts/aliases; rely on PR previews for confidence.

## 10. Project methodology

* Phased delivery with “walking skeleton” first (end-to-end deployment early).
* Short iterations: each iteration produces a shippable increment.
* Operational maturity comes from runbooks, templates, and checklists.

## 11. Backlog (prioritized)

### Epic A — Foundations (P0)

A1. Create Git repository and baseline documentation (README + runbooks)

* Story: As a platform owner, I want a repo structure and documentation so the project is maintainable.
* Acceptance: repo created; docs folder and placeholders present.

A2. Hugo scaffolding and local dev setup

* Story: As a contributor, I want to run the site locally and preview changes.
* Acceptance: `hugo server` works; basic config committed.

A3. Theme selection and initial customization baseline

* Story: As a business, I want a professional look consistent with underwater/ocean photography.
* Acceptance: theme integrated; navigation and fonts/colors adjusted minimally.

### Epic B — Site MVP (P0)

B1. Landing page sections

* Sections: Hero + value proposition, services, portfolio highlights, testimonials/clients (optional), CTA/contact.
* Acceptance: clear CTA; mobile-friendly; consistent spacing and typography.

B2. Core pages

* About, Services, Contact, Privacy/Terms (if needed).
* Acceptance: all pages reachable from nav/footer; contact method works.

B3. Blog implementation

* List page, single post template, tags/categories, RSS.
* Acceptance: at least 2 sample posts render correctly with featured images.

### Epic C — Content Model & Operations (P0)

C1. Define front matter schema and archetypes

* Required fields: title, date, summary, featured_image, tags, categories, draft.
* Acceptance: `hugo new posts/...` generates correct structure.

C2. Image workflow standards

* Define sizes/quality targets, naming conventions, folder taxonomy.
* Acceptance: documented; sample images comply.

C3. Publishing workflow (Git)

* Branching strategy, PR template, preview deploy process.
* Acceptance: contributor can publish via documented steps.

### Epic D — Cloudflare Pages Deployment (P0)

D1. Connect repo to Cloudflare Pages

* Build command, output directory, Hugo version pin, preview builds.
* Acceptance: prod deploy on merge; preview deploy on PR.

D2. Domain setup (P1)

* Start with pages.dev; add custom domain when ready.
* Acceptance: domain resolves; HTTPS enabled; redirects configured.

### Epic E — SEO and Social Readiness (P1)

E1. SEO baseline

* Titles, descriptions, sitemap, robots, canonical URLs.
* Acceptance: pages contain metadata; no obvious SEO regressions.

E2. Social cards + distribution fields

* OpenGraph/Twitter; social excerpt metadata.
* Acceptance: link previews render as intended.

### Epic F — Portfolio/Case Studies (P1)

F1. Portfolio section (optional)

* Case studies with services delivered, outcomes, and visuals.
* Acceptance: portfolio items list and detail page; consistent structure.

### Epic G — Distribution Foundation (P2)

G1. Distribution manifest convention

* Store per-post social copy variants, hashtags, channel notes.
* Acceptance: metadata supports later automation without manual rework.

G2. Automation exploration (only after stabilization)

* Evaluate lightweight automation approach (serverless or third-party) aligned to free/low cost.
* Acceptance: proof-of-concept for one channel, documented and controllable.

## 12. Milestones

* M1: Walking skeleton deployed (end-to-end) — Foundations + Cloudflare deploy working.
* M2: MVP content-ready — Landing + Blog + runbook.
* M3: Brand polish — typography, spacing, imagery consistent; initial portfolio optional.
* M4: Distribution-ready metadata — RSS + social cards + manifest fields.
