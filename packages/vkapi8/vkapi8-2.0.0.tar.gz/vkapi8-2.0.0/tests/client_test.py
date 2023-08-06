import requests
from pprint import PrettyPrinter

from vkapi8.api.client import ApiClient
from creds import login, password, client_id

printer = PrettyPrinter()
client = None


def test_init():
    global client
    scope =  'groups'
    client = ApiClient(login, password, client_id, scope, debug=True)
    client_session = ApiClient(login, password, client_id, scope, debug=True, session=requests.Session())
    assert client_session.token == client.token


def test_extractor():
    extractor = client.extractor
    printer.pprint(('EXTRACTOR', [x for x in dir(extractor) if '__' not in x]))


def test_userapi():
    userapi = client.userapi
    printer.pprint(('USERAPI', [x for x in dir(userapi) if '__' not in x]))


def test_fake_request():
    print('------------TESTING FAKE REQUESTS-----------')
    printer.pprint(client.fake_request())
    for chunk in client.extractor.extract_users_info([x for i in range(30) for x in range(i*100, i*100 + 20)]):
        printer.pprint(chunk)

#for chunk in api.get_groups_by_id_generator(list(range(20000000, 20003000)),
#                                            'description,age_limits,city,country,status'):
#    printer.pprint(chunk[0])
