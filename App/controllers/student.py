from flask import Blueprint, jsonify
from App.models import Student, Shortlist

student_bp = Blueprint("student", __name__)

@student_bp.route("/students/<int:student_id>/shortlist", methods=["GET"])
def view_shortlist(student_id):
    shortlists = Shortlist.query.filter_by(student_id=student_id).all()
    return jsonify([
        {"position": s.position.title, "status": s.status, "added": s.date_added}
        for s in shortlists
    ])
