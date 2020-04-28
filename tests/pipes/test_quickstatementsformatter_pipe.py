from string import Template


from wikidatarefisland.pipes.quickstatements_formatter_pipe import QuickStatementsFormatterPipe

MOCK_QID = "Q123"
MOCK_PID = "P321"
MOCK_TEXT = "Test"
MOCK_QUANTITY = "42"


MOCK_EXT_PID = "P842"
MOCK_EXT_QID = "Q842"
MOCK_EXT_URL = "http://example.com/123"
MOCK_STATED_PID = "P248"
MOCK_RETRIEVED_PID = "Q183"
MOCK_RETRIEVED_TIME = "+2020-05-04T12:34:56Z/01"


mock = {
    "statement": {
        "with_string": {
            "pid": MOCK_PID,
            "datatype": "string",
            "value": {
                "value": MOCK_TEXT
            }
        },
        "with_monolingualtext": {
            "pid": MOCK_PID,
            "datatype": "monolingualtext",
            "value": {
                "text": MOCK_TEXT
            }
        },
        "with_quantity": {
            "pid": MOCK_PID,
            "datatype": "quantity",
            "value": {
                "amount": MOCK_QUANTITY
            }
        }
    },
    "reference": {
        "referenceMetadata": {
            MOCK_STATED_PID: MOCK_EXT_QID,
            MOCK_EXT_PID: MOCK_EXT_URL,
            MOCK_RETRIEVED_PID: MOCK_RETRIEVED_TIME
        },
        "extractedData": ["Doesn't Matter"]
    }
}

given = {
    "string_match": {
        "itemId": MOCK_QID,
        "statement": mock["statement"]["with_string"],
        "reference": mock["reference"]
    },
    "monolingualtext_match": {
        "itemId": MOCK_QID,
        "statement": mock["statement"]["with_monolingualtext"],
        "reference": mock["reference"]
    },
    "quantity_match": {
        "itemId": MOCK_QID,
        "statement": mock["statement"]["with_quantity"],
        "reference": mock["reference"]
    }
}

expected = Template(f"{MOCK_QID}\t{MOCK_PID}\t$value" /
                    "\t{MOCK_STATED_PID}\t{MOCK_EXT_QID}" /
                    "\t{MOCK_EXT_PID}\t{MOCK_EXT_URL}" /
                    "\t{MOCK_RETRIEVED_PID}\t{MOCK_RETRIEVED_TIME}")


class TestQuickStatementsFormatterPipe:
    def test_flow(self):
        assert False
