import logging
import unittest

from sqlalchemy.exc import ProgrammingError
from sqlalchemy_utils import create_database, drop_database

from fasvaorm import init_engine, init_session_factory, init_session, close_session
from fasvaorm.models import Base

# check if running in gitlab-ci
import os

gitlab_ci_var = os.environ.get('CI_ENVIRONMENT_URL')

if gitlab_ci_var is None:
    # local testing
    host = '127.0.0.1'
else:
    # testing on gitlab-ci
    host = 'mysql'


TEST_DB_CONFIG = {
    'user': 'root',
    'host': host,
    'database': 'testing',
    'password': 'mysql'
}

DB_URL = url = "mysql+pymysql://{user}:{password}@{host}/{database}".format(**TEST_DB_CONFIG)


class EngineTestCase(unittest.TestCase):

    def setUp(self):

        # create the test database
        try:
            create_database(DB_URL)
        except ProgrammingError:
            drop_database(DB_URL)

            create_database(DB_URL)

        self.engine = init_engine(DB_URL,
                                  # unlimited number of connections
                                  pool_size=0,
                                  # set connection timeout to 50 minutes
                                  pool_timeout=300)

        init_session_factory(self.engine)
        self.session = init_session()

        # setup bindings and create tables
        Base.metadata.bind = self.engine
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        close_session()

        drop_database(DB_URL)
