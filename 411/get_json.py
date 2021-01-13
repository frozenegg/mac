# https://www.kickstarter.com/projects/search.json?search=id&term=Unique%20FPS%20survival

import requests
import json
import pandas as pd
import re
import pickle
import os

def get_urls(filename):
    try:
        with open('urls.txt', 'rb') as f:
            urls = pickle.load(f)
    except:
        urls = []

    # with open('urls.txt', 'rb') as f:
    #     urls = pickle.load(f)

    df = pd.read_csv(filename)
    for index, row in df.iterrows():
        url = json.loads(row['urls'])['web']['project'].split('?ref')[0]
        if row['state'] == 'successful':
            if url not in urls:
                urls.append(url)
                urls = list(set(urls))
                print(url)
            else:
                print('Already added')
        else:
            print("Not successful")
            continue

    # print(urls_states)

    with open('urls.txt', 'wb') as f:
        pickle.dump(urls, f)

    done_filename = list(set(done_filename))
    print(done_filename)

dirname_list = []

root_dirname = '/Volumes/dolphin/kick_csv3/'

for directory_name in os.listdir(root_dirname):
    dirname_list.append(directory_name)

print(dirname_list)


# root_dir = '/Volumes/dolphin/kick_csv/'
# dirname = '/Volumes/dolphin/kick_csv/Kickstarter_2019-08-15T03_20_03_022Z'
#
# for filename in os.listdir(dirname):
#     # print(dirname + '/' + filename)
#     get_urls(dirname + '/' + filename)
# get_urls("/Volumes/dolphin/kick_csv/Kickstarter_2019-08-15T03_20_03_022Z")

done_filename = []
i = 0
for dirname in dirname_list:
    root_dir = root_dirname + dirname
    if '._Kickstarter' in dirname:
        continue
    done_filename.append(dirname)
    done_filename = list(set(done_filename))
    print(i, ' ------------------------------------------------------------------------------------ ', dirname)
    print(done_filename)
    i += 1
    try:
        for filename in os.listdir(root_dir):
            print('===================================================================================== ')
            # print(dirname + '/' + filename)
            get_urls(root_dir + '/' + filename)
    except:
        continue
