function PlayButtonPressed() {
  SceneManager.DailyPuzzle();
}

function PauseButtonPressed() {
  SceneManager.Menu();
}

function ShareButtonPressed() {
  let shareText = "I solved today's Joinword in ⌛" + Timer.GetString() + "⌛\ndanielharris0.github.io/Joinword"

  try {
    navigator.share({'text': shareText})
  } catch {
    navigator.clipboard.writeText(shareText);
    picoModal("Copied message to clipboard: \n" + shareText).show();
  }
}

function CheckButtonPressed() {
  let floatingCircle = document.querySelector(".floatingCircle");
  floatingCircle.setAttribute('onmousedown','');
  
  console.assert(lines.length == puzzle.N);
  var incorrectLines = []
  lines.forEach((line) => {
    let correct = IsConnectionValid(line.ends[0], line.ends[1]); 
    if (!correct) incorrectLines.push(line)
  });

  incorrectLines.forEach((line) => {
    line.element.animate([{stroke: "red"},{stroke: "red"}, {stroke:"black"}], {duration: 250,iterations: 20})
  });

  let icon = floatingCircle.children[0];
  if (incorrectLines.length==0) {
    //Correct
    SetCookie('daily_isSolved', true);
    icon.setAttribute('src', 'icons/tick.png');
    CancelAllAnimations(icon);
    icon.animate([{transform: "scale(1)"}, {transform: "scale(2)"}, {transform: "scale(1)"}], {duration: 400,iterations: 1})
      .addEventListener('finish', (event) => {
        SceneManager.Menu();
      })
    Timer.Pause();

  } else {
    //Incorrect

    //Increment num attempts
    SetCookie('daily_numAttempts',parseInt(GetCookie('daily_numAttempts'))+1);

    //+20s to the timer
    const para = document.createElement("p");
    para.innerText = "+20s";
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

    Timer.AddTime(20 * 1000);
    


    //Cross icon and fade out
    icon.setAttribute('src', 'icons/cross.png');
    setTimeout(() => {floatingCircle.classList.remove("active");}, 500)
  }
}

function IsConnectionValid(l, r) {
  return puzzle.answer[l].includes(r);
}
