from app import app, api, querystring_get
from app import Alert
from app.models import WeatherCondition

from flask import render_template, session, redirect

@app.route("/weather/")
def list_weather():
    items = api.list(WeatherCondition, False)
    
    if not items and api.erred:
        Alert.bad(api.error)

    return render_template("weather/list.html", items=items)

@app.route("/weather/create/")
def create_weather():
    return render_template("/weather/view.html")

@app.route("/weather/<id>/")
def view_weather(id):
    item = api.get(WeatherCondition, id)
    
    if not item:
        Alert.bad("Could not find <strong>Weather Condition</strong> {}".format(id))
        return redirect("/weather/")
    
    data = {
        "id": id,
        "name": item.name,
        "description": item.description
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

    item = None
    if create:
        item = WeatherCondition()
    else:   
        item = api.get(WeatherCondition, id)
        if not item:
            Alert.bad("Could not find <strong>Weather Condition</strong> {}; {}".format(id, api.error))
            return render_template("weather/view.html", **data)

    item.name = data["name"]
    item.description = data["description"]
    item = api.update(WeatherCondition, item)
    
    if not item:
        Alert.bad(api.error)
        return render_template("weather/view.html", **data)
    
    Alert.good("Weather Condition <strong>{}</strong> {}".format(item.name, "created" if create else "updated"))
    return redirect("/weather/{}".format(item.id))

@app.route("/weather/<id>/delete")
def delete_weather(id):
    item = api.get(WeatherCondition, id)
    
    if not item:
        Alert.bad("Could not find <strong>Weather Condition</strong> {}".format(id))
        return redirect("/weather/")
    
    data = {
        "id": id,
        "name": item.name,
        "description": item.description
    }

    return render_template("weather/delete.html", **data) 

@app.route("/weather/<id>/delete", methods=["POST"])
def delete_weather_post(id):
    item = api.get(WeatherCondition, id)

    if not item:
        Alert.bad(api.error)
        return redirect("/weather/")

    deleted = api.delete(WeatherCondition, item)

    if not deleted:
        Alert.bad(api.error)
        return redirect("/weather/{}/".format(id))

    Alert.good("Deleted <strong>Weather Condition</strong> '{}'".format(item.name))
    return redirect("/weather/")

@app.route("/weather/<id>/restore")
def restore_weather(id):
    item = api.get(WeatherCondition, id)

    if not item:
        Alert.bad(api.error)
        return redirect("/weather/")

    restored = api.restore(WeatherCondition, item)

    if not restored:
        Alert.bad(api.error)
        return redirect("/weather/")

    Alert.good("Restored <strong>Weather Condition</strong> with name <strong>{}</strong>".format(item.name))
    return redirect("/weather/")