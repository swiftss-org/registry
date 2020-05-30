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

function is_checked(element)
{
    return element.prop('checked')
}

function show_hide(element_to_bind, element_to_show, show_func)
{
    f = function() {
        if(show_func($(element_to_bind)))
        {
            $(element_to_show).show();
        }
        else
        {
            $(element_to_show).hide();
        }
    };

    $(element_to_bind).bind('change', f);
    f();
}