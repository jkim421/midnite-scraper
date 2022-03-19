import json
from pprint import pprint

# Method to remove unnecessary properties from show JSON
properties_to_remove = [
    "created_at",
    "my_list_status",
    "broadcast",
    "average_episode_duration",
    "background",
    "related_manga",
]

property_rename_map = {
    "id": "mal_id",
    "main_picture": "pictures",
    "alternative_titles": "alt_titles",
    "mean": "mal_score",
    "rank": "mal_rank",
    "popularity": "mal_popularity",
}

def remove_properties(json):
    for property in properties_to_remove:
        if json.get(property) is not None:
            del json[property]

def rename_properties(json):
    for property in property_rename_map.keys():
        if json.get(property) is not None:
            new_name = property_rename_map[property]
            current = json[property]

            json[new_name] = current
            del json[property]

def get_format_by_name(property):
    def format_by_name(json):
        rawData = json[property]
        formatted = []

        for datum in rawData:
            name = datum["name"]
            formatted.append(name)

        return formatted

    return format_by_name

def format_related(json):
    related = json["related_anime"]
    formatted = []

    for relation in related:
        id = relation["node"]["id"]
        title = relation["node"]["id"]
        relation_type = relation["relation_type_formatted"]

        formatted.append({
            "id": id,
            "title": title,
            "relation_type": relation_type,
        })

    return formatted

def format_recommendations(json):
    recommendations = json["recommendations"]
    formatted = []

    for recommendation in recommendations:
        id = recommendation["node"]["id"]
        title = recommendation["node"]["title"]
        num_recommendations = recommendation["num_recommendations"]

        formatted.append({
            "id": id,
            "title": title,
            "num_recommendations": num_recommendations,
        })

    return formatted

property_formatter_map = {
    "genres": get_format_by_name("genres"),
    "studios": get_format_by_name("studios"),
    "relation_type_formatted": format_related,
    "recommendations": format_recommendations,
}

def format_properties(json):
    for property in property_formatter_map.keys():
        if json.get(property) is not None:
            formatter = property_formatter_map[property]
            formatted = formatter(json)

            json[property] = formatted

def clean_show(json):
    remove_properties(json)
    rename_properties(json)
    format_properties(json)

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
    # Delete _id field from Mongo to serialize JSON for comparison 
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