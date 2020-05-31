document.addEventListener("DOMContentLoaded", function(event) {
    show_hide('#pain', '#pain_comments_fieldset', function(element)
    {
        return element.val() != 'Pain.No_Pain';
    });
    show_hide('#mesh_awareness', '#mesh_awareness_comments_fieldset', is_checked);
    show_hide('#infection', '#infection_comments_fieldset', is_checked);
    show_hide('#seroma', '#seroma_comments_fieldset',  is_checked);
    show_hide('#numbness', '#numbness_comments_fieldset', is_checked);

    $('#date').datepicker(
    {
        format: 'yyyy-mm-dd',
        autoclose: true,
        assumeNearbyYear: true,
        endDate: '0d',
        todayHighlight: true,
        todayBtn: true
    });

    $('#spinner').hide();
});
