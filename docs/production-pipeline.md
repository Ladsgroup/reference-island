# Running the Data Pipeline
This documentation is for developers wishing to run the pipeline in a large scale. It concisely describes how to analyse **all of Wikidata** in order to obtain potential reference matches.

## Prerequisites
Running the Reference Island data pipeline on a large scale Wikidata dump is a process that requires multiple machines and a length of time. It is **not** recommended to run the entire pipeline on a developer laptop for large scale dumps because:

- Wikidata dumps are pretty large: ≈100s of GB uncompressed.
- Processing time for the entire pipeline is relatively long: According to the latest estimation, >40 days.

As a more robust solution, the development team recommends to run most of the pipeline on a Virtual Machine on [WMF's Cloud VPS](https://wikitech.wikimedia.org/wiki/Portal:Cloud_VPS) with the exception of [Pipe 1: Item Extractor](pipeline.md#pipe-1-item-extractor).

For Pipe 1 to read the complete dumps it is advisable to run on a machine in the [WMF Analytics cluster](https://wikitech.wikimedia.org/wiki/Analytics/Systems/Cluster). This is recommended because the machines in the Analytics cluster have the complete dumps available on fast storage.

The following documentation assumes that you:
- Have [set-up a Cloud VPS VM](https://wikitech.wikimedia.org/wiki/Help:Cloud_VPS_Instances)

    _**Note**: the Wikidata team has a Cloud VPS project called `wikidata-dev` for miscellaneous work_

- Have [permissions to access to the Analytics Cluster](https://wikitech.wikimedia.org/wiki/Analytics/Data_access)


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
