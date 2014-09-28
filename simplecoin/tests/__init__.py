import simplecoin
import unittest
import datetime

import simplecoin.models as m

from decimal import Decimal
from simplecoin import db


class UnitTest(unittest.TestCase):
    """ Represents a set of tests that only need the database iniailized, but
    no fixture data """
    def setUp(self, **kwargs):
        extra = dict()
        extra.update(kwargs)
        app = simplecoin.create_app('webserver', configs=['test.toml'], **extra)
        with app.app_context():
            self.db = simplecoin.db
            self.setup_db()

        self.app = app
        self._ctx = self.app.test_request_context()
        self._ctx.push()
        self.client = self.app.test_client()

    def tearDown(self):
        # dump the test elasticsearch index
        db.session.remove()
        db.drop_all()

    def setup_db(self):
        self.db.drop_all()
        self.db.create_all()
        db.session.commit()

    def make_block(self, **kwargs):
        vals = dict(currency="LTC",
                    height=1,
                    found_at=datetime.datetime.utcnow(),
                    time_started=datetime.datetime.utcnow(),
                    difficulty=12,
                    merged=False,
                    algo="scrypt",
                    total_value=Decimal("50"))
        vals.update(kwargs)
        blk = m.Block(**vals)
        db.session.add(blk)
        return blk


class RedisUnitTest(UnitTest):
    def setUp(self):
        UnitTest.setUp(self)
        self.app.redis.flushdb()
