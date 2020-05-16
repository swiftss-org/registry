from sqlalchemy import and_


def like_all(d):
    filter = []
    if d is not None:
        for k, v in d.items():
            if v is not None:
                if len(v) > 0:
                    filter.append(k.like('%' + str(v) + '%'))

    return and_(*filter)