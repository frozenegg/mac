from bs4 import BeautifulSoup
import requests
import random

payload1 = {
    'player[email]': 'silicondoo@gmail.com',
    'player[password]': 'pu7wrnvx56t85'
}

temp_list = [35.8, 35.9, 36.0, 36.1, 36.2]
body_temp = random.choice(temp_list)

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

s = requests.Session()
r = s.get('https://www.one-tap.jp/players/sign_in')
print(r.text)
soup = BeautifulSoup(r.text, features="lxml")
auth_token = soup.find(attrs={'name': 'authenticity_token'}).get('value')
payload1['authenticity_token'] = auth_token
payload2['authenticity_token'] = auth_token

r = s.post('https://www.one-tap.jp/players/sign_in', data=payload1)
print(r.text)
soup = BeautifulSoup(r.text, features="lxml")
auth_token = soup.find(attrs={'name': 'csrf-token'}).get('content')
payload2['authenticity_token'] = auth_token
r = s.get('https://www.one-tap.jp/teams/2873/player/condition_records/')
# print(r.text)
r = s.post('https://www.one-tap.jp/teams/2873/player/condition_records/', data=payload2)
print(r.text)
print(body_temp)
