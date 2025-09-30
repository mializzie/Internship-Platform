from datetime import datetime
from app.extensions import db

class Shortlist(db.Model):
    __tablename__ = "shortlists"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    position_id = db.Column(db.Integer, db.ForeignKey("positions.id"))
    status = db.Column(db.String(50))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship("Student", back_populates="shortlists")
    position = db.relationship("InternshipPosition")
