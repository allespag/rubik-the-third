class Move {

    static dispatcher = new Map([
        ["F", new Move("z", 1, 1)],
        ["F2", new Move("z", 1, 2)],
        ["F'", new Move("z", 1, -1)],
        ["R", new Move("x", -1, -1)],
        ["R2", new Move("x", -1, 2)],
        ["R'", new Move("x", -1, 1)],
        ["U", new Move("y", 1, 1)],
        ["U2", new Move("y", 1, 2)],
        ["U'", new Move("y", 1, -1)],
        ["B", new Move("z", -1, -1)],
        ["B2", new Move("z", -1, 2)],
        ["B'", new Move("z", -1, 1)],
        ["L", new Move("x", 1, 1)],
        ["L2", new Move("x", 1, 2)],
        ["L'", new Move("x", 1, -1)],
        ["D", new Move("y", -1, -1)],
        ["D2", new Move("y", -1, 2)],
        ["D'", new Move("y", -1, 1)],
    ]);

    constructor(axisName, axisValue, dir) {
        this.axisName = axisName;
        this.axisValue = axisValue;
        this.dir = dir;
    }

    static fromString(moveAsString) {
        return Move.dispatcher.get(moveAsString);
    }

    static getSequence(sequenceAsString) {
        let sequence = [];
        
        for (let moveAsString of sequenceAsString.split(' ')) {
            sequence.push(Move.fromString(moveAsString));
        }
        
        return sequence
    }
    
    
    static getRandomSequence(length) {
        let sequence = [];

        for (let i = 0; i < length; i++) {
            let randomKey = getRandomKey(Move.dispatcher);
            sequence.push(randomKey);
        }

        return sequence;
    }

    static getInverseStringFromString(moveAsString) {
        if (moveAsString.length == 1) {
            return moveAsString + "'";
        } else if (moveAsString.length == 2) {
            if (moveAsString[1] == "'") {
                return moveAsString[0];
            } else if (moveAsString[1] == "2") {
                return moveAsString;
            } else {
                return null;
            }
        } else {
            return null;
        }
    }
}