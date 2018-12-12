from app import app, api, querystring_get
from app import Alert
from app.models import ChargeType

from flask import render_template, session, redirect

@app.route("/chargetypes/")
def list_charge_type():
    items = api.list(ChargeType, False)
    
    if not items and api.erred:
        Alert.bad(api.error)

    return render_template("charge_type/list.html", items=items)

@app.route("/chargetypes/create/")
def create_charge_type():
    return render_template("charge_type/view.html")

@app.route("/chargetypes/<id>/")
def view_charge_type(id):
    item = api.get(ChargeType, id)
    
    if not item:
        Alert.bad("Could not find <strong>Charge Type</strong> {}".format(id))
        return redirect("/chargetypes/")
    
    data = {
        "id": id,
        "name": item.name,
        "description": item.description
    }

    return render_template("charge_type/view.html", **data)

@app.route("/chargetypes/<id>/", methods=["POST"])
def update_charge_type(id):
    data = {
        "name": querystring_get("name"),
        "description": querystring_get("description")
    }

    if not data["name"]:
        Alert.bad("The <strong>name</strong> field is required")
        return render_template("charge_type/view.html", **data)

    create = str(id).lower() == "create"

    item = None
    if create:
        item = ChargeType()
    else:   
        item = api.get(ChargeType, id)
        if not item:
            Alert.bad("Could not find <strong>Charge Type</strong> {}; {}".format(id, api.error))
            return render_template("charge_type/view.html", **data)

    item.name = data["name"]
    item.description = data["description"]
    item = api.update(ChargeType, item)
    
    if not item:
        Alert.bad(api.error)
        return render_template("charge_type/view.html", **data)
    
    Alert.good("Charge Type <strong>{}</strong> {}".format(item.name, "created" if create else "updated"))
    return redirect("/chargetypes/{}".format(item.id))

@app.route("/chargetypes/<id>/delete")
def delete_charge_type(id):
    item = api.get(ChargeType, id)
    
    if not item:
        Alert.bad("Could not find <strong>Charge Type</strong> {}".format(id))
        return redirect("/chargetypes/")
    
    data = {
        "id": id,
        "name": item.name,
        "description": item.description
    }

    return render_template("charge_type/delete.html", **data) 

@app.route("/chargetypes/<id>/delete", methods=["POST"])
def delete_charge_type_post(id):
    item = api.get(ChargeType, id)

    if not item:
        Alert.bad(api.error)
        return redirect("/chargetypes/")

    deleted = api.delete(ChargeType, item)

    if not deleted:
        Alert.bad(api.error)
        return redirect("/chargetypes/{}/".format(id))

    Alert.good("Deleted <strong>Charge Type</strong> '{}'".format(item.name))
    return redirect("/chargetypes/")

@app.route("/chargetypes/<id>/restore")
def restore_charge_type(id):
    item = api.get(ChargeType, id)

    if not item:
        Alert.bad(api.error)
        return redirect("/chargetypes/")

    restored = api.restore(ChargeType, item)

    if not restored:
        Alert.bad(api.error)
        return redirect("/chargetypes/")

    Alert.good("Restored <strong>Charge Type</strong> with name <strong>{}</strong>".format(item.name))
    return redirect("/chargetypes/")