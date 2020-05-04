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
            "value": "Test"
        },
        "with_url": {
            "datatype": 'url',
            "value": "Test"
        },
        "with_monolingualtext": {
            "datatype": 'monolingualtext',
            "value": {
                "text": "Test"
            }
        },
        "with_globe-coordinate": {
            "on_earth": {
                "datatype": 'globe-coordinate',
                "value": {
                    "latitude": 52.498469,
                    "longitude": 13.381021,
                    "globe": "http://www.wikidata.org/entity/Q2"
                }
            },
            "on_mars": {
                "datatype": 'globe-coordinate',
                "value": {
                    "latitude": 18.65,
                    "longitude": 226.2,
                    "globe": "http://www.wikidata.org/entity/Q111"
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
