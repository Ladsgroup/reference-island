from wikidatarefisland.pipes import AbstractPipe


class ItemMappingMatcherPipe(AbstractPipe):
    """A pipe segment to match potential references with statement data."""

    def __init__(self, mapping, whitelisted_external_identifiers):
        """Instantiate the pipe

        Arguments:
            matchers {wikidatarefisland.data_model.ValueMatchers} --
                A static class with value matcher functions
        """
        self.mapping = mapping
        self.whitelisted_external_identifiers = whitelisted_external_identifiers

    def flow(self, potential_match):
        """Applies transformations to data flow

        Arguments:
            potential_match {dict} -- A potential statement - reference match to examine.
                See: See: https://github.com/wmde/reference-island#statement-reference-blob

        Returns:
            The input, this class just observes.
        """
        if potential_match['statement']['datatype'] != 'wikibase-item':
            return []
        item_id = potential_match['statement']['value']['numeric-id']
        ext_id_property = None
        for pid in potential_match['reference']['referenceMetadata']:
            if pid not in self.whitelisted_external_identifiers:
                continue
            ext_id_property = pid
            break
        if not ext_id_property:
            return []
        extracted_data = potential_match['reference']['extractedData']
        for value in extracted_data:
            value = str(value)
            if not value:
                continue
            pid = potential_match['statement']['pid']
            if pid not in self.mapping[ext_id_property]:
                return []
            if item_id == self.mapping[ext_id_property][pid].get(str(value)):
                return [potential_match]
        return []
