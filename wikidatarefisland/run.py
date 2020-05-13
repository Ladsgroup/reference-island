import argparse
import os
import sys

from wikidatarefisland import (Config, data_access, data_model, external_identifiers, pipes,
                               services)

from wikidatarefisland import pumps
from wikidatarefisland.data_model import wikibase


def main(argv, filepath):
    parser = argparse.ArgumentParser(description='Run the pipes and/or side steps')
    parser.add_argument('--step', dest='step', type=str,
                        help='Step to run e.g. ss1 or pipe2')

    parser.add_argument('--input', default='input.json', dest='input_path', type=str,
                        help='File for the step to read input from')

    parser.add_argument('--output', default='output.json', dest='output_path', type=str,
                        help='File for the step to read output from')

    parser.add_argument('--side-service-input', default='side_service_input.json',
                        dest='side_service_input_path', type=str,
                        help='Optional file for the step to read input from')

    args = parser.parse_args(argv[1:])

    # Services
    file_path = os.path.realpath(filepath)
    config = Config.newFromScriptPath(file_path)
    wdqs_reader = data_access.WdqsReader.newFromConfig(config)
    storage = data_access.Storage.newFromScript(file_path)
    external_identifier_formatter = services.WdqsExternalIdentifierFormatter(wdqs_reader)
    schemaorg_mapper = services.WdqsSchemaorgPropertyMapper(wdqs_reader)
    schemaorg_normalizer = data_model.SchemaOrgNormalizer

    # Pumps
    simple_pump = pumps.SimplePump(storage)

    if 'ss1' == args.step:
        ext_ids = external_identifiers.GenerateWhitelistedExtIds(
            wdqs_reader, storage, config, external_identifier_formatter).run()

        storage.store(args.output_path, ext_ids)
        return

    if 'extract_items' == args.step:
        whitelisted_ext_ids = storage.get(args.side_service_input_path)
        item_extractor = pipes.ItemExtractorPipe(
            external_identifier_formatter,
            config.get('blacklisted_properties'),
            whitelisted_ext_ids,
            config.get('imported_from_properties')
        )
        simple_pump.run(item_extractor, args.input_path, args.output_path)

    if 'scrape' == args.step:
        the_scraper = pipes.ScraperPipe(config, schemaorg_normalizer, schemaorg_mapper)
        simple_pump.run(the_scraper, args.input_path, args.output_path)
        return

    if 'match' == args.step:
        pipe = pipes.ValueMatcherPipe(wikibase.ValueMatchers)
        simple_pump.run(pipe, args.input_path, args.output_path)
        return


if __name__ == "__main__":
    main(sys.argv, __file__)
