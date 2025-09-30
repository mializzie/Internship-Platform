from app.extensions import db
from App.models.user import User

class Employer(User):
    __mapper_args__ = {"polymorphic_identity": "employer"}
    positions = db.relationship("InternshipPosition", back_populates="employer")
