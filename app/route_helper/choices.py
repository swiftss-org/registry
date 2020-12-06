from application import db


def id_choices(session, named_entity, include_empty=False, empty_value='(Any)'):
    return choices(session.query(named_entity).order_by(named_entity.name).all(), include_empty, empty_value)


def choices(result, include_empty=False, empty_value='(Any)'):
    response = [(str(h.id), h.name) for h in result]

    if include_empty:
        return [('', empty_value)] + response

    return response
