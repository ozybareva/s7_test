import os
from ..settings import Settings


class FakeSettings(Settings):
    app_title_application: str = 'TEST CAMS service'

    class Config:
        if os.path.isfile('.env-test'):
            env_file = '.env-test'
        elif os.path.isfile('tests/.env-test'):
            env_file = 'tests/.env-test'
        elif os.path.isfile('../.env-test'):
            env_file = '../.env-test'
        else:
            raise FileNotFoundError('check where .env-test')
