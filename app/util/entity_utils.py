import importlib

from app.route_helper.event_helper import FollowupEventHelper, InguinalMeshHerniaRepairEventHelper


def entity_template(entity):
    return _format_name(entity.__name__, '_').lower() + '.html'


def entity_title(entity):
    return _format_name(entity.__name__, ' ')


def entity_form(entity):
    form_classname = _format_name(entity.__name__, '') + 'Form'

    clazz = getattr(importlib.import_module("app.forms"), form_classname)
    return clazz(obj=entity)



def _format_name(name, space_char):
    nice_name = ''
    for c in name:
        if c.isupper():
            nice_name += space_char
        else:
            nice_name += c

    return nice_name
