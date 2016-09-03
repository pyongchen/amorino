var menu_active = false;

$(document).ready(function () {
    $('.glyphicon-align-justify').click(function () {
        $('.glyphicon-align-justify').fadeOut(600);
        $('.glyphicon-remove').fadeIn(600);
        $('.mobile-menu').fadeIn(600);
    });
    $('.glyphicon-remove').click(function () {
        $('.glyphicon-remove').fadeOut(600);
        $('.glyphicon-align-justify').fadeIn(600);
        $('.mobile-menu').fadeOut(600);
    });
    setTimeout(function () {
        $('.mobile-menu-btn > div').click(function () {
            $(this).next().toggle(600);
        });
    }, 500)

});