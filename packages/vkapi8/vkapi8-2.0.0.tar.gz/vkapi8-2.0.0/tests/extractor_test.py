import reprlib

import requests
import pprint

from vkapi8.api.client import ApiClient
from creds import login, password, client_id

ppprint = lambda x: pprint.pprint(x, compact=True)
extractor = None


def test_init():
    global extractor
    scope =  'friends,video'
    client = ApiClient(login, password, client_id, scope, debug=True)
    extractor = client.extractor


def test_validate():
    print('-----------------CLEAN VALIDATE---------------')
    ids1 = extractor.validate_users(list(range(12345665, 12345765)))
    print('clean len: ', len(ids1['clean']))
    print('filtered len: ', len(ids1['filtered']['banned'] + ids1['filtered']['abandoned'] + ids1['filtered']['excluded']))
    print('-----------------OLD_VALIDATE---------------')
    ids2 = extractor.validate_users(list(range(13345665, 13345765)), days_to_del=30)
    print('clean len: ', len(ids2['clean']))
    print('filtered len: ', len(ids2['filtered']['banned'] + ids2['filtered']['abandoned'] + ids2['filtered']['excluded']))
    print('-----------------FILTER_VALIDATE---------------')
    ids3 = extractor.validate_users(list(range(14345665, 14345765)),
            fields='country', filter_func=lambda x: 'country' in x and x['country']['id'] == 1)
    print('clean len: ', len(ids3['clean']))
    print('filtered len: ', len(ids3['filtered']['banned'] + ids3['filtered']['abandoned'] + ids3['filtered']['excluded']))


def test_extract_all_members():
    group_url = 'https://vk.com/jazzcafeunderground'
    print('---------------- EXTRACT_ALL_MEMBERS-----------')
    ppprint(extractor.extract_all_members(group_url))


def test_extract_all_subs():
    user_url = 'https://vk.com/hmmmmmmm_m'
    print('---------------- EXTRACT_ALL_SUBS-----------')
    ppprint(extractor.extract_all_subs(user_url))


def test_extract_friends():
    user_url = 'https://vk.com/hmmmmmmm_m'
    print('---------------- EXTRACT_ALL_FRIENDS-----------')
    ppprint(extractor.extract_friends(user_url))


def test_extract_groups_members():
    groups_urls = list(range(123456, 123556))
    print('---------------- EXTRACT_GROUPS_MEMBERS-----------')
    for chunk in extractor.extract_groups_members(groups_urls, fields='country'):
        ppprint(chunk)


def test_extract_users_extended_info():
    users_urls = list(range(12345665, 12345765))
    print('----- EXTRACT_USERS_EXTENDED_INFO_MEMBERS---------')
    for data_chunk in extractor.extract_users_extended_info(users_urls,
                                                              ["friends", "subs",
                                                               "publics", "groups",
                                                               "videos"]):
        ppprint(next(iter(data_chunk.items())))


def test_extract_groups_info():
    groups_urls = list(range(20000000, 20003000))
    print('---------------- EXTRACT_GROUPS_INFOS-----------')
    for chunk in extractor.extract_groups_info(groups_urls,
            fields='description,age_limits,city,country,status'):
        ppprint(chunk[:10])
