let cam;
let running;
let shuffling;
let resetting;
let solving;

let cube;
let cubeController;
let undoIterator;
let sequence;

let speedSlider;
let resetButton;
let solveButton;
let domElements;

const rotateAngles = Array.from(Array(3)).map(() => getRandomArbitrary(-0.01, 0.01));
const keybinds = ['f', 'r', 'u', 'b', 'l', 'd', 'F', 'R', 'U', 'B', 'L', 'D'];

  

function setup() {
    canvas = createCanvas(windowWidth, windowHeight, WEBGL);

    cam = createEasyCam();
    cam.setDistanceMin(150);
    cam.setDistanceMax(1000);

    document.oncontextmenu = function () {
        return false;
    }

    running = false;
    shuffling = false;
    resetting = false;
    solving = false;

    // TODO: uncomment
    // idle = new Idle({
    //     onAway: () => running = false,
    //     awayTimeout: 5000
    // }).start();

    cube = new RubiksCube();
    cubeController = new RubiksCubeController(cube);
    undoIterator = null;

    speedSlider = createSlider(-50, -1, -25, 1);
    speedSlider.addClass('slider');
    speedSlider.updatePosition = () => {
        const offset = 20;
        speedSlider.position(width - speedSlider.width - offset, offset);
    };
    speedSlider.updatePosition();

    resetButton = createButton('Reset');
    resetButton.mousePressed(() => {
        resetting = true;
        shuffling = false;
        undoIterator = cubeController.reset();
    });
    resetButton.updatePosition = () => {
        const offset = 20;
        resetButton.position(width - resetButton.width - offset, height - resetButton.height - offset);
    };
    resetButton.updatePosition();

    solveButton = createButton('Solve');
    solveButton.mousePressed(() => {
        console.log(cubeController.undoStack)
        $.ajax({
            type: 'POST',
            url: $(location).attr('href'),
            data: JSON.stringify({
                "sequence": cubeController.undoStack.join(' ')
            }),
            success: function(response) {
                sequence = response.split(' ');
                solving = true;
            },
            error: function(e) {
                console.log(e)
            },
            dataType: 'json',
            contentType: 'application/json'
          });
    });
    solveButton.updatePosition = () => {
        const offset = 20;
        solveButton.position(width - solveButton.width - offset, height - resetButton.height - solveButton.height - offset * 1.5);
    };
    solveButton.updatePosition();

    domElements = [
        speedSlider,
        resetButton,
        solveButton,
    ];
}

function draw() {
    background('#FAF0D7');

    if (!running) {
        cam.rotateX(rotateAngles[0]);
        cam.rotateY(rotateAngles[1]);
        cam.rotateZ(rotateAngles[2]);
    }

    if (shuffling && frameCount % speedSlider.value() == 0) {
        cubeController.execute(Move.getRandomSequence(1)[0]);
    } else if (resetting && frameCount % speedSlider.value() == 0) {
        cubeController.execute(undoIterator.next().value);
    } else if (solving && frameCount % speedSlider.value() == 0) {
        const currentMove = sequence[0]
        console.log(currentMove)
        cubeController.execute(currentMove);
        sequence.splice(0, 1);
        
        if (sequence.length == 0) {
            solving = false;
        }
    }

    cube.show();
}

function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
    cam.setViewport([0, 0, windowWidth, windowHeight]);
    domElements.forEach(element => element.updatePosition());
}

function mousePressed() {
    running = true;
}

function keyPressed() {
    if (keybinds.includes(key)) {
        let m = key.toUpperCase() + (key == key.toUpperCase() ? "'": "");
        cubeController.execute(m);
    } else if (keyCode == RIGHT_ARROW) {
        cubeController.redo();
    } else if (keyCode == LEFT_ARROW) {
        cubeController.undo();
    } else if (key == ' ') {
        shuffling = !shuffling;
        resetting = false;
    }
}
