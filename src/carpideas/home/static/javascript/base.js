function likeButton(){
    var popup = document.getElementById("liked");
    popup.classList.toggle("show");
}
function dislikeButton(){
    var popup = document.getElementById("disliked");
    popup.classList.toggle("show");
}
function refreshPage(){
    window.location.reload();
} 



function openForm() {
    document.getElementById("myForm").style.display = "block";
  }
  
  function closeForm() {
    document.getElementById("myForm").style.display = "none";
  }



function showclock() {
  let today = new Date();
  let hours = today.getHours();
  let mins = today.getMinutes();
  let seconds = today.getSeconds();
  const addZero = num => {
    if(num < 10) { return '0' + num };
    return num;
  }
  $('#hour').text(addZero(hours));
  $('#min').text(addZero(mins));
  $('#second').text(addZero(seconds));
}
setInterval(showclock, 1000);
