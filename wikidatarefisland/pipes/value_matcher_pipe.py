class ValueMatcherPipe():
    """ValueMatcherPipe
    This pipe segment takes in a jsonl line and runs a series of matchers on each it
    to match between statement values and extracted data values. It then returns the new lines that
    pass the filter or None
    """
    def __init__(self, matchers):
        self.matchers = matchers

    def flow(self, item):
        filters = [
            self.matchers.match_text,
            self.matchers.match_number
        ]

        if any(match(item) for match in filters):
            return item
