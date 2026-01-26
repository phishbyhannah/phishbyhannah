# Repo Blueprint and Publishing Runbook

## 1. Repository blueprint (Hugo + Git + Cloudflare Pages)

### 1.1 Recommended repo structure

/

* archetypes/

  * post.md
  * page.md
  * portfolio.md (optional)
* assets/

  * css/ (if using Hugo Pipes)
  * js/  (if needed)
* content/

  * _index.md
  * about/_index.md
  * services/_index.md
  * contact/_index.md
  * posts/

    * 2026-01-17-example-post/

      * index.md
      * featured.jpg
  * portfolio/ (optional)
* layouts/ (theme overrides only; keep minimal)
* static/

  * images/

    * site/ (logo, favicon, defaults)
    * posts/ (only if not using page bundles)
* themes/ (or use Hugo Modules; choose one approach and stick to it)
* config/

  * _default/

    * hugo.toml (or config.toml)
    * menus.toml (optional)
    * params.toml (optional)
  * production/

    * hugo.toml (optional overrides)
  * development/

    * hugo.toml (optional overrides)
* .gitignore
* README.md
* docs/

  * operating-model.md (this runbook)
  * content-model.md
  * image-workflow.md
  * theme-notes.md
* scripts/ (optional)

  * optimize-images.sh (optional)
  * new-post.sh (optional convenience)

Notes:

* Prefer “page bundles” for posts (folder per post with `index.md` and images in same folder). This keeps content portable.
* Keep theme overrides in `layouts/` minimal to reduce maintenance burden.

### 1.2 Content model (front matter schema)

Use YAML or TOML consistently across the repo. Example (YAML):

---

title: "Example Post Title"
date: 2026-01-17T10:00:00+08:00
draft: true
summary: "One to two sentences that work for blog lists and social excerpts."
featured_image: "featured.jpg"   # relative to the page bundle
categories: ["Ocean Experiences"]
tags: ["Underwater", "Photography", "Lifestyle"]
social:
excerpt: "Optional short copy for social distribution."
hashtags: ["#underwater", "#ocean", "#travel"]
location:
name: "Rottnest Island"
country: "Australia"
--------------------

Required (Phase 1):

* title, date, draft, summary, featured_image, tags/categories

Optional (Phase 2):

* social.excerpt, social.hashtags, location fields, campaign identifiers

### 1.3 Naming conventions

Posts:

* Folder: `YYYY-MM-DD-short-slug/`
* Featured image: `featured.jpg` (or `featured.webp`)
* Inline images: `01.jpg`, `02.jpg` or meaningful names (`reef-dive-01.jpg`)

Tags/categories:

* Keep categories broad and stable (e.g., Ocean Experiences, Travel Comms, Lifestyle Content).
* Use tags for specifics (e.g., Underwater, Snorkeling, Brand Storytelling).

### 1.4 Image workflow standards (cost and performance control)

Golden rules:

* Do not commit RAW originals to Git.
* Commit only web-optimized derivatives.

Recommended targets (adjust later as needed):

* Featured images: 1600–2400px wide, JPEG quality ~75–85 or WebP equivalent.
* Inline images: 1200–2000px wide depending on layout.
* Keep individual committed images ideally under 500KB–800KB where possible.

Local folder approach:

* Masters (not in repo): `/Photos/Masters/...`
* Web exports (in repo): stored in the post bundle folder or `static/images/...`

### 1.5 Git workflow (simple, safe, reviewable)

Branch model:

* `main` = production
* `feat/<short-name>` = feature branches (e.g., `feat/new-post-ocean-safety`)

Publishing flow:

1. Create branch.
2. Make changes.
3. Open Pull Request.
4. Review Cloudflare Preview deployment.
5. Merge to `main` for production deploy.

Repository hygiene:

* Use a PR template to enforce metadata and image checks.
* Avoid frequent tiny commits that trigger unnecessary builds.

### 1.6 Cloudflare Pages configuration (implementation checklist)

In Cloudflare Pages (Project Settings):

* Connect to Git provider and select repo.
* Framework preset: Hugo (or custom build).
* Build command: `hugo --minify`
* Build output directory: `public`
* Environment variables:

  * `HUGO_VERSION`: pin to a specific version (set for Production and Preview environments).
  * Optional: `HUGO_ENV=production`

Preview deployments:

* Ensure PR previews are enabled.
* Use previews as the default review mechanism before merging.

### 1.7 Quality gates (automatable over time)

Minimum checks before merge:

* Site builds locally.
* New post has summary + featured image + tags/categories.
* Images are web-optimized and correctly referenced.
* Links work (no obvious 404s).
* Preview deployment looks correct on mobile.

Optional later:

* Add a link checker (CI) and/or HTML validation.
* Add a basic image size lint script (fail if over a threshold).

---

## 2. Publishing Runbook (step-by-step)

### 2.1 One-time setup (first workstation)

1. Install Hugo (extended if theme requires it).
2. Install Git and authenticate to the Git provider.
3. Clone the repository:

   * `git clone <repo-url>`
4. Run local server:

   * `hugo server -D`
5. Open the local URL and confirm you see the site.

### 2.2 Create a new blog post

Option A: Hugo archetype (recommended)

1. Create a new post bundle:

   * `hugo new posts/YYYY-MM-DD-short-slug/index.md`
2. Add images into the same folder:

   * `content/posts/YYYY-MM-DD-short-slug/featured.jpg`
   * additional images as needed

Option B: convenience script (optional)

* If you add `scripts/new-post.sh`, it can generate the folder and starter files consistently.

### 2.3 Write and format the post

1. Fill in front matter:

   * title, date, summary, featured_image, tags/categories
2. Write the content in Markdown.
3. Reference images relative to the bundle:

   * `![Alt text](featured.jpg)`
4. Add alt text for accessibility and SEO.

### 2.4 Optimize images (required)

1. Export from photo editor to web-friendly sizes.
2. Confirm file sizes are reasonable (avoid multi-MB images).
3. Verify images render correctly in local preview.

### 2.5 Local preview checklist (required)

1. Start server:

   * `hugo server -D`
2. Confirm:

   * The post appears in the blog list.
   * Featured image shows correctly.
   * Mobile layout is acceptable.
   * Links and headings are correct.

### 2.6 Commit and push changes (branch + PR workflow)

1. Create a feature branch:

   * `git checkout -b feat/<short-name>`
2. Check changes:

   * `git status`
3. Commit with a clear message:

   * `git add .`
   * `git commit -m "Add post: <short title>"`
4. Push branch:

   * `git push -u origin feat/<short-name>`
5. Open a Pull Request in the Git provider.

### 2.7 Review via Cloudflare Preview deployment

1. Wait for the PR to show a Preview URL from Cloudflare Pages.
2. Review:

   * Desktop and mobile rendering
   * Images, spacing, and typography
   * Metadata (title/description) if you have a quick way to validate
3. Make fixes on the same branch and push; the preview updates automatically.

### 2.8 Publish to production

1. Merge PR into `main`.
2. Confirm Cloudflare production deployment completes.
3. Validate production URL.

### 2.9 Post-publish (optional but recommended)

1. Add the post URL to a simple distribution tracker (even a markdown list).
2. Prepare social copy (if using the `social` fields).
3. Record performance notes for later optimization.

---

## 3. Operating cadence and maintenance

Weekly:

* Publish 1 post (or 1 site improvement) using the full workflow.
* Review backlog and pick next item.

Monthly:

* Check for theme updates and apply only if low risk.
* Validate forms/contact links.
* Light SEO hygiene: check titles, summaries, broken links.

Quarterly:

* Reassess taxonomy (categories/tags) and refine.
* Decide whether to begin Phase 2 distribution automation based on content consistency.

---

## 4. Quick-start “Definition of Ready” for posts

A post is ready to publish when:

* Summary is written and reads well as a social excerpt.
* Featured image is web-optimized and compelling.
* Tags/categories are assigned.
* Alt text is present for key images.
* Local preview looks correct on mobile.

---

## 5. Optional enhancements (only if needed)

* Add a lightweight `Makefile` or `justfile` with:

  * `make dev` → run server
  * `make build` → production build
  * `make new-post slug=...` → create new bundle
* Add an image optimizer script and document it.
* Add a PR template enforcing the content checklist.
