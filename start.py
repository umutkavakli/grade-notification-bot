import yaml
import time
import requests
from scrapper import initialize, check

def send(message, token, chat_id):
    message_url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(message_url)

if __name__ == '__main__':

    with open('info.yaml', 'r') as file:
        info = yaml.safe_load(file)

    driver, course_table, grade_columns = initialize(info['id'], info['password'], info['url'])

    while True:
        time.sleep(info['interval'])
        messagge, status, course_table = check(driver, course_table, grade_columns)

        if status:
            send(messagge, info['token'], info['chat_id'])
