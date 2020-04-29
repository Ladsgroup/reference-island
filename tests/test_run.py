import os
import json
import shutil
import requests

from wikidatarefisland import run_main
from wikidatarefisland.data_access import WdqsReader
from wikidatarefisland.services import WdqsExternalIdentifierFormatter


# Mocking checklist:
# - WDQSReader: Get all external idefs --> ['P1234', 'P1235', 'P1236'] done
# - WDQSReader: Check Usecases  --> [{ value: { value: '1234' } }] done
# - External Idefs Formatter: Format --> { url: 'http://www.example.com/1234' }
# - requests: get --> { status_code: 200, text: 'http://schema.org' }


def test_main_ss1(monkeypatch, tmpdir):
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
    mock_args = f"--step ss1 --output {test_filename}"
    mock_file_path = tmpdir.join('scripts', 'this_is_ignored.py')
    conf_dir = tmpdir.mkdir('config')
    tmpdir.mkdir('scripts')
    tmpdir.mkdir('data')
    config_file = conf_dir.join('default.yml')
    override_file = conf_dir.join('override.yml')
    override_file.write('')
    yaml_path = os.path.join(os.path.dirname(__file__), '../config/default.yml')
    shutil.copy(yaml_path, config_file.strpath)
    result_file = tmpdir.join('data').join(test_filename)

    run_main(mock_args.split(), mock_file_path)

    assert json.loads(result_file.read()) == ['P1234']
