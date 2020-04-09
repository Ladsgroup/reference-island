import concurrent.futures
import json
from time import gmtime, strftime

import extruct
import requests
from w3lib.html import get_base_url


class Scaraper(object):
    def __init__(self, config, storage, schemaorg_normalizer, schemaorg_mapper):
        """

        :type storage: wikidatarefisland.data_access.Storage
        :type config: wikidatarefisland.Config
        :type schemaorg_mapper: wikidatarefisland.services.SchemaorgPropertyMapper
        """
        self.config = config
        self.storage = storage
        self.schemaorg_normalizer = schemaorg_normalizer
        self.schemaorg_mapper = schemaorg_mapper
        self.inptut_file_name = config.get('pipe1_output_file')
        self.output_file_name = config.get('pipe2_output_file')

    def check_external_identifier(self, url):
        r = requests.get(url, timeout=30, user_agent=self.config.get('user_agent'))
        base_url = get_base_url(r.text, r.url)
        data = extruct.extract(r.text, base_url=base_url)
        return {'data': self.schemaorg_normalizer.normalize_from_extruct(data),
                'timestamp': strftime("%Y-%m-%d %H:%M:%S", gmtime())}

    def run(self):
        for item in self.storage.getLines(self.inptut_file_name):
            self.handle_item(item)

    def handle_item(self, item):
        resource_urls = {i['url']: i['referenceMetadata'] for i in item['resourceUrls']}
        schemaorg_mapping = {
            i['url']: i['property'] for i in self.schemaorg_mapper.get_mapping()}
        statement_pids = [i['pid'] for i in item['statements']]
        properties_to_check = filter(lambda t: t in schemaorg_mapping.values(), statement_pids)
        if not properties_to_check:
            # Bail out if we can't find any property that have schema.org equivalent
            return

        extracted_data = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            future_to_url = {
                executor.submit(self.check_external_identifier, i): i for i in resource_urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except KeyboardInterrupt:
                raise
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                extracted_data[url] = data

        final_data = self._match_extracted_data(extracted_data, resource_urls,
                                                schemaorg_mapping, item)

        self.storage.append(
            self.output_file_name, '\n'.join([json.dumps(i) for i in final_data]), raw=True)

    def _match_extracted_data(self, extracted_data, resourceUrls, mapping, item):
        final_data = []
        for url in extracted_data:
            resourceUrls[url]['dateRetrieved'] = extracted_data[url]['timestamp']
            for datum in extracted_data[url]['data']:
                if datum['type'] not in mapping:
                    continue
                pid = mapping[datum['type']]
                for statement in item['statements']:
                    if statement['pid'] != pid:
                        continue

                    final_data.append({
                        'statement': statement,
                        'itemId': item['itemId'],
                        'reference': {
                            'referenceMetadata': resourceUrls[url],
                            'extractedData': datum['properties']
                        }
                    })

        return final_data
