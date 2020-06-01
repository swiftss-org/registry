from datetime import date

from wtforms import ValidationError

from app.models import Pain


def validate_pain_comments(form, field):
    if form.pain.data != Pain.No_Pain:
        if field.data is None or len(field.data) == 0:
            raise ValidationError('Pain comments must be provided when a pain is recorded')


def validate_dob(form, field):
    if field.data:
        if field.data > date.today():
            raise ValidationError('Date of birth must be in the past')
        elif (date.today().year - field.year) > 150:
            raise ValidationError('Date of birth cannot be {} years ago'.format(date.today().year - field.year))
