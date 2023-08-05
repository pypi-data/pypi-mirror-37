import logging

import pytest

from falcon_helpers.contrib.logging import logrequest


@logrequest()
class FakeResource():
    def on_get(self, req, resp):
        pass

    def on_post(self, req, resp):
        raise Exception('Bad')

    def on_put(self, req, resp):
        pass

    def on_delete(self, req, resp):
        pass


class FakeResource2():
    @logrequest()
    def on_get(self, req, resp):
        pass


def test_class_decoration(client, caplog):

    client.app.add_route('/', FakeResource())

    with caplog.at_level(logging.DEBUG):
        client.simulate_get('/')

        assert len(caplog.records) == 2
        start, finish = caplog.records
        assert start.message.startswith('FakeResource.on_get called')
        assert finish.message.startswith('FakeResource.on_get succeeded')

    caplog.clear()

    with caplog.at_level(logging.DEBUG):
        with pytest.raises(Exception):
            client.simulate_post('/')

        assert len(caplog.records) == 2
        start, finish = caplog.records
        assert start.message.startswith('FakeResource.on_post called')
        assert finish.message.startswith('FakeResource.on_post raised Exception')


def test_method_decoration(client, caplog):

    client.app.add_route('/', FakeResource2())

    with caplog.at_level(logging.DEBUG):
        client.simulate_get('/')

        assert len(caplog.records) == 2
        start, finish = caplog.records
        assert start.message.startswith('FakeResource2.on_get called')
        assert finish.message.startswith('FakeResource2.on_get succeeded')
