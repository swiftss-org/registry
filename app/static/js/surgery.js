document.addEventListener("DOMContentLoaded", function(event) {
  $('#date_of_discharge').datepicker({
    format: "yyyy-mm-dd",
    todayHighlight: true,
    autoclose: true,
  });

  $('#opd_rv_date').datepicker({
    format: "yyyy-mm-dd",
    todayHighlight: true,
    autoclose: true,
  });
});



