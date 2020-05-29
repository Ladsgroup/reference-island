# Data Pipeline Reference

## Glossary

The following terms will be used throughout this document, their meanings are as follows:

**Pump**: Represents a class that "flows" data into a pipeline segment, and is responsible for reading and writing the results of each segment to an from the disk.

**Pipe #:** Represents a sequential segment in the main data pipeline, which processes Wikidata item serializations into a formatted list of potential references. 

**SS #:** Represents a "side stream", to provide additional data to segments in the main pipeline, which will aid in making decisions or filter and format potential references.

## Pumps

### Dump Reader Pump

[[Code]](../wikidatarefisland/pumps/pump.py#L25-L49)

### Simple Pump

[[Code]](../wikidatarefisland/pumps/pump.py#L14-L22)

### Observer Pump

[[Code]](../wikidatarefisland/pumps/pump.py#L52-L59)

## Pipeline Segments

### Pipe 1: Item Extractor

[[Code]](../wikidatarefisland/pipes/item_extractor_pipe.py)

### Pipe 2: Scraper

[[Code]](../wikidatarefisland/pipes/scraper.py)

### Pipe 3: Value Matcher

[[Code]](../wikidatarefisland/pipes/value_matcher_pipe.py)

### Pipe 4: Statistical Matcher

[[Code: Statistical Analysis]](../wikidatarefisland/pipes/item_statistical_analysis_pipe.py), [[Code: Item Matching]](../wikidatarefisland/pipes/item_mapping_matcher_pipe.py)

## Side Streams

### SS 1: External Resource Whitelister

[[Code]](../wikidatarefisland/external_identifiers/generate_whitelisted_ext_ids.py)

### SS 2: Schema.org JSON-LD context fetcher

[[Code]](../wikidatarefisland/data_access/schema_context_downloader.py)

This stream downloads the Schema.org JSON-LD context to prevent multiple calls to http://schema.org to resolve JSON-LD document contexts.

Until 2020-05-19 it was possible for PyLD to automatically obtain it through content-negotiation of schema.org but this broke. To mitigate this, the side-stream has a backup method to get the context from the schema.org docs.

## Noteworthy Utility Classes

### Wikidata - Schema.org Property Mapper

[[Code]](../wikidatarefisland/services/schemaorg_property_mapper.py)

A service to retrieve the most recent state of mappings between Wikidata Properties and Schema.org properties.

Outputs a list of objects representing a mapping. Each object has the following structure:

* `property`: String representing a property on Wikidata.
* `url`: A Schema.org property URL

Example:

```js
[
    {
        "property": "P1476",
        "url": "http://schema.org/name"
    },
    //...
]
```

### Schema.org Data Normalizer

[[Code]](../wikidatarefisland/data_model/schemaorg_normalizer.py)

This service takes in an object containing raw scraped data in `json-ld` format (For example, the results of the following scraping library: https://github.com/scrapinghub/extruct with the [`uniform` option set to true](https://github.com/scrapinghub/extruct#uniform)).

The output of this service will be a list of objects representing a Schema.org type with the following structure: 

```js
[
    {
        "http://schema.org/name": [ "Ludwig Wittgenstein" ],
        "http://schema.org/sameAs": [ "http://viaf.org/viaf/24609378" ],
        "http://schema.org/birthPlace": {
          "http://schema.org/name": [ "Vienna" ],
          "http://schema.org/geo": {
            "http://schema.org/geo/latitude": "48.20849",
            "http://schema.org/geo/longitude": "16.37208"
          }
        }
    },
    //...
]
```

### Wikidata External Id URL Formatter

[[Code]](../wikidatarefisland/services/external_identifier_formatter.py)

This service takes in a string representation of an external id property and attempts to output a formatted URL  for an external resource, as well as reference metadata according to the Wikidata mapping. See [`ResourceBlob`](result.md#resourceblob) for output. If no formatter is found is found the formatter returns `false`.
