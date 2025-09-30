import click
from flask.cli import AppGroup
from App.main import create_app
from App.database import db, get_migrate
from App.controllers import (
    create_user, get_all_users, get_all_users_json, initialize
)
from App.controllers.employer import (
    create_employer, get_employer_by_id, get_all_employers,
    view_positions, view_position_shortlist
)
from App.controllers.staff import create_staff, get_all_staff, get_staff_by_id
from App.controllers.student import create_student, get_all_students, get_student_by_id
from App.controllers.internshipposition import create_position, get_position_by_id
from App.models.user import User
from App.models.employer import Employer
from App.models.staff import Staff
from App.models.student import Student, Student_Position
from App.models.internshipposition import InternshipPosition

app = create_app()
migrate = get_migrate(app)

# ----------------------
# Database Commands
# ----------------------

@app.cli.command("init", help="Initialize database")
def init():
    initialize()
    print("Database initialized.")

@app.cli.command("list-all", help="List all database objects")
def list_all():
    print("\nEmployers:")
    for emp in get_all_employers() or []:
        print(emp)

    print("\nStaff:")
    for sta in get_all_staff() or []:
        print(sta)

    print("\nStudents:")
    for stu in get_all_students() or []:
        print(stu)

    print("\nInternship Positions:")
    for pos in InternshipPosition.query.all() or []:
        print(pos)

    print("\nStudent Positions:")
    for sp in Student_Position.query.all() or []:
        print(sp)
    print("")

# ----------------------
# User CLI
# ----------------------

user_cli = AppGroup("user", help="User commands")

@user_cli.command("create", help="Create a user")
@click.argument("username")
@click.argument("password")
def create_user_command(username, password):
    create_user(username, password)
    print(f"User '{username}' created.")

@user_cli.command("list", help="List users")
@click.option("--format", default="string", type=click.Choice(["string", "json"]))
def list_user_command(format):
    if format == "json":
        print(get_all_users_json())
    else:
        print(get_all_users())

app.cli.add_command(user_cli)

# ----------------------
# Employer CLI
# ----------------------

employer_cli = AppGroup("employer", help="Employer commands")

@employer_cli.command("create", help="Create an employer")
@click.argument("username")
@click.argument("password")
@click.argument("company_name")
def create_employer_command(username, password, company_name):
    if Employer.query.filter_by(username=username, companyName=company_name).first():
        print("Employer already exists.")
        return
    create_employer(username, password, company_name)
    print(f"Employer '{username}' created.")

@employer_cli.command("view-positions", help="View positions for employer")
@click.argument("employer_id")
def view_positions_command(employer_id):
    positions = view_positions(employer_id)
    if not positions:
        print("No positions found.")
        return
    for pos in positions:
        print(pos)

@employer_cli.command("view-shortlist", help="View shortlist for a position")
@click.argument("position_id")
def view_shortlist_command(position_id):
    shortlist = view_position_shortlist(position_id)
    if not shortlist:
        print("No students in shortlist.")
        return
    for sp in shortlist:
        print(sp)

@employer_cli.command("create-position", help="Create internship position")
@click.argument("employer_id")
@click.argument("title")
@click.argument("department")
@click.argument("description")
def create_position_command(employer_id, title, department, description):
    pos = create_position(employer_id, title, department, description)
    print(f"Position '{pos.positionTitle}' created for employer {employer_id}.")

@employer_cli.command("accept-reject", help="Accept or reject a student application")
@click.argument("employer_id")
@click.argument("position_id")
@click.argument("student_id")
@click.argument("status")
@click.option("--message", default=None, help="Optional message")
def accept_reject_command(employer_id, position_id, student_id, status, message):
    emp = get_employer_by_id(employer_id)
    if not emp:
        print("Employer not found.")
        return
    if emp.acceptReject(student_id, position_id, status, message):
        print(f"Application status updated to '{status}'.")
    else:
        print("Failed to update application status.")

app.cli.add_command(employer_cli)

# ----------------------
# Staff CLI
# ----------------------

staff_cli = AppGroup("staff", help="Staff commands")

@staff_cli.command("create", help="Create staff")
@click.argument("employer_id")
@click.argument("username")
@click.argument("password")
def create_staff_command(employer_id, username, password):
    staff = create_staff(username, password, employer_id)
    db.session.add(staff)
    db.session.commit()
    print(f"Staff '{username}' created for employer {employer_id}.")

@staff_cli.command("add-to-shortlist", help="Add student to position shortlist")
@click.argument("staff_id")
@click.argument("position_id")
@click.argument("student_id")
def add_to_shortlist_command(staff_id, position_id, student_id):
    staff = get_staff_by_id(staff_id)
    if staff.addToShortlist(position_id, student_id):
        print("Student added to shortlist.")
    else:
        print("Failed to add student.")

app.cli.add_command(staff_cli)

# ----------------------
# Student CLI
# ----------------------

student_cli = AppGroup("student", help="Student commands")

@student_cli.command("create", help="Create student")
@click.argument("username")
@click.argument("password")
@click.argument("faculty")
@click.argument("department")
@click.argument("degree")
@click.argument("gpa")
def create_student_command(username, password, faculty, department, degree, gpa):
    stu = create_student(username, password, faculty, department, degree, gpa)
    db.session.add(stu)
    db.session.commit()
    print(f"Student '{username}' created.")

@student_cli.command("view-shortlists", help="View shortlists a student is in")
@click.argument("student_id")
def view_student_shortlists(student_id):
    shortlists = Student_Position.query.filter_by(studentID=student_id).all()
    if not shortlists:
        print("No shortlists found.")
        return
    for s in shortlists:
        print(s)

app.cli.add_command(student_cli)

# ----------------------
# Position CLI
# ----------------------

position_cli = AppGroup("position", help="Position commands")

@position_cli.command("list", help="List all positions")
def list_positions_command():
    positions = InternshipPosition.query.all()
    if not positions:
        print("No positions found.")
        return
    for pos in positions:
        print(pos)

app.cli.add_command(position_cli)

# ----------------------
# WSGI entry point
# ----------------------
# gunicorn -w 4 'App.wsgi:app'