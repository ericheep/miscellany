$(document).ready(function() {
    $('name').mouseenter(function() {
        $('name').animate({
            left: 50
        });
    });
    $('name').mouseleave(function() {
        $('name').animate({
            left: 0
        });
    });
});
