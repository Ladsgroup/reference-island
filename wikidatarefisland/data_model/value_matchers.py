class StringValue:
    """
    A class to represent Wikidata String Values
    """
    def __init__(self, statement):
        pass


class ValueMatchers:
    """
    A class to collect static methods to match between two data values on an itemblob
    """
    STRING_DATATYPES = ["string", "url", "monolingualtext"]

    @staticmethod
    def match_string(statement_reference):
        statement = statement_reference["statement"]

        if statement["datatype"] not in ValueMatchers.STRING_DATATYPES:
            return False

        value = statement["value"]["value"]["text"] if statement["datatype"] == "monolingualtext" else statement["value"]["value"]
        reference = statement_reference["reference"]

        return value in reference["extractedData"]
