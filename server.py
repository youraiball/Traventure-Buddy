"""Server for Traventure Buddy app."""

from flask import Flask, render_template, flash, redirect, session, request
from model import connect_to_db, db

from jinja2 import StrictUndefined

app = Flask(__name__)
app.app_context().push()

@app.route("/")
def show_homepage():
    """Render the homepage."""
    
    return render_template("homepage.html")

if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)