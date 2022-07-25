class Cube {
    constructor() {
        this.cubies = [];

        for (let i = -1; i < 2; i++) {
            for (let j = -1; j < 2; j++) {
                for (let k = -1; k < 2; k++) {
                    this.cubies.push(new Cubie(i, j, k));
                }
            }
        }
    }

    turnX(axisValue, angle) {
        for (let cubie of this.cubies) {
            if (cubie.x == axisValue) {
                cubie.turnX(angle);
            }
        }
    }

    turnY(axisValue, angle) {
        for (let cubie of this.cubies) {
            if (cubie.y == axisValue) {
                cubie.turnY(angle);
            }
        }
    }

    turnZ(axisValue, angle) {
        for (let cubie of this.cubies) {
            if (cubie.z == axisValue) {
                cubie.turnZ(angle);
            }
        }
    }

    apply(move) {
        if (move.x) {
            this.turnX(move.x, move.dir * HALF_PI);
        } else if (move.y) {
            this.turnY(move.y, move.dir * HALF_PI);
        } else if (move.z) {
            this.turnZ(move.z, move.dir * HALF_PI);
        }
        else {
            throw 'Trying to apply an invalid move'
        }
    }

    show() {
        push();

        scale(50);
        for (let cubie of this.cubies) {
            cubie.show();
        
        }
        pop();
    }
}

class CubeController {
    constructor(cube) {
        this.cube = cube;
        this.undoStack = [];
        this.redoStack = [];
    }

    execute(move) {
        this.cube.apply(move);
        this.undoStack.push(move);
        this.redoStack = [];
    }

    undo() {
        if (!this.undoStack.length) {
            return;
        }

        let move = this.undoStack.pop();
        let reverse = move.getReverse();
        this.cube.apply(reverse);
        this.redoStack.push(reverse);
    }

    redo() {
        if (!this.redoStack.length) {
            return;
        }

        let move = this.redoStack.pop();
        this.cube.apply(move);
        this.undoStack.push(move);
    }
}