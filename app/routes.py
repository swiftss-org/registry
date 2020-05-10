import datetime
import logging

from flask import current_app as application
from flask import request, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import db, login, initalise, constants
from app.route_helper.event_helper import populate_mesh_hernia_repair_choices, copy_to_mesh_hermia_repair, \
    population_followup_choices, copy_to_followup
from app.route_helper.choices import id_choices
from app.forms import LoginForm, PatientSearchForm, PatientEditForm, UserEditForm, InguinalMeshHerniaRepairForm, \
    FollowupForm
from app.models import User, Patient, Event, Center, InguinalMeshHerniaRepair, Followup
from app.route_helper.patient_helper import _copy_to_patient
from app.util import restful
from app.util.filter import like_all


@application.before_first_request
def before_first_request():
    initalise.initalise(application)


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
    return render_template('index.html', title='Index')


@application.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if application.config.get('DEFAULT_TEST_ACCOUNT_LOGIN'):
        form.username.data = constants.TEST_ACCOUNT_EMAIL
        form.password.data = constants.TEST_ACCOUNT_PASSWORD

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
        f = like_all({
            Patient.name: form.name.data,
            Patient.national_id: form.national_id.data,
            Patient.birth_year: form.birth_year.data,
            Patient.gender: form.gender.data,
            Patient.phone: form.phone.data,
            Patient.address: form.address.data,
        })

        if form.center_id.data != '':
            f.append(Patient.center_id == form.center_id.data)

        patients = db.session.query(Patient).filter(f).order_by(Patient.name).all()
        return render_template('patient_search.html', title='Patient Search', form=form, results=patients)
    else:
        form.center_id.data = str(current_user.center.id)

    return render_template('patient_search.html', title='Patient Search', form=form, results=[])


@application.route('/patient/create', methods=['GET', 'POST'])
@login_required
def patient_create():
    patient = Patient()
    events = db.session.query(Event).filter(Event.patient_id == patient.id).all()

    form = PatientEditForm(obj=patient)
    form.center_id.choices = id_choices(db.session, Center, include_empty=True)

    if form.validate_on_submit():
        _copy_to_patient(form, patient)
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

    return render_template('patient.html', title='New Patient Details', form=form, events=events)


@application.route('/patient/<int:id>', methods=['GET', 'POST'])
@login_required
def patient(id):
    patient = db.session.query(Patient).filter(Patient.id == id).first()
    if patient is None:
        return error('Unable to find patient with id {}.'.format(id))

    events = db.session.query(Event).filter(Event.patient_id == patient.id).all()

    form = PatientEditForm(obj=patient)
    form.center_id.choices = id_choices(db.session, Center, include_empty=True)

    if form.validate_on_submit():
        _copy_to_patient(form, patient)
        patient.updated_by = current_user

        db.session.commit()
        flash('Patient details for {} have been updated.'.format(patient.name))
        return redirect(url_for('patient', id=patient.id))
    else:
        form.age.data = datetime.date.today().year - patient.birth_year
        form.center_id.data = str(current_user.center.id)

    return render_template('patient.html', title='Patient Details for {}'.format(patient.name), form=form, events=events)


@application.route('/event/<int:id>', methods=['GET', 'POST'])
@login_required
def event(id):
    event = db.session.query(Event).filter(Event.id == id).first()
    if event is None:
        return error("Couldn't find an event with id {}".format(str(id)))

    if event.type == InguinalMeshHerniaRepair.__mapper_args__['polymorphic_identity']:
        return redirect(url_for('hernia_repair', id=event.id))
    elif event.type == Followup.__mapper_args__['polymorphic_identity']:
        return redirect(url_for('followup', id=event.id))

    return error("Don't know how to show an event of type {}".format(event.type))


@application.route('/event/followup/<int:id>', methods=['GET', 'POST'])
@login_required
def followup(id):
    _event = db.session.query(Followup).filter(Followup.id == id).first()

    form = FollowupForm(obj=_event)
    population_followup_choices(db.session, form)

    if form.validate_on_submit():
        copy_to_followup(_event, form)
        _event.updated_by = current_user

        db.session.commit()
        flash('Follow-up details for {} have been updated.'.format(_event.patient.name))

        return redirect(url_for('followup', id=_event.id))

    return render_template('followup.html', title='Follow-Up', form=form)


@application.route('/event/followup/create', methods=['GET', 'POST'])
@login_required
def followup_create():
    _event = Followup()

    form = FollowupForm(obj=_event)
    population_followup_choices(db.session, form)

    if form.validate_on_submit():
        copy_to_followup(_event, form)

        _event.created_by = current_user
        _event.updated_by = current_user

        db.session.add(_event)
        db.session.commit()
        flash('New follow-up details for {} have been recorded.'.format(_event.patient.name))

        return redirect(url_for('followup', id=_event.id))

    return render_template('followup.html', title='Follow-Up', form=form)


@application.route('/event/hernia_repair/<int:id>', methods=['GET', 'POST'])
@login_required
def hernia_repair(id):
    _inguinal_mesh_hernia_repair = db.session.query(InguinalMeshHerniaRepair).filter(
        InguinalMeshHerniaRepair.id == id).first()

    form = InguinalMeshHerniaRepairForm(obj=_inguinal_mesh_hernia_repair)
    populate_mesh_hernia_repair_choices(db.session, form)

    if form.validate_on_submit():
        copy_to_mesh_hermia_repair(_inguinal_mesh_hernia_repair, form)
        _inguinal_mesh_hernia_repair.updated_by = current_user

        db.session.commit()
        flash('New inguinal mesh hernia surgery details for {} have been updated.'.format(
            _inguinal_mesh_hernia_repair.patient.name))

        return redirect(url_for('hernia_repair', id=_inguinal_mesh_hernia_repair.id))

    return render_template('hernia_repair.html', title='Inguinal Mesh Hernia Surgery', form=form)


@application.route('/event/hernia_repair/create', methods=['GET', 'POST'])
@login_required
def hernia_repair_create():
    _inguinal_mesh_hernia_repair = InguinalMeshHerniaRepair()

    form = InguinalMeshHerniaRepairForm(obj=_inguinal_mesh_hernia_repair)
    populate_mesh_hernia_repair_choices(db.session, form)

    if form.validate_on_submit():
        copy_to_mesh_hermia_repair(_inguinal_mesh_hernia_repair, form)

        _inguinal_mesh_hernia_repair.created_by = current_user
        _inguinal_mesh_hernia_repair.updated_by = current_user

        db.session.add(_inguinal_mesh_hernia_repair)
        db.session.commit()
        flash('New inguinal mesh hernia surgery details for {} have been recorded.'.format(
            _inguinal_mesh_hernia_repair.patient.name))

        return redirect(url_for('hernia_repair', id=_inguinal_mesh_hernia_repair.id))

    return render_template('inguinal_mesh_hernia_repair.html', title='Record New Inguinal Mesh Hernia Surgery',
                           form=form)


@application.route('/prefetch/patients', methods=['GET'])
def patients_prefetch():
    return restful.json_dumps(db.session.query(Patient.name).all())


@application.route('/prefetch/centers', methods=['GET'])
def centers_prefetch():
    return restful.json_dumps(db.session.query(Center.name).all())


def _field_errors(form):
    errors = []
    for field in form:
        for error in field.errors:
            errors.append((field.name, error))

    return errors
