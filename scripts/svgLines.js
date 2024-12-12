function OnLinesChanged() {
    let popup = document.querySelector(".popup");
    if (lines.length == puzzle.N) {
        popup.setAttribute('onmousedown','CheckButtonPressed()');
        let icon = popup.children[0];
        CancelAllAnimations(icon);
        icon.animate([{transform: "scale(1.1)"}, {transform:"scale(1.0)"}], {duration: 1000,iterations: Infinity})
        icon.setAttribute('src', 'icons/question.png');
        popup.classList.add("active");
    } else {
        popup.classList.remove("active");
    }        
}

function GetLineConnectedToLabel(xIndex, yIndex) {
    for (let line of lines) {
      if (line.ends[xIndex] == yIndex) return line;
    }
    return null;
}

function RemoveLine(line) {
    line.element.remove(); //remove the svg line element
    lines = lines.filter((x) => x!=line); //remove the entry from the list of lines
    OnLinesChanged();
}

function NewDraggingLine(xIndex, yIndex) {
    var [x,y] = GetDotPosition(xIndex, yIndex);
    var lineEl = AddElementToSVG('line', {"class": "connectorLine", x1:x, y1:y, x2:x, y2:y});
    currentDraggingLine = {"element": lineEl, ends: [null, null]};
    currentDraggingLine.ends[xIndex] = yIndex;
    currentDraggingLineStartX = xIndex;
}

function AddDraggingToLines() {
    lines.push({"element": currentDraggingLine.element, "ends": currentDraggingLine.ends});
    currentDraggingLine = null;
    OnLinesChanged();
}

//Dragging Inputs:
function OnDrag(x, y) {
    if (currentDraggingLine!=null) {
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
  
  function OnDragEnd() {
    if (currentDraggingLine!=null) {
  
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