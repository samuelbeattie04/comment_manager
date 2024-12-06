from library.extensions import db
from datetime import datetime

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class FeedbackComment(db.Model):
    __tablename__ = 'feedback'
id = db.Column(db.Integer, primary_key=True)
comment = db.Column(db.Text, nullable=False)
type = db.Column(db.String(50), nullable=True)
date_created = db.Column(db.DateTime, default=datetime.utcnow)
