from app import app, api
from app import Alert
from flask import render_template, redirect
from app.models import generate_controller, EventRole, ChargeType, Partnership, EventType, EventLocation

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/init/")
def init():
    import os

    try:
        generate_controller(ChargeType, "Charge Type", "charge_type", "chargetypes", "charge_type.gen.py")
        generate_controller(Partnership, "Partnership", "partnership", "partnerships", "partnership.gen.py")
        generate_controller(EventType, "Event Type", "event_type", "eventtypes", "event_type.gen.py")
        generate_controller(EventRole, "Event Role", "event_role", "eventroles", "event_role.gen.py")
        generate_controller(EventLocation, "Location", "location", "locations", "locations.gen.py")
    except Exception as e:
        Alert.bad(str(e))
    
    return redirect("/")

