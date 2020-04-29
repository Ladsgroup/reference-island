import json
import shutil

from wikidatarefisland import run_main
from wikidatarefisland.data_access import WdqsReader
from wikidatarefisland.services import ExternalIdentifierFormatter
import importlib.resources as pkg_resources


# Mocking checklist:
# - WDQSReader: Get all external idefs --> ['P1234', 'P1235', 'P1236'] done
# - WDQSReader: Check Usecases  --> [{ value: { value: '1234' } }] done
# - External Idefs Formatter: Format --> { url: 'http://www.example.com/1234' }
# - requests: get --> { status_code: 200, text: 'http://schema.org' }


def test_main_ss1(monkeypatch, tmpdir):
    def mock_external_ids(_):
        return ['P1234']

    def mock_usecases():
        return [{'value': {'value': 'cat1234'}}]

    def mock_formatter():
        return {
            'url': 'http://example.com/cat1234',
            'referenceMetadata': {}  # not needed here; leaked in from SS4
        }

    monkeypatch.setattr(WdqsReader, "get_all_external_identifiers", mock_external_ids)
    monkeypatch.setattr(WdqsReader, "get_usecases", mock_usecases)
    monkeypatch.setattr(ExternalIdentifierFormatter, "format", mock_formatter)

    # Worry about default.yml later
    test_filename = "test_result_ss1.json"
    mock_args = f"--step ss1 --output {test_filename}"
    mock_file_path = tmpdir.join('scripts', 'this_is_ignored.py')
    conf_dir = tmpdir.mkdir('config')
    tmpdir.mkdir('scripts')
    tmpdir.mkdir('data')
    config_file = conf_dir.join('default.yml')
    override_file = conf_dir.join('override.yml')
    override_file.write('')
    shutil.copy('../config/default.yml', config_file.strpath)
    result_file = tmpdir.join('data').join(test_filename)

    run_main(mock_args.split(), mock_file_path)

    # assert json.loads(result_file.read()) == ['P1234', 'P1235']
    assert False
