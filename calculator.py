"""Simple command-line calculator module."""
from __future__ import annotations

import argparse
from typing import Callable, Iterable


Number = float


def add(numbers: Iterable[Number]) -> Number:
    """Return the sum of all numbers in *numbers*."""
    total = 0.0
    for value in numbers:
        total += value
    return total


def subtract(numbers: Iterable[Number]) -> Number:
    """Return the result of subtracting subsequent numbers from the first."""
    iterator = iter(numbers)
    try:
        result = next(iterator)
    except StopIteration as exc:  # pragma: no cover - guard clause
        raise ValueError("at least one number is required") from exc

    for value in iterator:
        result -= value
    return result


def multiply(numbers: Iterable[Number]) -> Number:
    """Return the product of all numbers in *numbers*."""
    result = 1.0
    for value in numbers:
        result *= value
    return result


def divide(numbers: Iterable[Number]) -> Number:
    """Return the result of dividing the first number by the rest."""
    iterator = iter(numbers)
    try:
        result = next(iterator)
    except StopIteration as exc:  # pragma: no cover - guard clause
        raise ValueError("at least one number is required") from exc

    for value in iterator:
        if value == 0:
            raise ZeroDivisionError("cannot divide by zero")
        result /= value
    return result


OPERATIONS: dict[str, Callable[[Iterable[Number]], Number]] = {
    "add": add,
    "sub": subtract,
    "mul": multiply,
    "div": divide,
}


def calculate(operation: str, numbers: Iterable[Number]) -> Number:
    """Calculate *operation* over *numbers*.

    Parameters
    ----------
    operation:
        One of ``add``, ``sub``, ``mul`` or ``div``.
    numbers:
        An iterable of numeric values to be used as operands.
    """

    try:
        func = OPERATIONS[operation]
    except KeyError as exc:  # pragma: no cover - sanity check
        raise ValueError(f"unsupported operation: {operation}") from exc
    return func(numbers)


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the command-line interface."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "operation",
        choices=sorted(OPERATIONS),
        help="operation to perform",
    )
    parser.add_argument(
        "numbers",
        nargs="+",
        type=float,
        help="operands to use during calculation",
    )
    return parser


def main(argv: list[str] | None = None) -> Number:
    """Entry point for the command-line interface."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if len(args.numbers) < 1:
        raise ValueError("at least one number is required")
    return calculate(args.operation, args.numbers)


if __name__ == "__main__":
    result = main()
    print(result)
