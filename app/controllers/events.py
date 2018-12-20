from app import app, api, querystring_get
from app import Alert
from app.models import Event, EventType, EventLocation, ChargeType

from flask import render_template, session, redirect

@app.route("/events/")
def list_event():
    items = api.list(Event, False)
    
    if not items and api.erred:
        Alert.bad(api.error)

    return render_template("event/list.html", items=items)

@app.route("/events/create/")
def create_event():
    charge_types = api.list(ChargeType)
    locations = api.list(EventLocation)
    event_types = api.list(EventType)

    data = {
        "event_types": event_types,
        "charge_types": charge_types,
        "locations": locations
    }

    return render_template("event/view.html", **data)

@app.route("/events/<id>/")
def view_event(id):
    item = api.get(Event, id)

    charge_types = api.list(ChargeType)
    locations = api.list(EventLocation)
    event_types = api.list(EventType)
    
    if not item:
        Alert.bad("Could not find <strong>Event</strong> {}".format(id))
        return redirect("/events/")
    
    data = {
        "id": id,
        "name": item.name,
        "description": item.description,
        "event_types": event_types,
        "charge_types": charge_types,
        "locations": locations
    }

    return render_template("event/view.html", **data)

@app.route("/events/<id>/", methods=["POST"])
def update_event(id):
    data = {
        "name": querystring_get("name"),
        "description": querystring_get("description")
    }

    if not data["name"]:
        Alert.bad("The <strong>name</strong> field is required")
        return render_template("event/view.html", **data)

    create = str(id).lower() == "create"

    item = None
    if create:
        item = Event()
    else:   
        item = api.get(Event, id)
        if not item:
            Alert.bad("Could not find <strong>Event</strong> {}; {}".format(id, api.error))
            return render_template("event/view.html", **data)

    item.name = data["name"]
    item.description = data["description"]
    item = api.update(Event, item)
    
    if not item:
        Alert.bad(api.error)
        return render_template("event/view.html", **data)
    
    Alert.good("Event <strong>{}</strong> {}".format(item.name, "created" if create else "updated"))
    return redirect("/events/{}".format(item.id))

@app.route("/events/<id>/delete")
def delete_event(id):
    item = api.get(Event, id)
    
    if not item:
        Alert.bad("Could not find <strong>Event</strong> {}".format(id))
        return redirect("/events/")
    
    data = {
        "id": id,
        "name": item.name,
        "description": item.description
    }

    return render_template("event/delete.html", **data) 

@app.route("/events/<id>/delete", methods=["POST"])
def delete_event_post(id):
    item = api.get(Event, id)

    if not item:
        Alert.bad(api.error)
        return redirect("/events/")

    deleted = api.delete(Event, item)

    if not deleted:
        Alert.bad(api.error)
        return redirect("/events/{}/".format(id))

    Alert.good("Deleted <strong>Event</strong> '{}'".format(item.name))
    return redirect("/events/")

@app.route("/events/<id>/restore")
def restore_event(id):
    item = api.get(Event, id)

    if not item:
        Alert.bad(api.error)
        return redirect("/events/")

    restored = api.restore(Event, item)

    if not restored:
        Alert.bad(api.error)
        return redirect("/events/")

    Alert.good("Restored <strong>Event</strong> with name <strong>{}</strong>".format(item.name))
    return redirect("/events/")