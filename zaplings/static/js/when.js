// when.js
// assumes jQuery is already initialized.

// if the user doesn't have JS enabled, 
// we'll show .times-specific by default
// but since we're executing JS, hide it.

$('.times-specific').hide();

// when state of specificity checkbox-button changes, change text of label and toggle the visibility of general & specific sections, 
$('#checkbox-get-more-specific').change(function() {
    ($('#checkbox-get-more-specific').prop('checked')) ? $('#label-get-more-specific').text('Get less specific') : $('#label-get-more-specific').text('Get more specific')
    $('.times-general, .times-specific').slideToggle();
});

// modify specific time checkboxes based on general checkbox-buttons
$('.times-general input:checkbox').change(function() {

    // first, figure out what times-general boxes are checked.
    // then, check times-specific boxes based on what's checked.

    // these should all be boolean true or false
    var weekdays = $('#weekdays').prop('checked');
    var weekends = $('#weekends').prop('checked');
    var mornings = $('#mornings').prop('checked');
    var afternoons = $('#afternoons').prop('checked');
    var evenings = $('#evenings').prop('checked');
    var nights = $('#nights').prop('checked');

    // uncheck all checkboxes - might be undesired behavior, if someone has already customized it and goes back...
    $('.times-specific input:checkbox').prop('checked', false);

    // if weekdays
    if (weekdays) {
        if (mornings) {
            $('.weekday.morning').prop('checked', true);
        }
        if (afternoons) {
            $('.weekday.afternoon').prop('checked', true);
        }
        if (evenings) {
            $('.weekday.evening').prop('checked', true);
        }
        if (nights) {
            $('.weekday.night').prop('checked', true);
        }
        // if only weekdays and not times of day
        if (!(mornings || afternoons || evenings || nights)) {
            $('.weekday').prop('checked', true);
        }
    }

    // if weekends
    if (weekends) {
        if (mornings) {
            $('.weekend.morning').prop('checked', true);
        }
        if (afternoons) {
            $('.weekend.afternoon').prop('checked', true);
        }
        if (evenings) {
            $('.weekend.evening').prop('checked', true);
        }
        if (nights) {
            $('.weekend.night').prop('checked', true);
        }
        // if only weekends and not times of day
        if (!(mornings || afternoons || evenings || nights)) {
            $('.weekend').prop('checked', true);
        }
    }

    // if only times of day but not weekday/end
    if ((mornings || afternoons || evenings || nights) && !(weekdays || weekends)) {
        if (mornings) {
            $('.morning').prop('checked', true);
        }
        if (afternoons) {
            $('.afternoon').prop('checked', true);
        }
        if (evenings) {
            $('.evening').prop('checked', true);
        }
        if (nights) {
            $('.night').prop('checked', true);
        }
    }

});