import re
import itertools


def get_region(api, query, city_id):
    json_response = api.api_request('database.getCities', {'country_id':1, 'q':query})
    if json_response.get('error'):
        raise Exception("Error while getting region, error_code=".format(
            str(json_response['error']['error_code'])))
    if not json_response['response']['items']:
        return None
    for item in json_response["response"]["items"]:
        if 'region' in item:
            if item["id"] == city_id:
                return item["region"]
    return json_response['response']['items'][0]["title"]


def group_url_to_id(api, group_url):
    group_url = str(group_url).split('/')[-1].strip()
    after_id_digits = re.match(r'(club|public)!(\d*)', group_url)
    if after_id_digits:
        return int(after_id_digits.group(2))
    return group_url


def user_url_to_id(api, user_url):
    user_url = str(user_url).split('/')[-1].strip()
    after_id_digits = re.match(r'(id)*(\d*)', user_url)
    if after_id_digits and after_id_digits.group(2):
        return int(after_id_digits.group(2))
    return get_user_id(api, user_url)


def get_user_id(api, link):
    domain = link.split("/")[-1]
    resp = api.api_request('users.get', {'user_ids':domain})
    if resp.get('error'):
        raise MethodException('''Error while getting user_id,
         error: {}'''.format(str(resp['error'])))
    return resp['response'][0]['id']


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"

    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)
