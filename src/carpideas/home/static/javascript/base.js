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

  