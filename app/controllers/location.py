from app import app, api, querystring_get
from app import Alert
from app.models import EventLocation, Address

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
        "description": item.description,
        "address1": item.address.line1 if item.address else "",
        "address2": item.address.line2 if item.address else "",
        "address3": item.address.line3 if item.address else "",
        "county": item.address.county if item.address else "",
        "postcode": item.address.postcode if item.address else "",
        "contactname": item.contact_name,
        "contactemail": item.contact_email_address,
        "contactphone1": item.contact_telephone1,
        "contactphone2": item.contact_telephone2
    }

    return render_template("location/view.html", **data)

@app.route("/locations/<id>/", methods=["POST"])
def update_location(id):
    data = {
        "name": querystring_get("name"),
        "description": querystring_get("description"),
        "address1": querystring_get("address1"),
        "address2": querystring_get("address2"),
        "address3": querystring_get("address3"),
        "county": querystring_get("county"),
        "postcode": querystring_get("postcode"),
        "contactname": querystring_get("contactname"),
        "contactemail": querystring_get("contactemail"),
        "contactphone1": querystring_get("contactphone1"),
        "contactphone2": querystring_get("contactphone2"),
    }

    if not data["name"]:
        Alert.bad("The <strong>Name</strong> field is required")
        return render_template("location/view.html", **data)
    
    if not data["address1"]:
        Alert.bad("The <strong>Address 1</strong> field is required")
        return render_template("location/view.html", **data)
    
    if not data["postcode"]:
        Alert.bad("The <strong>Post Code</strong> field is required")
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
            return render_template("location/view.html", **data)
    else:
        address = api.update(Address, address)
        if not address:
            Alert.bad("Failed to update <strong>Address</strong>; {}".format(api.error))
            return render_template("location/view.html", **data)

    item.name = data["name"]
    item.description = data["description"]
    item.contact_name = data["contactname"]
    item.contact_email_address = data["contactemail"]
    item.contact_telephone1 = data["contactphone1"]
    item.contact_telephone2 = data["contactphone2"]
    item.address = address

    item = api.update(EventLocation, item)
    
    if not item:
        Alert.bad("Failed to create <strong>Address</strong>; {}".format(api.error))
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