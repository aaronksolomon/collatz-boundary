"""Exact regression tests for the paper's bridge coordinates.

Copyright (C) 2026 Aaron Kyle Solomon
SPDX-License-Identifier: GPL-3.0-or-later
"""

from __future__ import annotations

import unittest

from collatz_boundary import (
    boundary_coordinates,
    bridge_coordinates,
    cycle_numerator,
)


class PaperExampleTests(unittest.TestCase):
    """Reproduce every coordinate displayed for the (8,5,3) example."""

    def test_mechanical_reference(self) -> None:
        data = bridge_coordinates(8, 5, (0, 0, 0, 0, 0, 0))
        self.assertEqual(data.mechanical, (0, 0, 1, 1, 2, 3))
        self.assertEqual(data.increments, (0, 1, 0, 1, 1))
        self.assertEqual(data.word_text, "11011010")

    def test_bridge_reconstructs_rooted_word(self) -> None:
        data = bridge_coordinates(8, 5, (0, 0, 1, 0, 1, 0))
        self.assertEqual(data.cumulative, (0, 0, 0, 1, 1, 3))
        self.assertEqual(data.gaps, (0, 0, 1, 0, 2))
        self.assertEqual(data.odd_positions, (0, 1, 2, 4, 5))
        self.assertEqual(data.word_text, "11101100")
        self.assertEqual(cycle_numerator(data.word), 251)
        self.assertNotEqual(cycle_numerator(data.word) % 13, 0)

    def test_residue_profile_and_boundary(self) -> None:
        data = boundary_coordinates(8, 5, (0, 0, 1, 0, 1, 0))
        self.assertEqual(data.residues_by_time, (0, 3, 1, 4, 2))
        self.assertEqual(data.time_by_residue, (0, 2, 4, 1, 3))
        self.assertEqual(data.heights, (0, 1, 1, 0, 0))
        self.assertEqual(data.profile, (2, 1, 1, 2, 2))
        self.assertEqual(data.boundary_coefficients, (2, 0, 1, 0, -1))
        self.assertEqual(data.support, (0, 2, 4))
        self.assertEqual(data.plateaux, ((0, 0), (1, 2), (3, 4)))
        self.assertEqual(data.plateau_count, 3)


class ValidationTests(unittest.TestCase):
    """Reject inputs outside the demonstrated coordinate domain."""

    def test_invalid_bridge_endpoints(self) -> None:
        with self.assertRaisesRegex(ValueError, "endpoints"):
            bridge_coordinates(8, 5, (1, 0, 0, 0, 0, 0))

    def test_illegal_rise(self) -> None:
        with self.assertRaisesRegex(ValueError, "legal-rise"):
            bridge_coordinates(8, 5, (0, 1, 1, 0, 0, 0))

    def test_noncoprime_residue_order(self) -> None:
        with self.assertRaisesRegex(ValueError, "gcd"):
            boundary_coordinates(10, 6, (0, 0, 0, 0, 0, 0, 0))


if __name__ == "__main__":
    unittest.main()
