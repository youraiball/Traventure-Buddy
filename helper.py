import requests
import crud
import model
import os
import country_converter as coco

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

def get_coordinates(city, country):
    """Return longitude and latitude for a destination."""

    country_code = coco.convert(names=country, to="ISO2")
    opentrip_res = requests.get(f"https://api.opentripmap.com/0.1/en/places/geoname?name={city}&country={country_code}&apikey={os.environ['OPENTRIPMAP_API']}")
    opentrip_data = opentrip_res.json()
    lat = opentrip_data["lat"]
    lon = opentrip_data["lon"]

    return [lon, lat]