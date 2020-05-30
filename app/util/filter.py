from sqlalchemy import and_


def like_all(d):
    filter = []
    if d is not None:
        for k, v in d.items():
            if v is not None:
                s = str(v)
                if len(s) > 0:
                    filter.append(k.like('%' + s + '%'))

    return and_(*filter)
