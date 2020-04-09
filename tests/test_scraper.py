import requests

from wikidatarefisland import Config, Scaraper
from wikidatarefisland.data_access import Storage
from wikidatarefisland.services import (ExternalIdentifierFormatter,
                                        SchemaorgPropertyMapper)


class MockResponse:
    def __init__(self, url):
        with open('data/test_response.html', 'r') as f:
            self.text = f.read()
        self.status_code = 200


class MockExternalIdentifierFormatter(ExternalIdentifierFormatter):
    def format(self, pid, value):
        if pid == 'P1':
            return {'url': 'https://example_with_schema.org/' + value}
        return {'url': 'https://example_without_schema.org/' + value}

class MockSchemaorgPropertyMapper(SchemaorgPropertyMapper):
    def get_mapping(self):
        return [{'property': 'P2360', 'url': 'http://schema.org/audience'}]


class MockStorage(Storage):
    def __init__(self):
        self.values = {}

    def get(self, key):
        return self.values.get(key, {})

    def store(self, key, value, raw=False):
        self.values[key] = value


class MockConfig(Config):
    def __init__(self):
        pass

    def get(self, key):
        if key == 'blacklisted_properties':
            return ['P3']


def test_run(monkeypatch):
    def mock_get(url, *args, **kwargs):
        return MockResponse(url)

    monkeypatch.setattr(requests, "get", mock_get)
    storage = MockStorage()
    scraper = Scaraper(MockConfig(), storage, MockSchemaorgNormalizer, MockSchemaorgPropertyMapper())
    scraper.run()
    assert storage.get(scraper.output_file_name) == \
           {'P1': {'good_responses': 10, 'has_schema': 10, 'total_requests': 10},
            'P2': {'good_responses': 10, 'has_schema': 0, 'total_requests': 10}}
