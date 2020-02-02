import json
from urllib.request import urlopen


# VK API has a limit of how much requests one can send to their server
# So I have to check if server had returned and error or not
def getResponseStatus(jsonObj):
    data = []
    for status, temp in jsonObj.items():
        data.append(status)
        return data[0]


# To extract all data about group members correctly and fastly by batches I have to control a number of members when
# requesting server
def getMembersCount(group_id, access_token):
    r = urlopen(
        'https://api.vk.com/method/groups.getById?group_ids=' + group_id + '&fields=members_count&access_token=' + access_token + '&v=5.85')
    groupInfo = json.loads(r.read().decode('utf-8'))
    try:
        return groupInfo.get('response')[0].get('members_count')
    except:
        return getMembersCount(group_id, access_token)


# Same about crawling a huge bunch of data like a wall
def getWallLength(domain, access_token):
    r1 = urlopen('https://api.vk.com/method/wall.get?domain=' + domain + '&access_token=' + access_token + '&v=5.92')
    groupInfo1 = json.loads(r1.read().decode('utf-8'))
    try:
        return groupInfo1.get('response').get('count')
    except:
        getWallLength(domain, access_token)