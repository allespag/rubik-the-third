class Move {
    static dispatcher = new Map([
        ["U", new Move(0, 1, 0, 1)],
        ["U2", new Move(0, 1, 0, 2)],
        ["U'", new Move(0, 1, 0, -1)],
        ["R", new Move(-1, 0, 0, 1)],
        ["R2", new Move(-1, 0, 0, 2)],
        ["R'", new Move(-1, 0, 0, -1)],
        ["F", new Move(0, 0, 1, 1)],
        ["F2", new Move(0, 0, 1, 2)],
        ["F'", new Move(0, 0, 1, -1)],
        ["D", new Move(0, -1, 0, 1)],
        ["D2", new Move(0, -1, 0, 2)],
        ["D'", new Move(0, -1, 0, -1)],
        ["L", new Move(1, 0, 0, 1)],
        ["L2", new Move(1, 0, 0, 2)],
        ["L'", new Move(1, 0, 0, -1)],
        ["B", new Move(0, 0, -1, 1)],
        ["B2", new Move(0, 0, -1, 2)],
        ["B'", new Move(0, 0, -1, -1)],
    ]);

    constructor(x, y, z, dir) {
        this.x = x;
        this.y = y;
        this.z = z;
        this.dir = dir;
    }

    static fromString(moveAsString) {
        return Move.dispatcher.get(moveAsString);
    }

    getReverse() {
        return new Move(this.x, this.y, this.z, -this.dir)
    }
}

function createSequence(sequenceAsString) {
    let sequence = [];

    for (let moveAsString of sequenceAsString.split(' ')) {
        sequence.push(Move.fromString(moveAsString));
    }

    return sequence;
}