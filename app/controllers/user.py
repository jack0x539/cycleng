from app import app, api, querystring_get
from app import Alert
from app.models import User, Address

from flask import render_template, session, redirect

@app.route("/users/")
def list_user():
    items = api.list(User, False)
    
    if not items and api.erred:
        Alert.bad(api.error)

    return render_template("user/list.html", items=items)

@app.route("/users/create/")
def create_user():
    return render_template("user/view.html")

@app.route("/users/<id>/")
def view_user(id):
    item = api.get(User, id)
    
    if not item:
        Alert.bad("Could not find <strong>User</strong> {}".format(id))
        return redirect("/users/")
    
    data = {
        "id": id,
        "username": item.username,
        "forename": item.forename,
        "surname": item.surname,
        "email": item.email_address,
        "dob": item.dob,
        "address1": item.address.line1,
        "address2": item.address.line2,
        "address3": item.address.line3,
        "county": item.address.county,
        "postcode": item.address.postcode
    }

    return render_template("user/view.html", **data)

@app.route("/users/<id>/", methods=["POST"])
def update_user(id):
    data = {
        "username": querystring_get("username"),
        "forename": querystring_get("forename"),
        "surname": querystring_get("surname"),
        "email": querystring_get("email"),
        "dob": querystring_get("dob"),
        "address1": querystring_get("address1"),
        "address2": querystring_get("address2"),
        "address3": querystring_get("address3"),
        "county": querystring_get("county"),
        "postcode": querystring_get("postcode")
    }

    if not data["username"]:
        Alert.bad("The <strong>username</strong> field is required")
        return render_template("user/view.html", **data)
    
    if not data["forename"]:
        Alert.bad("The <strong>forename</strong> field is required")
        return render_template("user/view.html", **data)
    
    if not data["surname"]:
        Alert.bad("The <strong>surname</strong> field is required")
        return render_template("user/view.html", **data)

    if not data["address1"]:
        Alert.bad("The <strong>Address 1</strong> field is required")
        return render_template("user/view.html", **data)
    
    if not data["postcode"]:
        Alert.bad("The <strong>Post Code</strong> field is required")
        return render_template("user/view.html", **data)

    create = str(id).lower() == "create"

    item = None
    if create:
        item = User()
    else:   
        item = api.get(User, id)
        if not item:
            Alert.bad("Could not find <strong>User</strong> {}; {}".format(id, api.error))
            return render_template("user/view.html", **data)
    
    address = None
    if create or not item.address:
        address = Address()
    else:
        address = item.address

    address.line1 = data["address1"]
    address.line2 = data["address2"]
    address.line3 = data["address3"]
    address.county = data["county"]
    address.postcode = data["postcode"]

    if create or not item.address:
        address = api.create(Address, address)
        if not address:
            Alert.bad("Failed to create <strong>Address</strong>; {}".format(api.error))
            return render_template("user/view.html", **data)
    else:
        address = api.update(Address, address)
        if not address:
            Alert.bad("Failed to update <strong>Address</strong>; {}".format(api.error))
            return render_template("user/view.html", **data)

    item.username = data["username"]
    item.forename = data["forename"]
    item.surname = data["surname"]
    item.email_address = data["email"]
    item.dob = data["dob"]
    item.address = address
    item = api.update(User, item)
    
    if not item:
        Alert.bad(api.error)
        return render_template("user/view.html", **data)
    
    Alert.good("User <strong>{}</strong> {}".format(item.name, "created" if create else "updated"))
    return redirect("/users/{}".format(item.id))

@app.route("/users/<id>/delete")
def delete_user(id):
    item = api.get(User, id)
    
    if not item:
        Alert.bad("Could not find <strong>User</strong> {}".format(id))
        return redirect("/users/")
    
    data = {
        "id": id,
        "username": item.username,
        "forename": item.forename,
        "surname": item.surname,
        "email": item.email_address,
        "dob": item.dob,
        "address1": item.address.line1,
        "address2": item.address.line2,
        "address3": item.address.line3,
        "county": item.address.county,
        "postcode": item.address.postcode
    }

    return render_template("user/delete.html", **data) 

@app.route("/users/<id>/delete", methods=["POST"])
def delete_user_post(id):
    item = api.get(User, id)

    if not item:
        Alert.bad(api.error)
        return redirect("/users/")

    deleted = api.delete(User, item)

    if not deleted:
        Alert.bad(api.error)
        return redirect("/users/{}/".format(id))

    Alert.good("Deleted <strong>User</strong> '{}'".format(item.name))
    return redirect("/users/")

@app.route("/users/<id>/restore")
def restore_user(id):
    item = api.get(User, id)

    if not item:
        Alert.bad(api.error)
        return redirect("/users/")

    restored = api.restore(User, item)

    if not restored:
        Alert.bad(api.error)
        return redirect("/users/")

    Alert.good("Restored <strong>User</strong> with name <strong>{}</strong>".format(item.name))
    return redirect("/users/")