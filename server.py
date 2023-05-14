"""Server for Traventure Buddy app."""

from flask import Flask, render_template, flash, redirect, session, request
from model import connect_to_db, db
from jinja2 import StrictUndefined
import crud

app = Flask(__name__)
app.app_context().push()
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# HOMEPAGE
@app.route("/")
def show_homepage():
    """Render the homepage."""
    
    return render_template("homepage.html")

# USER ROUTES
@app.route("/login")
def show_login():
    """Show the login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    """Let user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user is not None and email == user.email and password == user.password:
        session["user"] = user.user_id
        flash("You are logged in")
        return redirect("/")
    else:
        flash("Unable to log in. Please try again")
        return render_template("login.html")

@app.route("/activities")
def show_activities():
    """Render the activities page."""

    city = request.args.get("city").capitalize()
    country = request.args.get("country").capitalize()

    activities = crud.get_all_activities()

    return render_template("activities.html", city=city, country=country, activities=activities)

@app.route("/create_account", methods=["POST"])
def create_account():
    """Create a new user account."""

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")

    if crud.get_user_by_email(email):
        flash("Email in use. Login or try again.")
    else:
        new_user = crud.create_user(fname, email, password, lname)
        db.session.add(new_user)
        db.session.commit()
        flash("Account successfully created")
    
    return redirect("/")


@app.route("/activities/<activity_id>")
def show_activity_details(activity_id):
    """View details for a particular activity"""

    activity = crud.get_activity_by_id(activity_id)
    activity_type = activity.type.type

    return render_template("activity_details.html", activity=activity, activity_type=activity_type)

@app.route("/itinerary")
def show_itinerary():
    """View a user's itinerary if account exists and is logged in"""

    # user stuff, login, create account, something something

    return render_template("itinerary.html")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)