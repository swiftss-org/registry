from datetime import date

from wtforms import ValidationError

from app.models import Pain


def validate_pain_comments(form, field):
    if form.pain.data != Pain.No_Pain:
        if field.data is None or len(field.data) == 0:
            raise ValidationError('Comments must be provided when a pain is recorded')


def validate_aware_of_mesh(form, field):
    if form.mesh_awareness.data:
        _validate_comments(field.data,
                           'Comments must be provided when mesh awareness is recorded.')


def validate_infection(form, field):
    if form.infection.data:
        _validate_comments(field.data,
                           'Comments must be provided when infection is recorded.')


def validate_seroma(form, field):
    if form.seroma.data:
        _validate_comments(field.data,
                           'Comments must be provided when seroma is recorded.')


def validate_numbness(form, field):
    if form.numbness.data:
        _validate_comments(field.data,
                           'Comments must be provided when numbness is recorded.')


def validate_dob(form, field):
    if field.data:
        if field.data > date.today():
            raise ValidationError('Date of birth must be in the past')
        elif (date.today().year - field.year) > 150:
            raise ValidationError('Date of birth cannot be {} years ago'.format(date.today().year - field.year))


def _validate_comments(comment, err):
    if comment is None or len(comment) == 0:
        raise ValidationError(err)
