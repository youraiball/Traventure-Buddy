"""Crud operations for Traventure Buddy app."""

from model import db, User, Destination, Trip, Activity, ActivityType, connect_to_db

# # # # # # # # # #
# USER FUNCTIONS  #
# # # # # # # # # #

def create_user(fname, email, password, lname=None):
    """Create and return new user."""

    user = User(fname=fname, email=email, password=password, lname=lname)

    return user

def get_all_users():
    """"Get all users."""

    return User.query.all()

def get_user_by_id(user_id):
    """Get a user by id."""
    
    return User.query.get(user_id)

def get_user_by_email(email):
    """Get a user by their email."""

    return User.query.filter_by(email = email).first()

# # # # # # # # # # # # #
# DESTINATION FUNCTIONS #
# # # # # # # # # # # # #

def create_destination(city, country, lat, lon):
    """Create new destination."""

    destination = Destination(city=city, country=country, lat=lat, lon=lon)

    return destination

def get_all_destinationss():
    """"Get all destinations."""

    return Destination.query.all()

def get_destination_by_id(destination_id):
    """Get a user by id."""
    
    return Destination.query.get(destination_id)

def get_destination_by_city_country(city, country):
    """Get a destination by city."""

    return Destination.query.filter(Destination.city == city, Destination.country == country).first()

def get_destination_by_coords(lat, lon):
    """Get a destination by latitude and longitude."""

    return Destination.query.filter_by(lat=lat, lon=lon).first()

# # # # # # # # # #
# TRIP FUNCTIONS  #
# # # # # # # # # # 

def create_trip(destination, user, name):
    """Create new trip."""

    trip = Trip(destination=destination, user=user, name=name)

    return trip

def get_trip_by_id(trip_id):
    """Get a trip by its ID."""

    return Trip.query.get(trip_id)

def delete_trip_by_id(trip_id):
    """Delete a trip by id."""

    return Trip.query.filter(Trip.trip_id == trip_id).delete()

# # # # # # # # # # 
# TYPE FUNCTIONS  #
# # # # # # # # # # 

def create_activity_type(type):
    """Create new type of activity."""

    type = ActivityType(type=type)

    return type

def get_activity_type_by_name(name):
    """Get activity type by name."""

    return ActivityType.query.filter(ActivityType.type == name).first()

# # # # # # # # # # # #
# ACTIVITY FUNCTIONS  #
# # # # # # # # # # # #

def create_activity(destination, name, type, description=None):
    """Create new activity."""

    activity = Activity(destination=destination, name=name,
                        type=type, description=description)

    return activity

def get_all_activities():
    """"Get all activitiess."""

    return Activity.query.all()

def get_activity_by_id(activity_id):
    """Get an activity by its id."""

    return Activity.query.get(activity_id)

# # # # # # # # # # 

if __name__ == "__main__":
    from server import app
    connect_to_db(app)