import json
import os
import shutil

import pytest
import requests

from wikidatarefisland import run_main
from wikidatarefisland.data_access import WdqsReader
from wikidatarefisland.data_model import SchemaOrgNormalizer
from wikidatarefisland.services import WdqsExternalIdentifierFormatter, WdqsSchemaorgPropertyMapper


def relative_path(*paths):
    """Generate absolute path from script relative path.

    Returns:
        str -- Absolute path string
    """
    return os.path.join(os.path.dirname(__file__), *paths)


class MockResponse:
    def __init__(self, url):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, 'data/test_response.html'), 'r') as f:
            self.text = f.read()
        self.status_code = 200
        self.url = url


class MockSession():
    def __init__(self):
        self.headers = {}

    def get(self, url, *args, **kwargs):
        return MockResponse(url)


@pytest.fixture()
def test_directory(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp('directory')
    conf_dir = tmpdir.mkdir('config')
    tmpdir.mkdir('scripts')
    tmpdir.mkdir('data')
    config_file = conf_dir.join('default.yml')
    override_file = conf_dir.join('override.yml')
    override_file.write('')
    yaml_path = relative_path('..', 'config', 'default.yml')
    shutil.copy(yaml_path, config_file.strpath)
    return tmpdir


def test_main_ss1(monkeypatch, test_directory):
    def mock_external_ids(_):
        return ['P1234']

    def mock_usecases(*args):
        return [{'value': {'value': 'cat1234'}}] * 6

    def mock_formatter(*args):
        return {
            'url': 'http://example.com/cat1234',
            'referenceMetadata': {}  # not needed here; leaked in from SS4
        }

    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self):
                self.text = 'http://schema.org'
                self.status_code = 200

        return MockResponse()

    monkeypatch.setattr(WdqsReader, "get_all_external_identifiers", mock_external_ids)
    monkeypatch.setattr(WdqsReader, "get_usecases", mock_usecases)
    monkeypatch.setattr(WdqsExternalIdentifierFormatter, "format", mock_formatter)
    monkeypatch.setattr(requests, "get", mock_get)

    test_filename = "test_result_ss1.json"
    mock_args = f"this_is_ignored.py --step ss1 --output {test_filename}"
    mock_file_path = test_directory.join('scripts', 'this_is_ignored.py')
    result_file = test_directory.join('data', test_filename)

    run_main(mock_args.split(), mock_file_path)

    assert json.loads(result_file.read()) == ['P1234']


def test_main_match(test_directory):
    test_given_filename = "test_given_match.jsonl"
    test_result_filename = "test_result_match.jsonl"
    test_expected_filename = "test_expected_match.jsonl"

    given_file = test_directory.join('data', test_given_filename)
    result_file = test_directory.join('data', test_result_filename)

    mock_input_path = relative_path('mock_data', test_given_filename)
    mock_expected_path = relative_path('mock_data', test_expected_filename)

    mock_args = f"this_is_ignored.py --step match --input {test_given_filename}" \
                f" --output {test_result_filename}"
    mock_file_path = test_directory.join('scripts', 'this_is_ignored.py')

    shutil.copy(mock_input_path, given_file.strpath)

    run_main(mock_args.split(), mock_file_path)

    with open(mock_expected_path) as expected:
        assert result_file.read() == expected.read()


def test_scraper(monkeypatch, test_directory):
    def mock_get_mapping(_):
        return [
            {'property': 'P321', 'url': 'http://schema.org/director'},
            {'property': 'P123', 'url': 'http://schema.org/name'},
        ]

    def mock_normalize_from_extruct(_, data):
        return [{
            "http://schema.org/director": [
                data['microdata'][0]['director']['name']
            ],
            "http://schema.org/genre": [
                data['microdata'][0]['genre']
            ]
        }]

    monkeypatch.setattr(SchemaOrgNormalizer, "normalize_from_extruct", mock_normalize_from_extruct)
    monkeypatch.setattr(WdqsSchemaorgPropertyMapper, "get_mapping", mock_get_mapping)
    monkeypatch.setattr(requests, "Session", MockSession)

    test_given_filename = "test_given_pipe1.jsonl"
    mock_input_path = relative_path('mock_data', test_given_filename)
    given_file = test_directory.join('data', test_given_filename)
    shutil.copy(mock_input_path, given_file.strpath)

    side_service_file = test_directory.join('data', 'side_service_input.json')
    shutil.copy(relative_path('mock_data', 'empty.json'), side_service_file.strpath)

    test_filename = "test_result_scraper.jsonl"
    mock_file_path = test_directory.join('scripts', 'this_is_ignored.py')
    result_file = test_directory.join('data', test_filename)

    mock_args = f"this_is_ignored.py --step scrape " \
                f"--input {test_given_filename} --output {test_filename}"

    run_main(mock_args.split(), mock_file_path)

    expected_result = {
        'statement': {
            'pid': 'P321',
            'datatype': 'wikibase-item',
            'value': {'numeric-id': 214917, 'id': 'Q214917'}},
        'itemId': 'Q42',
        'reference': {'referenceMetadata': {
            'a': 'b',
            'P854': 'https://example_with_schema.org/wow'},
            'extractedData': ['James Cameron']}}
    result = json.loads(result_file.read())
    assert 'dateRetrieved' in result['reference']['referenceMetadata']
    del result['reference']['referenceMetadata']['dateRetrieved']
    assert result == expected_result
