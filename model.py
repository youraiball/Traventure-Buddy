"""Models for Traventure Buddy app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    fname = db.Column(db.String(20), nullable = False)
    lname = db.Column(db.String(20))
    email = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(10), nullable = False)
    num_destins = db.Column(db.Integer, nullable = False)

    destinations = db.relationship("Destination", back_populates = "users")

    def __repr__(self):
        return f'<User user_id={self.user_id} fname={self.fname} email={self.email}>'

class Destination(db.Model):
    """A destination."""

    __tablename__ = "destinations"

    destination_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    name = db.Column(db.String(50), nullable = False)

    users = db.relationship("User", back_populates = "destinations")
    activities = db.relationship("Activity", back_popluates = "destination")
    
    def __repr__(self):
        return f'<Destination destination_id={self.destination_id} name={self.name}>'
    
class Activity(db.Model):
    """An activity."""

    __tablename__ = "activities"

    activity_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.destination_id'), nullable = False)
    name = db.Column(db.String(50), nullable = False)
    type = db.Column(db.String(50), nullable = False)
    description = db.Column(db.Text)

    destination = db.relationship("Destination", back_populates = "activits")
    

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