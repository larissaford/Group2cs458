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