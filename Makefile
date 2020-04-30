data/whitelisted_ext_idefs.json: 
	python3 wikidatarefisland/run.py --step ss1 --output "whitelisted_ext_idefs.json"

data/matched_references.jsonl: \
	data/scraped_data.jsonl
	python3 wikidatarefisland/run.py --step match --input "scraped_data.jsonl" --output "matched_references.jsonl"
