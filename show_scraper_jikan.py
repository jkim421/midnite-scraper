import requests
import time
from sys import argv, exit

from utils.mongo_connect import connect_to_midnite
from utils.db_actions_jikan import get_existing_data, insert_show, update_show
from utils.config import API_URL, ERROR_STATUSES, SLEEP_TIME, MAX_RETRIES
from utils.logging import log_show_info, log_error, log_retry

MAL_CLIENT_ID, MONGO_PASSWORD = argv

#  MAX CHECKED mal_id: 60000
#  CURRENT MAX mal_id: 56250
START_ID = 1
END_ID = 60000

def run_scraper():
    collection = connect_to_midnite(MONGO_PASSWORD)

    rate_limit_count = 0
    server_error_count = 0

    for mal_id in range(START_ID, END_ID):
        retries = 0

        while retries <= MAX_RETRIES:
            print(f"Sending GET request for { mal_id }...\n")

            res = requests.get(
                f"{API_URL}/{mal_id}/full",
                headers={
                    "Content-Type": 'application/json',
                }
            )

            status = res.status_code

            print(f"STATUS        {status}")

            if status == 404:
                print(f"NO DATA for mal_id: {mal_id}...\n")

                break
            elif status == 429:
                print(f"RATE LIMITED - retrying fetch for {mal_id}...\n")

                rate_limit_count+= 1
                
                retries += 1
                time.sleep(1)
            elif status == 500:
                print(f"JIKAN SERVER ERROR - retrying fetch for {mal_id}...\n")

                server_error_count += 1

                retries += 1
                time.sleep(10)
            else:
                show_data = res.json()["data"]

                if (show_data["status"]) == 404:
                    print(f"RECEIVED STATUS 200, BUT 404 NO DATA for mal_id: {mal_id}...\n")
                    break
                if (show_data["status"]) == 500:
                    print(f"RECEIVED STATUS 200, BUT 500 SERVER ERROR for mal_id: {mal_id}...\n")
                    break


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
                        show_id = insert_show(show_data, collection, mal_id)
                        print(f"INSERT for show { show_id } succeeded...")

                break

            if retries > MAX_RETRIES:
                print(f"MAX RETRIES reached for mal_id {mal_id}...")
                continue

        print(f"\n----------------------------------------------------------------\n")

        time.sleep(SLEEP_TIME)

    print(f"\n----------------------------------------------------------------\n")
    print(f"rate_limit_count: {rate_limit_count}")
    print(f"server_error_count: {server_error_count}")
    print(f"\n----------------------------------------------------------------\n")

run_scraper()