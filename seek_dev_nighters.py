import requests
import datetime
import pytz


def load_data():
    url = "https://devman.org/api/challenges/solution_attempts/"
    page = 1
    number_of_pages = 1
    while page <= number_of_pages:
        devman_response = requests.get(url, params={"page": page})
        page_info = devman_response.json()
        number_of_pages = int(page_info["number_of_pages"])
        for record in page_info["records"]:
            yield record
        page += 1


def local_time(time_stamp, timezone):
    local_date_time = datetime.datetime.fromtimestamp(
        float(time_stamp),
        tz=pytz.timezone(timezone)
    )
    return local_date_time.time()


def get_users(dev_users):
    get_users_dict = {}
    for user in dev_users:
        time = local_time(user["timestamp"], user["timezone"])
        get_users_dict.update({user["username"]: time})
    return get_users_dict


def get_midnighters(users):
    night_start = datetime.time(0, 0, 0)
    night_end = datetime.time(6, 0, 0)
    midnighters_dict = {}
    for user, time in users.items():
        if night_start <= time < night_end:
            midnighters_dict.update({user: time})
    return midnighters_dict


def print_midnighters(midnighters):
    print("Совы: ")
    for user, time in midnighters.items():
        print(user, time)


if __name__ == '__main__':
    dev_users = load_data()
    users = get_users(dev_users)
    midnighters = get_midnighters(users)
    print_midnighters(midnighters)
