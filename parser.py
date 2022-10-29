import requests
import pandas as pd
import json
import logging
import time

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


url = 'https://jsonplaceholder.typicode.com/users/'


def find_emails(url):
    st = time.time()
    info_users = requests.get(url).json()
    emails = []
    for i in range(len(info_users)):
        emails.append(info_users[i]['email'])
    et = time.time()
    delta_time = et - st
    logging.info(f"delta_time for find_emails = {delta_time}")
    return list(map(lambda x: f'"{x}"', emails))


emails = (find_emails(url))
write_emails = pd.DataFrame(emails).transpose().to_csv(r'emails.csv', header=0, index=False, quotechar=',')
read_emails = pd.read_csv('emails.csv', sep=',')


def find_id(url):
    st = time.time()
    info_users = requests.get(url).json()
    ids = []
    for i in range(len(info_users)):
        logging.info(f"Starts parsing for {info_users[i]['email']}")
        for j in read_emails.columns.tolist():
            if info_users[i]['email'] == j:
                ids.append(info_users[i]['id'])
    et = time.time()
    delta_time = et - st
    logging.info(f"delta_time for find_id = {delta_time}")
    return ids


def get_info():

    ids = find_id(url)
    logging.info(f'Count of users: {len(ids)}')
    i = 1
    while i <= len(ids):
        st = time.time()
        post = rf"https://jsonplaceholder.typicode.com/users/%s/posts" % i
        album = rf"https://jsonplaceholder.typicode.com/users/%s/albums" % i
        todo = rf"https://jsonplaceholder.typicode.com/users/%s/todos" % i
        response_post = requests.get(post).text
        response_album = requests.get(album).text
        response_todo = requests.get(todo).text
        dict = {'posts': json.loads(response_post), 'albums': json.loads(response_album),
                'todos': json.loads(response_todo)}
        with open('./users/{}.json'.format(i), 'w') as file:
            json.dump(dict, file, indent=4)
        et = time.time()
        delta_time = et - st
        logging.info("delta_time for get_info for {} user = {}".format(i, delta_time))
        i += 1


get_info()
