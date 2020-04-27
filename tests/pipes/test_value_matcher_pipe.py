import pytest

from wikidatarefisland.pipes.value_matcher_pipe import ValueMatcherPipe

given = {
    "string_match": {
        "method": "match_text",
        "return": True
    },
    "string_mismatch": {
        "method": "match_text",
        "return": False
    },
    "number_match": {
        "method": "match_quantity",
        "return": True
    },
    "number_mismatch": {
        "method": "match_quantity",
        "return": False
    }
}


class MockMatchers:
    @staticmethod
    def match_text(item):
        return False

    @staticmethod
    def match_quantity(item):
        return False


class TestValueMatcherPipe:

    @pytest.mark.parametrize("mock,expected", [
        (given["string_match"], "Test"),
        (given["string_mismatch"], None),
        (given["number_match"], "Test"),
        (given["number_mismatch"], None)
    ])
    def test_flow(self, monkeypatch, mock, expected):
        monkeypatch.setattr(MockMatchers, mock["method"], lambda item: mock["return"])

        pipe = ValueMatcherPipe(MockMatchers)

        assert pipe.flow("Test") == expected
