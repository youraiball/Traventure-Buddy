"""Server for Traventure Buddy app."""

from flask import Flask, render_template, flash, redirect, session, request
from model import connect_to_db, db
from jinja2 import StrictUndefined
from helper import get_activity_by_type
import crud
import requests
import os
import country_converter as coco

app = Flask(__name__)
app.app_context().push()
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# HOMEPAGE  #
@app.route("/")
def show_homepage():
    """Render the homepage."""
    
    return render_template("homepage.html")

# USER ROUTES #
@app.route("/login")
def show_login():
    """Show the login form."""

    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    """Let user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        flash("Please enter all required fields.")
        return redirect("/login")

    user = crud.get_user_by_email(email)
    if user is not None and email == user.email and password == user.password:
        session["user"] = user.user_id
        flash("You are logged in")
        return redirect("/profile")
    else:
        flash("Unable to log in. Please try again")
        return redirect("/login")

@app.route("/logout")
def logout():
    """Let user log out."""

    del session["user"]
    flash("You have been logged out")

    return redirect("/")

@app.route("/create_account")
def show_create_account():
    """Show the create account form."""

    return render_template("create_account.html")
    
@app.route("/create_account", methods=["POST"])
def create_account():
    """Create a new user account."""

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")

    if fname == None or email == None or password == None:
        flash("Please enter required fields)")
        return render_template("create_account.html")

    elif crud.get_user_by_email(email):
        flash("Email in use. Login or try again.")
        return render_template("create_account.html")
    else:
        new_user = crud.create_user(fname, email, password, lname)
        db.session.add(new_user)
        db.session.commit()
        session["user"] = new_user.user_id
        flash("Account successfully created")
        return redirect("/")

@app.route("/profile")
def show_profile():
    """Show profile page."""

    if "user" in session:
        user = crud.get_user_by_id(session["user"])
        trips = user.trips
        return render_template("profile.html", user=user, trips=trips)
    else:
        return redirect("/login")

# ACTIVITY ROUTES
@app.route("/activities")
def show_activities():
    """Render the activities page."""

    city = request.args.get("city").capitalize()
    country = request.args.get("country").capitalize()
    from_date = request.args.get("from")
    to_date = request.args.get("to")
    
    if not city or not country:
        flash("Please enter a city and country.")
        return redirect("/")

    destination = crud.get_destination_by_city_country(city, country)

    if destination:
        activities = destination.activities
    else:
        country_code = coco.convert(names=country, to="ISO2")
        opentrip_res = requests.get(f"https://api.opentripmap.com/0.1/en/places/geoname?name={city}&country={country_code}&apikey={os.environ['OPENTRIPMAP_API']}")
        opentrip_data = opentrip_res.json()
        lat = opentrip_data["lat"]
        lon = opentrip_data["lon"]
        new_destination = crud.create_destination(city, country, lat, lon)

        db.session.add(new_destination)
        db.session.commit()

        get_activity_by_type("catering", city, lat, lon, new_destination)
        get_activity_by_type("commercial", city, lat, lon, new_destination)
        get_activity_by_type("tourism", city, lat, lon, new_destination)
        get_activity_by_type("entertainment", city, lat, lon, new_destination)

        activities = new_destination.activities

    return render_template("activities.html", trip=None, city=city, country=country, activities=activities,
                           from_date=from_date, to_date=to_date)

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

@app.route("/trips/<trip_id>")
def show_activities_by_trip(trip_id):
    """Show activities for a saved trip."""

    trip = crud.get_trip_by_id(trip_id)
    destination = trip.destination
    city = destination.city 
    country = destination.country
    activities = destination.activities

    return render_template("activities.html", trip=trip, city=city, country=country, activities=activities,
                           from_date="", to_date="")

@app.route("/save-list", methods=["POST"])
def save_list():
    """Save list to user's profile."""

    city = request.form.get("city")
    country = request.form.get("country")
    #trip_name = request.form.get("tname")

    user = crud.get_user_by_id(session["user"])
    destination = crud.get_destination_by_city_country(city, country)

    trip = crud.create_trip(destination, user, name=f"{city}, {country}")
    db.session.add(trip)
    db.session.commit()
    
    return redirect("/profile")

@app.route("/delete-list")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)