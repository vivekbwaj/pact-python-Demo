import atexit
import unittest
from pact import Consumer, Provider
import requests
import ipdb
from shutil import copy


pact = Consumer('My Consumer').has_pact_with(Provider('My Provider')) #default port of pact-python is 1234, we can change by adding arg port=port#
pact.start_service()
atexit.register(pact.stop_service)

def posts():
    """Fetch a user object by user_name from the server."""
    uri = 'http://localhost:1234/posts'
    return requests.get(uri).json()

class GetPostsInfo(unittest.TestCase):
  def test_get_posts(self):
    expected = {
          "userId": 1,
          "id": 1,
          "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
          "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
        }

    (pact
     .given('The jsonplaceholder data exists')
     .upon_receiving('A request for post for user 1')
     .with_request('get', '/posts')
     .will_respond_with(200, body=expected))

    with pact:
      result = posts()

    self.assertEqual(result, expected)
 
    copy('my_consumer-my_provider.json','./providertest')
      



    ####################### 
        # ipdb.set_trace()  
        # pact._interactions[0]['response']['body']
        # pact-verifier --provider-base-url=http://localhost:3000 --pact-url=my_consumer-my_provider.json
     ###################### 
     # Provider states :
     #     --provider-states-setup-url
            # The URL which should be called to setup a specific provider state before a Pact is verified. 
            # This URL will be called with a POST request, and the JSON body {consumer: 'Consumer name', state: 'a thing exists'}. 