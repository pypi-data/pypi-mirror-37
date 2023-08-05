import sys
import unittest

from config_loader import ConfigLoader


class InfluxDBTest(unittest.TestCase):

    @staticmethod
    def test_influxdb():
        local = ConfigLoader('test.conf')
        assert local.config['influxdb']

    @staticmethod
    def test_influxdb_address():
        local = ConfigLoader('test.conf')
        assert local.config['influxdb']['address']

    @staticmethod
    def test_influxdb_port():
        local = ConfigLoader('test.conf')
        assert local.config['influxdb']['port']

    @staticmethod
    def test_influxdb_password():
        local = ConfigLoader('test.conf')
        assert local.config['influxdb']['password']

    @staticmethod
    def test_influxdb_user():
        local = ConfigLoader('test.conf')
        assert local.config['influxdb']['user']

    @staticmethod
    def test_influxdb_db():
        local = ConfigLoader('test.conf')
        assert local.config['influxdb']['db']


if __name__ == '__main__':
    unittest.main()
