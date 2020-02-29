from app import attendees_parser


def test_from_json():
    json = '[{"":"X","Id":"7","Name":"Thompson, Amelia","Comments":"Supervisor"},{"":"X","Id":"8","Name":"Roberts, Lily","Comments":""},{"":"X","Id":"1","Name":"Test, Account","Comments":""}]'
    attendees = attendees_parser.from_json(json, -1)

    assert len(attendees) == 3

    assert attendees[0].user_id == 7
    assert attendees[0].episode_id == -1
    assert attendees[0].comments == 'Supervisor'

    assert attendees[1].user_id == 8
    assert attendees[1].episode_id == -1
    assert attendees[1].comments == ''

    assert attendees[2].user_id == 1
    assert attendees[2].episode_id == -1
    assert attendees[2].comments == ''
