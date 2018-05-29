import requests
from datetime import datetime
import pytz


def load_data():
    url = "https://devman.org/api/challenges/solution_attempts/"
    page = 1
    number_of_pages = 1
    while page <= number_of_pages:
        devman_response = requests.get(url, params={"page": page})
        page_info = devman_response.json()
        number_of_pages = page_info["number_of_pages"]
        for record in page_info["records"]:
            yield record
        page += 1


def get_local_time(time_stamp, timezone):
    local_time = datetime.fromtimestamp(time_stamp, tz=pytz.timezone(timezone))
    return local_time.hour


def get_midnighters(dev_users):
    get_users_dict = {}
    for user in dev_users:
        time = get_local_time(user["timestamp"], user["timezone"])
        get_users_dict.update({user["username"]: time})
    night_start = 0
    night_end = 6
    midnighters_list = []
    for user, time in get_users_dict.items():
        if night_start <= time < night_end:
            midnighters_list.append(user)
    return midnighters_list


def print_midnighters(midnighters):
    print("Совы: ")
    for user in midnighters:
        print(user)


if __name__ == "__main__":
    dev_users = load_data()
    midnighters = get_midnighters(dev_users)
    print_midnighters(midnighters)
