"""Server for Traventure Buddy app."""

from flask import Flask

app = Flask(__name__)
app.app_context().push()

if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)