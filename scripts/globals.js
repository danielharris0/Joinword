let mouseDown = false;
let svg = document.getElementById("svgCanvas");
let timerElement = document.getElementById("timer");
let lineDrawingActive = false;

let puzzle;
let lines = [];
let currentDraggingLine;
let currentDraggingLineStartX;

const CONSTS = {
    LABEL_WIDTH: 100,
    LABEL_HEIGHT: 50,
    DOT_RADIUS: 5,
  
    PADDING_X: 5,
  
    LABEL_VERTICAL_SPACING: 15,
    LABEL_HORIZONTAL_TEXT_MARGIN: 1,
  
    DOT_RADIUS: 5,
  
    LINE_VERTICAL_SQUASH: 3, //How many pixels one line can be allowed to bleed into another (according to their bounding boxes)
}