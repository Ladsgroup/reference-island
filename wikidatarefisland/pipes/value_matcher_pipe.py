class ValueMatcherPipe():
    """A pipesegment to match potential references with statement data"""
    def __init__(self, matchers):
        """Instantiate the pipe

        Arguments:
            matchers {wikidatarefisland.data_model.ValueMatchers} --
                A static class with value matcher functions
        """
        self.matchers = matchers

    def flow(self, potential_match):
        """Applies transformations to data flow

        Arguments:
            potential_match {dict} -- A potential statement - reference match to examine.
                See: See: https://github.com/wmde/reference-island#statement-reference-blob 

        Returns:
            dict|None -- The input potential match if there's a match, None otherwise.
        """
        filters = [
            self.matchers.match_text,
            self.matchers.match_number
        ]

        if any(match(potential_match) for match in filters):
            return potential_match
