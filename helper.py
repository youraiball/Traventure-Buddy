import requests
import crud
import model
import os

def get_activity_by_type(activity_type, city, lat, lon, destination):
    url = "https://api.geoapify.com/v2/places"

    if activity_type == "catering":
        db_activity_type = crud.get_activity_type_by_name("Restaurants")
    elif activity_type == "commercial":
        db_activity_type = crud.get_activity_type_by_name("Shopping")
    elif (activity_type == "tourism") or (activity_type == "entertainment"):
        db_activity_type = crud.get_activity_type_by_name("Tourism")

    payload = {  
        "apiKey": os.environ["GEO_API_KEY"],
        "name": city,
        "categories": activity_type,
        "bias": f"proximity:{lon},{lat}",
        "lang": "en"
    }

    res = requests.get(url, params=payload)

    data = res.json()
    features = data["features"]


    for feature in features:
        name = feature["properties"]["name"]
        description = feature["properties"]["categories"]
        activity = crud.create_activity(destination, name, db_activity_type, description)
        model.db.session.add(activity)
        model.db.session.commit()