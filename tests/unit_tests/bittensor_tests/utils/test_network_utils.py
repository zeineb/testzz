from bittensor import utils
import unittest.mock as mock
from unittest.mock import MagicMock
import os 
import requests
import urllib
import pytest

def test_int_to_ip_zero():
    assert utils.networking.int_to_ip(0) == "0.0.0.0"
    assert utils.networking.ip_to_int("0.0.0.0") == 0
    assert utils.networking.ip__str__(4, "0.0.0.0", 8888) == "/ipv4/0.0.0.0:8888" 

def test_int_to_ip_range():
    for i in range(10):
        assert utils.networking.int_to_ip(i) == "0.0.0." + str(i)
        assert utils.networking.ip_to_int("0.0.0." + str(i)) == i
        assert utils.networking.ip__str__(4, "0.0.0."+ str(i), 8888) == "/ipv4/0.0.0." + str(i) + ":8888"

def test_int_to_ip4_max():
    assert utils.networking.int_to_ip(4294967295) == "255.255.255.255"
    assert utils.networking.ip_to_int( "255.255.255.255") == 4294967295
    assert utils.networking.ip__str__(4, "255.255.255.255", 8888) == "/ipv4/255.255.255.255:8888"

def test_int_to_ip6_zero():
    assert utils.networking.int_to_ip(4294967296) == "::1:0:0"
    assert utils.networking.ip_to_int("::1:0:0") == 4294967296
    assert utils.networking.ip__str__(6, "::1:0:0", 8888) == "/ipv6/::1:0:0:8888"

def test_int_to_ip6_range():
    for i in range(10):
        assert utils.networking.int_to_ip(4294967296 + i) == "::1:0:" + str(i)
        assert utils.networking.ip_to_int("::1:0:" + str(i)) == 4294967296 + i
        assert utils.networking.ip__str__(6, "::1:0:" + str(i), 8888) == "/ipv6/::1:0:" + str(i) + ":8888"

def test_int_to_ip6_max():
    max_val = 340282366920938463463374607431768211455
    assert utils.networking.int_to_ip(max_val) == 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'
    assert utils.networking.ip_to_int('ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff') == max_val
    assert utils.networking.ip__str__(6, "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff", 8888) == "/ipv6/ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff:8888"

def test_int_to_ip6_overflow():
    overflow = 340282366920938463463374607431768211455 + 1
    try:
        utils.networking.int_to_ip(overflow) 
    except:
        assert True

def test_int_to_ip6_underflow():
    underflow = -1
    try:
        utils.networking.int_to_ip(underflow) 
    except:
        assert True

def test_get_external_ip():
    assert utils.networking.get_external_ip()

def test_get_external_ip_os_broken():
    class fake():
        def readline(self):
            return 1
    def mock_call():
        return fake()
        
    with mock.patch.object(os, 'popen', new=mock_call):
        assert utils.networking.get_external_ip()

def test_get_external_ip_os_request_urllib_broken():
    class fake():
        def readline(self):
            return 1
    def mock_call():
        return fake()

    class fake_s():
        def text(self):
            return 1
    def mock_call_two():
        return fake_s()

    class fake_a():
        def urlopen(self):
            return 1


    with mock.patch.object(os, 'popen', new=mock_call):
        with mock.patch.object(requests, 'get', new=mock_call_two):
            urllib.request= MagicMock(return_value = fake_a()) 
            with pytest.raises(Exception):
                assert utils.networking.get_external_ip()

if __name__ == "__main__":
    test_get_external_ip()
