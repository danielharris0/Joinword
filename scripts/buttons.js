function CheckButtonPressed() {
 /* try {
    navigator.share({'text': "text test"})
  } catch {
    navigator.clipboard.writeText("test text");
    picoModal("Copied message to clipboard: test text.").show();
  }*/

  

  let popup = document.querySelector(".popup");
  popup.setAttribute('onmousedown','');
  
  console.assert(lines.length == puzzle.N);
  var incorrectLines = []
  lines.forEach((line) => {
    let correct = IsConnectionValid(line.ends[0], line.ends[1]); 
    if (!correct) incorrectLines.push(line)
  });

  incorrectLines.forEach((line) => {
    line.element.animate([{stroke: "red"},{stroke: "red"}, {stroke:"black"}], {duration: 250,iterations: 20})
  });

  let icon = popup.children[0];
  if (incorrectLines.length==0) {
    //Correct
    icon.setAttribute('src', 'icons/tick.png');
    CancelAllAnimations(icon);
    icon.animate([{transform: "scale(1)"}, {transform: "scale(2)"}, {transform: "scale(1)"}], {duration: 250,iterations: 1}).addEventListener('finish', (event) => {window.location = 'share.html'})
    Timer.Pause();

  } else {
    //Incorrect

    //Cross icon and fade out
    icon.setAttribute('src', 'icons/cross.png');
    setTimeout(() => {popup.classList.remove("active");}, 500)

    //+10s to the timer
    const para = document.createElement("p");
    para.innerText = "+10s";
    document.body.appendChild(para);
    para.classList.add('floatingNum');

    let iconRect = icon.getBoundingClientRect();
    let timerRect = timerElement.getBoundingClientRect();

    const xShift = (p) => (timerRect.left - iconRect.left)*p + iconRect.left;
    let y = iconRect.top;

    para.style.transform = `translate(${xShift(0.6)}px, ${y}px)`;
    para.style.opacity = 1;

    para.animate([{transform: `translate(${xShift(0.6)}px, ${-20}px)`, opacity: 0}], {duration: 1000,iterations: 1}).addEventListener('finish', () => {para.remove();});
    timerElement.animate([{color: "red"},{color: "red"}, {color:"black"}], {duration: 500,iterations: 2})
    
    Timer.AddSeconds(10);
  }
}

function IsConnectionValid(l, r) {
  return puzzle.answer[l].includes(r);
}
