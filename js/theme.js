function darkTheme() {
  document.getElementById('theme').href = "css/style.css";
  document.getElementById('light-theme-button').style="display:block";
  document.getElementById('dark-theme-button').style="display:none";
}

function lightTheme() {
  document.getElementById('theme').href = "css/lightstyle.css";
  document.getElementById('dark-theme-button').style="display:block";
  document.getElementById('light-theme-button').style="display:none";
}
