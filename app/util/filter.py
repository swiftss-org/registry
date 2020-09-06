from sqlalchemy import and_


def like_all(d):
    filter = []
    if d is not None:
        for k, v in d.items():
            like_append(filter, k, v)

    return and_(*filter)


def like_append(filter, column, value):
    if value is not None:
        s = str(value)
        if len(s) > 0:
            filter.append(column.like('%' + s + '%'))
