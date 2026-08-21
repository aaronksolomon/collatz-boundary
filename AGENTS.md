# AGENTS.md

Project guidance for agents working in the public manuscript distribution
repository.

## Repository Boundary

- This repository is the public website and computational companion for
  *Polynomial Boundary Coordinates for Collatz Cycles*.
- The canonical manuscript source and release metadata live in the sibling
  `collatz` repository at
  `docs/research/integer-admissibility/manuscript-v5/`. Do not reconstruct or
  edit the mathematical manuscript from this repository.
- Treat `docs/paper/collatz-boundary-paper.pdf` as a generated publication
  artifact copied from `../collatz/output/pdf/ia-v5-letter-review.pdf`.
- Preserve the licensing boundary: scholarly prose, figures, and the manuscript
  remain all rights reserved; program code and verification tooling are
  GPL-3.0-or-later.

## Manuscript Release Synchronization

- Before synchronizing a manuscript release, read
  `../collatz/docs/research/integer-admissibility/manuscript-v5/release.json`.
  Its manuscript version and date are authoritative.
- On every manuscript version bump, synchronize all of the following:
  - the tracked public PDF;
  - `CHECKSUMS.sha256`;
  - website version, date, theorem summary, abstract, and citation;
  - the current-manuscript line in `README.md`;
  - the manuscript entry under `preferred-citation` in `CITATION.cff`.
- Keep the manuscript version independent of the computational package version.
  Do not change `pyproject.toml` or the top-level software version in
  `CITATION.cff` unless the user also requests a code release.
- Do not create or update a Git tag or GitHub release unless the user explicitly
  requests publication of that release.

## Validation

Run after every website or release synchronization change:

```bash
python3 tools/check_site.py
git diff --check
```

- Preserve user edits in a dirty worktree and stage only explicitly reviewed
  files.
- Keep `.DS_Store` ignored and out of commits.

## Git Workflow

- This is a single-contributor repository with a lightweight direct-to-`main`
  workflow; do not introduce pull-request ceremony unless requested.
- Staging, committing, pushing, tagging, and release creation each require
  explicit user authorization.
- Never use destructive Git operations without explicit approval.
