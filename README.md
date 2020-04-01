# Wikidata Reference Island

## Glossary

The following terms will be used throughout this document, their meanings are as follows:

**Pipe <#>:** Represents a sequential step in the main data pipeline, which processes wikidata item serializations into a formatted list of potential references. 

**SS<#>:** Represents a "side service", to provide additional data to steps in the main pipeline, which will aid in making decisions or filter and format potential references.

## General Agreements

* The output formats for each step in the pipeline is to be formatted and encoded in `jsonl` with the exception of [Pipe 5](pipe-5).

## Pipe 1: Find unreferenced statements and URLs for a given list of wikidata items<a name="pipe-1"></a>

This step will take in the following inputs, and will output the data expected in [Pipe 2](#pipe-2).

* `<varname>`: List of strings representing white listed Wikidata external id properties. Example:

  ```json
  ['P1234', 'P1233', /*...*/]
  ```

* `<varname>`: List of Wikidata item serializations, as described in https://www.mediawiki.org/wiki/Wikibase/DataModel/JSON

## Pipe 2: Scrape given URLs for potential matches between  unreferenced statements and structured data<a name="pipe-2"></a>

This step will take in the following inputs and will output the data expected in [Pipe 3](#pipe-3).

* `<varname>`:  List of objects to represent Wikidata Items with the following keys:

  * `itemId`: The Wikidata id of the item being examined

  * `resourceUrls`: List of objects describing external resources to scrape, and reference meta data to be added to references.

    * `url`: String representing the url to scrape
    * `referenceMetadata`: Data to append to the potential references matched at the end of this stage with optional reference keys as provided by [SS4](#ss4).

    Example (Bnf Record for Ludwig Wittgenstein, with Wikidata property mapping):
    
     ```json
    {
        url: "https://catalogue.bnf.fr/ark:/12148/cb11929322k",
        referenceMetadata: {
            "P248": "Q19938912",
            "P268": "11929322k",
    		"P854": "https://catalogue.bnf.fr/ark:/12148/cb11929322k"
        }
    }
     ```

    Will translate to (`*` denotes an optional property)
    
    ```json
    {
        url: [String],
        referenceMetadata: {
            *[statedInPropId]: [externalIdItem],
            *[externalIdProp]: [externalIdVal],
    		*[referenceUrl]: [String]
        }
}
    ```
  
  
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

## Pipe 5: Format potential references into quickstatements format

