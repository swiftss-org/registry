from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, \
    HiddenField, IntegerField, RadioField, DateField
from wtforms.validators import DataRequired, Optional

from app.models import Cepod, Side, Occurrence, InguinalHerniaType, Complexity, MeshType, AnestheticType, Pain
from app.util.form_utils import choice_for_bool, coerce_for_bool, choice_for_enum, coerce_for_enum


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    center_id = SelectField('Center')


class UserCreateForm(UserForm):
    new_password = PasswordField('New Password')
    verify_password = PasswordField('Verify Password')
    submit = SubmitField('Register User')


class UserEditForm(UserForm):
    current_password = PasswordField('Current Password')
    new_password = PasswordField('New Password')
    verify_password = PasswordField('Verify Password')
    active = SelectField('Active',
                         default=True,
                         choices=choice_for_bool(),
                         coerce=coerce_for_bool())
    submit = SubmitField('Save Changes')


class PatientEditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    national_id = StringField('National Id')
    birth_year = IntegerField('Year of Birth')
    age = IntegerField('Age')
    center_id = SelectField('Center', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female')], validators=[DataRequired()])
    phone = StringField('Phone #')
    address = TextAreaField('Address (e.g. Village, District)')
    next_action = HiddenField('NextAction')
    created_by = HiddenField('Created By')
    created_at = HiddenField('Created At')
    updated_by = HiddenField('Updated By')
    updated_at = HiddenField('Updated At')
    submit = SubmitField('Save Changes')


class PatientSearchForm(FlaskForm):
    name = StringField('Name')
    national_id = StringField('National Id')
    birth_year = IntegerField('Year of Birth', validators=[Optional()])
    age = IntegerField('Age', validators=[Optional()])
    center_id = SelectField('Center')
    gender = SelectField('Gender', choices=[('', 'Any'), ('M', 'Male'), ('F', 'Female')])
    phone = StringField('Phone #')
    address = TextAreaField('Address (e.g. Village, District)')
    next_action = HiddenField('NextAction')
    created_by = HiddenField('Created By')
    created_at = HiddenField('Created At')
    updated_by = HiddenField('Updated By')
    updated_at = HiddenField('Updated At')
    submit = SubmitField('Search')


class EventForm(FlaskForm):
    id = HiddenField('id')
    version = HiddenField('version')

    type = HiddenField('Type')
    date = DateField('Date')

    patient_id = SelectField('Patient')
    center_id = SelectField('Center')
    comments = TextAreaField('Comments')

    created_by = HiddenField('Created By')
    created_at = HiddenField('Created At')
    updated_by = HiddenField('Updated By')
    updated_at = HiddenField('Updated At')
    submit = SubmitField('Save Changes')


class FollowupForm(EventForm):
    attendee_id = SelectField('Attendee', validators=[DataRequired()])

    pain = SelectField('Pain',
                       choices=choice_for_enum(Pain, include_blank=False),
                       coerce=coerce_for_enum(Pain),
                       validators=[DataRequired()])
    pain_comments = StringField('Pain Description', validators=[Optional()])

    mesh_awareness = BooleanField('Aware of Mesh?')
    mesh_awareness_comments = StringField('Mesh Awareness Description', validators=[Optional()])

    infection = BooleanField('Infection?')
    infection_comments = StringField('Infection Description', validators=[Optional()])

    seroma = BooleanField('Seroma?')
    seroma_comments = StringField('Seroma Description', validators=[Optional()])

    numbness = BooleanField('Numbness?')
    numbness_comments = StringField('Numbness Description', validators=[Optional()])


class InguinalMeshHerniaRepairForm(EventForm):
    discharge_date = StringField('Discharge Date')

    cepod = SelectField('CEPOD',
                        choices=choice_for_enum(Cepod, include_blank=False),
                        coerce=coerce_for_enum(Cepod),
                        validators=[DataRequired()])
    side = SelectField('Side',
                       choices=choice_for_enum(Side, include_blank=False),
                       coerce=coerce_for_enum(Side),
                       validators=[DataRequired()])
    occurrence = SelectField('Occurrence',
                             choices=choice_for_enum(Occurrence, include_blank=False),
                             coerce=coerce_for_enum(Occurrence),
                             validators=[DataRequired()])
    hernia_type = SelectField('Hernia Type',
                              choices=choice_for_enum(InguinalHerniaType, include_blank=False),
                              coerce=coerce_for_enum(InguinalHerniaType),
                              validators=[DataRequired()])
    complexity = SelectField('Complexity',
                             choices=choice_for_enum(Complexity, include_blank=False),
                             coerce=coerce_for_enum(Complexity),
                             validators=[DataRequired()])

    mesh_type = StringField('Mesh Type', validators=[DataRequired()])

    anaesthetic_type = SelectField('Anaesthetic Type',
                                   choices=choice_for_enum(AnestheticType, include_blank=False),
                                   coerce=coerce_for_enum(AnestheticType),
                                   validators=[DataRequired()])

    anaesthetic = StringField('Anaesthetic', validators=[DataRequired()])
    diathermy_used = BooleanField('Diathermy Used?',
                                  coerce=coerce_for_bool(),
                                  validators=[DataRequired()])

    primary_surgeon_id = SelectField('Primary Surgeon', validators=[Optional()])
    secondary_surgeon_id = SelectField('Secondary Surgeon', validators=[Optional()])
    tertiary_surgeon_id = SelectField('Tertiary Surgeon', validators=[Optional()])

    additional_procedure = TextAreaField('Additional Procedure', validators=[Optional()])
    complications = TextAreaField('Complications', validators=[Optional()])
