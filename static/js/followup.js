document.addEventListener("DOMContentLoaded", function (event) {
    show_hide('#pain', '#pain_comments_fieldset', function (element) {
        return element.val() != 'Pain.No_Pain';
    }, 'change');

    toggle_btns("#mesh_awareness", "#mesh_awareness_yes_btn", "#mesh_awareness_no_btn")
    show_hide('#mesh_awareness', '#mesh_awareness_comments_fieldset', is_true, 'toggle');

    toggle_btns("#infection", "#infection_yes_btn", "#infection_no_btn")
    show_hide('#infection', '#infection_comments_fieldset', is_true, 'toggle');

    toggle_btns("#seroma", "#seroma_yes_btn", "#seroma_no_btn")
    show_hide('#seroma', '#seroma_comments_fieldset', is_true, 'toggle');

    toggle_btns("#numbness", "#numbness_yes_btn", "#numbness_no_btn")
    show_hide('#numbness', '#numbness_comments_fieldset', is_true, 'toggle');
});
