import logging
import random

import pandas as pd
from alive_progress import alive_bar  # type: ignore

from rubik.cube import Cube
from rubik.move import create_random_sequence, sequence_to_readable
from rubik.report import Report
from rubik.solver import Solver

logger = logging.getLogger("rubik")
logger.disabled = False

BENCHMARK_SIZE = 1000


def main() -> None:
    random.seed(42)
    reports: list[Report] = []
    solutions: list[tuple[float, str]] = []

    with alive_bar(BENCHMARK_SIZE, title="Benchmark", spinner="wait3", spinner_length=25) as bar:  # type: ignore
        for _ in range(BENCHMARK_SIZE):
            sequence = create_random_sequence(42)
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
    print(max(solutions, key=lambda x: x[0]))


if __name__ == "__main__":
    main()
