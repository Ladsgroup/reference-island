# Wikidata Reference Island

## Glossary

The following terms will be used throughout this document, their meanings are as follows:

**Pipe <#>:** Represents a sequential step in the main data pipeline, which processes wikidata item serializations into a formatted list of potential references. 

**SS<#>:** Represents a "side service", to provide additional data to steps in the main pipeline, which will aid in making decisions or filter and format potential references.

## Pipe 1: Find unreferenced statements and URLs for a given list of wikidata items

## Pipe 2: Scrape given URLs for potential matches between  unreferenced statements and structured data

## Pipe 3: Filter extracted values by plain text matching

## Pipe 5: Format potential references into quickstatements format

