document.addEventListener("DOMContentLoaded", function (event) {
    date_controls = $("input[id$='date']")
    for (i = 0; i < date_controls.length; i++) {
        $('#' + date_controls[i].id).datepicker({
            format: "yyyy-mm-dd",
            todayHighlight: true,
            autoclose: true,
        });
    }

    $('#spinner').hide();
});

function is_checked(element) {
    return element.prop('checked');
}

function is_true(element) {
    return element.val() == 'True';
}

function show_hide(element_to_bind, element_to_show, show_func, bind_on) {
    f = function () {
        if (show_func($(element_to_bind))) {
            $(element_to_show).show();
        } else {
            $(element_to_show).hide();
        }
    };

    $(element_to_bind).bind(bind_on, f);
    f();
}

function toggle_btns(state_element_id, yes_btn_id, no_btn_id) {
    on_class = "btn-primary"
    off_class = "btn-light"
    initial_class = "btn-light"

    f_no = function () {
            $(state_element_id).val('False');
            $(state_element_id).trigger("toggle");
            toggle_class(yes_btn_id, off_class, on_class, initial_class);
            toggle_class(no_btn_id, on_class, off_class, initial_class);
    };

    f_yes = function() {
            $(state_element_id).val('True');
            $(state_element_id).trigger("toggle");
            toggle_class(yes_btn_id, on_class, off_class, initial_class);
            toggle_class(no_btn_id, off_class, on_class, initial_class);
    };

    if ($(state_element_id).val() == 'True') {
        toggle_class(yes_btn_id, on_class, null, null);
        toggle_class(no_btn_id, off_class, null, null);
    } else if ($(state_element_id).val() == 'False') {
        toggle_class(yes_btn_id, off_class, null, null);
        toggle_class(no_btn_id, on_class, null, null);
    } else {
        toggle_class(yes_btn_id, initial_class, null, null);
        toggle_class(no_btn_id, initial_class, null, null);
    }

    $(yes_btn_id).bind('click', f_yes);
    $(no_btn_id).bind('click', f_no);
}

function toggle_class(element_id, new_class, old_class, initial_class) {
    if ($(element_id).hasClass(initial_class)) {
        $(element_id).removeClass(initial_class)
    }

    if ($(element_id).hasClass(old_class)) {
        $(element_id).removeClass(old_class)
    }

    $(element_id).addClass(new_class)
}