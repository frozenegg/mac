from bs4 import BeautifulSoup
import requests
import random
import datetime
from datetime import datetime, timedelta, date
import json

today = date.today()
yesterday = today - timedelta(days=1)
two_days_ago = today - timedelta(days=2)
yesterday = str(yesterday)
two_days_ago = str(two_days_ago)

payload1 = {
    'player[email]': '',
    'player[password]': ''
}

s = requests.Session()
r = s.get('https://api.ouraring.com/v1/sleep?start={}&end{}&access_token=7JMT6BHEF3TI77K4M53ITWXXINLCV6SN'.format(two_days_ago, yesterday))
json_data = r.json()
temp_delta = json_data['sleep'][0]['temperature_delta']
abs_temp = 36.0

body_temp = abs_temp + temp_delta

payload2 = {
    'condition_record[condition_item_values_attributes][0][condition_item_field_id]': 23941,
    'condition_record[condition_item_values_attributes][1][condition_item_field_id]': 23942,
    'condition_record[condition_item_values_attributes][2][condition_item_field_id]': 23943,
    'condition_record[condition_item_values_attributes][3][condition_item_field_id]': 23944,
    'condition_record[condition_item_values_attributes][4][condition_item_field_id]': 23945,
    'condition_record[condition_item_values_attributes][5][condition_item_field_id]': 23946,
    'condition_record[condition_item_values_attributes][6][condition_item_field_id]': 33194,
    'condition_record[condition_item_values_attributes][0][float_value]': body_temp,
    'condition_record[condition_item_values_attributes][1][check_values][]': 23961,
    'condition_record[condition_item_values_attributes][2][check_values][]': 23964,
    'condition_record[condition_item_values_attributes][3][check_values][]': 23967,
    'condition_record[condition_item_values_attributes][4][check_values][]': 23970,
    'condition_record[condition_item_values_attributes][5][check_values][]': 23973,
    'condition_record[condition_item_values_attributes][6][check_values][]': 35439
}

r = s.get('https://www.one-tap.jp/players/sign_in')
# print(r.text)
soup = BeautifulSoup(r.text)
auth_token = soup.find(attrs={'name': 'authenticity_token'}).get('value')
payload1['authenticity_token'] = auth_token

r = s.post('https://www.one-tap.jp/players/sign_in', data=payload1)
# print(r.text)
soup = BeautifulSoup(r.text, features="lxml")
auth_token = soup.find(attrs={'name': 'csrf-token'}).get('content')
payload2['authenticity_token'] = auth_token
r = s.get('https://www.one-tap.jp/teams/2873/player/condition_records/')
# print(r.text)
r = s.post('https://www.one-tap.jp/teams/2873/player/condition_records/', data=payload2)
# print(r.text)
# print(body_temp)
