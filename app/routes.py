import datetime
import logging

from flask import current_app as application
from flask import request, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import initialise, constants
from app.forms import LoginForm, PatientSearchForm, PatientEditForm, UserEditForm
from app.models import User, Patient, Event, Center, PatientDischargeTracker
from app.route_helper import event_helper
from app.route_helper.choices import id_choices
from app.route_helper.patient_helper import copy_to_patient
from app.util import restful
from app.util.filter import like_all

from application import db, login

from sqlalchemy import and_, or_


if application.config.get('TESTING'):
    @application.before_first_request
    def before_first_request():
        initialise.initialise(application)


@login.user_loader
def load_user(user_id):
    if not isinstance(user_id, int):
        user_id = int(user_id)

    u = db.session.query(User).filter(User.id == user_id).first()
    return u


@application.route('/', methods=['GET'])
def root():
    return redirect(url_for('index'))


@application.route('/not_implemented', methods=['GET'])
def not_implemented():
    return render_template('not_implemented.html', title='Ooops')


@application.route('/error', methods=['GET'])
def error(e):
    return render_template('error.html', title='Ooops', e=e)


@application.route('/index', methods=['GET'])
@login_required
def index():
    results = []
    for pdt in db.session.query(PatientDischargeTracker).order_by(PatientDischargeTracker.event_date).all():
        results.append(pdt.patient)

    return render_template('index.html', title='Index', results=results)


@application.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if application.config.get('DEFAULT_TEST_ACCOUNT_LOGIN'):
        form.username.data = constants.TEST_ACCOUNT_EMAIL

    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        login_msg = 'Login successful for {}'.format(form.username.data)
        logging.info(login_msg)
        flash(login_msg)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('index'))
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@application.route('/logout')
def logout():
    logout_user()
    flash('Logout successful.')
    return redirect(url_for('index'))


@application.route('/health_check', methods=['GET'])
def health_check():
    try:
        if not application:
            raise ValueError('No application running!')

        if db.session.query(User).count() < 1:
            raise ValueError('No users defined!')

        logging.info('Health Check Passed')
        return '', 204
    except Exception as e:
        logging.error('Health Check Failed!')
        raise e


@application.route('/user/self', methods=['GET', 'POST'])
@login_required
def user_self():
    return redirect(url_for('user', id=current_user.id))


@application.route('/user/<int:id>', methods=['GET', 'POST'])
@login_required
def user(id):
    user = db.session.query(User).filter(User.id == id).first()
    form = UserEditForm(obj=user)
    form.center_id.choices = id_choices(db.session, Center, include_empty=True)

    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Unable to save changes as current password is not correct!'.format(user.name))
            return redirect(url_for('user', id=user.id))

        user.name = form.name.data
        user.email = form.email.data
        user.active = form.active.data

        if len(form.new_password.data) > 0:
            if form.new_password.data != form.verify_password.data:
                flash('Unable to save changes as passwords for not match for {}!'.format(user.name))
                return render_template('user_edit.html', title='Register New User', form=form, edit_disabled=False)

            minimum_password_strength = application.config.get('MINIMUM_PASSWORD_STRENGTH', 0.3)
            if user.check_password_strength(form.new_password.data) < minimum_password_strength:
                flash('Unable to save changes as password is not strong enough for {}!'.format(user.name))
                return render_template('user_edit.html', title='Register New User', form=form, edit_disabled=False)

            user.set_password(form.new_password.data)

        db.session.commit()

        flash('User details for {} have been updated.'.format(user.name))
        return redirect(url_for('user', id=user.id))

    return render_template('user_edit.html', title='User Details', form=form, edit_disabled=False)


@application.route('/user/create', methods=['GET', 'POST'])
def user_create():
    user = User()
    form = UserEditForm(obj=user)
    form.center_id.choices = id_choices(db.session, Center, include_empty=True)

    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.active = form.active.data

        if form.new_password.data != form.verify_password.data:
            flash('Unable to save changes as passwords for not match for {}!'.format(user.name))
            return render_template('user_create.html', title='Register New User', form=form, edit_disabled=False)

        minimum_password_strength = application.config.get('MINIMUM_PASSWORD_STRENGTH', 0.3)
        if user.check_password_strength(form.new_password.data) < minimum_password_strength:
            flash('Unable to save changes as password is not strong enough for {}!'.format(user.name))
            return render_template('user_create.html', title='Register New User', form=form, edit_disabled=False)

        user.set_password(form.new_password.data)

        db.session.add(user)
        db.session.commit()

        flash('User details for {} have been updated.'.format(user.name))
        return redirect(url_for('user', id=user.id))

    return render_template('user_create.html', title='Register New User', form=form, edit_disabled=False)


@application.route('/patient_search', methods=['GET', 'POST'])
@login_required
def patient_search():
    form = PatientSearchForm()
    form.center_id.choices = id_choices(db.session, Center, include_empty=True)

    if form.validate_on_submit():
        if form.id.data and len(form.id.data.strip()) > 0:
            return redirect(url_for('patient', id=form.id.data))

        f = like_all({
            Patient.name: form.name.data,
            Patient.national_id: form.national_id.data,
            Patient.birth_year: form.birth_year.data,
            Patient.gender: form.gender.data,
            Patient.address: form.address.data,
        })

        f = and_(f, or_(Patient.phone_1.like('%' + form.phone.data + '%'),
                    Patient.phone_2.like('%' + form.phone.data + '%'), ))

        if form.center_id.data != '':
            f = and_(f, Patient.center_id.is_(form.center_id.data))

        patients = db.session.query(Patient).filter(f).order_by(Patient.name).all()
        return render_template('patient_search.html', title='Patient Search', form=form, results=patients)
    else:
        form.center_id.data = str(current_user.center.id)

    return render_template('patient_search.html', title='Patient Search', form=form, results=[])


@application.route('/patient/create', methods=['GET', 'POST'])
@login_required
def patient_create():
    patient = Patient()
    events = db.session.query(Event).filter(Event.patient_id == patient.id).order_by(Event.date).all()

    form = PatientEditForm(obj=patient)
    form.center_id.choices = id_choices(db.session, Center, include_empty=True)

    if form.validate_on_submit():
        copy_to_patient(form, patient)
        patient.created_by = current_user
        patient.updated_by = current_user

        db.session.add(patient)
        db.session.commit()
        flash('New patient {} has been recorded.'.format(patient.name))
        return redirect(url_for('patient', id=patient.id))
    else:
        if patient.birth_year:
            form.age.data = datetime.date.today().year - patient.birth_year

        form.center_id.data = str(current_user.center.id)

    return render_template('patient.html', title='New Patient Details',
                           form=form, patient=patient, events=events, mode='create')


@application.route('/patient/<int:id>', methods=['GET', 'POST'])
@login_required
def patient(id):
    patient = db.session.query(Patient).filter(Patient.id == id).first()
    if patient is None:
        return error('Unable to find patient with id {}.'.format(id))

    events = db.session.query(Event).filter(Event.patient_id == patient.id).order_by(Event.date).all()

    form = PatientEditForm(obj=patient)
    form.center_id.choices = id_choices(db.session, Center, include_empty=True)

    if form.validate_on_submit():
        copy_to_patient(form, patient)
        patient.updated_by = current_user

        db.session.commit()
        flash('Patient details for {} have been updated.'.format(patient.name))
        return redirect(url_for('patient', id=patient.id))
    else:
        form.age.data = datetime.date.today().year - patient.birth_year
        if current_user.center:
            form.center_id.data = str(current_user.center.id)

    return render_template('patient.html', title='Patient Details for {}'.format(patient.name),
                           form=form, patient=patient, events=events, mode='load')


@application.route('/event/<int:id>', methods=['GET', 'POST'])
@login_required
def event(id):
    return _event(id, False)


@application.route('/event_inline/<int:id>', methods=['GET', 'POST'])
@login_required
def event_inline(id):
    return _event(id, True)


def _event(id, inline):
    event = db.session.query(Event).filter(Event.id == id).first()
    if event is None:
        return error('Unable to find an event with id {}.'.format(id))

    helper = event_helper.find_helper(event)
    form = helper.form(event, inline)
    helper.populate_choices(db.session, form)

    if form.validate_on_submit():
        helper.copy_to_event(form, event)
        event.updated_by = current_user

        db.session.commit()
        flash('{} details have been updated.'.format(helper.title()))
        return redirect(url_for('event', id=event.id))

    return render_template(helper.template(inline), title=helper.title(),
                           form=form, event=event, mode='load', inline=inline)


@application.route('/event/create/<string:type>', methods=['GET', 'POST'])
@login_required
def event_create(type):
    return _event_create(type, False)


@application.route('/event_inline/create/<string:type>', methods=['GET', 'POST'])
@login_required
def event_create_inline(type):
    return _event_create(type, True)


def _event_create(type, inline):
    helper = event_helper.find_helper(type)
    event = helper.event()
    form = helper.form(event, inline)
    helper.populate_choices(db.session, form)

    if form.validate_on_submit():
        helper.copy_to_event(form, event)

        event.created_by = current_user
        event.updated_by = current_user

        db.session.add(event)
        db.session.commit()
        flash('New {} has been recorded.'.format(helper.title()))
        return redirect(url_for('event', id=event.id))

    _log_errors(form)
    return render_template(helper.template(inline), title=helper.title(),
                           form=form, event=event, mode='create')


@application.route('/prefetch/patients', methods=['GET'])
def patients_prefetch():
    return restful.json_dumps(db.session.query(Patient.name).order_by(Patient.name).all())


@application.route('/prefetch/centers', methods=['GET'])
def centers_prefetch():
    return restful.json_dumps(db.session.query(Center.name).order_by(Center.name).all())


def _field_errors(form):
    errors = []
    for field in form:
        for error in field.errors:
            errors.append((field.name, error))

    return errors


def _log_errors(form):
    if form.errors:
        for field, err in form.errors.items():
            logging.warning('Error in field {}: {}'.format(field, err))
