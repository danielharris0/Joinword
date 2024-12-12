if (!CookieExists('hasBeenToldAboutCookies')) {
  picoModal("Hello! There are cookies involved. However, they are essential and as such I don't think I need permission.").show();
  SetCookie('hasBeenToldAboutCookies');
}

SceneManager.DailyPuzzle();