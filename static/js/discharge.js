document.addEventListener("DOMContentLoaded", function (event) {
    toggle_btns("#perioperative_complication", "#perioperative_complication_yes_btn", "#perioperative_complication_no_btn")
    show_hide('#perioperative_complication', '#perioperative_complication_comments_fieldset', is_true, 'toggle');

    toggle_btns("#post_operative_antibiotics", "#post_operative_antibiotics_yes_btn", "#post_operative_antibiotics_no_btn")
    show_hide('#post_operative_antibiotics', '#post_operative_antibiotics_comments_fieldset', is_true, 'toggle');
});
