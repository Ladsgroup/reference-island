import json

from wikidatarefisland.pipes import AbstractPipe
from wikidatarefisland.pumps import DumpReaderPump, SimplePump

mock_input_data = {'mock': 'inputdata'}
mock_output_data = {'mock': 'outputdata'}
mock_input_file_path = 'input_file_name'
mock_output_file_path = 'output_file_path'


class MockStorage():
    def __init__(self):
        self.mock_output_file_content = ''

    def getLines(self, input_file_name):
        assert input_file_name == mock_input_file_path, 'should pass input file name to Storage'
        return [mock_input_data]

    def get_dump_lines(self, input_file_name):
        assert input_file_name == mock_input_file_path, 'should pass input file name to Storage'
        return [mock_input_data]*3

    def append(self, output_file_name, data, raw=False):
        assert output_file_name == mock_output_file_path, 'should pass output file name to Storage'
        if not raw:
            self.mock_output_file_content += json.dumps(data)
        else:
            self.mock_output_file_content += data + '\n'


class MockPipe(AbstractPipe):
    def flow(self, input):
        assert input == mock_input_data
        return [mock_output_data]


def test_simple_pump():
    mock_storage = MockStorage()
    pump = SimplePump(mock_storage)
    pipe = MockPipe()
    pump.run(pipe, mock_input_file_path, mock_output_file_path)
    assert mock_storage.mock_output_file_content == json.dumps(mock_output_data)


def test_dump_reader_pump():
    mock_storage = MockStorage()
    pump = DumpReaderPump(mock_storage, 1)
    pipe = MockPipe()
    pump.run(pipe, mock_input_file_path, mock_output_file_path)
    assert mock_storage.mock_output_file_content.strip() == \
        '\n'.join([json.dumps(mock_output_data)] * 3)


def test_dump_reader_pump_batch():
    mock_storage = MockStorage()
    batch_size = 2
    pump = DumpReaderPump(mock_storage, batch_size)
    pipe = MockPipe()
    pump.run(pipe, mock_input_file_path, mock_output_file_path)
    assert mock_storage.mock_output_file_content.strip() == \
        '\n'.join([json.dumps(mock_output_data)] * batch_size)
