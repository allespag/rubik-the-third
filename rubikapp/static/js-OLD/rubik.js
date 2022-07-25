const SIZE = 10;


class Face {
    constructor(pos, color) {
        this.pos = pos;
        this.color = color;
    }

    turnX(angle) {
        let rotatedVec = vec3.rotateX(vec3.create(), this.pos.array(), [0, 0, 0], angle);
        this.pos.x = round(rotatedVec[0]);
        this.pos.y = round(rotatedVec[1]);
        this.pos.z = round(rotatedVec[2]);
    }

    turnY(angle) {
        let rotatedVec = vec3.rotateY(vec3.create(), this.pos.array(), [0, 0, 0], angle);
        this.pos.x = round(rotatedVec[0]);
        this.pos.y = round(rotatedVec[1]);
        this.pos.z = round(rotatedVec[2]);
    }

    turnZ(angle) {
        let rotatedVec = vec3.rotateZ(vec3.create(), this.pos.array(), [0, 0, 0], angle);
        this.pos.x = round(rotatedVec[0]);
        this.pos.y = round(rotatedVec[1]);
        this.pos.z = round(rotatedVec[2]);
    }

    show() {
        push();
        fill(this.color);
        rectMode(CENTER);
        let v = this.pos.copy().mult(SIZE);
        translate(v);
        // if (abs(this.pos.x) > 0) {
        //     rotateY(HALF_PI);
        // } else if (abs(this.pos.y) > 0) {
        //     rotateX(HALF_PI);
        // }
        if (abs(v.x) > 0) {
            rotateY(HALF_PI);
        } else if (abs(v.y) > 0) {
            rotateX(HALF_PI);
        }

        square(0, 0, SIZE * 2);
        pop();
    }
}

class Cubie {
    constructor(pos) {
        this.pos = pos;
        this.faces = [
            new Face(createVector(0, 0, 1), color('#009B48')), // Front
            new Face(createVector(0, 0, -1), color('#0046AD')), // Back
            new Face(createVector(0, 1, 0), color('#FFFFFF')), // Up
            new Face(createVector(0, -1, 0), color('#FFD500')), // Down
            new Face(createVector(1, 0, 0), color('#FF5800')), // Right
            new Face(createVector(-1, 0, 0), color('#B71234')), // Left
        ];   

        // this.faces = [
        //     new Face(createVector(0, 0, 1), color('#009B48')), // Front
        //     new Face(createVector(0, 0, -1), color('#0046AD')), // Back
        //     new Face(createVector(0, 1, 0), color('#FFFFFF')), // Up
        //     new Face(createVector(0, -1, 0), color('#FFD500')), // Down
        //     new Face(createVector(1, 0, 0), color('#B71234')), // Right
        //     new Face(createVector(-1, 0, 0), color('#FF5800')), // Left
        // ];
    }

    turnX(angle) {
        let matrix = mat2d.create();
        mat2d.rotate(matrix, matrix, angle);
        mat2d.translate(matrix, matrix, [this.pos.y, this.pos.z]);
        this.pos = createVector(this.pos.x, round(matrix[4]), round(matrix[5]));

        for (let face of this.faces) {
            face.turnX(angle);
        }
    }

    turnY(angle) {
        let matrix = mat2d.create();
        mat2d.rotate(matrix, matrix, angle);
        mat2d.translate(matrix, matrix, [this.pos.x, this.pos.z]);
        this.pos = createVector(round(matrix[4]), this.pos.y, round(matrix[5]));

        for (let face of this.faces) {
            face.turnY(angle);
        }
    }

    turnZ(angle) {
        let matrix = mat2d.create();
        mat2d.rotate(matrix, matrix, angle);
        mat2d.translate(matrix, matrix, [this.pos.x, this.pos.y]);
        this.pos = createVector(round(matrix[4]), round(matrix[5]), this.pos.z);

        for (let face of this.faces) {
            face.turnZ(angle);
        }
    }

    show() {
        push();
        let v = this.pos.copy().mult(SIZE * 2);
        translate(v);
        for (let face of this.faces) {
            face.show();
        }
        pop();
    }
}

class RubiksCube {
    constructor() {
        this.cubies = [];
        for (let i = -1; i < 2; i++) {
            for (let j = -1; j < 2; j++) {
                for (let k = -1; k < 2; k++) {
                    this.cubies.push(new Cubie(createVector(i, j, k)));
                }
            }
        }
    }

    turnX(x, angle) {
        for (let cubie of this.cubies) {
            if (cubie.pos.x == x) {
                cubie.turnX(angle)
            }
        }
    }

    turnY(y, angle) {
        for (let cubie of this.cubies) {
            if (cubie.pos.y == y) {
                cubie.turnY(angle);
            }
        }
    }

    turnZ(z, angle) {
        for (let cubie of this.cubies) {
            if (cubie.pos.z == z) {
                cubie.turnZ(angle);
            }
        }
    }

    applyMove(move) {
        switch (move.axisName) {
            case 'x':
                this.turnX(move.axisValue, move.dir * HALF_PI);
                break;
            case 'y':
                this.turnY(move.axisValue, move.dir * HALF_PI);
                break;
            case 'z':
                this.turnZ(move.axisValue, move.dir * HALF_PI);
                break;
        }
    }

    applySequence(sequence) {
        for (let move of sequence) {
            this.applyMove(move);
        }
    }

    show() {
        for (let cubie of this.cubies) {
            cubie.show();
        }
    }
}

class RubiksCubeController {
    constructor(cube) {
        this.cube = cube;
        this.undoStack = [];
        this.redoStack = [];
    }

    execute(obj) {
        console.log(obj)
        if (obj instanceof Array) {
            this.cube.applySequence(obj.flatMap(
                (currentValue) => Move.fromString(currentValue)
            ));
            this.undoStack = this.undoStack.concat(obj);
        } else if (typeof obj === 'string') {
            this.cube.applyMove(Move.fromString(obj));
            this.undoStack.push(obj);
        }
        this.redoStack = [];
    }

    undo() {
        if (!this.undoStack.length) {
            return;
        }
        let move = this.undoStack.pop();
        let reverse = Move.getInverseStringFromString(move);
        this.cube.applyMove(Move.fromString(reverse));
        this.redoStack.push(move);
    }

    redo() {
        if (!this.redoStack.length) {
            return;
        }
        let move = this.redoStack.pop();
        this.cube.applyMove(Move.fromString(move));
        this.undoStack.push(move);
    }

    *reset() {
        for (let i = this.undoStack.length; i > 0; i--) {
            yield this.undo();
        }
    }
}