function LoadLinesFromCookies() {
  let connections = JSON.parse(GetCookie('daily_lines'));
  console.log(connections);
  for (let connection of connections) {
    var [xa,ya] = GetDotPosition(0, connection[0]);
    var [xb,yb] = GetDotPosition(1, connection[1]);
    var element = AddElementToSVG('line', {"class": "connectorLine", x1:xa, y1:ya, x2:xb, y2:yb});
    lines.push({"element": element, "ends": connection});
  }
}

function OnLinesChanged() {
    let floatingCircle = document.querySelector(".floatingCircle");
    if (lines.length == puzzle.N) {
        floatingCircle.setAttribute('onmousedown','CheckButtonPressed()');
        let icon = floatingCircle.children[0];
        CancelAllAnimations(icon);
        icon.animate([{transform: "scale(1.1)"}, {transform:"scale(1.0)"}], {duration: 1000,iterations: Infinity})
        icon.setAttribute('src', 'icons/question.png');
        floatingCircle.classList.add("active");
    } else {
      floatingCircle.classList.remove("active");
    }
    
    
    //Save lines to cookies
    let connections = [];
    for (let line of lines) connections.push(line.ends);
    SetCookie('daily_lines', JSON.stringify(connections));
}

function GetLineConnectedToLabel(xIndex, yIndex) {
    for (let line of lines) {
      if (line.ends[xIndex] == yIndex) return line;
    }
    return null;
}


function NewDraggingLine(xIndex, yIndex) {
    var [x,y] = GetDotPosition(xIndex, yIndex);
    var lineEl = AddElementToSVG('line', {"class": "connectorLine", x1:x, y1:y, x2:x, y2:y});
    currentDraggingLine = {"element": lineEl, ends: [null, null]};
    currentDraggingLine.ends[xIndex] = yIndex;
    currentDraggingLineStartX = xIndex;
}

function RemoveLine(line) {
  line.element.remove(); //remove the svg line element
  lines = lines.filter((x) => x!=line); //remove the entry from the list of lines
  OnLinesChanged();
}

function AddDraggingToLines() {
    lines.push({"element": currentDraggingLine.element, "ends": currentDraggingLine.ends});
    currentDraggingLine = null;
    OnLinesChanged();
}

//Dragging Inputs:
function OnDrag(x, y) {
    if (lineDrawingActive && currentDraggingLine!=null) {
      var point = new DOMPoint(x, y);
      point = point.matrixTransform(svg.getScreenCTM().inverse());
  
      //Set end position to mouse
      currentDraggingLine.element.setAttribute("x2", point.x)
      currentDraggingLine.element.setAttribute("y2", point.y)
  
      //Try to SNAP it to a label
      var xIndex = 1 - currentDraggingLineStartX;
      for (var yIndex=0; yIndex<puzzle.N; yIndex++) {
        if (IsPointOnLabel(point.x, point.y, xIndex, yIndex)) {
          currentDraggingLine.ends[xIndex] = yIndex;
  
          let [x,y] = GetDotPosition(xIndex, yIndex);
          currentDraggingLine.element.setAttribute('x2', x);
          currentDraggingLine.element.setAttribute('y2', y);
          return;
        }
      }
    }
  }
  
  function OnDragStart(x, y) {
    if (lineDrawingActive) {
      for (let yIndex=0; yIndex<puzzle.N; yIndex++) {
        for (let xIndex=0; xIndex<2; xIndex++) {
          if (IsPointOnLabel(x,y,xIndex,yIndex)) {
            var line = GetLineConnectedToLabel(xIndex, yIndex);
            if (line!=null) RemoveLine(line);
    
            NewDraggingLine(xIndex, yIndex);
    
            return; 
          }
        }
      }
    }
  }
  
  function OnDragEnd() {
    if (lineDrawingActive && currentDraggingLine!=null) {
  
      var x = currentDraggingLine.element.getAttribute('x2');
      var y = currentDraggingLine.element.getAttribute('y2');
  
      //Test possible end label locations
      var xIndex = 1 - currentDraggingLineStartX;
      for (var yIndex=0; yIndex<puzzle.N; yIndex++) {
        if (IsPointOnLabel(x,y,xIndex,yIndex)) {
          //Remove existing connections
          var line = GetLineConnectedToLabel(xIndex, yIndex);
          if (line!=null) RemoveLine(line);
  
          var [x,y] = GetDotPosition(xIndex, yIndex);
          currentDraggingLine.element.setAttribute('x2', x);
          currentDraggingLine.element.setAttribute('y2', y);
  
          //Add to lines
          currentDraggingLine.ends[xIndex] = yIndex;
          AddDraggingToLines()
          return; 
          
        }
      }
      currentDraggingLine.element.remove();
    }
    currentDraggingLine = null;
  }