function GetDailyPuzzleNum() {
    //The 'zero date' (the moment the first puzzles goes live) is midnight in whatever timezone the play is in - thus 24 hours later is also at midnight
    let dateZero = new Date('December 10, 2024 00:00:00');
    //Daily puzzle increments at midnight local time
    return Math.floor((new Date() - dateZero) / (1000*60*60*24));
}


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

    static SetTime(time) {
        Timer.Reset();
        Timer.AddTime(time);
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

    static AddTime(s) {
        if (Timer.paused) Timer.time += s;
        Timer.timeShownOnPause += s;
        UpdateTimer();
    }


    static GetString() {
        let secs = Math.floor((Timer.time / 1000) % 60).toString();
        let mins = Math.floor(Timer.time / 60000).toString();

        if (mins>=60) return ">1hr"
        else {
            if (secs.length==1) secs = '0'+secs;
            if (mins.length==1) mins = '0'+mins;

            return mins.toString() + ":" + secs.toString();
        }
    }
}

function UpdateTimer() {
    if (!Timer.paused) Timer.time = Timer.timeShownOnPause + new Date().getTime() - Timer.dateTimeOnUnpause;

    timerElement.textContent = Timer.GetString();

    SetCookie('daily_timer', Timer.time);
}