def log_show_info(show_data):
    print(f'''
TITLE         {show_data["title"]}
ENG TITLE     {show_data['alternative_titles']["en"]}
ALT TITLES    {show_data['alternative_titles']["synonyms"]}

SYNOPSIS
{show_data['synopsis']}
    ''')


def log_retry(res, mal_id):
    print(f'''
{res.text}
RETRYING
MAL_ID        {mal_id}
----------------------------------------------------------------

    ''')


def log_error(show_data, fail_count):
    print(f"ERROR         {show_data['error']}")
    print(f"FAIL COUNT    {fail_count}")
