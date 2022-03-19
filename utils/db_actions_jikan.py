import json
from pprint import pprint

# Method to remove unnecessary properties from show JSON
properties_to_remove = [
  "request_hash",
  "request_cached",
  "request_cache_expiry",
  "trailer_url",
  "title_japanese",
  "title_synonyms",
  "related",
  "producers",
  "licensors",
  "opening_themes",
  "ending_themes",
  "external_links",
  "premiered",
  "broadcast",
]

properties_to_flatten = [
  "studios",
  "genres",
  "explicit_genres",
  "themes",
  "demographics",
]

def clean_show(json):
    for property in properties_to_remove:
        if json.get(property) is not None:
            del json[property]

    for property in properties_to_flatten:
      if json.get(property) is not None:
        data = json[property]
        flattened_data = []

        for datum in data:
          name = datum["name"]
          flattened_data.append(name)

        json[property] = flattened_data
    
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