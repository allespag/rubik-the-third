class Cubie {
    constructor(x, y, z) {
        this.x = x;
        this.y = y;
        this.z = z;

        this.faces = [
            new Face(0, 1, 0, color('#FFFFFF')),    // Up
            new Face(1, 0, 0, color('#FF5800')),    // Right
            new Face(0, 0, 1, color('#009B48')),    // Front
            new Face(0, -1, 0, color('#FFD500')),   // Down
            new Face(-1, 0, 0, color('#B71234')),   // Left
            new Face(0, 0, -1, color('#0046AD')),   // Back
        ];
    }

    turnX(angle) {
        for (let face of this.faces) {
            face.turnX(angle);
        }
    }

    turnY(angle) {
        for (let face of this.faces) {
            face.turnY(angle);
        }
    }

    turnZ(angle) {
        for (let face of this.faces) {
            face.turnZ(angle);
        }
    }

    show() {
        push();
        
        translate(this.x, this.y, this.z);
        for (let face of this.faces) {
            face.show();
        }

        pop();
    }
}