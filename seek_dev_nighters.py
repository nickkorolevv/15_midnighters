import requests
import datetime
import argparse


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("pages")
    return parser


def load_data(page_num):
    url = "https://devman.org/api/challenges/solution_attempts/"
    page = page_num
    param = {"page": page}
    response_from_dev = requests.get(url, params=param)
    return response_from_dev.json()


def get_users(decoded_json):
    get_users_dict = {}
    for user in decoded_json["records"]:
        time = datetime.datetime.fromtimestamp(user["timestamp"])
        formatted_time = time.strftime('%H:%M:%S')
        get_users_dict.update({user["username"]: formatted_time})
    return get_users_dict


def get_midnighters(users):
    night_start = "00:00:00"
    night_end = "06:00:00"
    midnighters_dict = {}
    for user, time in users.items():
        if night_start <= time < night_end:
            midnighters_dict.update({user: time})
    return midnighters_dict


def print_midnighters(midnighters):
    print("Совы:", midnighters)


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    pages = int(namespace.pages)
    for page in range(1, pages):
        print("Страница {}".format(page))
        decoded_json = load_data(page)
        users = get_users(decoded_json)
        midnighters = get_midnighters(users)
        print_midnighters(midnighters)
