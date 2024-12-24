class SceneManager {
    static DailyPuzzle() {
        document.querySelector(".floatingCircle").classList.remove("active");
        let solved = GetCookie('daily_isSolved', 'false') == 'true';
        if (!solved) Timer.Unpause();

        document.querySelector('.pauseButton img').setAttribute('src', 'icons/pause.png');
        document.querySelector('.pauseButton').setAttribute('onmousedown', 'PauseButtonPressed()');

        document.querySelector('.svgContainer').style.visibility = 'visible';
        document.querySelector('.content').style.visibility = 'hidden';

        lineDrawingActive = !solved;
        if (!solved) OnLinesChanged(); //In case the saved lines are complete
    }

    static Menu() {
        Timer.Pause();
        lineDrawingActive = false;

        //Date
        document.querySelector(".date").innerHTML = GetDateString(new Date());

        //Menu bar play button
        document.querySelector('.pauseButton img').setAttribute('src', 'icons/play.png');
        document.querySelector('.pauseButton').setAttribute('onmousedown', 'PlayButtonPressed()');


        document.querySelector('.svgContainer').style.visibility = 'hidden';
        document.querySelector('.content').style.visibility = 'visible';

        let solved = GetCookie('daily_isSolved', 'false') == 'true';
        let timer = parseInt(GetCookie('daily_timer', '0'));

        //Clear the context-specific part of the menu to be remade
        let menu = document.querySelector(".context-specific-menu-section")
        menu.innerHTML = "";


        if (solved) {
            //Solved
            document.querySelector("#mainPlayButton span").innerHTML = "Admire";
            document.querySelector("#mainPlayButton img").setAttribute('src', 'icons/eye.png');

            //Timer
            AddElementAsChild(menu, "span", {'class': 'progressNotifier solved fontSizeMedium'}).innerHTML = 'Solved';
            AddElementAsChild(menu, "span", {'class': 'progressNotifier in fontSizeMedium'}).innerHTML = 'in';
            AddElementAsChild(menu, "span", {'class': 'stat-block prevent-select blue fontSizeMedium'}).innerHTML = Timer.GetString();

            AddElementAsChild(menu, "div", {'class':'smallDivider'});

            //Attempts count
            AddElementAsChild(menu, "span", {'class': 'progressNotifier in fontSizeSmall'}).innerHTML = '(';
            let numAttempts = parseInt(GetCookie('daily_numAttempts'));
            console.log(numAttempts);
            AddElementAsChild(menu, "span", {'class': 'stat-block prevent-select orange fontSizeSmall'}).innerHTML = numAttempts;
            if (numAttempts>0) {
                AddElementAsChild(menu, "span", {'class': 'progressNotifier in fontSizeSmall'}).innerHTML = 'attempts';
                AddElementAsChild(menu, "span", {'class': 'stat-block prevent-select orange fontSizeSmall'}).innerHTML = '+' + (numAttempts*20).toString() + 's';
                AddElementAsChild(menu, "span", {'class': 'progressNotifier in'}).innerHTML = ')';
            } else {
                AddElementAsChild(menu, "span", {'class': 'progressNotifier in fontSizeSmall'}).innerHTML = 'attempts)';
            }

            AddElementAsChild(menu, "div", {'class':'smallDivider'});
            AddElementAsChild(menu, "div", {'class':'smallDivider'});

            let flexbox = AddElementAsChild(menu, "div", {'class': 'content', 'style':'margin-left:10px;'});
            let shareButton = AddElementAsChild(flexbox, "div", {'class': 'mainMenuButton orange', 'onmousedown':'ShareButtonPressed()'});
            AddElementAsChild(shareButton, "span", {}).innerHTML = 'Share';
            AddElementAsChild(shareButton, "img", {'src':'icons/share.png'});
        } else {
            document.querySelector(".floatingCircle").classList.remove("active");

            document.querySelector("#mainPlayButton img").setAttribute('src', 'icons/play.png');

            if (timer > 0) {
                //In Progress
                AddElementAsChild(menu, "div", {'class': 'progressNotifier in-progress'}).innerHTML = 'Puzzle in progress...';
                document.querySelector("#mainPlayButton span").innerHTML = "Resume";
            } else {
                //Not started
                AddElementAsChild(menu, "div", {'class': 'progressNotifier unsolved'}).innerHTML = 'Fresh puzzling awaits!';
                document.querySelector("#mainPlayButton span").innerHTML = "Play";
            }
        }
    }
}