document.addEventListener("DOMContentLoaded", function(event) {
  $('#discharge_date').datepicker({
    format: "yyyy-mm-dd",
    todayHighlight: true,
    autoclose: true,
  });
});
