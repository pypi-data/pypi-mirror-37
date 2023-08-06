from six.moves.urllib.parse import urljoin
from social_core.backends.oauth import BaseOAuth2

class TUOAuth2(BaseOAuth2):
    name = 'tu'
    AUTH_SERVER = 'api.tu.ac.th'
    AUTHORIZATION_URL = 'https://{}/o/authorize'.format(AUTH_SERVER)
    ACCESS_TOKEN_URL = 'https://{}/o/token/'.format(AUTH_SERVER)
    REFRESH_TOKEN_URL = 'https://{}/o/token/'.format(AUTH_SERVER)
    ACCESS_TOKEN_METHOD = 'POST'
    REVOKE_TOKEN_METHOD = 'GET'
    USER_DATA_URL = 'https://{}/api/me'.format(AUTH_SERVER)

    SCOPE_SEPARATOR = ' '
    EXTRA_DATA = [
        ('expires_in', 'expires_in'),
        ('refresh_token', 'refresh_token'),
        ('scope', 'scope'),
    ]

    def get_user_id(self, details, response):
        return details['username']

    def get_user_details(self, response):
        res = {'username': response.get('username'),
                    'email': response.get('tumail') or '',
                    'first_name': response.get('firstname'),
                    'last_name': response.get('lastname'),
                }
        return res

    def user_data(self, access_token, *args, **kwargs):
        data = self._user_data(access_token)
        return data
                        
    def _user_data(self, access_token, path=None):
        return self.get_json(self.USER_DATA_URL, params={'access_token': access_token})
