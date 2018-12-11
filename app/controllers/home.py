from app import app, api
from app import Alert
from flask import render_template, redirect

from app.models import EventRole

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/init/")
def init():
    event_roles = [EventRole(name=name) for name in ["Staff", "Volunteer", "Carer", "Participant"]]

    for role in event_roles:
        created = api.create(EventRole, role)
        if not created:
            Alert.bad(api.error)

    return redirect("/")