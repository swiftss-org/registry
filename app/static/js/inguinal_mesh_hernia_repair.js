document.addEventListener("DOMContentLoaded", function(event)
{
    show_hide('#anaesthetic_type', '#anaesthetic_other_fieldset', function(element)
    {
        return element.val() == 'AnestheticType.Other';
    });

    toggle_btns("#diathermy_used", "#diathermy_used_yes_btn", "#diathermy_used_no_btn")
});
