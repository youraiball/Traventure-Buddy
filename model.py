"""Models for Traventure Buddy app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(10), nullable=False)

    trips = db.relationship("Trip", back_populates="user")

    def __repr__(self):
        return f'<User user_id={self.user_id} fname={self.fname} email={self.email}>'


class Destination(db.Model):
    """A destination."""

    __tablename__ = "destinations"

    destination_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    lon = db.Column(db.Float, nullable=False)
    lat = db.Column(db.Float, nullable=False)

    trips = db.relationship("Destination", back_populates="destination")
    activites = db.relationship("Activity", back_populates="destination")

    def __repr__(self):
        return f'<Destination destination_id={self.destination_id} city={self.city} country={self.country}>'


class Trip(db.Model):
    """A trip."""

    __tablename__ = "trips"

    trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.destination_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    name = db.Column(db.String(20), nullable=False)

    user = db.relationship("User", back_populates="trips")
    destination = db.relationship("Destination", back_populates="trips")

    def __repr__(self):
        return f'<Trip trip_id={self.trip_id} name={self.name}>'


class Activity(db.Model):
    """An activity."""

    __tablename__ = "activities"

    activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.destination_id"), nullable=False)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    type_id = db.Column(db.Integer, db.ForeignKey("activity_types.type_id"), nullable = False)
    
    destination = db.relationship("Destination", back_populates="activities")
    type = db.relationship("ActivityType", back_populates="activities")

    def __repr__(self):
        return f'<Activity activity_id={self.activity_id} name={self.name}>'
    

class ActivityType(db.Model):
    """A type of activity."""

    __tablename__ = "activity_types"

    type_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    type = db.Column(db.String(50), nullable = False)

    activities = db.relationship("Activity", back_populates="type")

    def __repr__(self):
        return f'<Activity_type type_id={self.type_id} type={self.type}>'


def connect_to_db(flask_app, db_uri="postgresql:///traventures", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)