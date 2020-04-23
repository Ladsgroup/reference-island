import pytest

from wikidatarefisland.data_model.value_matchers import ValueMatchers, StringValue, QuantityValue

mock = {
    "statement": {
        "with_quantity": {
            "datatype": 'quantity',
            "value": {
                "amount": "12"
            }
        },
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
        "without_type": {
            "datatype": 'some-other-data'
        }
    },
    "reference": {
        "with_one_quantity_match": {
            "extractedData": ["12"]
        },
        "with_one_string_match": {
            "extractedData": ["Test"]
        },
        "with_multiple_values_match": {
            "extractedData": ["12", "Test"]
        },
        "without_match": {
            "extractedData": ["Some", "Other", "Values"]
        }
    }
}

given = {
    "no_type": {
        "statement": mock["statement"]["without_type"]
    },
    "no_quantity_match": {
        "statement": mock["statement"]["with_quantity"],
        "reference": mock["reference"]["without_match"]
    },
    "single_quantity_match": {
        "statement": mock["statement"]["with_quantity"],
        "reference": mock["reference"]["with_one_quantity_match"]
    },
    "multiple_quantity_match": {
        "statement": mock["statement"]["with_quantity"],
        "reference": mock["reference"]["with_multiple_values_match"]
    },
    "no_string_match": {
        "statement": mock["statement"]["with_string"],
        "reference": mock["reference"]["without_match"]
    },
    "single_string_match": {
        "statement": mock["statement"]["with_string"],
        "reference": mock["reference"]["with_one_string_match"]
    },
    "single_url_match": {
        "statement": mock["statement"]["with_url"],
        "reference": mock["reference"]["with_one_string_match"]
    },
    "single_monolingualtext_match": {
        "statement": mock["statement"]["with_monolingualtext"],
        "reference": mock["reference"]["with_one_string_match"]
    },
    "multiple_string_match": {
        "statement": mock["statement"]["with_string"],
        "reference": mock["reference"]["with_multiple_values_match"]
    }
}


class TestQuantityValue:

    @pytest.mark.parametrize("statement,equivalent", [
        (mock["statement"]["with_quantity"], "12")
    ])
    def test_equivalence(self, statement, equivalent):
        assert QuantityValue(statement) == equivalent


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
        (given["no_type"], False),
        (given["no_string_match"], False),
        (given["single_string_match"], True),
        (given["single_url_match"], True),
        (given["single_monolingualtext_match"], True),
        (given["multiple_string_match"], True),
    ])
    def test_match_string(self, given, expected):
        assert ValueMatchers.match_string(given) == expected

    @pytest.mark.parametrize("given,expected", [
        (given["no_type"], False),
        (given["no_quantity_match"], False),
        (given["single_quantity_match"], True),
        (given["multiple_quantity_match"], True),
    ])
    def test_match_number(self, given, expected):
        assert ValueMatchers.match_number(given) == expected
