from app import app, api, querystring_get
from app import Alert
from app.models import WeatherCondition

from flask import render_template, session, redirect

@app.route("/weather/")
def list_weather():
    roles = api.list(WeatherCondition, True)
    
    if not roles and api.erred:
        Alert.bad(api.error)

    return render_template("weather/list.html", conditions=roles)

@app.route("/weather/create/")
def create_weather():
    return render_template("/weather/view.html")

@app.route("/weather/<id>/")
def view_weather(id):
    role = api.get(WeatherCondition, id)
    
    if not role:
        Alert.bad("Could not find <strong>Weather Condition</strong> {}".format(id))
        return redirect("/weather/")
    
    data = {
        "id": id,
        "name": role.name,
        "description": role.description
    }

    return render_template("weather/view.html", **data)

@app.route("/weather/<id>/", methods=["POST"])
def update_weather(id):
    data = {
        "name": querystring_get("name"),
        "description": querystring_get("description")
    }

    if not data["name"]:
        Alert.bad("The <strong>name</strong> field is required")
        return render_template("weather/view.html", **data)

    create = str(id).lower() == "create"

    role = None
    if create:
        role = WeatherCondition()
    else:   
        role = api.get(WeatherCondition, id)
        if not role:
            Alert.bad("Could not find <strong>Weather Condition</strong> {}; {}".format(id, api.error))
            return render_template("weather/view.html", **data)

    role.name = data["name"]
    role.description = data["description"]
    role = api.update(WeatherCondition, role)
    
    if not role:
        Alert.bad(api.error)
        return render_template("weather/view.html", **data)
    
    Alert.good("Weather Condition <strong>{}</strong> {}".format(role.name, "created" if create else "updated"))
    return redirect("/weather/{}".format(role.id))

@app.route("/weather/<id>/delete")
def delete_weather(id):
    role = api.get(WeatherCondition, id)
    
    if not role:
        Alert.bad("Could not find <strong>Weather Condition</strong> {}".format(id))
        return redirect("/weather/")
    
    data = {
        "id": id,
        "name": role.name,
        "description": role.description
    }

    return render_template("weather/delete.html", **data) 

@app.route("/weather/<id>/delete", methods=["POST"])
def delete_weather_post(id):
    role = api.get(WeatherCondition, id)

    if not role:
        Alert.bad(api.error)
        return redirect("/weather/")

    deleted = api.delete(WeatherCondition, role)

    if not deleted:
        Alert.bad(api.error)
        return redirect("/weather/{}/".format(id))

    Alert.good("Deleted <strong>Weather Condition</strong> '{}'".format(role.name))
    return redirect("/weather/")

@app.route("/weather/<id>/restore")
def restore_weather(id):
    role = api.get(WeatherCondition, id)

    if not role:
        Alert.bad(api.error)
        return redirect("/weather/")

    restored = api.restore(WeatherCondition, role)

    if not restored:
        Alert.bad(api.error)
        return redirect("/weather/")

    Alert.good("Restored <strong>Weather Condition</strong> with name <strong>{}</strong>".format(role.name))
    return redirect("/weather/")

        
    