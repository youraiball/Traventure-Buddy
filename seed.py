"""Script to seed traventures database"""

import os
import json

import crud
import model
import server
import requests

os.system("dropdb traventures")
os.system("createdb traventures")

model.connect_to_db(server.app)
model.db.create_all()

user = crud.create_user("Turbo", "turbonoemail@email.com", "menolikeyowner")

google_search_payload = {
    "q": "Seoul South Korea",
    "cx": "2357895293d054097",
    "key": os.environ["GOOGLE_CSE_API"],
    "searchType": "image"
}
google_search_res = requests.get("https://customsearch.googleapis.com/customsearch/v1", params=google_search_payload)
google_search_json = google_search_res.json()
destination_imgs = google_search_json["items"]
image = destination_imgs[0]["link"]

destination = crud.create_destination("Seoul", "South Korea", 37.566, 126.9784, image)
trip = crud.create_trip(destination, user, "Seoul, S-Korea")

restaurant_activity = crud.create_activity_type("Restaurants")
shopping_activity = crud.create_activity_type("Shopping")
tourism_activity = crud.create_activity_type("Tourism")

model.db.session.add_all([user, destination, trip, restaurant_activity, shopping_activity, tourism_activity])
model.db.session.commit()

def get_activity_by_type(activity_type, lat, lon, destination):
    url = "https://api.geoapify.com/v2/places"

    if activity_type == "catering":
        db_activity_type = restaurant_activity
    elif activity_type == "commercial":
        db_activity_type = shopping_activity
    elif (activity_type == "tourism") or (activity_type == "entertainment"):
        db_activity_type = tourism_activity

    payload = {  
        "apiKey": os.environ["GEO_API_KEY"],
        "name": "seoul",
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

get_activity_by_type("catering", 37.5519, 126.9918, destination)
get_activity_by_type("commercial", 37.5519, 126.9918, destination)
get_activity_by_type("tourism", 37.5519, 126.9918, destination)
get_activity_by_type("entertainment", 37.5519, 126.9918, destination)

lotte = crud.create_activity(destination, "Lotte Department Store", shopping_activity,
                             description="14 Floors shopping mall with 3 connected buildings")
lotte_world = crud.create_activity(destination, "Lotte World Tower Mall", shopping_activity,
    description="5th tallest skyscraper in the world, 123 stories, with mall, hotel, restaurants, and more")
mdong = crud.create_activity(destination, "Myeongdong Street", shopping_activity,
                             description="popular walking area with shops and street food")
kyoja = crud.create_activity(destination, "Myeongdong Kyoja", restaurant_activity,
                             description="Michelin Bib Gourmand restaurant")

model.db.session.add_all([lotte, lotte_world, mdong, kyoja])
model.db.session.commit()