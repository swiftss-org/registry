document.addEventListener("DOMContentLoaded", function(event) {
    date_controls = $("input[id$='date']")
    for (i = 0; i < date_controls.length; i++)
    {
        $('#' + date_controls[i].id).datepicker({
            format: "yyyy-mm-dd",
            todayHighlight: true,
            autoclose: true,
      });
    }
});
