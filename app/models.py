import enum
from datetime import datetime, date

from flask_login import UserMixin
from password_strength import PasswordStats
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Enum, Boolean, event, func, and_
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from application import db

SHORT_TEXT_LENGTH = 60
LONG_TEXT_LENGTH = 240


class ExtendedBase:
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def from_dict(self, d):
        for k, v in d.items():
            setattr(self, k, v)


class Cepod(enum.Enum):
    Planned = 1
    Emergency = 2


class Side(enum.Enum):
    Left = 1
    Right = 2


class Occurrence(enum.Enum):
    Primary = 1
    Recurrent = 2
    ReRecurrent = 3


class InguinalHerniaType(enum.Enum):
    Direct = 1
    Indirect = 2
    # A pantaloon hernia (dual hernia, Romberg hernia or saddle bag hernia) is defined as ipsilateral,
    # concurrent direct and indirect inguinal hernias.
    Pantaloon = 3


class Complexity(enum.Enum):
    Simple = 1
    Sliding = 2
    Complicated = 3


class Size(enum.Enum):
    Small = 1
    Medium = 2
    Large = 3
    Massive = 4


class Pain(enum.Enum):
    No_Pain = 1
    Minimal = 2
    Mild = 3
    Moderate = 4
    Severe = 5


class DrugType(enum.Enum):
    Anesthetic = 1
    Antibiotic = 2


class AnestheticType(enum.Enum):
    Spinal = 1
    GA_Ketamine = 2
    GA_With_Intubation = 3
    Local = 4
    Other = 5


# This is necessary so that the Custom JSONEncoder/Decoder in restful.py can know which enums to
# encode or decode.
#
KNOWN_ENUMS = {
    'Cepod': Cepod,
    'Side': Side,
    'Occurrence': Occurrence,
    'Type': InguinalHerniaType,
    'Complexity': Complexity,
    'Size': Size,
    'Pain': Pain,
    'DrugType': DrugType,
    'AnestheticType': AnestheticType,
}


class Center(db.Model, ExtendedBase):
    __tablename__ = 'Centers'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    version_id = Column(Integer, nullable=False)
    name = Column(String(SHORT_TEXT_LENGTH), nullable=False, unique=True)
    address = Column(String(LONG_TEXT_LENGTH), nullable=True)

    __mapper_args__ = {
        "version_id_col": version_id
    }

    def __repr__(self):
        return "{}: [id='{}', name='{}', ...]".format(self.__tablename__, self.id, self.name)


class User(db.Model, ExtendedBase, UserMixin):
    __tablename__ = 'Users'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    version_id = Column(Integer, nullable=False)
    name = Column(String(SHORT_TEXT_LENGTH), unique=True, nullable=False)
    email = Column(String(SHORT_TEXT_LENGTH), unique=True, nullable=False)

    center_id = Column(ForeignKey('Centers.id'), nullable=True)
    center = relationship(Center)

    active = Column(Boolean, nullable=False, default=True)
    password_hash = Column(String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def check_password_strength(password):
        return PasswordStats(password).strength()

    __mapper_args__ = {
        "version_id_col": version_id
    }

    def __repr__(self):
        return self.name


class Patient(db.Model, ExtendedBase):
    __tablename__ = 'Patients'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    version_id = Column(Integer, nullable=False)
    name = Column(String(SHORT_TEXT_LENGTH), nullable=False)
    gender = Column(String(1), nullable=False)
    dob = Column(Date(), nullable=True)
    dob_year_only = Column(Boolean(), nullable=True)
    phone_1 = Column(String(20), nullable=True)
    phone_1_comments = Column(String(SHORT_TEXT_LENGTH), nullable=True)
    phone_2 = Column(String(20), nullable=True)
    phone_2_comments = Column(String(SHORT_TEXT_LENGTH), nullable=True)
    hospital_number = Column(String(SHORT_TEXT_LENGTH), nullable=True)
    national_id = Column(String(SHORT_TEXT_LENGTH), nullable=True)
    address = Column(String(LONG_TEXT_LENGTH), nullable=True)

    center_id = Column(ForeignKey('Centers.id'), nullable=False)
    center = relationship(Center)

    created_at = Column('created_at', DateTime(), default=datetime.now, nullable=False)
    created_by_id = Column(ForeignKey('Users.id'), nullable=False)
    created_by = relationship(User, foreign_keys=[created_by_id])

    updated_at = Column('updated_at', DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)
    updated_by_id = Column(ForeignKey('Users.id'), nullable=False)
    updated_by = relationship(User, foreign_keys=[updated_by_id])

    @property
    def birth_year(self):
        if self.dob:
            return self.dob.year

        return None

    @birth_year.setter
    def birth_year(self, year):
        self.dob_year_only = True
        self.dob = date(year, 1, 1)

    __mapper_args__ = {
        "version_id_col": version_id
    }

    def __repr__(self):
        return self.name


class MeshType(db.Model, ExtendedBase):
    __tablename__ = 'MeshTypes'

    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    version_id = Column(Integer, nullable=False)
    name = Column('name', String(SHORT_TEXT_LENGTH), nullable=False, unique=True)

    __mapper_args__ = {
        "version_id_col": version_id
    }

    def __repr__(self):
        return "{}: [id='{}', name='{}']".format(self.__tablename__, self.id, self.name)


class Drug(db.Model, ExtendedBase):
    __tablename__ = 'Drugs'

    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    version_id = Column(Integer, nullable=False)
    name = Column('name', String(SHORT_TEXT_LENGTH), nullable=False, unique=True)
    type = Column(Enum(DrugType), nullable=False)

    __mapper_args__ = {
        "version_id_col": version_id
    }

    def __repr__(self):
        return "{}: [id='{}', name='{}', type='{}']".format(self.__tablename__, self.id, self.name, self.type)


class DrugEventAssociation(db.Model, ExtendedBase):
    __tablename__ = 'DrugEvents'

    event_id = Column(Integer, ForeignKey('Events.id'), primary_key=True)
    drug_id = Column(Integer, ForeignKey('Drugs.id'), primary_key=True)

    drug = relationship("Drug")


class Event(db.Model, ExtendedBase):
    __tablename__ = 'Events'

    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    version_id = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    date = Column(Date, nullable=False, default=datetime.today())

    patient_id = Column(ForeignKey('Patients.id'), nullable=False)
    patient = relationship(Patient)

    center_id = Column(ForeignKey('Centers.id'), nullable=False)
    center = relationship(Center)

    comments = Column(String(LONG_TEXT_LENGTH), nullable=False, default='none')

    created_at = Column('created_at', DateTime(), default=datetime.now, nullable=False)
    created_by_id = Column(ForeignKey('Users.id'), nullable=False)
    created_by = relationship(User, foreign_keys=[created_by_id])

    updated_at = Column('updated_at', DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)
    updated_by_id = Column(ForeignKey('Users.id'), nullable=False)
    updated_by = relationship(User, foreign_keys=[updated_by_id])

    requires_discharge = False

    __mapper_args__ = {
        'version_id_col': version_id,
        'polymorphic_on': type,
    }

    def __repr__(self):
        return "{}: [id='{}', type='{}', date='{}', patient='{}', center='{}']".format(self.__tablename__,
                                                                                       self.id,
                                                                                       self.type,
                                                                                       self.date.isoformat(),
                                                                                       self.patient_id,
                                                                                       self.center_id)


class InguinalMeshHerniaRepair(Event):
    __tablename__ = 'MeshHerniaRepairs'

    id = Column(Integer, ForeignKey('Events.id'), primary_key=True)

    cepod = Column(Enum(Cepod), nullable=False)
    side = Column(Enum(Side), nullable=False)
    occurrence = Column(Enum(Occurrence), nullable=False)
    hernia_type = Column(Enum(InguinalHerniaType), nullable=False)
    complexity = Column(Enum(Complexity), nullable=False)
    mesh_type = Column(String(SHORT_TEXT_LENGTH), nullable=False)
    antibiotics = relationship("DrugEventAssociation")
    anaesthetic_type = Column(Enum(AnestheticType), nullable=False)
    anaesthetic_other = Column(String(SHORT_TEXT_LENGTH), nullable=False)
    diathermy_used = Column(Boolean, nullable=True)
    discharge_date = Column(Date, nullable=True)

    primary_surgeon_id = Column(ForeignKey('Users.id'), primary_key=True, nullable=True)
    primary_surgeon = relationship(User, foreign_keys=[primary_surgeon_id])

    secondary_surgeon_id = Column(ForeignKey('Users.id'), primary_key=True, nullable=True)
    secondary_surgeon = relationship(User, foreign_keys=[secondary_surgeon_id])

    tertiary_surgeon_id = Column(ForeignKey('Users.id'), primary_key=True, nullable=True)
    tertiary_surgeon = relationship(User, foreign_keys=[tertiary_surgeon_id])

    additional_procedure = Column(String(LONG_TEXT_LENGTH), nullable=True)
    complications = Column(String(LONG_TEXT_LENGTH), nullable=True)

    requires_discharge = True
    INGUINAL_MESH_HERNIA_REPAIR = 'Inguinal Mesh Hernia Repair'

    __mapper_args__ = {
        'polymorphic_identity': 'Mesh Hernia Repair',
    }


class Followup(Event):
    __tablename__ = 'Followups'

    id = Column(Integer, ForeignKey('Events.id'), primary_key=True)

    attendee_id = Column(ForeignKey('Users.id'), nullable=True)
    attendee = relationship(User)

    pain = Column(Enum(Pain), default=Pain.No_Pain, nullable=False)
    pain_comments = Column(String(LONG_TEXT_LENGTH), nullable=True)

    mesh_awareness = Column(Boolean, nullable=True)
    mesh_awareness_comments = Column(String(LONG_TEXT_LENGTH), nullable=True)

    infection = Column(Boolean, nullable=True)
    infection_comments = Column(String(LONG_TEXT_LENGTH), nullable=True)

    seroma = Column(Boolean, nullable=True)
    seroma_comments = Column(String(LONG_TEXT_LENGTH), nullable=True)

    numbness = Column(Boolean, nullable=True)
    numbness_comments = Column(String(LONG_TEXT_LENGTH), nullable=True)

    FOLLOWUP = "Follow-Up"
    __mapper_args__ = {
        'polymorphic_identity': FOLLOWUP,
    }


class Discharge(Event):
    __tablename__ = 'Discharges'

    id = Column(Integer, ForeignKey('Events.id'), primary_key=True)

    perioperative_complication = Column(Boolean, nullable=True)
    perioperative_complication_comments = Column(String(LONG_TEXT_LENGTH), nullable=True)

    post_operative_antibiotics = Column(Boolean, nullable=True)
    post_operative_antibiotics_comments = Column(String(LONG_TEXT_LENGTH), nullable=True)
    post_operative_antibiotics_iv_days = Column(Integer, nullable=True)
    post_operative_antibiotics_oral_days = Column(Integer, nullable=True)

    DISCHARGE = 'Discharge'
    __mapper_args__ = {
        'polymorphic_identity': DISCHARGE,
    }


class PatientDischargeTracker(db.Model, ExtendedBase):
    __tablename__ = 'PatientDischargeTracker'

    patient_id = Column(ForeignKey('Patients.id'), primary_key=True)
    patient = relationship(Patient)

    event_date = Column(Date, nullable=False)


@event.listens_for(db.session, 'before_flush')
def receive_before_flush(session, flush_context, instances):
    for o in session.new:
        _before_flush(session, o)

    for o in session.dirty:
        _before_flush(session, o)


def _before_flush(session, instance):
    if isinstance(instance, Discharge):
        track = session.query(PatientDischargeTracker).filter(
            PatientDischargeTracker.patient_id == instance.patient_id).first()

        # If patient is tracked and event date is prior to the discharge then stop tracking
        if track and track.event_date <= instance.date:
            session.delete(track)

        if not track:
            last_event_date = session.query(Event.date, func.max(Event.date)).filter(
                and_(Event.type.in_(InguinalMeshHerniaRepair.INGUINAL_MESH_HERNIA_REPAIR),
                     Event.patient_id == instance.patient_id)).scalar()

            # If patient is not tracked BUT there is an trackable event after the discharge date then start tracking
            if last_event_date and last_event_date > instance.date:
                track = PatientDischargeTracker()
                track.patient_id = instance.patient_id
                track.event_date = instance.date
                session.add(track)
    elif isinstance(instance, Event):
        last_discharge_date = session.query(Discharge.date, func.max(Discharge.date)).filter(
            Discharge.patient_id == instance.patient_id).scalar()

        track = session.query(PatientDischargeTracker).filter(
            PatientDischargeTracker.patient_id == instance.patient_id).first()

        if not last_discharge_date or last_discharge_date < instance.date:
            if track:
                track.event_date = max(instance.date, track.event_date)
                session.add(track)
            else:
                track = PatientDischargeTracker()
                track.patient_id = instance.patient_id
                track.event_date = instance.date
                session.add(track)
