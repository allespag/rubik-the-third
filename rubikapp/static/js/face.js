class Face {
    constructor(x, y, z, color) {
        this.x = x;
        this.y = y;
        this.z = z;
        this.color = color;
    }

    turnX(angle) {
        const x = round(this.x);
        const y = round(this.y * cos(angle) - this.z * sin(angle));
        const z = round(this.y * sin(angle) + this.z * cos(angle));

        this.x = x;
        this.y = y;
        this.z = z;
    }

    turnY(angle) {
        const x = round(this.x * cos(angle) - this.z * sin(angle));
        const y = round(this.y);
        const z = round(this.x * sin(angle) + this.z * cos(angle));
        
        this.x = x;
        this.y = y;
        this.z = z;   
    }

    turnZ(angle) {
        const x = round(this.x * cos(angle) - this.y * sin(angle));
        const y = round(this.x * sin(angle) + this.y * cos(angle));
        const z = round(z);

        this.x = x;
        this.y = y;
        this.z = z;
    }

    show() {
        push();

        fill(this.color);
        strokeWeight(2);
        rectMode(CENTER);
        translate(this.x * 0.5, this.y * 0.5, this.z * 0.5);
        if (abs(this.x) > 0) {
            rotateY(HALF_PI);
        } else if (abs(this.y) > 0) {
            rotateX(HALF_PI);
        }
        square(0, 0, 1);

        pop();
    }
}