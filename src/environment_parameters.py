import os


class EnvironmentParameters:
    user_pool_id = ""
    client_ids = ""
    issuer_url = ""
    region = ""

    def __init__(self):
        self.user_pool_id = os.getenv('USER_POOL_ID')
        self.region = os.getenv('REGION')
        self.client_ids = os.getenv('CLIENT_IDS')
        self.issuer_url = 'https://cognito-idp.{}.amazonaws.com/{}'.format(
            self.region, self.user_pool_id)
