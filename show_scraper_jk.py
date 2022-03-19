import requests
import time
from pprint import pprint

from utils.mongo_connect import connect_to_midnite
from utils.db_actions_jikan import get_existing_data, insert_show, update_show

collection = connect_to_midnite()

ERROR_CODES = [400, 404, 429, 500, 503]
LIMIT = 20000
mal_id = 58
#  CURRENT MAX mal_id: 50886
#  LAST HIT: 55231

for id in range(1, LIMIT):
    print(f"Sending GET request for { mal_id }...")

    res = requests.get(f"https://api.jikan.moe/v4/anime/{ mal_id }/")
    res_json = res.json()
    # res_status = res_json["data"]["status"]
    res_status = res_json["data"]["status"] if 'data' in res_json else res_json["status"]

    # pprint(res_json, sort_dicts=False)

    if res_status in ERROR_CODES:
        print(f"ERROR { res_status } ")
    else:
      show_data = res_json["data"]
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
    time.sleep(3)
    
