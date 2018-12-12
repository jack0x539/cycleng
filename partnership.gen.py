from app import app, api, querystring_get
from app import Alert
from app.models import Partnership

from flask import render_template, session, redirect

@app.route("/partnerships/")
def list_partnership():
    items = api.list(Partnership, False)
    
    if not items and api.erred:
        Alert.bad(api.error)

    return render_template("partnership/list.html", items=items)

@app.route("/partnerships/create/")
def create_partnership():
    return render_template("partnership/view.html")

@app.route("/partnerships/<id>/")
def view_partnership(id):
    item = api.get(Partnership, id)
    
    if not item:
        Alert.bad("Could not find <strong>Partnership</strong> {}".format(id))
        return redirect("/partnerships/")
    
    data = {
        "id": id,
        "name": item.name,
        "description": item.description
    }

    return render_template("partnership/view.html", **data)

@app.route("/partnerships/<id>/", methods=["POST"])
def update_partnership(id):
    data = {
        "name": querystring_get("name"),
        "description": querystring_get("description")
    }

    if not data["name"]:
        Alert.bad("The <strong>name</strong> field is required")
        return render_template("partnership/view.html", **data)

    create = str(id).lower() == "create"

    item = None
    if create:
        item = Partnership()
    else:   
        item = api.get(Partnership, id)
        if not item:
            Alert.bad("Could not find <strong>Partnership</strong> {}; {}".format(id, api.error))
            return render_template("partnership/view.html", **data)

    item.name = data["name"]
    item.description = data["description"]
    item = api.update(Partnership, item)
    
    if not item:
        Alert.bad(api.error)
        return render_template("partnership/view.html", **data)
    
    Alert.good("Partnership <strong>{}</strong> {}".format(item.name, "created" if create else "updated"))
    return redirect("/partnerships/{}".format(item.id))

@app.route("/partnerships/<id>/delete")
def delete_partnership(id):
    item = api.get(Partnership, id)
    
    if not item:
        Alert.bad("Could not find <strong>Partnership</strong> {}".format(id))
        return redirect("/partnerships/")
    
    data = {
        "id": id,
        "name": item.name,
        "description": item.description
    }

    return render_template("partnership/delete.html", **data) 

@app.route("/partnerships/<id>/delete", methods=["POST"])
def delete_partnership_post(id):
    item = api.get(Partnership, id)

    if not item:
        Alert.bad(api.error)
        return redirect("/partnerships/")

    deleted = api.delete(Partnership, item)

    if not deleted:
        Alert.bad(api.error)
        return redirect("/partnerships/{}/".format(id))

    Alert.good("Deleted <strong>Partnership</strong> '{}'".format(item.name))
    return redirect("/partnerships/")

@app.route("/partnerships/<id>/restore")
def restore_partnership(id):
    item = api.get(Partnership, id)

    if not item:
        Alert.bad(api.error)
        return redirect("/partnerships/")

    restored = api.restore(Partnership, item)

    if not restored:
        Alert.bad(api.error)
        return redirect("/partnerships/")

    Alert.good("Restored <strong>Partnership</strong> with name <strong>{}</strong>".format(item.name))
    return redirect("/partnerships/")