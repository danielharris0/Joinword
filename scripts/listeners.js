//Whenever the viewport changes size, we use the auto-rescaled svg element to set the width of the menu bar
function LimitHTMLWidthToSVGCanvas() {
    let svgBackground = document.getElementById("background")
    let rect = svgBackground.getBoundingClientRect();
    document.getElementById("menuBar").style["width"] = rect.width.toString() + "px";

    document.querySelector(".content").style["width"] = rect.width.toString() + "px";
    document.querySelector(".content").style["top"] = rect.top.toString() + "px";
    document.querySelector(".content").style["left"] = rect.left.toString() + "px";
    document.querySelector(".content").style["height"] = rect.height.toString() + "px";
  }
  window.onresize = LimitHTMLWidthToSVGCanvas;
  LimitHTMLWidthToSVGCanvas();
  
  
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