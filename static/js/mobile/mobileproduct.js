var alert_ative = false;
$(document).ready(function () {
	$('.collect-btn').click(function() {
		$("html,body").animate({scrollTop:0},500);
		$('.alert_collect').fadeIn(600);
		$('.fade-area').fadeTo(500, 0.6);
	});
	$('.close').click(function() {
		$('.alert_collect').fadeOut(600);
		$('.fade-area').fadeTo(500, 0);
	});
});