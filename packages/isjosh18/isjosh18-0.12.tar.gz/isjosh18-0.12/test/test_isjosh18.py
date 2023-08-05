from collections import namedtuple
import sys

try:
    from unittest import mock
except ImportError:
    import mock

import pytest
import requests

from isjosh18.__main__ import main, run, make_balloons


def test_invocation(stdout):
    with pytest.raises(SystemExit) as e:
        with mock.patch.object(sys, 'argv', ['isjosh18']):
            main()
    assert stdout().startswith('Josh')


def test_balloon_invocation(stdout):
    with pytest.raises(SystemExit) as e:
        with mock.patch.object(sys, 'argv', ['isjosh18', '--balloons', '--force', '--duration', '1']):
            main()
    assert 'party is over' in stdout()


def test_answer(stdout):
    Args = namedtuple('Args', ['balloons', 'force'])
    class MockResponse:
        def __init__(self, obj):
            self._json = obj
        def json(self):
            return self._json

    with mock.patch.object(requests, 'get', lambda _: MockResponse({'hasTurned18': True})):
        res = run(Args(force=False, balloons=False))
    assert res == 0
    assert 'is 18' in stdout()

    with mock.patch.object(requests, 'get', lambda _: MockResponse({'hasTurned18': False})):
        res = run(Args(force=False, balloons=False))
    assert res == 1
    assert 'is NOT 18' in stdout()


def test_balloons():
    with pytest.raises(KeyboardInterrupt) as e:
        make_balloons(
            width=50,
            speed=10,
            frequency=0.5,
            duration=1
        )
