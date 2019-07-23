import jwt
import self as self

from .redis import RedisMethods
from .models import User


def api_login_required(method):
    def token_verification(ref):
        retoken = RedisMethod.get_token(self, 'token')
        decoded_token = jwt.decode(retoken, 'secret', algorithms=['HS256'])
        print("decode token ", decoded_token)
        decoded_id = decoded_token.get('id')
        print("user id", decoded_id)
        user = User.objects.get(id=decoded_id)
        print("username", user)
        if decoded_id:
            return method(ref)
        else:
            raise PermissionError

    return token_verification


def note_login_required(function):
    """ This method is give the authorization to another method"""

    def token_verification(varg):
        from Fundoonotes.noteapp.views import r
        token_val = r.get_token('key')  # get the value of token from cache
        if token_val is None:
            raise Exception("Token is None")
        else:
            decoded_token = jwt.decode(token_val, 'Cypher', algorithms=['HS256'])
            decoded_id = decoded_token.get('username')
            print("user id", decoded_id)
            user = User.objects.get(username=decoded_id)  # validate the decoded_id with User id
            print("username", user)
            if decoded_id:
                return function(varg)  # if decoded id is found
            else:
                raise Exception("User Permission is Required")  # else raise exception User Permission is valid

    return token_verification
