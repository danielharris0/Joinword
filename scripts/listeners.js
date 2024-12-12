//Whenever the viewport changes size, we use the auto-rescaled svg element to set the width of the menu bar
function LimitMenuBarWidthToSVGCanvas() {
    const element = document.getElementById("background");
    let width = element.getBoundingClientRect().width.toString() + "px";
    document.getElementById("menuBar").style["width"] = width;
  }
  window.onresize = LimitMenuBarWidthToSVGCanvas;
  LimitMenuBarWidthToSVGCanvas();
  
  
addEventListener("mouseup", (event) => {
    mouseDown=false;
    OnDragEnd();
});
addEventListener("mousedown", (event) => {mouseDown=true;});
addEventListener("mousemove", (event) => {
    if (mouseDown) OnDrag(event.clientX, event.clientY);
});

addEventListener("pointerdown", (event) => {
    mouseDown=true;

    let point = new DOMPoint(event.clientX, event.clientY);
    point = point.matrixTransform(svg.getScreenCTM().inverse());

    OnDragStart(point.x, point.y);
});
addEventListener("touchend", (event) => OnDragEnd());
addEventListener("touchmove", (event) => {
    for (let i=0; i<event.touches.length; i++) {let touch = event.touches.item(i); OnDrag(touch.clientX, touch.clientY); }
});