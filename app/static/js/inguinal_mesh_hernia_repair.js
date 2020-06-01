document.addEventListener("DOMContentLoaded", function(event)
{
    show_hide('#anaesthetic_type', '#anaesthetic_other_fieldset', function(element)
    {
        return element.val() == 'AnestheticType.Other';
    });
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