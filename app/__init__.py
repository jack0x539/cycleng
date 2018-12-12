from flask import Flask, render_template, session, request
from flask_sqlalchemy import SQLAlchemy
from app.api import Api

app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy(app)
api = Api(db)

class Alert:
    @staticmethod
    def alert(message, kind):
        if not "alerts" in session:
            session["alerts"] = []
        session["alerts"].append((message, kind))

    @staticmethod
    def good(message):
        Alert.alert(message, "alert-success")

    @staticmethod
    def bad(message):
        Alert.alert(message, "alert-danger")

def querystring_get(key, alternate=""):
    return request.form[key].strip() if key in request.form else alternate

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

from app.controllers import home, event_role, weather, charge_type, partnership, event_type, location

db.create_all()