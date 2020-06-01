from app import strtobool


def choice_for_enum(enum, include_blank=False, blank_value='(Any)'):
    l = [(e, str(e.name).replace('_', ' ')) for e in enum]
    if include_blank:
        l.insert(0, ('', '(Any)'))
    return l


def coerce_for_enum(enum):
    def coerce(name):
        if name is None or str(name) == '':
            return None

        if isinstance(name, enum):
            return name

        try:
            name = str(name).replace(' ', '_')
            id = int(name)
            try:
                return enum(id)
            except KeyError:
                raise ValueError(name)
        except ValueError:
            try:
                if '.' in name:
                    name = name[name.find('.') + 1:]
                return enum[name]
            except KeyError:
                raise ValueError(name)

    return coerce


def coerce_for_bool():
    def coerce(name):
        if isinstance(name, bool):
            return name

        return strtobool(name)

    return coerce



def choice_for_bool():
    return [(True, 'True'), (False, 'False')]
