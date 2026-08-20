"""Exact canonical-bridge data for an already rooted legal bridge.

The input bridge is assumed to use the odd root selected in the paper. This
module validates bridge legality and reconstructs the corresponding rooted
word; it does not select a canonical root from an arbitrary cyclic word.

Copyright (C) 2026 Aaron Kyle Solomon
SPDX-License-Identifier: GPL-3.0-or-later
"""

from __future__ import annotations

from dataclasses import dataclass
from math import floor, gcd


@dataclass(frozen=True)
class BridgeCoordinates:
    """Mechanical and rooted-word coordinates of one legal bridge."""

    n: int
    u: int
    z: int
    bridge: tuple[int, ...]
    mechanical: tuple[int, ...]
    increments: tuple[int, ...]
    cumulative: tuple[int, ...]
    gaps: tuple[int, ...]
    odd_positions: tuple[int, ...]
    word: tuple[int, ...]

    @property
    def word_text(self) -> str:
        """Return the rooted binary word without separators."""
        return "".join(map(str, self.word))


@dataclass(frozen=True)
class BoundaryCoordinates:
    """Coprime residue profile and reduced polynomial boundary."""

    bridge_data: BridgeCoordinates
    residues_by_time: tuple[int, ...]
    time_by_residue: tuple[int, ...]
    heights: tuple[int, ...]
    maximum_height: int
    profile: tuple[int, ...]
    profile_coefficients: tuple[int, ...]
    boundary_coefficients: tuple[int, ...]
    plateaux: tuple[tuple[int, int], ...]

    @property
    def support(self) -> tuple[int, ...]:
        """Return occupied exponents of the boundary polynomial."""
        return tuple(
            exponent
            for exponent, coefficient in enumerate(self.boundary_coefficients)
            if coefficient != 0
        )

    @property
    def plateau_count(self) -> int:
        """Return the number of maximal constant intervals in the profile."""
        return len(self.plateaux)


def _validate_parameters(n: int, u: int) -> None:
    if not isinstance(n, int) or not isinstance(u, int):
        raise TypeError("n and u must be integers")
    if not 0 < u < n:
        raise ValueError("expected 0 < u < n")


def mechanical_path(n: int, u: int) -> tuple[int, ...]:
    """Return ``A(t)=floor((n-u)t/u)`` for ``0 <= t <= u``."""
    _validate_parameters(n, u)
    z = n - u
    return tuple(floor(z * t / u) for t in range(u + 1))


def word_from_gaps(gaps: tuple[int, ...]) -> tuple[int, ...]:
    """Return the rooted word having one odd symbol followed by each gap."""
    if not gaps:
        raise ValueError("a gap vector must be nonempty")
    if any(not isinstance(gap, int) or gap < 0 for gap in gaps):
        raise ValueError("zero gaps must be nonnegative integers")
    return tuple(bit for gap in gaps for bit in (1, *(0 for _ in range(gap))))


def bridge_coordinates(
    n: int,
    u: int,
    bridge: tuple[int, ...],
) -> BridgeCoordinates:
    """Validate a rooted bridge and reconstruct its path, gaps, and word."""
    _validate_parameters(n, u)
    if len(bridge) != u + 1:
        raise ValueError(f"bridge must contain exactly {u + 1} heights")
    if any(not isinstance(height, int) for height in bridge):
        raise TypeError("bridge heights must be integers")
    if bridge[0] != 0 or bridge[-1] != 0:
        raise ValueError("bridge endpoints must be zero")
    if any(height < 0 for height in bridge):
        raise ValueError("bridge heights must be nonnegative")

    mechanical = mechanical_path(n, u)
    increments = tuple(mechanical[t + 1] - mechanical[t] for t in range(u))
    if any(bridge[t + 1] > bridge[t] + increments[t] for t in range(u)):
        raise ValueError("bridge violates the legal-rise inequality")

    cumulative = tuple(mechanical[t] - bridge[t] for t in range(u + 1))
    gaps = tuple(cumulative[t + 1] - cumulative[t] for t in range(u))
    if any(gap < 0 for gap in gaps):
        raise ValueError("bridge reconstruction produced a negative zero gap")

    word = word_from_gaps(gaps)
    if len(word) != n or sum(word) != u:
        raise ArithmeticError("bridge reconstruction has the wrong length or weight")
    odd_positions = tuple(index for index, bit in enumerate(word) if bit)

    return BridgeCoordinates(
        n=n,
        u=u,
        z=n - u,
        bridge=bridge,
        mechanical=mechanical,
        increments=increments,
        cumulative=cumulative,
        gaps=gaps,
        odd_positions=odd_positions,
        word=word,
    )


def _plateaux(values: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    starts = [0]
    starts.extend(
        index for index in range(1, len(values)) if values[index] != values[index - 1]
    )
    return tuple(
        (
            start,
            starts[position + 1] - 1 if position + 1 < len(starts) else len(values) - 1,
        )
        for position, start in enumerate(starts)
    )


def boundary_coordinates(
    n: int,
    u: int,
    bridge: tuple[int, ...],
) -> BoundaryCoordinates:
    """Return the coprime residue profile and boundary of a rooted bridge."""
    bridge_data = bridge_coordinates(n, u, bridge)
    if gcd(n, u) != 1:
        raise ValueError("residue reordering requires gcd(n,u)=1")

    residues = tuple(((n - u) * t) % u for t in range(u))
    if len(set(residues)) != u:
        raise ArithmeticError("residue order is not a permutation")
    inverse = [0] * u
    for t, residue in enumerate(residues):
        inverse[residue] = t

    heights = tuple(bridge[inverse[residue]] for residue in range(u))
    maximum = max(heights)
    profile = tuple(2 ** (maximum - height) for height in heights)

    # V_L(X)=sum_r d_r X^(u-1-r), stored here in increasing exponent order.
    profile_coefficients = tuple(reversed(profile))
    boundary = [-coefficient for coefficient in profile_coefficients]
    for exponent, coefficient in enumerate(profile_coefficients):
        if exponent + 1 < u:
            boundary[exponent + 1] += coefficient
        else:
            boundary[0] += 2 * coefficient

    plateaux = _plateaux(profile)
    if sum(coefficient != 0 for coefficient in boundary) != len(plateaux):
        raise ArithmeticError("boundary support does not equal plateau count")

    return BoundaryCoordinates(
        bridge_data=bridge_data,
        residues_by_time=residues,
        time_by_residue=tuple(inverse),
        heights=heights,
        maximum_height=maximum,
        profile=profile,
        profile_coefficients=profile_coefficients,
        boundary_coefficients=tuple(boundary),
        plateaux=plateaux,
    )


def cycle_numerator(word: tuple[int, ...]) -> int:
    """Return the prescribed-parity numerator in the paper's convention."""
    if not word or any(bit not in (0, 1) for bit in word):
        raise ValueError("word must be a nonempty binary tuple")
    suffix_ones = 0
    numerator = 0
    for position in range(len(word) - 1, -1, -1):
        if word[position]:
            numerator += 2**position * 3**suffix_ones
            suffix_ones += 1
    return numerator
