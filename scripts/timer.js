class Timer {
    paused = false;
    dateTimeOnUnpause;
    timeShownOnPause;
    intervalID;

    time = 0;

    //Resets and pauses the timer
    static Reset() {
        Timer.time = 0;
        Timer.Pause();
    }

    static Pause() {
        Timer.paused = true;
        Timer.timeShownOnPause = Timer.time;
        clearInterval(Timer.intervalID);
    }

    static Unpause() {
        Timer.paused = false;
        Timer.dateTimeOnUnpause = new Date().getTime();
        Timer.intervalID = setInterval(UpdateTimer, 500);
    }

    static AddSeconds(s) {
        Timer.timeShownOnPause += s * 1000;
        UpdateTimer();
    }
}

function UpdateTimer() {
    if (!Timer.paused) {
        Timer.time = Timer.timeShownOnPause + new Date().getTime() - Timer.dateTimeOnUnpause;
        let secs = Math.floor((Timer.time / 1000) % 60).toString();
        let mins = Math.floor(Timer.time / 60000).toString();

        if (mins>=60) timerElement.textContent = ">1hr"
        else {
            if (secs.length==1) secs = '0'+secs;
            if (mins.length==1) mins = '0'+mins;
    
            timerElement.textContent = mins.toString() + ":" + secs.toString();
        }

    }
}