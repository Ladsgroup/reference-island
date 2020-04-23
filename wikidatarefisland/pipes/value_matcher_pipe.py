class ValueMatcherPipe():
    """ValueMatcherPipe
    This pipe takes in a jsonl and filters it's items by running a series of matchers on each item,
    to match between statement values and extracted data values. It then writes the new lines that
    pass the filter
    """
    def __init__(self):
        super().__init__()
