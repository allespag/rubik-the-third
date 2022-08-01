import argparse
import logging
import random

import pandas as pd
from alive_progress import alive_bar  # type: ignore

from rubik.cube import Cube
from rubik.move import create_random_sequence, sequence_to_readable
from rubik.report import Report
from rubik.solver import Solver

logger = logging.getLogger("rubik")
logger.disabled = True


def main(args: argparse.Namespace) -> None:
    random.seed(args.seed)
    reports: list[Report] = []
    solutions: list[tuple[float, str]] = []

    with alive_bar(args.iter, title="Benchmark", spinner="wait3", spinner_length=25) as bar:  # type: ignore
        for _ in range(args.iter):
            sequence = create_random_sequence(args.length)
            readable_sequence = sequence_to_readable(sequence)
            cube = Cube.from_sequence(sequence)
            report = Report(readable_sequence)
            solver = Solver(cube, report)

            solver.run()
            reports.append(report)
            solutions.append((report.time_taken_in_s, report.author))
            bar()

    df = pd.DataFrame(
        [
            [
                report.time_taken_in_s,
                report.result,
                report.raw_result,
                report.author,
            ]
            for report in reports
        ],
        columns=[
            "time taken",
            "solution length",
            "solution",
            "scramble",
        ],
    )

    print(df.describe())


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="benchmark")

    parser.add_argument("--iter", "-i", type=int, default=42)
    parser.add_argument("--length", "-l", type=int, default=42)
    parser.add_argument("--seed", "-s", default=42)

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    main(args)
