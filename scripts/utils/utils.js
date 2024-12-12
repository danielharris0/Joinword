function CancelAllAnimations(element) {
    for (let animation of element.getAnimations()) animation.cancel();
}

function GetCanvasSize() { return svg.viewBox.baseVal; }

function AddElementToSVG(name, attrs ) {
  var el = document.createElementNS(svg.getAttribute('xmlns'), name); //We need to add the elements to the same XML Namespace for SVG, otherwise they won't show up
  SetAttributes(el, attrs);
  return svg.appendChild(el);
}

function SetAttributes(el, attrs) {
  for (var attr in attrs) el.setAttribute(attr,attrs[attr]);
}

function SetCookie(cname, cvalue, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  let expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function GetCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function CookieExists(cname) {
  return GetCookie(cname)!="";
}