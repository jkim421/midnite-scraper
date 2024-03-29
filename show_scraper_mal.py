import requests
import time
from sys import argv, exit

from utils.mongo_connect import connect_to_midnite
from utils.db_actions_mal import get_existing_data, insert_show, update_show
from utils.config import API_URL, API_FIELDS, ERROR_STATUSES, SLEEP_TIME
from utils.logging import log_show_info, log_error, log_retry

MAL_CLIENT_ID, MONGO_PASSWORD, START_ID, END_ID = argv

def run_scraper():
  collection = connect_to_midnite(MONGO_PASSWORD)

  for mal_id in range(START_ID, END_ID):
      print(f"Sending GET request for { mal_id }...\n")

      res = requests.get(
          f"{API_URL}/{mal_id}?fields={API_FIELDS}",
          headers={
              "Content-Type": 'application/json',
              "X-MAL-CLIENT-ID": MAL_CLIENT_ID,
          }
      )

      status = res.status_code
      print(f"STATUS        {status}")

      if status == 403:
          log_retry(res, mal_id)
          time.sleep(5)
      else:
          show_data = res.json()

          if status in ERROR_STATUSES:
              log_error(show_data)

          else:
              if "title" in show_data:
                  log_show_info(show_data)

              prev_data = get_existing_data(mal_id, collection)

              if prev_data:
                  show_id = update_show(prev_data, show_data, collection, mal_id)
                  if show_id != None:
                    print(f"UPDATE for show { show_id } succeeded...")
                  else:
                    print(f"FAILED to UPDATE show { show_id }...")   
              else:
                  show_id = insert_show(show_data, collection, mal_id)
                  print(f"INSERT for show { show_id } succeeded...")

          print(f"\n----------------------------------------------------------------\n")

          time.sleep(SLEEP_TIME)

run_scraper()
