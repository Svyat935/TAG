$( document ).ready(function() {
    // setTimeout(() => {}, 5000)
    $('.down-messages').bind('animationend webkitAnimationEnd oAnimationEnd MSAnimationEnd', function(e) { $(this).remove(); });
});