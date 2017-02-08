import redis
from time import time
settings = dict(redis='redis 6379 0')
REDIS_POOL_SIZE = 1
NUM_KEYS = 50_000
BIG_KEY = 'big_key'

redis_conn_pool = redis.ConnectionPool(
    **dict(zip(('host', 'port', 'db'), settings["redis"].split())),
    max_connections=REDIS_POOL_SIZE)
cache = redis.StrictRedis(connection_pool=redis_conn_pool)
JSON_DOC = """{
    "_id": "589ba169637430378ea0c99d",
    "index": 0,
    "guid": "cf468213-a57e-4a85-bf1d-d3b40bb63c1c",
    "isActive": false,
    "balance": "$3,282.69",
    "picture": "http://placehold.it/32x32",
    "age": 20,
    "eyeColor": "blue",
    "name": "Casey Lawson",
    "gender": "female",
    "company": "MEDESIGN",
    "email": "caseylawson@medesign.com",
    "phone": "+1 (940) 557-3296",
    "address": "944 Pershing Loop, Cliff, Virgin Islands, 5755",
    "about": "Ut proident et cillum eu. Commodo sint deserunt cupidatat laborum aliquip aliquip. Proident velit laborum anim aliquip elit ad esse nisi et. In enim elit velit minim enim id est magna. Magna pariatur pariatur nostrud duis ut incididunt et in. Ad ex officia dolore nulla non incididunt amet do proident.\r\n",  # noqa
    "registered": "2014-08-16T12:45:07 -02:00",
    "latitude": 88.984883,
    "longitude": -24.001337,
    "tags": [
      "nisi",
      "adipisicing",
      "cupidatat",
      "ipsum",
      "mollit",
      "cupidatat",
      "aliquip"
    ],
    "friends": [
      {
        "id": 0,
        "name": "Deana Curry"
      },
      {
        "id": 1,
        "name": "Mccarthy Obrien"
      },
      {
        "id": 2,
        "name": "Sheri Craft"
      }
    ],
    "greeting": "Hello, Casey Lawson! You have 6 unread messages.",
    "favoriteFruit": "banana"
  },"""


def insert_keys():
    for x in range(NUM_KEYS):
        key = f'key_{x}'
    cache.set(key, JSON_DOC)
    cache.set([JSON_DOC for _ in range(NUM_KEYS)], BIG_KEY)


def get_tons_of_keys():
    pipe = cache.pipeline()
    for x in range(NUM_KEYS):
        pipe.get(f'key_{x}')
    result = pipe.execute()


def get_big_key():
    pipe = cache.pipeline()
    pipe.get(BIG_KEY)
    result = pipe.execute()


def measure_time(fnx):
    print('running: ', fnx.__name__)
    start = time()
    fnx()
    end = time()
    print(end - start)


if '__main__' == __name__:
    insert_keys()
    measure_time(get_tons_of_keys)
    measure_time(get_big_key)
