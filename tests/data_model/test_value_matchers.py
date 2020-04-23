import pytest

from wikidatarefisland.data_model.value_matchers import ValueMatchers, StringValue

mock = {
    "statement": {
        "with_string": {
            "datatype": 'string',
            "value": {
                "value": "Test"
            }
        },
        "with_url": {
            "datatype": 'url',
            "value": {
                "value": "Test"
            }
        },
        "with_monolingualtext": {
            "datatype": 'monolingualtext',
            "value": {
                "value": { 
                    "text": "Test"
                }
            }
        },
        "without_string": {
            "datatype": 'some-other-data'
        }
    },
    "reference": {
        "with_one_value_match": {
            "extractedData": ["Test"]
        },
        "with_multiple_values_match": {
            "extractedData": ["Some", "Test"]
        },
        "without_match": {
            "extractedData": ["Some", "Other", "Values"]
        }
    }
}

given = {
    "no_string": {
        "statement": mock["statement"]["without_string"]
    },
    "no_match": {
        "statement": mock["statement"]["with_string"],
        "reference": mock["reference"]["without_match"]
    },
    "single_string_match": {
        "statement": mock["statement"]["with_string"],
        "reference": mock["reference"]["with_one_value_match"]
    },
    "single_url_match": {
        "statement": mock["statement"]["with_url"],
        "reference": mock["reference"]["with_one_value_match"]
    },
    "single_monolingualtext_match": {
        "statement": mock["statement"]["with_monolingualtext"],
        "reference": mock["reference"]["with_one_value_match"]
    },
    "multiple_values_match": {
        "statement": mock["statement"]["with_string"],
        "reference": mock["reference"]["with_multiple_values_match"]
    }
}


class TestStringValue:

    @pytest.mark.parametrize("statement,equivalent", [
        (mock["statement"]["with_string"], "Test"),
        (mock["statement"]["with_url"], "Test"),
        (mock["statement"]["with_monolingualtext"], "Test"),
        (mock["statement"]["with_string"], "test"),
        (mock["statement"]["with_string"], "  Test ")
    ])
    def test_equivalence(self, statement, equivalent):
        assert StringValue(statement) == equivalent


class TestValueMatchers:

    @pytest.mark.parametrize("given,expected", [
        (given["no_string"], False),
        (given["no_match"], False),
        (given["single_string_match"], True),
        (given["single_url_match"], True),
        (given["single_monolingualtext_match"], True),
        (given["multiple_values_match"], True),
    ])
    def test_match_string(self, given, expected):
        assert ValueMatchers.match_string(given) == expected
