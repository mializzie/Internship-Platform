from app.extensions import db

class InternshipPosition(db.Model):
    __tablename__ = "positions"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.Text)
    employer_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    employer = db.relationship("Employer", back_populates="positions")
