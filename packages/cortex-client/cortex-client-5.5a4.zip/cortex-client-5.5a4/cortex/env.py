import os
from .utils import get_cortex_profile

DEFAULT_API_ENDPOINT = 'https://api.cortex.insights.ai'


class CortexEnv:

    def __init__(self):
        profile = get_cortex_profile()

        self.api_endpoint = os.getenv('CORTEX_URI', profile.get('url'))
        self.token = os.getenv('CORTEX_TOKEN', profile.get('token'))
        self.account = os.getenv('CORTEX_ACCOUNT', profile.get('account'))
        self.username = os.getenv('CORTEX_USERNAME', profile.get('username'))
        self.password = os.getenv('CORTEX_PASSWORD')
