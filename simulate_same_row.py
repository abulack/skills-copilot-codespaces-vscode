#!/usr/bin/env python3
"""Monte Carlo simulation: probability that two people sit in the same row.

Three rows with seat counts 5, 6, 7. Randomly choose two distinct seats.
Also computes the exact probability for verification.
"""
import argparse
import random
import math
from typing import List


def exact_probability(rows: List[int]) -> float:
    total = sum(rows)
    # P = sum comb(r,2) / comb(total,2) = sum r*(r-1) / (total*(total-1))
    return sum(r * (r - 1) for r in rows) / (total * (total - 1))


def simulate(rows: List[int], trials: int, seed: int | None = None) -> float:
    if seed is not None:
        random.seed(seed)
    total = sum(rows)
    # precompute row boundaries (exclusive upper bounds)
    boundaries = []
    acc = 0
    for r in rows:
        acc += r
        boundaries.append(acc)

    def seat_row(seat_idx: int) -> int:
        # seat_idx in [0, total-1]
        for i, b in enumerate(boundaries):
            if seat_idx < b:
                return i
        return len(boundaries) - 1

    same = 0
    for _ in range(trials):
        a, b = random.sample(range(total), 2)
        if seat_row(a) == seat_row(b):
            same += 1
    return same / trials


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", "-n", type=int, default=200_000, help="number of Monte Carlo trials")
    parser.add_argument("--seed", type=int, default=None, help="random seed (optional)")
    args = parser.parse_args()

    rows = [5, 6, 7]
    exact = exact_probability(rows)
    estimate = simulate(rows, args.trials, args.seed)
    # standard error for proportion
    stderr = math.sqrt(estimate * (1 - estimate) / args.trials)

    print("Rows:", rows)
    print(f"Trials: {args.trials}")
    if args.seed is not None:
        print(f"Seed: {args.seed}")
    print()
    print(f"Estimated probability (Monte Carlo): {estimate:.6f}")
    print(f"Standard error: {stderr:.6e}")
    print(f"Exact probability: {exact:.6f}")
    print(f"Absolute error: {abs(estimate - exact):.6e}")


if __name__ == "__main__":
    main()
