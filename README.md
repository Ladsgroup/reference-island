# Wikidata Reference Island

## Glossary

The following terms will be used throughout this document, their meanings are as follows:

**Pipe <#>:** Represents a sequential step in the main data pipeline, which processes Wikidata item serializations into a formatted list of potential references. 

**SS<#>:** Represents a "side service", to provide additional data to steps in the main pipeline, which will aid in making decisions or filter and format potential references.

## General Agreements

* The output formats for each step in the pipeline is to be formatted and encoded in `jsonl` with the exception of [Pipe 5](pipe-5).

## Pipe 1: Find unreferenced statements and URLs for a given list of Wikidata items<a name="pipe-1"></a>

This step will take in the following inputs, and will output the data expected in [Pipe 2](#pipe-2).

* `<varname>`: List of strings representing white listed Wikidata external id properties, same as output of [SS1](#ss-1).

* `<varname>`: List of Wikidata item serializations, as described in https://www.mediawiki.org/wiki/Wikibase/DataModel/JSON

## Pipe 2: Scrape given URLs for potential matches between  unreferenced statements and structured data<a name="pipe-2"></a>

This step will take in the following inputs and will output the data expected in [Pipe 3](#pipe-3).

* `<varname>`:  List of objects to represent Wikidata Items with the following keys:

  * `itemId`: The Wikidata id of the item being examined

  * `resourceUrls`: List of objects describing external resources to scrape, and reference meta data to be added to references.

    * `url`: String representing the url to scrape
    * `referenceMetadata`: Data to append to the potential references matched at the end of this stage with optional reference keys. 

    ***Note***: An example for this property can be found in the output provided by [SS4](#ss-4).
    
  * `statements`: List of unreferenced statements in the following structure:
    
    * `pid`: The property id of the statement
    * `dataValue`: The data value of the statement / Item id of the Wikidata item value.
  
    Example:
  
      ```json
    [
        {
            "pid": "P321", 
            "dataValue": "2020-04-01",
        },
        {
            "pid": "P777",
            "dataValue": "Q666"
        }
        // ...
    ]
      ```

## Pipe 3: Filter extracted values by plain text matching<a name="pipe-3"></a>

## Pipe 5: Format potential references into Quickstatements format<a name="pipe-5"></a>

## SS1: Find good external ID Properties<a name="ss-1"></a>

A service to white-list external id properties based on a predefined blacklist, and the amount of Schema.org definitions found in a sample external resource.

This service takes in a list of  manually blacklisted external ids, and retrieves a list of currently available external ids from Wikidata.

The output for this service is a listed of string representation of white-listed external ids. For example:  

  ```json
  ['P1234', 'P1233', ...]
  ```

## SS2: Fetch current mappings between Wikidata Properties and Schema.org Properties<a name="ss-2"></a>

A service to retrieve the most recent state of mappings between Wikidata Properties and Schema.org properties.

Outputs a list of objects representing a mapping. Each object has the following structure:

* `property`: String representing a property on Wikidata.
* `url`: A Schema.org property URL

Example:

```json
[
    {
        "property": "P1476",
        "url": "http://schema.org/name"
    },
    ...
]
```



## SS3: Normalize data from various scraped raw formats<a name="ss-3"></a>

This service takes in raw scraped data in either `json-ld`, `microdata` or `rdfa` format (For example, the results of the following scraping library: https://github.com/scrapinghub/extruct).

The output of this service will be a list of objects representing a Schema.org type with the following structure:

* `type`: Schema.org type url
* `properties`: An object representing Schema.org property value pairs where the keys are Schema.org property urls, and the values are the actual data from the site. 

Example:

```json
[
    {
        "type": "http://schema.org/Person",
        "properties": {
            "http://schema.org/name": "Ludwig Wittgenstein",
            "http://schema.org/sameAs": "http://viaf.org/viaf/24609378",
            "http://schema.org/additionalName": "Ludvigs Vitgenšteins"
        }
    },
    ...
]
```

## SS4: Map External ID Properties and Values to URL and reference meta-data<a name="ss-4"></a>

This service takes in a string representation of an external id property and attempts to output a formatted url  for an external resource, as well as reference metadata according to the wikidata mapping. If non is found it will return `false`.

The output format is an object with the following properties:

* `url`: The formatted URL of an external resource

* `referenceMetadata`: An object representing meta data for a potential reference, with the following key-value pairs:

  | Key                              | Value                                     |
  | -------------------------------- | ----------------------------------------- |
  | "P248" ("stated in" Property id) | Wikidata item representing an external ID |
  | Passed in external id Property   | Passed in external id value               |

  Example (WorldCat Identitites record for Ludwig Wittgenstein, with Wikidata property mapping):

   ```json
  {
      "url": "https://www.worldcat.org/identities/lccn-n79032058/",
      "referenceMetadata": {
          "P248": "Q76630151",
          "P7859": "lccn-n79032058"
      }
  }
   ```

  

