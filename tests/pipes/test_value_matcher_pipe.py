import pytest

from wikidatarefisland.pipes.value_matcher_pipe import ValueMatcherPipe

given = {
    "string_match": {
        "method": "match_string",
        "return": True
    },
    "string_mismatch": {
        "method": "match_string",
        "return": False
    }
}


class MockValueMatchers:
    @staticmethod
    def match_string():
        return False


class TestValueMatcherPipe:

    @pytest.mark.parametrize("mock,expected", [
        (given["string_match"], "Test"),
        (given["string_mismatch"], None)
    ])
    def test_flow(self, monkeypatch, mock, expected):
        monkeypatch.setattr(MockValueMatchers, mock["method"], lambda item: mock["return"])

        pipe = ValueMatcherPipe(MockValueMatchers)

        assert pipe.flow("Test") == expected
