import pytest
from random import choices
from collections import namedtuple
import iplocalize
import requests
from geoip2.database import Reader

one_ip = ['1.2.3.4', '8888']
many_ip = [ [ '1.2.3.%s' % (str((port * 1234) % 255)), str(port) ] for port in choices(range(8192, 32768), k=2000) ]
# just random IPs and ports

class FakeReturn: 
    '''
    geoip2 and requests behavior rely on non-public datas, let's fake those
    '''
    @staticmethod
    def get(self, proxies, timeout):
        class Response:
            status_code = 200
            elapsed = namedtuple('elapsed', 'total_seconds')
            elapsed.total_seconds = lambda: 1.0
        return Response

def test_localize(monkeypatch):
    monkeypatch.setattr(requests, 'get', FakeReturn.get)
    expected = { 'ip': ':'.join(one_ip), 'cc': 'PC', 'time': 1.0 }
    loc = iplocalize.IPLoc(geolite_file='./tests/fake-data.mmdb')
    assert loc.localize(one_ip) == expected

def test_threaded_localize(monkeypatch):
    monkeypatch.setattr(requests, 'get', FakeReturn.get)
    expected = [ { 'ip': ':'.join(ip), 'cc': 'PC', 'time': 1.0 } for ip in many_ip ]
    loc = iplocalize.IPLoc(geolite_file='./tests/fake-data.mmdb')
    assert loc.threaded_localize(many_ip) == expected

