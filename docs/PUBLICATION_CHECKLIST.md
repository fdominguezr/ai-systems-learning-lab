# Technical publication acceptance

Applies to new publications and edits of existing publications, including shared images and indexes. Review date is not control expiry: keep effective checks.

## 1. Evidence and scope

- Identify the intended reader and what the article helps them understand or decide.
- Match images to the relevant setup/period. Label historical photos and distinguish illustration from evidence of a measurement configuration.
- Check numbers, units, source references and observation coverage. State exploratory versus controlled results accurately.
- Preserve uncertainty; never invent original data, missing curves or causal attribution.
- Review licensing, provenance and public/private boundaries.

## 2. Reading and navigation

- Root README orients; series cover introduces; chapters explain; supporting files enable reproduction.
- Maintain a compact root index with a short description for every published series and update the relevant series index for each new chapter.
- Check previous/next/index links as applicable, including bottom navigation. First/last pages have appropriate endpoints.
- Keep an understandable opening and useful conclusions. Use specific reproduction/discussion questions where relevant; do not manufacture engagement claims.

## 3. Visual review (must be observed, not inferred from code)

- Inspect every changed exported figure and every affected page using it, at desktop and a representative narrow/mobile width.
- Check legends, labels, arrows, text boundaries, cropping, contrast, font readability and photo/caption alignment.
- Fix shared figure generators/templates where possible. Search for the same defect across all figures using that pattern.
- Record the artifact/version, reviewed view/width and any remaining defect. A file hash identifies the version; it does not prove inspection.
- Native-device behavior remains unverified unless actually tested on that device.

## 4. Mechanical checks and publication

Run `python scripts/check_publication.py` and the test suite. CI runs on all pushes and pull requests, including experiments and figure changes. The checker validates inline Markdown/HTML local targets, nonempty Markdown image alt text, primary headings, basic article navigation and series inclusion in the root index. It does not verify external URLs, fragments, reference-style links, image semantics, visual layout or factual accuracy; inspect those separately.

Before merging, complete the PR checklist and preserve relevant evidence. Do not tick unperformed checks. No automatic approval of visual/factual quality from CI success.

After publication, read the exact destination commit and changed files back. Inspect the intended rendered surface. A prepared ZIP, local render or branch commit is not proof of delivery on main. Report:

`TARGET/COMMIT | STRUCTURAL | VISUAL | EVIDENCE | PUBLISHED_READBACK | OPEN_ITEMS`

Any pending mandatory check means partial delivery. Existing published material is not retroactively certified by adding this checklist. GitHub branch protection is separate; this workflow does not claim to prevent every direct write to main.

## 5. Recurrence measurement

Reuse the existing review process, rather than adding a new monitor. One publication change/version is one opportunity; multiple review passes do not increase successful-delivery counts. Count shared-asset defects once, with affected pages separately. Distinguish controls applied, missing or unknown; defects caught before/after publication; user-requested corrections; recurrence by defect type. Missing observations are not successes. Keep private operational measurements outside this public repository.
