import json
from app.models import User, Patient, Episode, Hospital, EpisodeAttendee


def from_json(json_str, episode_id):
    l = json.loads(json_str)
    return from_list(l, episode_id)


def from_list(l, episode_id):
    attendees = []
    for row in l:
        attendees.append(from_dict(row, episode_id))

    return attendees


def from_dict(dict, episode_id):
    user_id = dict.get('Id')

    if not isinstance(user_id, int):
        user_id = int(user_id)

    comments = dict.get('Comments')
    attendee = EpisodeAttendee(episode_id=episode_id, user_id=user_id, comments=comments)
    return attendee
