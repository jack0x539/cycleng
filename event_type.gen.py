from app import app, api, querystring_get
from app import Alert
from app.models import EventType

from flask import render_template, session, redirect

@app.route("/eventtypes/")
def list_event_type():
    items = api.list(EventType, False)
    
    if not items and api.erred:
        Alert.bad(api.error)

    return render_template("event_type/list.html", items=items)

@app.route("/eventtypes/create/")
def create_event_type():
    return render_template("event_type/view.html")

@app.route("/eventtypes/<id>/")
def view_event_type(id):
    item = api.get(EventType, id)
    
    if not item:
        Alert.bad("Could not find <strong>Event Type</strong> {}".format(id))
        return redirect("/eventtypes/")
    
    data = {
        "id": id,
        "name": item.name,
        "description": item.description
    }

    return render_template("event_type/view.html", **data)

@app.route("/eventtypes/<id>/", methods=["POST"])
def update_event_type(id):
    data = {
        "name": querystring_get("name"),
        "description": querystring_get("description")
    }

    if not data["name"]:
        Alert.bad("The <strong>name</strong> field is required")
        return render_template("event_type/view.html", **data)

    create = str(id).lower() == "create"

    item = None
    if create:
        item = EventType()
    else:   
        item = api.get(EventType, id)
        if not item:
            Alert.bad("Could not find <strong>Event Type</strong> {}; {}".format(id, api.error))
            return render_template("event_type/view.html", **data)

    item.name = data["name"]
    item.description = data["description"]
    item = api.update(EventType, item)
    
    if not item:
        Alert.bad(api.error)
        return render_template("event_type/view.html", **data)
    
    Alert.good("Event Type <strong>{}</strong> {}".format(item.name, "created" if create else "updated"))
    return redirect("/eventtypes/{}".format(item.id))

@app.route("/eventtypes/<id>/delete")
def delete_event_type(id):
    item = api.get(EventType, id)
    
    if not item:
        Alert.bad("Could not find <strong>Event Type</strong> {}".format(id))
        return redirect("/eventtypes/")
    
    data = {
        "id": id,
        "name": item.name,
        "description": item.description
    }

    return render_template("event_type/delete.html", **data) 

@app.route("/eventtypes/<id>/delete", methods=["POST"])
def delete_event_type_post(id):
    item = api.get(EventType, id)

    if not item:
        Alert.bad(api.error)
        return redirect("/eventtypes/")

    deleted = api.delete(EventType, item)

    if not deleted:
        Alert.bad(api.error)
        return redirect("/eventtypes/{}/".format(id))

    Alert.good("Deleted <strong>Event Type</strong> '{}'".format(item.name))
    return redirect("/eventtypes/")

@app.route("/eventtypes/<id>/restore")
def restore_event_type(id):
    item = api.get(EventType, id)

    if not item:
        Alert.bad(api.error)
        return redirect("/eventtypes/")

    restored = api.restore(EventType, item)

    if not restored:
        Alert.bad(api.error)
        return redirect("/eventtypes/")

    Alert.good("Restored <strong>Event Type</strong> with name <strong>{}</strong>".format(item.name))
    return redirect("/eventtypes/")