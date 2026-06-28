# Migration Plan: Unified Deploy + Hosting the Interactive Card

Working notes for moving haydnenthusiasts.org toward a single, automated
deploy and a more integrated home for the Haydn card. Captured so the plan
outlives any one conversation. Nothing here is committed to yet — it's a
decision record and a checklist.

## Drivers

1. **Unified deploy** — one push should publish the site. Today publishing
   requires a local `build.py` + `deploy.sh` run (plus a CloudFront
   invalidation), or the local `.githooks/post-commit` hook, both of which
   need AWS credentials on the committer's machine.
2. **UX / single domain** — the interactive web version currently lives at
   `https://jsundram.github.io/haydn-info-card/`, a separate origin. Clicking
   through feels like leaving the site.
3. **Less maintenance friction** — the "update the submodule, commit, push"
   dance (see README) and frugal-CloudFront-invalidation machinery are more
   moving parts than the site needs.

## Current State (as of this writing)

- **Hosting:** static files in an S3 bucket (`s3://www.haydnenthusiasts.org/`)
  served via CloudFront for HTTPS (distribution `EA8YGAHXI8LCE`).
- **Build:** custom Python/Jinja2 build (`build.py`) — not plain Jekyll.
  Renders templates in `templates/`, copies `static/`, and pulls the latest
  PDF(s) out of the `external/haydn-info-card` git submodule.
- **Deploy:** `deploy.sh` (`s3 sync`) + a manual CloudFront invalidation,
  or the `.githooks/post-commit` script which builds + deploys + invalidates
  on each local commit.
- **The card, two outputs:** the `haydn-info-card` repo produces both a
  printable **PDF** (consumed here via the submodule) and an **interactive
  web app** (self-published to that repo's own GitHub Pages).
- **No measurement / SEO infra:** no analytics tag, no `sitemap.xml`, no
  `robots.txt`, no `<link rel="canonical">` tags.

## Decisions Made

- **Rebrand** the card page as "The Periodic Table of Haydn Quartets"
  (display name only; the printable PDF is still called a *card*). Shipped
  separately from this migration — see PR #11. The URL `haydn_card.html`
  was deliberately left unchanged to preserve links/SEO.

## Open Decisions

### 1. How integrated should the interactive web version be?

| Option | What it is | Trade-off |
| --- | --- | --- |
| **A. Link-out (current)** | Hub links to `jsundram.github.io/haydn-info-card/` | Simplest; zero coupling. Feels like a separate site. |
| **B. Same-domain subpath** | Serve the app at `haydnenthusiasts.org/info-card/` (or `card.haydnenthusiasts.org`) | Best UX, one domain. Couples two build systems; app must be rebuilt for the new base path (Pages base-path gotcha). |
| **C. Fully merged** | Move the app's source into this repo; make it *the* card page | Most coupling/work; only worth it for a single repo + lifecycle. |

**Leaning:** B, done as part of the migration (not bolted onto the current
S3 flow). A is a fine resting state if B proves fiddly.

### 2. How should the PDF be delivered?

The submodule today exists solely to hand `build.py` the latest PDF, and
`git submodule update --remote` makes builds non-reproducible (the pinned
SHA drifts from what's built).

- **Option:** switch to fetching the PDF from a **GitHub Release asset** of
  `haydn-info-card` — lighter and reproducible.
- **Or:** keep the submodule but actually commit the pointer for
  reproducibility.

### 3. URL strategy (pretty slug + redirect)

- Today: zero SEO risk because the URL is unchanged.
- If a prettier slug is wanted (e.g. `/periodic-table.html`): new canonical
  URL + **301 redirect** from `haydn_card.html`, kept permanently.
- **Hosting caveat:** S3/CloudFront can do a true 301 (S3 redirect object
  metadata or a CloudFront Function). **GitHub Pages cannot** do server-side
  301s — only meta-refresh / JS redirect stubs (`jekyll-redirect-from`
  generates these), which Google honors but are weaker. → Do the slug change
  *during* the migration so the redirect is set up once on the final host.

## Target Architecture (proposed)

- **GitHub Actions** workflow replacing `build.py` + `deploy.sh`:
  checkout (with submodules), `pip install -r requirements.txt`, build the
  PDF/app inputs, `python3 build.py`, publish `site-deploy/` to **GitHub
  Pages**.
- **GitHub Pages** for hosting: free Let's Encrypt HTTPS on the custom apex
  domain (replaces CloudFront's role), no cache invalidations to manage.
- Interactive app served at a subpath (Option B) if chosen.
- Optional: `haydn-info-card` fires a `repository_dispatch` to rebuild this
  site whenever the card updates — replaces the manual submodule dance.

## Checklist

### Can ship now (low-risk, current S3 setup)
- [ ] Add `<link rel="canonical">` tags to templates (none exist today).
- [ ] Add a `sitemap.xml` and `robots.txt`.
- [ ] Set up **Google Search Console** (+ Bing Webmaster Tools) to get a
      ranking/traffic baseline *before* bigger changes. Optionally add a
      lightweight analytics tag (GA4 / Plausible / Fathom).

### Migration (sequence)
- [ ] Decide #1 (integration level) and #2 (PDF delivery).
- [ ] Write the GitHub Actions build-and-deploy-to-Pages workflow
      (keep it side-by-side with S3 first — no-risk preview).
- [ ] Verify the Pages build output matches the current site (paths,
      `/assets/` references, the PDF, the app subpath).
- [ ] Add a `CNAME` file for the apex domain.
- [ ] **DNS cutover:** point A/AAAA/CNAME records from CloudFront to GitHub
      Pages IPs; wait for cert provisioning + propagation (plan a short
      cutover window).
- [ ] If pretty-URL'ing the card: add the 301/redirect stub from
      `haydn_card.html` → new slug; update nav `href`, `og:` URL, canonical.
- [ ] Decommission S3/CloudFront once Pages is confirmed healthy.

### Follow-ups
- [ ] Update `haydn-info-card`'s own branding to "Periodic Table" for
      consistency across the click-through (separate repo).
- [ ] Update README deploy instructions for the new flow.

## Notes / Caveats

- This is a niche enthusiast site; search volumes are small, so SEO
  before/after signal will be noisy. Search Console is still worth setting
  up, but calibrate expectations.
- The `haydn-info-card` repo is a separate project with its own
  dev/deploy lifecycle; prefer keeping its source there and consuming its
  outputs, rather than absorbing it wholesale (unless Option C is chosen).
