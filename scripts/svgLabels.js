//Generous collision detection (including screen margins and the dots)
function IsPointOnLabel(x, y, xIndex, yIndex) {
  let lX = GetLabelX(xIndex); let lY = GetLabelY(yIndex);

  let xIntersect =  xIndex==0 ? (x <= lX + CONSTS.LABEL_WIDTH + CONSTS.DOT_RADIUS*2) : (x >= lX - CONSTS.DOT_RADIUS*2);
  let yIntersect = y >= lY - CONSTS.LABEL_VERTICAL_SPACING/2 && y <= lY + CONSTS.LABEL_HEIGHT + CONSTS.LABEL_VERTICAL_SPACING/2;
  return xIntersect && yIntersect;
}

const GetLabelX = (xIndex) => xIndex==0 ? CONSTS.PADDING_X : GetCanvasSize(svg).width - CONSTS.PADDING_X - CONSTS.LABEL_WIDTH;
const GetLabelY = (yIndex) => CONSTS.LABEL_VERTICAL_SPACING + yIndex * (CONSTS.LABEL_HEIGHT + CONSTS.LABEL_VERTICAL_SPACING);

function BuildLabelSVG(text, xIndex, yIndex) {
  var x = GetLabelX(xIndex);
  var y = GetLabelY(yIndex);

  //Background
  AddElementToSVG('rect', {"class":"labelBackground", "x":x, "y":y, "width":CONSTS.LABEL_WIDTH, "height": CONSTS.LABEL_HEIGHT});

  //Break the text into lines
  var lines = TextWrapper.wrap({"class":"labelText"}, text, CONSTS.LABEL_WIDTH - CONSTS.LABEL_HORIZONTAL_TEXT_MARGIN);

  //Calculate the total height of the text - thus work out the starting y pos for writing the lines
  var textHeight = 0;
  lines.forEach((line) => { textHeight += line.BBox.height-CONSTS.LINE_VERTICAL_SQUASH; })
  y += (CONSTS.LABEL_HEIGHT-textHeight)/2 + lines[0].BBox.height*0.75;

  //Add each line
  lines.forEach((line) => {
    textEl = AddElementToSVG('text', {"class":"labelText", x:x + (CONSTS.LABEL_WIDTH-line.BBox.width)/2, y:y});
    textEl.innerHTML = line.word;
    y += line.BBox.height - CONSTS.LINE_VERTICAL_SQUASH;
  });
}

const GetDotPosition = (xIndex, yIndex) => [
  GetLabelX(xIndex) + (xIndex==0 ? CONSTS.DOT_RADIUS + CONSTS.LABEL_WIDTH : -CONSTS.DOT_RADIUS),
  GetLabelY(yIndex) + CONSTS.LABEL_HEIGHT/2
];

function BuildDotSVG(xIndex, yIndex) {
  let [x,y] = GetDotPosition(xIndex, yIndex);
  AddElementToSVG('circle', {"class":"dot", cx:x, cy:y, r:CONSTS.DOT_RADIUS});
}

function BuildNodeSVG(puzzle, xIndex, yIndex) {
  BuildLabelSVG(puzzle.clues[xIndex][yIndex], xIndex, yIndex);
  BuildDotSVG(xIndex, yIndex);
}

function AddSVGBackground() {
  let canvasSize = GetCanvasSize();
  AddElementToSVG('rect', {x:"0", y:"0", width:canvasSize.width, height:canvasSize.height, "id":"background"});
}

function BuildPuzzleSVG(puzzle) {
  svg.innerHTML = ""; //Remove all existing svg elements

  //Re-Add Background
  AddSVGBackground();

  for (let i=0; i<puzzle.N; i++) {
      if (puzzle.clues[0]!=null) BuildNodeSVG(puzzle, 0, i);
      if (puzzle.clues[1]!=null) BuildNodeSVG(puzzle, 1, i);
  }
}

