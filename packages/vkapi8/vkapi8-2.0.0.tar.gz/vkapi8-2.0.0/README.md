# VKApi8, Python3 based

Usage:
```
from vk_api8.api import ApiClient

login = "+78005553535"
password = "shashlichok72"
client = "12345678" #VK App client id
scope = "friends,messages,groups" #OPTIONAL
version = "5.69" #Api version OPTIONAL
session = requests.Session() #OPTIONAL

client = ApiClient(login, password, client, scope, version, session)
```

Extractor:
```
extractor = client.extractor
user_id = '125341435'
count, user_friends = extractor.extract_friends(user_id)
```

Instalation:
--------------------

``pip3 install vkapi8``
  
