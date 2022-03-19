import requests
import time
from pprint import pprint

from utils.mongo_connect import connect_to_midnite
from utils.db_actions_mal import get_existing_data, insert_show, update_show

collection = connect_to_midnite()

MAL_CLIENT_ID="07a8d3c8462853cf1d3c6846bee02f45"
ERROR_MESSAGES = ["not-found"]

SAMPLE = 51000
mal_id = 15

#  CURRENT MAX mal_id: 50886
#  LAST HIT: 55231

for id in range(1, SAMPLE):
    print(f"Sending GET request for { mal_id }...")

    res = requests.get(
      f"https://api.myanimelist.net/v2/anime/{mal_id}?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,source,rating,background,recommendations,studios,statistics",
      headers={
        "Content-Type": 'application/json',
        "X-MAL-CLIENT-ID": "07a8d3c8462853cf1d3c6846bee02f45",
      }
    )
    show_data = res.json()

    if 'error' in show_data:
        print(f"ERROR {show_data['error']}")
    else:
      prev_data = get_existing_data(mal_id, collection)

      if prev_data:
          show_id = update_show(prev_data, show_data, collection, mal_id)
          if show_id != None:
            print(f"UPDATE for show { show_id } succeeded...")
      else:
          show_id = insert_show(show_data, collection, mal_id)
          print(f"INSERT for show { show_id } succeeded...")

    print('')
    print(f"---------------------- SLEEPING --------------------------")
    print('')

    mal_id += 1
    time.sleep(1)
