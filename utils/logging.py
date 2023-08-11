def log_show_info(show_data):
    print(f'''
MAL_ID        {show_data["mal_id"]}
TITLE         {show_data["title"]}
ENG TITLE     {show_data["title_english"]}
JP TITLE      {show_data["title_japanese"]}
    ''')


def log_retry(res, mal_id):
    print(f'''
{res.text}

RETRYING
MAL_ID        {mal_id}

----------------------------------------------------------------

    ''')


def log_error(show_data):
    print(f"ERROR         {show_data['error']}")
