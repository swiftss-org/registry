document.addEventListener("DOMContentLoaded", function(event) {
  $('#date').datepicker({
    format: "yyyy-mm-dd",
    todayHighlight: true,
    autoclose: true,
  });
});

function submit_and_record_surgery()
{
    $("#next_action").val("RecordSurgery")
    $(this).closest('form').submit();
}