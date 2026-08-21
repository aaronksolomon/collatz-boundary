# Collatz Boundary

This repository accompanies the unpublished manuscript **Polynomial Boundary
Coordinates for Collatz Cycles** by Aaron Kyle Solomon.

The manuscript develops exact coordinates for prescribed Collatz parity patterns:
a canonically rooted parity class is measured against a mechanical reference,
reindexed by residues, and represented by a sparse polynomial boundary. The
small computational companion here reproduces those constructions exactly.

## Manuscript

- [Project website](https://aaronksolomon.github.io/collatz-boundary/)
- [Manuscript PDF](https://aaronksolomon.github.io/collatz-boundary/paper/collatz-boundary-paper.pdf)

The manuscript is shared for scholarly review and has not undergone peer
review.

Current manuscript version: **0.4.1** (21 August 2026).

## Reproduce the (8,5,3) example

Python 3.12 or newer is required. The core package uses only the standard
library.

```bash
git clone https://github.com/aaronksolomon/collatz-boundary.git
cd collatz-boundary
python -m pip install .
collatz-boundary
```

The default command reconstructs the manuscript's `(n,u,z)=(8,5,3)` example from
the rooted bridge `L=(0,0,1,0,1,0)`. Machine-readable output is available with
`collatz-boundary --json`.

Run the exact regression tests with:

```bash
python -m unittest discover -s tests -v
python tools/check_site.py
```

The companion demonstrates definitions and identities from the manuscript. It is
not a search for Collatz cycles and does not test the theorem asymptotically.

## Licensing

Program code, tests, examples, and build or verification scripts are licensed
under the GNU General Public License, version 3 or later. See `COPYING`.

The article, abstract, figures, and substantive scholarly prose are copyright
© 2026 Aaron Kyle Solomon. All rights reserved. They are not licensed under
the GPL. See `COPYRIGHT.md` for the exact repository boundary.
