import pandas as pd
import re
import pickle

df = pd.read_csv('train.csv')
df2 = pd.read_csv('test.csv')
# url = df['url'][0]
# print(df.head())

with open('url_cotent.txt', 'rb') as f:
    content_state = pickle.load(f)

try:
    with open('html_content2_missing_dict.txt', 'rb') as f:
        html_content2_missing_dict = pickle.load(f)
except:
    html_content2_missing_dict = {}


count = 0
right_pred = 0
found_num = 0
right_num = 0

content_list = content_state.values()
print(len(content_list))

for index, row in df.iterrows():
    html_content = row['html_content']
    html_content = re.findall(r'<p>(.*?)</p>', html_content)
    try:
        html_content1 = re.sub('<.*?>', '', html_content[0])
        html_content1 = html_content1.lstrip()
        html_content1 = html_content1[:50]
        if len(html_content1) < 2:
            html_content1 = True
    except:
        html_content1 = True

    try:
        html_content2 = re.sub('<.*?>', '', html_content[1])
        html_content2 = html_content2.lstrip()
        html_content2 = html_content2[:50]
    except:
        try:
            html_content2 = re.sub('<.*?>', '', html_content[2])
            html_content2 = html_content2.lstrip()
            html_content2 = html_content2[:50]
        except:
            html_content2 = ''
            html_content2_missing = True

    if html_content1 == True:
        pred = 0
    else:
        for content in content_list:
            if html_content1 in content and html_content2 in content:
                if html_content2_missing:
                    missing_dict = {html_content1: row['state']}
                    html_content2_missing_dict.update(missing_dict)
                    with open('html_content2_missing_dict.txt', 'wb') as f:
                        pickle.dump(html_content2_missing_dict, f)
                # else:
                #     pred = 1
                pred = 1

                print('My contents', row['state'], html_content1, html_content2)
                if html_content2 == '':
                    print(html_content)
                if pred == row['state']:
                    right_num += 1
                found_num += 1
                break
            else:
                pred = 0
    count += 1
    if pred == row['state']:
        # print('Right Prediction')
        right_pred += 1
        print(count, right_pred, found_num, right_num, end='\r')
#     if pred == 1:
#         print(html_content)
#         found_num += 1
#
print(count, right_pred, found_num, right_num, right_num / found_num)
