import argparse
import os

from wikidatarefisland import (Config, data_access, external_identifiers,
                               services)

# from wikidatarefisland import pumps


def main():
    parser = argparse.ArgumentParser(description='Run the pipes and/or side steps')
    parser.add_argument('--step', dest='step', type=str,
                        help='Step to run e.g. ss1 or pipe2')

    parser.add_argument('--input', default='input.json', dest='input_path', type=str,
                        help='File for the step to read input from')

    parser.add_argument('--output', default='output.json', dest='output_path', type=str,
                        help='File for the step to read output from')

    args = parser.parse_args()

    # Services
    file_path = os.path.realpath(__file__)
    config = Config.newFromScriptPath(file_path)
    wdqs_reader = data_access.WdqsReader.newFromConfig(config)
    storage = data_access.Storage.newFromScript(file_path)
    external_identifier_formatter = services.WdqsExternalIdentifierFormatter(wdqs_reader)

    # Pumps
    # simple_pump = pumps.SimplePump(storage)

    if 'ss1' == args.step:
        external_identifiers.GenerateWhitelistedExtIds(
            wdqs_reader, storage, config, external_identifier_formatter).run()
        return


if __name__ == "__main__":
    main()
