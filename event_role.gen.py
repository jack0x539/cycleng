from app import app, api, querystring_get
from app import Alert
from app.models import EventRole

from flask import render_template, session, redirect

@app.route("/eventroles/")
def list_event_role():
    items = api.list(EventRole, False)
    
    if not items and api.erred:
        Alert.bad(api.error)

    return render_template("event_role/list.html", items=items)

@app.route("/eventroles/create/")
def create_event_role():
    return render_template("event_role/view.html")

@app.route("/eventroles/<id>/")
def view_event_role(id):
    item = api.get(EventRole, id)
    
    if not item:
        Alert.bad("Could not find <strong>Event Role</strong> {}".format(id))
        return redirect("/eventroles/")
    
    data = {
        "id": id,
        "name": item.name,
        "description": item.description
    }

    return render_template("event_role/view.html", **data)

@app.route("/eventroles/<id>/", methods=["POST"])
def update_event_role(id):
    data = {
        "name": querystring_get("name"),
        "description": querystring_get("description")
    }

    if not data["name"]:
        Alert.bad("The <strong>name</strong> field is required")
        return render_template("event_role/view.html", **data)

    create = str(id).lower() == "create"

    item = None
    if create:
        item = EventRole()
    else:   
        item = api.get(EventRole, id)
        if not item:
            Alert.bad("Could not find <strong>Event Role</strong> {}; {}".format(id, api.error))
            return render_template("event_role/view.html", **data)

    item.name = data["name"]
    item.description = data["description"]
    item = api.update(EventRole, item)
    
    if not item:
        Alert.bad(api.error)
        return render_template("event_role/view.html", **data)
    
    Alert.good("Event Role <strong>{}</strong> {}".format(item.name, "created" if create else "updated"))
    return redirect("/eventroles/{}".format(item.id))

@app.route("/eventroles/<id>/delete")
def delete_event_role(id):
    item = api.get(EventRole, id)
    
    if not item:
        Alert.bad("Could not find <strong>Event Role</strong> {}".format(id))
        return redirect("/eventroles/")
    
    data = {
        "id": id,
        "name": item.name,
        "description": item.description
    }

    return render_template("event_role/delete.html", **data) 

@app.route("/eventroles/<id>/delete", methods=["POST"])
def delete_event_role_post(id):
    item = api.get(EventRole, id)

    if not item:
        Alert.bad(api.error)
        return redirect("/eventroles/")

    deleted = api.delete(EventRole, item)

    if not deleted:
        Alert.bad(api.error)
        return redirect("/eventroles/{}/".format(id))

    Alert.good("Deleted <strong>Event Role</strong> '{}'".format(item.name))
    return redirect("/eventroles/")

@app.route("/eventroles/<id>/restore")
def restore_event_role(id):
    item = api.get(EventRole, id)

    if not item:
        Alert.bad(api.error)
        return redirect("/eventroles/")

    restored = api.restore(EventRole, item)

    if not restored:
        Alert.bad(api.error)
        return redirect("/eventroles/")

    Alert.good("Restored <strong>Event Role</strong> with name <strong>{}</strong>".format(item.name))
    return redirect("/eventroles/")