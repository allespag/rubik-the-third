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

BENCHMARK_SIZE = 100


def main() -> None:
    random.seed(42)
    reports: list[Report] = []

    with alive_bar(BENCHMARK_SIZE, title="Benchmark", spinner="wait3", spinner_length=25) as bar:  # type: ignore
        for _ in range(BENCHMARK_SIZE):
            sequence = create_random_sequence(42)
            readable_sequence = sequence_to_readable(sequence)
            cube = Cube.from_sequence(sequence)
            report = Report(readable_sequence)
            solver = Solver(cube, report)

            solver.run()
            reports.append(report)
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


if __name__ == "__main__":
    main()
