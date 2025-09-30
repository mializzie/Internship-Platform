from App.models.user import User

class Staff(User):
    __mapper_args__ = {"polymorphic_identity": "staff"}
    # Staff does not need extra fields; logic is handled in controllers
