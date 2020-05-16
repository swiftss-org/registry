document.addEventListener("DOMContentLoaded", function(event) {
    $('#spinner').hide();
});

$('#birth_year').bind('change', function() {
    $('#age').val(new Date().getFullYear() - $('#birth_year').val())
});

$('#age').bind('change', function() {
    $('#birth_year').val(new Date().getFullYear() - $('#age').val())
});

function submit_and_create_episode()
{
    $("#next_action").val("CreateEpisode")
    $(this).closest('form').submit();
}
