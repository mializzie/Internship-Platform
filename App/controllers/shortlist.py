from flask import Blueprint, jsonify
from App.models import Shortlist

shortlist_bp = Blueprint("shortlist", __name__)

@shortlist_bp.route("/shortlists", methods=["GET"])
def list_shortlists():
    shortlists = Shortlist.query.all()
    return jsonify([
        {"student": s.student.username, "position": s.position.title, "status": s.status}
        for s in shortlists
    ])
