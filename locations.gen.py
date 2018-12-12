from app import app, api, querystring_get
from app import Alert
from app.models import EventLocation

from flask import render_template, session, redirect

@app.route("/locations/")
def list_location():
    items = api.list(EventLocation, False)
    
    if not items and api.erred:
        Alert.bad(api.error)

    return render_template("location/list.html", items=items)

@app.route("/locations/create/")
def create_location():
    return render_template("location/view.html")

@app.route("/locations/<id>/")
def view_location(id):
    item = api.get(EventLocation, id)
    
    if not item:
        Alert.bad("Could not find <strong>Location</strong> {}".format(id))
        return redirect("/locations/")
    
    data = {
        "id": id,
        "name": item.name,
        "description": item.description
    }

    return render_template("location/view.html", **data)

@app.route("/locations/<id>/", methods=["POST"])
def update_location(id):
    data = {
        "name": querystring_get("name"),
        "description": querystring_get("description")
    }

    if not data["name"]:
        Alert.bad("The <strong>name</strong> field is required")
        return render_template("location/view.html", **data)

    create = str(id).lower() == "create"

    item = None
    if create:
        item = EventLocation()
    else:   
        item = api.get(EventLocation, id)
        if not item:
            Alert.bad("Could not find <strong>Location</strong> {}; {}".format(id, api.error))
            return render_template("location/view.html", **data)

    item.name = data["name"]
    item.description = data["description"]
    item = api.update(EventLocation, item)
    
    if not item:
        Alert.bad(api.error)
        return render_template("location/view.html", **data)
    
    Alert.good("Location <strong>{}</strong> {}".format(item.name, "created" if create else "updated"))
    return redirect("/locations/{}".format(item.id))

@app.route("/locations/<id>/delete")
def delete_location(id):
    item = api.get(EventLocation, id)
    
    if not item:
        Alert.bad("Could not find <strong>Location</strong> {}".format(id))
        return redirect("/locations/")
    
    data = {
        "id": id,
        "name": item.name,
        "description": item.description
    }

    return render_template("location/delete.html", **data) 

@app.route("/locations/<id>/delete", methods=["POST"])
def delete_location_post(id):
    item = api.get(EventLocation, id)

    if not item:
        Alert.bad(api.error)
        return redirect("/locations/")

    deleted = api.delete(EventLocation, item)

    if not deleted:
        Alert.bad(api.error)
        return redirect("/locations/{}/".format(id))

    Alert.good("Deleted <strong>Location</strong> '{}'".format(item.name))
    return redirect("/locations/")

@app.route("/locations/<id>/restore")
def restore_location(id):
    item = api.get(EventLocation, id)

    if not item:
        Alert.bad(api.error)
        return redirect("/locations/")

    restored = api.restore(EventLocation, item)

    if not restored:
        Alert.bad(api.error)
        return redirect("/locations/")

    Alert.good("Restored <strong>Location</strong> with name <strong>{}</strong>".format(item.name))
    return redirect("/locations/")