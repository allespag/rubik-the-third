from flask import jsonify, redirect, render_template, request, url_for
from rubik.cube import Cube
from rubik.move import create_sequence, sequence_to_readable
from rubik.solver import Solver

from rubikapp import app

solver = Solver()


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    solution = None

    if request.method == "POST":
        print(request.get_json()["sequence"])
        sequence = create_sequence(request.get_json()["sequence"])
        print(sequence)
        cube = Cube.from_sequence(sequence)

        solution = solver.run(cube)
        solution = sequence_to_readable(solution)
        print(solution)
        return jsonify(solution)

    return render_template("index.html", solution=solution)
