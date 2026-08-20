"""Command-line report for the exact bridge construction.

Copyright (C) 2026 Aaron Kyle Solomon
SPDX-License-Identifier: GPL-3.0-or-later
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence

from collatz_boundary.coordinates import boundary_coordinates, cycle_numerator

DEFAULT_N = 8
DEFAULT_U = 5
DEFAULT_BRIDGE = (0, 0, 1, 0, 1, 0)


def _bridge_value(text: str) -> tuple[int, ...]:
    try:
        return tuple(int(value.strip()) for value in text.split(","))
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "bridge must be a comma-separated list of integers"
        ) from error


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compute exact residue-profile and boundary coordinates."
    )
    parser.add_argument("--n", type=int, default=DEFAULT_N, help="word length")
    parser.add_argument("--u", type=int, default=DEFAULT_U, help="odd-symbol count")
    parser.add_argument(
        "--bridge",
        type=_bridge_value,
        default=DEFAULT_BRIDGE,
        help="rooted bridge heights, separated by commas",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON")
    return parser


def _payload(n: int, u: int, bridge: tuple[int, ...]) -> dict[str, object]:
    boundary = boundary_coordinates(n, u, bridge)
    bridge_data = boundary.bridge_data
    numerator = cycle_numerator(bridge_data.word)
    denominator = 2**n - 3**u
    return {
        "parameters": {"n": n, "u": u, "z": n - u, "D": denominator},
        "bridge": list(bridge_data.bridge),
        "mechanical_path": list(bridge_data.mechanical),
        "mechanical_increments": list(bridge_data.increments),
        "cumulative_path": list(bridge_data.cumulative),
        "zero_gaps": list(bridge_data.gaps),
        "rooted_word": bridge_data.word_text,
        "numerator": numerator,
        "integrally_realizable": denominator != 0 and numerator % denominator == 0,
        "residues_by_time": list(boundary.residues_by_time),
        "time_by_residue": list(boundary.time_by_residue),
        "residue_heights": list(boundary.heights),
        "dyadic_profile": list(boundary.profile),
        "boundary_coefficients": list(boundary.boundary_coefficients),
        "boundary_support": list(boundary.support),
        "plateaux": [list(interval) for interval in boundary.plateaux],
        "plateau_count": boundary.plateau_count,
    }


def _human_report(payload: dict[str, object]) -> str:
    parameters = payload["parameters"]
    if not isinstance(parameters, dict):
        raise TypeError("parameters payload is malformed")
    lines = [
        "Collatz bridge and boundary coordinates",
        f"(n,u,z)=({parameters['n']},{parameters['u']},{parameters['z']}), D={parameters['D']}",
        f"L={tuple(payload['bridge'])}",
        f"A={tuple(payload['mechanical_path'])}",
        f"a={tuple(payload['mechanical_increments'])}",
        f"P={tuple(payload['cumulative_path'])}",
        f"gamma={tuple(payload['zero_gaps'])}",
        f"w={payload['rooted_word']}",
        f"N(w)={payload['numerator']}",
        f"integrally realizable={payload['integrally_realizable']}",
        f"r(t)={tuple(payload['residues_by_time'])}",
        f"t(r)={tuple(payload['time_by_residue'])}",
        f"H={tuple(payload['residue_heights'])}",
        f"d={tuple(payload['dyadic_profile'])}",
        f"coeff(Q_L)={tuple(payload['boundary_coefficients'])}",
        f"supp(Q_L)={tuple(payload['boundary_support'])}",
        f"plateaux={tuple(tuple(item) for item in payload['plateaux'])}",
        f"K(L)={payload['plateau_count']}",
    ]
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> None:
    """Run the command-line companion."""
    args = _parser().parse_args(argv)
    payload = _payload(args.n, args.u, args.bridge)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(_human_report(payload))


if __name__ == "__main__":
    main()
