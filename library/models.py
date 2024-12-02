from app import db

class FeedbackComment(db.Model):
    __tablename__ = "feedback_comments"
    comment_id = db.Column(db.Integer, primary_key=True)         
    category = db.Column(db.String(50), nullable=False)     
    comment_name = db.Column(db.Text, nullable=False)           
    date = db.Column(db.DateTime, nullable=False)
    type  = db.Column(db.String(50), nullable=False) 
    forename  = db.Column(db.String(50), nullable=False) 
    surname  = db.Column(db.String(50), nullable=False) 

