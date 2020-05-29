# Running SS1
This should *not* be run on a production machine. It can be run on either labs or a developer laptop.

Clone the repository and run: `make data/whitelisted_ext_idefs.json` from the root of the project.

# Running the item extraction pipe
When running over the whole of the Wikidata entity dumps this should be done on a powerful machine that has access to
the complete dump file.

The development team ran it on  stat1005.

Make sure that you've run SS1 first so that `whitelisted_ext_idefs.json` is available.

Clone the code from the repo to the powerful machine. Also copy across your generated `whitelisted_ext_idefs.json` to
the data folder.

Run: ` make data/extracted_unreferenced_statements.jsonl`
