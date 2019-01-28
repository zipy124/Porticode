var percent = 10;
document.querySelector(".progress-bars").style.width = percent + "%";
function increase(){
  percent = percent > 90 ? 10 : percent + 10;
  document.querySelector(".progress-bars").style.width = percent + "%";
}
