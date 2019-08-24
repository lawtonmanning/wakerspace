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
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    rfid = db.Column(db.Integer, nullable=True, unique=True, default=None)
    classification = db.Column(db.Enum(Classification), nullable=False)
    year = db.Column(db.Enum(Year), nullable=True)
    staff = db.relationship('Staff', back_populates='maker', uselist=False)



    def __repr__(self):
        return '<Maker id={:08d} first={} last={}></Maker>'.format(self.id, self.first_name, self.last_name)

    def role(self):
        if self.staff is not None:
            return 'Staff'
        return 'Maker'



class Staff(db.Model):
    __tablename__ = 'staff'
    maker_id = db.Column(db.Integer, db.ForeignKey('maker.id'), primary_key=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    maker = db.relationship('Maker', back_populates='staff')


class Visit(db.Model):
    maker_id = db.Column(db.Integer, db.ForeignKey('maker.id'), primary_key=True)
    in_time = db.Column(db.DateTime, primary_key=True)
    out_time = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Visit maker={:08d} in={} out={}></Maker>'.format(self.maker_id, self.in_time, self.out_time)


class Training(db.Model):
    maker_id = db.Column(db.Integer, db.ForeignKey('maker.id'), primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), primary_key=True)
    date = db.Column(db.Date, nullable=False)


class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(50), nullable=False, unique=True)
    room = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    color = db.Column(db.String(6), nullable=False, unique=True)


