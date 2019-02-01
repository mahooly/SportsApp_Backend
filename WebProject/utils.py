from rest_auth.serializers import UserDetailsSerializer


def my_jwt_response_handler(token, user=None, request=None):
    print("jwt handled")
    return {
        'token': token,
        'temp': "temp",
        'user': UserDetailsSerializer(user, context={'request': request}).data
    }
