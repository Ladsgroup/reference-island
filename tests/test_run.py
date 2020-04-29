import json

from wikidatarefisland import run_main
from wikidatarefisland.data_access import WdqsReader


# Mocking checklist:
# - WDQSReader: Get all external idefs --> ['P1234', 'P1235', 'P1236']
# - WDQSReader: Check Usecases  --> [{ value: { value: '1234' } }] X 2
# - External Idefs Formatter: Format --> { url: 'http://www.example.com/1234' }
# - requests: get --> { status_code: 200, text: 'http://schema.org' }

def test_main_ss1(monkeypatch, tmpdir):
    def mock_external_ids():
        return ['P1234']

    monkeypatch.setattr(WdqsReader, "get_all_external_identifiers", mock_external_ids)
    # Worry about default.yml later
    test_filename = "test_result_ss1.json"
    mock_args = f"--step ss1 --output {test_filename}"
    mock_file_path = tmpdir.join('scripts', 'this_is_ignored.py')
    result_file = tmpdir.join('data').join(test_filename)

    run_main(mock_args.split(), mock_file_path)

    # assert json.loads(result_file.read()) == ['P1234', 'P1235']
    assert False
