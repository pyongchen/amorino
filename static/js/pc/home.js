var homepage_current_slide = 0;
var homepage_slide_cnt = 3;

$(document).ready(function () {

	setTimeout(function () {
		homepage_slide_cnt = $(".backimg").length;
		$(".backimg").hide();
		$(".backimg:eq(0)").show();

    	$(".right-box").click(right_arrow_click);
    	$(".left-box").click(function() {
    	    $(".backimg:eq(" + homepage_current_slide + ")").fadeOut(600);
    	    homepage_current_slide --;
    	    if (homepage_current_slide < 0)
    	        homepage_current_slide = homepage_slide_cnt - 1;
    	    $(".backimg:eq(" + homepage_current_slide + ")").fadeIn(600);
    	});

    	var timer = $.timer(function() {
    	    right_arrow_click();
    	});
	    timer.set({ time : 10000, autostart : true });
	}, 500);
});

function right_arrow_click() {
    $(".backimg:eq(" + homepage_current_slide + ")").fadeOut(600);
    homepage_current_slide ++;
    if (homepage_current_slide >= homepage_slide_cnt)
        homepage_current_slide = 0;
    $(".backimg:eq(" + homepage_current_slide + ")").fadeIn(600);
    console.log(homepage_current_slide);
}
