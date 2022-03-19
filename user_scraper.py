import requests
import json

print("Sending GET request...")

# anime_response = requests.get("https://api.jikan.moe/v3/anime/40908/")
user_response1 = requests.get("https://api.jikan.moe/v3/user/wisetail/animelist/all/")
user_response2 = requests.get("https://api.jikan.moe/v3/user/wisetail/animelist/all/2")

print("Writing files...")

# with open('ex_anime.json', 'w', encoding='utf-8') as f:
    # json.dump(anime_response.json(), f, ensure_ascii=False, indent=4)

# f.close()

with open('ex_user1.json', 'w', encoding='utf-8') as f:
    json.dump(user_response1.json(), f, ensure_ascii=False, indent=4)

with open('ex_user2.json', 'w', encoding='utf-8') as f:
    json.dump(user_response2.json(), f, ensure_ascii=False, indent=4)

f.close()

print("Files updated")
