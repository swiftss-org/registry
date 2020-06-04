from datetime import date

from wtforms import ValidationError

from app.models import Pain
from app.util.strtobool import strtobool_optional


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


def validate_perioperative_complication(form, field):
    if strtobool_optional(form.perioperative_complication.data):
        _validate_comments(field.data,
                           'Comments must be provided when a perioperative complication is recorded.')


def validate_post_operative_antibiotics(form, field):
    if strtobool_optional(form.post_operative_antibiotics.data):
        _validate_comments(field.data,
                           'Comments must be provided when post-operative antibiotics are recorded.')


def validate_antibiotics_iv_days(form, field):
    if strtobool_optional(form.post_operative_antibiotics.data):
        if not form.post_operative_antibiotics_iv_days.data:
            raise ValidationError('No. days must be provided when post-operative antibiotics are recorded.')

        if form.post_operative_antibiotics_iv_days.data < 0:
            raise ValidationError('No. days cannot be negative.')

        if form.post_operative_antibiotics_iv_days.data and form.post_operative_antibiotics_oral_days.data:
            if form.post_operative_antibiotics_iv_days.data + form.post_operative_antibiotics_oral_days.data == 0:
                raise ValidationError('Total no. days cannot be zero when post-operative antibiotics are recorded.')


def validate_antibiotics_oral_days(form, field):
    if strtobool_optional(form.post_operative_antibiotics.data):
        if not form.post_operative_antibiotics_oral_days.data:
            raise ValidationError('No. days must be provided when post-operative antibiotics are recorded.')

        if form.post_operative_antibiotics_oral_days.data < 0:
            raise ValidationError('No. days cannot be negative.')

        if form.post_operative_antibiotics_iv_days.data and form.post_operative_antibiotics_oral_days.data:
            if form.post_operative_antibiotics_iv_days.data + form.post_operative_antibiotics_oral_days.data == 0:
                raise ValidationError('Total no. days cannot be zero when post-operative antibiotics are recorded.')


def validate_dob(form, field):
    if field.data:
        if field.data > date.today():
            raise ValidationError('Date of birth must be in the past')
        elif (date.today().year - field.year) > 150:
            raise ValidationError('Date of birth cannot be {} years ago'.format(date.today().year - field.year))


def _validate_comments(comment, err):
    if comment is None or len(comment) == 0:
        raise ValidationError(err)
