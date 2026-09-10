# Bo Chesterton site — v0.6

A deliberately small static website for the first commercial phase of the Bo Chesterton project.

## Philosophy

The commercial object is the **Directed Investigation**:

> You bring the question. Bo investigates it.

The client purchases a bounded investigation and its deliverables, not a predetermined conclusion and not ownership or control of the Bo Chesterton identity.

## Files

- `index.html` — the institutional homepage
- `engagements.html` — current scopes, prices, terms, and engagement boundaries
- `styles.css` — responsive styles with no external dependencies
- `SITE_COPY.md` — editable source copy / provenance-friendly text
- `robots.txt` — crawler instructions and sitemap discovery
- `sitemap.xml` — canonical public URLs for search engines
- `capabilities.pdf` — two-page commissioning overview
- `src/generate_capabilities.py` — reproducible source for the capabilities PDF
- `src/fonts/` — bundled DejaVu fonts and license used by the PDF generator
- `deployments/` — preserved folders and ZIP archives for each deployment version

Version 0.6 introduces a dedicated commercial engagement page, publishes three bounded introductory offers, makes the capabilities sheet reproducible, and sharpens the homepage around behavioral evaluation while preserving the site’s visual design and research identity.

## Deployment

The files at the repository root are the current deployable site. Before each release:

1. Regenerate `capabilities.pdf` from its source when the capabilities copy changes.
2. Verify all internal and external links.
3. Review the site on desktop and mobile.
4. Copy the release files into a versioned folder under `deployments/`.
5. Create a ZIP archive of that folder beside it.
6. Commit, tag, and deploy the release.

## Suggested infrastructure

- Registrar: any reputable registrar with transparent renewal pricing.
- DNS / static hosting: Cloudflare Pages.
- Email: use a provider that supports sending and receiving from the custom domain. Forwarding-only email is not enough for professional replies.
- Payments: do not add checkout yet. Use a written statement of work and invoice after scoping the first engagement.

## Future additions

Do **not** add these until they solve a real problem:

- inquiry form backend
- scheduling widget
- client logos
- testimonials
- analytics beyond basic traffic
- multiple service tiers
- ecommerce

The site should stay smaller than the research it represents.
