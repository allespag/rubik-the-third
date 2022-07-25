let canvas;
let cam;

let cube;
let cubeController;

let domElements;

const keybinds = new Map();

function setup() {
    canvas = createCanvas(windowWidth, windowHeight, WEBGL);

    cam = createEasyCam();
    cam.setDistanceMin(260);
    cam.setDistanceMax(1000);

    document.oncontextmenu = function () {
        return false;
    }

    cube = new Cube();
    cubeController = new CubeController(cube);

    domElements = [];

    keybinds["ArrowLeft"] = () => cubeController.undo();
    keybinds["ArrowRight"] = () => cubeController.redo();
    keybinds['u'] = () => {cubeController.execute(Move.fromString("U"))};
    keybinds['U'] = () => {cubeController.execute(Move.fromString("U'"))};
    keybinds['r'] = () => {cubeController.execute(Move.fromString("R"))};
    keybinds['R'] = () => {cubeController.execute(Move.fromString("R'"))};
    keybinds['f'] = () => {cubeController.execute(Move.fromString("F"))};
    keybinds['F'] = () => {cubeController.execute(Move.fromString("F'"))};
    keybinds['d'] = () => {cubeController.execute(Move.fromString("D"))};
    keybinds['D'] = () => {cubeController.execute(Move.fromString("D'"))};
    keybinds['l'] = () => {cubeController.execute(Move.fromString("L"))};
    keybinds['L'] = () => {cubeController.execute(Move.fromString("L'"))};
    keybinds['b'] = () => {cubeController.execute(Move.fromString("B"))};
    keybinds['B'] = () => {cubeController.execute(Move.fromString("B'"))};
}

function draw() {
    background('#FAF0D7');

    cube.show();
}

function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
    cam.setViewport([0, 0, windowWidth, windowHeight]);
    domElements.forEach(element => element.updatePosition());
}

// -> redo
// <- undo
// moves

function keyPressed() {
    if (key in keybinds) {
        keybinds[key]();
    }
}
