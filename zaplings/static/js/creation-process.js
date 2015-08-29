$(document).ready(function(){
	var slick = $('.single-item').slick({
        arrows: false,
        appendArrows: $('#process-arrows')
	});
    
    $('.process-next').on('click', function () {
        slick.slickNext();
    });
    $('.process-prev').on('click', function () {
        slick.slickPrev();
    });
});