data/whitelisted_ext_idefs.json: 
	python3 wikidatarefisland/run.py --step ss1 --output "whitelisted_ext_idefs.json"
data/extracted_unreferenced_statements.jsonl: \
	data/whitelisted_ext_idefs.json
	python3 wikidatarefisland/run.py --step extract_items --side-service-input "whitelisted_ext_idefs.json" --input "dump.json" --output "extracted_unreferenced_statements.jsonl"
data/scraped_data.jsonl: \
	extracted_unreferenced_statements.jsonl
	python3 wikidatarefisland/run.py --step scrape --input "extracted_unreferenced_statements.jsonl" --output "scraped_data.jsonl"
data/matched_references.jsonl: \
	data/scraped_data.jsonl
	python3 wikidatarefisland/run.py --step match --input "scraped_data.jsonl" --output "matched_references.jsonl"
