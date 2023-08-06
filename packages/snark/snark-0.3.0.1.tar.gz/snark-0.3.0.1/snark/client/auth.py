import snark
from snark import config
from snark.log import logger
from snark.client.base import SnarkHttpClient
from snark.exceptions import SnarkException

class AuthClient(SnarkHttpClient):
    """
    Authentication through rest api
    """
    def __init__(self):
        super(AuthClient, self).__init__()

    def check_token(self, access_token):
        auth = "Bearer {}".format(access_token)
        response = self.request('GET', config.CHECK_TOKEN_REST_SUFFIX, headers={"Authorization": auth})

        try:
            response_dict = response.json()
            is_valid = response_dict["is_valid"]
        except Exception as e:
            logger.error("Exception occured while validating token: {}.".format(e))
            raise SnarkException("Error while validating the token. \
                                  Please try logging in using username ans password.")

        return is_valid

    def get_access_token(self, username, password):
        response = self.request('GET', config.GET_TOKEN_REST_SUFFIX,
                                json={'username': username,
                                      'password': password})
        try:
            token_dict = response.json()
            token = token_dict['access_token']
        except Exception as e:
            logger.error("Exception occured while getting token: {}.".format(e))
            raise SnarkException("Error while loggin in. \
                                  Please try logging in using access token.")
        return token





