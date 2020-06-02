# Setting up a labs VM
If you need an environment to run this scraper other than a laptop consider using cloud-vps
See https://wikitech.wikimedia.org/wiki/Help:Cloud_VPS_Instances

_**Note**: that there is an existing project used by the Wikidata team for miscellaneous work: wikidata-dev_

# Running SS1
This should *not* be run on a production machine. It can be run on either labs or a developer laptop.

Clone the repository and run: `make data/whitelisted_ext_idefs.json` from the root of the project.

# Running the item extraction pipe
Make sure that you've run SS1 first so that `whitelisted_ext_idefs.json` is available.

When running over the whole of the Wikidata entity dumps this should be done on a _powerful_ machine that has access to
the complete dump file.

(The development team ran it on  stat1005.)

1 .Clone the code from the repo to the powerful machine. Also copy across your generated `whitelisted_ext_idefs.json` to
the data folder. e.g. using scp.

2. Run:
`DUMP_PATH="/mnt/data/xmldatadumps/public/wikidatawiki/entities/latest-all.json.gz" make data/extracted_unreferenced_statements.jsonl`

Where dump path is set to the patch to the dump. We recommend using the gzipped dump due to the quicker decompression
time.

# Running the scraper and matchers
This should *not* be run on a production machine. It can be run on either labs (or a developer laptop with a small dataset).

You should copy `extracted_unreferenced_statements.jsonl` from the production machine to where you will run the scraper.
You should also copy in the `data/whitelisted_ext_idefs.json` file you made earlier

Run `make` #todo double check

This should trigger all the remaining jobs and the resultant data in `data/references.jsonl` is now ready for further
manual processing by you or to be loaded into the Wikidata game. See `./wikidata-game.md`
