from enum import Enum
from wakerspace import db

class FormEnum(Enum):
    @classmethod
    def choices(cls):
        return [(choice.value, choice.name) for choice in cls]

    @classmethod
    def coerce(cls, item):
        return cls(item) if not isinstance(item, cls) else item



class Maker(db.Model):
    __tablename__ = 'maker'

    class Classification(FormEnum):
        STUDENT = 'STUDENT'
        FACULTY = 'FACULTY'
        STAFF = 'STAFF'
        RESEARCHER = 'RESEARCHER'

    class Year(FormEnum):
        FRESHMAN = 'FRESHMAN'
        SOPHOMORE = 'SOPHOMORE'
        JUNIOR = 'JUNIOR'
        SENIOR = 'SENIOR'
        GRADUATE = 'GRADUATE'

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    rfid = db.Column(db.Integer, nullable=True, unique=True, default=None)
    classification = db.Column(db.Enum(Classification), nullable=False)
    year = db.Column(db.Enum(Year), nullable=True)
    staff = db.Column(db.Boolean, nullable=False, default=False)
    trainings = db.relationship('Training', cascade='save-update, merge, delete, delete-orphan')
    visits = db.relationship('Visit', cascade='save-update, merge, delete, delete-orphan')



    def __repr__(self):
        return '{} {} ({:08d})'.format(self.first_name, self.last_name, self.id)

    def role(self):
        if self.staff:
            return 'Staff'
        return 'Maker'

    def status(self):
        last_visit = self.last_visit()
        if last_visit is None or last_visit.out_time is not None:
            return "OUT"
        return "IN"

    def last_visit(self):
        return Visit.query.filter_by(maker_id=self.id).order_by(Visit.in_time.desc()).first()




class Visit(db.Model):
    maker_id = db.Column(db.Integer, db.ForeignKey('maker.id'), primary_key=True)
    in_time = db.Column(db.DateTime, primary_key=True)
    out_time = db.Column(db.DateTime, nullable=True)
    purpose = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=True)

    maker = db.relationship('Maker')
    activity = db.relationship('Activity')

    def __repr__(self):
        return '{} ({}, {})'.format(self.maker, self.in_time, self.out_time)

class Training(db.Model):
    maker_id = db.Column(db.Integer, db.ForeignKey('maker.id'), primary_key=True)
    training_type_id = db.Column(db.Integer, db.ForeignKey('training_type.id'), primary_key=True)
    date = db.Column(db.Date, nullable=False)

    maker = db.relationship('Maker')
    type = db.relationship('TrainingType')

    def __repr__(self):
        return '{} - {} ({})'.format(self.maker, self.equipment, self.date)


class TrainingType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    color_id = db.Column(db.Integer, db.ForeignKey('color.id'), nullable=False, unique=True)

    activities = db.relationship('Activity')
    color = db.relationship('Color')

    def __repr__(self):
        return self.name


class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(6), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return self.name


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    training_type_id = db.Column(db.Integer, db.ForeignKey('training_type.id'), nullable=False)

    training = db.relationship('TrainingType')
    
    def __repr__(self):
        return self.name


