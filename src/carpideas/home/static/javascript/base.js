function likeButton(){ //liked button displays popup
    var popup = document.getElementById("liked");
    popup.classList.toggle("show");
}
function dislikeButton(){ //disliked button displays popup
    var popup = document.getElementById("disliked");
    popup.classList.toggle("show");
}
function refreshPage(){ //skip button refreshes page
    window.location.reload();
} 



function openForm() { //used for costumization menu
    document.getElementById("myForm").style.display = "block";
  }
  
  function closeForm() {
    document.getElementById("myForm").style.display = "none";
  }



function showclock() { //getting time for the digital clock (currently commented out so not displayed)
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
