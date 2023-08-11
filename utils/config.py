# API_URL = "https://api.myanimelist.net/v2/anime"
API_URL = "https://api.jikan.moe/v4/anime"
API_FIELDS = "id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,source,rating,background,recommendations,studios,statistics"

ERROR_STATUSES = [400, 405, 500]

SLEEP_TIME = 0.4

MAX_RETRIES = 5