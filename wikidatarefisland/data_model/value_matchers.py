class QuantityValue:
    """
    A class to represent Wikibase Quantity Values
    """
    def __init__(self, statement):
        self.type = statement["datatype"]
        self.value = statement["value"]["amount"]

    def __eq__(self, other):
        if not isinstance(other, str):
            return self == other

        return self.value == other


class StringValue:
    """
    A class to represent Wikibase String Values
    """
    def __init__(self, statement):
        self.type = statement["datatype"]
        self.value = statement["value"]["value"]["text"] \
            if self.type == "monolingualtext" \
            else statement["value"]["value"]

    def __eq__(self, other):
        if not isinstance(other, str):
            return self == other

        return self.value.lower().strip() == other.lower().strip()


class ValueMatchers:
    """
    A class to collect static methods to match between two data values on an itemblob
    """
    STRING_DATATYPES = ["string", "url", "monolingualtext"]
    NUMBER_DATATYPES = ["quantity"]

    @staticmethod
    def match_string(statement_reference):
        statement = statement_reference["statement"]

        if statement["datatype"] not in ValueMatchers.STRING_DATATYPES:
            return False

        value = StringValue(statement)
        reference = statement_reference["reference"]

        return value in reference["extractedData"]

    @staticmethod
    def match_number(statement_reference):
        statement = statement_reference["statement"]

        if statement["datatype"] not in ValueMatchers.NUMBER_DATATYPES:
            return False

        value = QuantityValue(statement)
        reference = statement_reference["reference"]

        return value in reference["extractedData"]
