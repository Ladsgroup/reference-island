class QuantityValue:
    """Represents Wikibase Quantity Values"""
    def __init__(self, statement):
        """Instantiates a quantity value

        Arguments:
            statement {dict} -- A statement dictionary.
                See: https://github.com/wmde/reference-island#statement-dict
        """
        self.type = statement["datatype"]
        self.value = statement["value"]["amount"]

    def __eq__(self, other):
        if not isinstance(other, str):
            return self == other

        return self.value == other


class TextValue:
    """Represent Wikibase Text Values"""
    def __init__(self, statement):
        """Instantiates a text value according to it's datatype

        Arguments:
            statement {dict} -- A statement dictionary.
                See: https://github.com/wmde/reference-island#statement-dict
        """
        self.type = statement["datatype"]
        self.value = statement["value"]["value"]["text"] \
            if self.type == "monolingualtext" \
            else statement["value"]["value"]

    def __eq__(self, other):
        if not isinstance(other, str):
            return self == other

        return self.value.lower().strip() == other.lower().strip()


class ValueMatchers:
    """Collects static methods to match between two data values on a statement - reference blob"""
    STRING_DATATYPES = ["string", "url", "monolingualtext"]
    NUMBER_DATATYPES = ["quantity"]

    @staticmethod
    def match_text(statement_reference):
        """Matches two text values

        Arguments:
            statement_reference {dict} -- A statement - reference blob dictionary.
                See: https://github.com/wmde/reference-island#statement-reference-blob

        Returns:
            bool -- True if a match exists, False otherwise
        """
        statement = statement_reference["statement"]

        if statement["datatype"] not in ValueMatchers.STRING_DATATYPES:
            return False

        value = TextValue(statement)
        reference = statement_reference["reference"]

        return value in reference["extractedData"]

    @staticmethod
    def match_number(statement_reference):
        """Matches two string values

        Arguments:
            statement_reference {dict} -- a statement -reference blob dictionary.
                See: https://github.com/wmde/reference-island#statement-reference-blob

        Returns:
            bool -- True if a match exists, False otherwise
        """
        statement = statement_reference["statement"]

        if statement["datatype"] not in ValueMatchers.NUMBER_DATATYPES:
            return False

        value = QuantityValue(statement)
        reference = statement_reference["reference"]

        return value in reference["extractedData"]
