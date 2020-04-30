data/whitelisted_ext_idefs.json: 
	python3 wikidatarefisland/run.py --step ss1 --output "whitelisted_ext_idefs.json"

data/matched_references.jsonl: \
	data/potential_references.jsonl
	python3 wikidatarefisland/run.py --step match --input "potential_references.jsonl" --output "matched_references.jsonl"
