from flask import Blueprint, request, jsonify
from app.extensions import db
from App.models import Employer, InternshipPosition

employer_bp = Blueprint("employer", __name__)

@employer_bp.route("/positions", methods=["POST"])
def create_position():
    data = request.json
    employer_id = data.get("employer_id")
    position = InternshipPosition(
        title=data["title"],
        description=data["description"],
        employer_id=employer_id
    )
    db.session.add(position)
    db.session.commit()
    return jsonify({"message": "Position created", "id": position.id})
