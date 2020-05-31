import enum
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Enum, Boolean
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash
from password_strength import PasswordPolicy, PasswordStats

from app import db

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
    birth_year = Column(Integer(), nullable=True)
    phone = Column(String(20), nullable=True)
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


    __mapper_args__ = {
        'polymorphic_identity': 'Mesh Hernia Repair',
    }


class Followup(Event):
    __tablename__ = 'Followups'

    id = Column(Integer, ForeignKey('Events.id'), primary_key=True)

    attendee_id = Column(ForeignKey('Users.id'), primary_key=True, nullable=True)
    attendee = relationship(User)

    pain = Column(Enum(Pain), default=Pain.No_Pain, nullable=False)
    pain_comments = Column(String(LONG_TEXT_LENGTH), nullable=True)

    mesh_awareness = Column(Boolean, default=False, nullable=False)
    mesh_awareness_comments = Column(String(LONG_TEXT_LENGTH), nullable=True)

    infection = Column(Boolean, default=False, nullable=False)
    infection_comments = Column(String(LONG_TEXT_LENGTH), nullable=True)

    seroma = Column(Boolean, default=False, nullable=False)
    seroma_comments = Column(String(LONG_TEXT_LENGTH), nullable=True)

    numbness = Column(Boolean, default=False, nullable=False)
    numbness_comments = Column(String(LONG_TEXT_LENGTH), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'Follow-Up',
    }
