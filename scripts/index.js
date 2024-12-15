/*
    TODO:
    - special puzzle elements / modes
        - semantic lock
        - seperate the central dots
    - fix what happens when we run as a local instance (no cookies)

    - increase penalty
    - multi-dot labels
    - support for custom label styling (e.g. bold, italics, colors)

    - auto gen from dataset
    - 'special edition' indicator
    - play special editions archive button


    - black dots and white dots (white dots *could* be connected but needn't be)
*/

SetCurrentPuzzle(GetDailyPuzzleNum());

ReadCookiesAndCompareToCurrentDay();
LoadLinesFromCookies();
Timer.SetTime(parseInt(GetCookie('daily_timer', '0')));

SceneManager.Menu();

function ReadCookiesAndCompareToCurrentDay() {
    let lastDayPlayed = GetCookie('lastDayPlayed',-1);
    let currentDay = GetDailyPuzzleNum();

    console.log('currentDay: ', currentDay);

    if (lastDayPlayed != currentDay) {
        console.log('lastDayPlayed: ', lastDayPlayed, ' did not match current Day. Discarding cookies.');
        console.log('daily_timer: ', GetCookie('daily_timer'));
        console.log('daily_isSolved: ', GetCookie('daily_isSolved'));
        console.log('daily_numAttempts: ', GetCookie('daily_numAttempts'));
        console.log('daily_lines: ', GetCookie('daily_lines'));


        //Then discard the saved data
        SetCookie('lastDayPlayed', currentDay);
        SetCookie('daily_timer', 0);
        SetCookie('daily_isSolved', false);
        SetCookie('daily_numAttempts',0);
        SetCookie('daily_lines',JSON.stringify([]));
    }

    console.log('daily_timer: ', GetCookie('daily_timer'));
    console.log('daily_isSolved: ', GetCookie('daily_isSolved'));
    console.log('daily_numAttempts: ', GetCookie('daily_numAttempts'));
    console.log('daily_lines: ', GetCookie('daily_lines'));
}