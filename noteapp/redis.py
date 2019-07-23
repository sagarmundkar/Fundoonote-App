import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

"""This class is used to set , get , slength from Redis cache"""


class RedisMethods:
    """ this method is used to add the data to redis"""

    def set_token(self, key, value):
        r.set(key, value)
        print('token set')

    """this method is used to get the data out of redis"""

    def get_token(self, key):
        token = r.get(key)
        return token

    """ This method is used to display the length of value"""

    def length_str(self, key):
        token_len = r.strlen(key)
        return token_len
