import numpy as np
import pandas as pd
import json
import requests
from urllib.request import urlopen
from datetime import datetime, timedelta
import re

from functions.auxiliary_functions import getResponseStatus, getMembersCount, getWallLength


# This method is designed to collect all members of a particular group
# Here you can find an example of how one can use TypeScript like language to execute code efficiently on server side
def getVkGroupMembers(group_id, access_token):
    vk_ids = []
    offset = 0
    MembersCount = getMembersCount(group_id, access_token)
    while offset < MembersCount:
        code = ''.join(str('''
        var memb=[];
        var i=1;
        var offset=''' + str(offset) + ''';

        while (i<26)
        {;
        memb=memb%2BAPI.groups.getMembers({"group_id":"''' + group_id + '''", "count":1000,
        "offset":offset}).items;
        offset=offset%2B1000;
        i=i%2B1;
        };

        return memb;
        ''').splitlines())

        link = 'https://api.vk.com/method/execute?&code=' + code + '&access_token=' + access_token + '&v=5.85'
        r = requests.get(link)
        jsonObj = json.loads(r.text)
        if getResponseStatus(jsonObj) == 'error':
            continue
        vk_ids.extend(jsonObj.get('response'))
        offset = offset + 25000
    print('Quantity of members collected throughout passed groups: ' + str(len(vk_ids)))
    return vk_ids


# Concatenate all members of multiple groups choice
def getAllGroupVkIds(group_ids, access_token):
    df = pd.DataFrame(columns=['vk_id', 'group_id'])
    for group_id in group_ids:
        group_members = getVkGroupMembers(group_id, access_token)
        temp_df = pd.DataFrame(group_members, columns=['vk_id'])
        temp_df['group_id'] = group_id
        df = pd.concat([df, temp_df])
    return df


# Collect people's names by their vk ids
def getVkIdsNames(arr, access_token):
    print("Now collecting names. It may take some time...")
    df_names = pd.DataFrame(columns=['vk_id', 'name', 'surname'])
    offset = 0

    while offset < len(arr):
        print("Numbers of names collected: " + str(offset))
        code = ''.join(str('''
        var memb=[];
        var it=1;
        var arr=''' + str(arr[offset:offset + 9000]) + ''';
        var in=0;

        while (it<10)
        {;
        memb=memb + API.users.get({"user_ids":arr.slice(in, in + 1000)});
        in=in + 1000;
        it=it + 1;
        };

        return memb;
        ''').splitlines())

        link = 'https://api.vk.com/method/execute'
        r = requests.post(link, data={'code': code, 'access_token': access_token, 'v': '5.85'})

        if getResponseStatus(json.loads(r.text)) == 'error':
            continue
        vk_id_info = json.loads(r.text).get('response')

        df_temp = pd.DataFrame(
            [[vk_id_info[i].get('id'), vk_id_info[i].get('first_name'), vk_id_info[i].get('last_name')]
             for i in range(len(vk_id_info))], columns=['vk_id', 'name', 'surname'])
        df_names = pd.concat([df_names, df_temp])
        offset = offset + 9000

    return df_names


def getGroupWallData(domain, access_token):
    def extractPostAuthorId(x):
        try:
            return re.findall('\[id([0-9]*)', x)[0]
        except IndexError:
            return ''

    print("We are going to collect data of vk.com/" + domain + " group...")

    posts_data = pd.DataFrame(columns=['vk_id', 'text', 'date'])
    offset = 0
    while offset < getWallLength(domain, access_token):
        print("Already collected: " + str(offset))
        code = ''.join(str('''
        var posts=[];
        var i=1;
        var domain="''' + domain + '''";
        var offset=''' + str(offset) + ''';

        while (i<13)
        {;
        posts=posts+([API.wall.get({"domain":domain, "offset":offset, "count":100}).items@.text,API.wall.get({"domain": domain, "offset":offset, "count":100}).items@.date]);
        offset=offset+100;
        i=i+1;
        };

        return posts;
        ''').splitlines())

        link = 'https://api.vk.com/method/execute'
        r = requests.post(link, data={'code': code, 'access_token': access_token, 'v': '5.85'})
        if getResponseStatus(json.loads(r.text)) == 'error':
            continue
        offset = offset + 1200
        temp_df = pd.DataFrame(
            np.array([[text1 for text100 in json.loads(r.text).get('response')[::2] for text1 in text100],
                      [date1 for date100 in json.loads(r.text).get('response')[1::2] for date1 in
                       date100]]).transpose(),
            columns=['text', 'date'])
        temp_df['vk_id'] = temp_df.text.apply(extractPostAuthorId)
        temp_df['date'] = temp_df.date.apply(
            lambda x: datetime.utcfromtimestamp(int(x) + 10800).strftime('%Y-%m-%d %H:%M:%S'))
        posts_data = pd.concat([posts_data, temp_df], sort=False)
    posts_data = posts_data.replace({r'\s+$': '', r'^\s+': ''}, regex=True).replace(r'\n', ' ', regex=True)
    return posts_data
