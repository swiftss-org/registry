document.addEventListener("DOMContentLoaded", function(event) {
  $('#spinner').hide();
});

function submit_and_create_episode()
{
    $("#next_action").val("CreateEpisode")
    $(this).closest('form').submit();
}