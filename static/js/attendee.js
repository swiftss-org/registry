document.getElementById("submit").addEventListener("click", function () {
    document.getElementById("attendees").value = attendeeTableToJSON()
});

function addAttendee() {
    attendee_text = $("#attendee_id :selected").text();
    attendee_id = $("#attendee_id :selected").val();

    if ($("#attendee_row_" + attendee_id).length > 0) {
        /* Item already added so do nothing */
        return
    }

    html_row = `
            <tr id=attendee_row_` + attendee_id + `>
                <td>
                    <button type="button" class="btn btn-danger" onclick="removeAttendee(` + attendee_id + `)">X</button>
                </td>
                <td style="display:none;">` + attendee_id + `</td>
                <td>` + attendee_text + `</td>
                <td><input id="attendee_comments_` + attendee_id + `" class="form-control" type="text" placeholder=""></td>
            </tr>`

    $('#attendee_table tr:last').after(html_row);
}

function removeAttendee(attendee_id) {
    attendee_row_id = 'attendee_row_' + attendee_id
    $('#' + attendee_row_id).remove();
}

function attendeeTableToJSON() {
    var table = $('#attendee_table').tableToJSON(); // Convert the table into a javascript object
    console.log(table)
    var json = JSON.stringify(table);
    return json
}
