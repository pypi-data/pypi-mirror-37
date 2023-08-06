from flask import Flask
from marshmallow import Schema, fields
from sqlalchemy.types import PickleType
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
mam = Marshmallow()

class Profile(db.Model):

    __tablename__ = 'profile'
    job = db.Column(db.String(250))
    company = db.Column(db.String(250))
    ssn = db.Column(db.String(250))
    residence = db.Column(db.String(250))
    website = db.Column(PickleType)
    blood_group = db.Column(db.String(250))
    username = db.Column(db.String(250), primary_key=True)
    name = db.Column(db.String(250))
    current_location = db.Column(PickleType)
    sex = db.Column(db.String(250))
    address = db.Column(db.String(250))
    mail = db.Column(db.String(250))
    birthdate = db.Column(db.String(250))


class ProfileSchema(mam.ModelSchema):
        job = fields.String(required=True)
        company = fields.String(required=True)
        ssn = fields.String(required=False)
        residence = fields.String(required=True)
        blood_group = fields.String(required=False)
        website = fields.List(fields.String(), required=True)
        current_location = fields.List(fields.Float(required=True),required=True)
        username = fields.String(required=True)
        name = fields.String(required=False)
        sex = fields.String(required=False)
        address = fields.String(required=False)
        mail = fields.String(required=False)
        birthdate = fields.String(required=False)


