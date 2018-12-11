from app import app, api, querystring_get
from app import Alert
from app.models import Address, EventRole

from flask import render_template, session, redirect

@app.route("/eventroles/")
def list_event_roles():
    roles = api.list(EventRole, False)
    
    if not roles and api.erred:
        Alert.bad(api.error)

    return render_template("event_role/list.html", roles=roles)

@app.route("/eventroles/create/")
def create_event_role():
    return render_template("/event_role/view.html")

@app.route("/eventroles/<id>/")
def view_event_role(id):
    role = api.get(EventRole, id)
    
    if not role:
        Alert.bad("Could not find <strong>Event Role</strong> {}".format(id))
        return redirect("/eventroles/")
    
    data = {
        "id": id,
        "name": role.name,
        "description": role.description,
        "status": role.status
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

    role = None
    if str(id).lower() == "create":
        role = EventRole()
    else:
        role = api.get(EventRole, id)
        if not role:
            Alert.bad("Could not find <strong>Event Role</strong> {}; {}".format(id, api.error))
            return render_template("event_role/view.html", **data)

    role.name = data["name"]
    role.description = data["description"]
    role = api.update(EventRole, role)
    
    if not role:
        Alert.bad(api.error)
        return render_template("event_role/view.html", **data)
    
    return redirect("/eventroles/{}".format(role.id))

@app.route("/eventroles/<id>/delete")
def delete_event_role(id):
    role = api.get(EventRole, id)
    
    if not role:
        Alert.bad("Could not find <strong>Event Role</strong> {}".format(id))
        return redirect("/eventroles/")
    
    data = {
        "id": id,
        "name": role.name,
        "description": role.description
    }

    return render_template("event_role/delete.html", **data) 

@app.route("/eventroles/<id>/delete", methods=["POST"])
def delete_event_role_post(id):
    role = api.get(EventRole, id)

    if not role:
        Alert.bad(api.error)
        return redirect("/eventroles/")

    deleted = api.delete(EventRole, role)

    if not deleted:
        Alert.bad(api.error)
        return redirect("/eventroles/{}/".format(id))

    Alert.good("Deleted <strong>Event Role</strong> '{}'".format(role.name))
    return redirect("/eventroles/")

@app.route("/eventroles/<id>/restore")
def restore_event_role(id):
    role = api.get(EventRole, id)

    if not role:
        Alert.bad(api.error)
        return redirect("/eventroles/")

    undeleted = api.restore(EventRole, role)

    if not undeleted:
        Alert.bad(api.error)
        return redirect("/eventroles/")

    Alert.good("Restored <strong>Event Role</strong> with name <strong>{}</strong>".format(role.name))
    return redirect("/eventroles/")

        
    