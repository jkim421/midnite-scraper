import json
from datetime import datetime
from pprint import pprint


# Method to remove unnecessary properties from show JSON
properties_to_remove = [
  "trailer",
  "approved",
  "title_english",
  "title_japanese",
  "title_synonyms",
  "airing",
  "duration",
  "favorites",
  "background",
  "season",
  "year",
  "broadcast",
  "producers",
  "licensors",
  "relations",
  "explicit_genres",
  # for /full endpoint
  "theme",
  "external",
  "streaming",
]

properties_to_flatten = [
  "studios",
  "genres",
  "themes",
  "demographics",
]

def get_year_from_iso_date(iso_date):
  if iso_date == None:
    return None

  date_obj = datetime.fromisoformat(iso_date)
  year = date_obj.year

  return year


def clean_show(json):
    # delete properties to remove
    for field in properties_to_remove:
        if field in json:
            del json[field]

    # flatten properties that are lists of dicts with "name" field
    for field in properties_to_flatten:
        if json.get(field) is not None:
            data = json[field]

            json[field] = sorted([item["name"] for item in data])

    # clean .titles field
    titles = json.get("titles", {})

    default_title = next((item for item in titles if item["type"] == "Default"), {})
    english_title = next((item for item in titles if item["type"] == "English"), {})

    json["titles"] = {
      "default": default_title.get("title"),
      "english": english_title.get("title"),
    }

    # clean .images field
    images = json.get("images", {})
    webp = images.get("webp", {})

    json["images"] = {
        "small": webp.get("image_url"),
        "large": webp.get("large_image_url"),
    }

    # append start/end years from .aired 
    air_dates = json.get("aired", {})

    json["years"] = {
        "start": get_year_from_iso_date(air_dates.get("from")),
        "end": get_year_from_iso_date(air_dates.get("to")),
    }

    del json["aired"]

    # flatten studios
    # studios = json.get("studios", [])
    # json["studios"] = sorted([item["name"] for item in studios])

    return json

def get_existing_data(mal_id, collection):
    match = collection.find_one({ "mal_id": mal_id })

    if match:
      print(f"Data exists in collection for { mal_id }")
      return match
    else:
      print(f"No data in collection for { mal_id }")
      return None

# Method to write show JSON data to DynamoDB
def insert_show(show_data, collection, mal_id):
    cleaned_res = clean_show(show_data)
    collection.insert_one(cleaned_res)

    return mal_id


def update_show(prev_data, show_data, collection, mal_id):
    # Delete _id field to serialize JSON for comparison 
    del prev_data["_id"] 
    cleaned_res = clean_show(show_data)

    prev = json.dumps(prev_data, sort_keys=True)
    curr = json.dumps(cleaned_res, sort_keys=True)

    if prev != curr:
        print(f"Show data has changed - UPDATING data for { mal_id }")

        collection.replace_one({ "mal_id": mal_id }, cleaned_res)

        return mal_id
    else:
        print(f"Show data is unchanged. SKIPPING update for { mal_id }.")
