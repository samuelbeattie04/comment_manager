import uuid

from library.extensions import db

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.String(10), primary_key=True, default=lambda: str(uuid.uuid4())[:10])
    category = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(50), nullable=True)
    forename = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)

class Archive(db.Model):
    __tablename__ = 'archive'
    id = db.Column(db.String(10), primary_key=True, default=lambda: str(uuid.uuid4())[:10])
    category = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(50), nullable=True)
    forename = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)