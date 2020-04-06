var style_cookie_name = "style";

function setDarkTheme() {
  document.getElementById('theme').href = "css/style.css";
  document.getElementById('light-theme-button').style="display:block";
  document.getElementById('dark-theme-button').style="display:none";
  setStyleCookie("dark");
}

function setLightTheme() {
  document.getElementById('theme').href = "css/lightstyle.css";
  document.getElementById('dark-theme-button').style="display:block";
  document.getElementById('light-theme-button').style="display:none";
  setStyleCookie("light");
}

function setStyleFromCookie() {
  var cookies = document.cookie;
  if (cookies.length == 0) return;
  var array = cookies.split('; ');
  for (i = 0 ; i < array.length ; i++)
  {
    var matches = array[i].match(style_cookie_name+'=.*');
    if (matches == null) return;
    var value_index = matches[0].indexOf('=');
    if (value_index == -1) return;
    var value = matches[0].substr(value_index+1);
    if (value.localeCompare("light") == 0)
	  setLightTheme();
  }
}

function setStyleCookie(style_name) {
  document.cookie = style_cookie_name+'='+style_name;
}
