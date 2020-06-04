# Running the Data Pipeline
This documentation is for developers wishing to run the pipeline in a large scale. It concisely describes how to analyse **all of Wikidata** in order to obtain potential reference matches.

## Prerequisites
Running the Reference Island data pipeline on a large scale Wikidata dump is a process that requires multiple machines and a length of time. Generally speaking, it is **not** recommended to run the entire pipeline on a developer laptop for large scale Wikidata dumps, for the following reasons:

- Wikidata dumps are pretty large - ~100GB uncompressed.
- Processing time for the entire pipe line is relatively long: According to the latest estimation, >40 days.

Therefore, as a more robust solution, the development team recommends to run most of the pipeline on a Virtual Machine on WMF's Cloud VPS with the exception of [Pipe 1: Item Extractor](#pipe-1-item-extractor).

The item extraction pipe reads the complete dumps. The machines in the WMF stats cluster have the complete dumps
available and are on storage that is quick to read. Therefore, the stats cluster is the best place to run the item extraction pipe.  

## Setting up a Cloud-VPS VM
Documentation for setting up a VM on Cloud-VPS is available [here](https://wikitech.wikimedia.org/wiki/Help:Cloud_VPS_Instances).

_**Note**: that there is an existing project used by the Wikidata team for miscellaneous work: wikidata-dev_

## Access to the WMF Production Stats machines
Documentation for gaining permission to use the stats machines and technical details for accessing this is available
[here](https://wikitech.wikimedia.org/wiki/Analytics/Data_access).

# Steps to run
## 1. Running SS1
This should *not* be run on a production machine.

Clone the repository and run: `make data/whitelisted_ext_idefs.json` from the root of the project.

## 2. Running the item extraction pipe
When running over the whole of the Wikidata entity dumps this should be done on a _powerful_ machine that has access to
the complete dump file.

(The initial development team ran it on stat1005.)

1. Clone the code from the repo to the powerful machine.

2. Copy across your generated `whitelisted_ext_idefs.json` to the data folder. e.g. using scp.

3. Run:
```bash
DUMP_PATH=<path-to-dump-file> make data/extracted_unreferenced_statements.jsonl
```

Make sure to set the `DUMP_PATH` to the dump. We recommend using the gzipped dump due to the quicker decompression
time.

_**Note**:On `stat1005` the path to the dump is: `/mnt/data/xmldatadumps/public/wikidatawiki/entities/latest-all.json.gz`_

## 2. Running the scraper and matchers
This should *not* be run on a production machine. Run it on a Cloud-VPS VM.

Copy `extracted_unreferenced_statements.jsonl` from the stats cluster machine to where you will run the scraper.
Copy in the `data/whitelisted_ext_idefs.json` file you made earlier if not already present.

Run `make`

This should trigger all the remaining jobs and the resultant data in `data/references.jsonl` is now ready for further
manual processing by you or to be [loaded into the Wikidata game](./wikidata-game.md).
