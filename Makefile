data/whitelisted_ext_idefs.json: 
	python3 wikidatarefisland/run.py --step ss1 --output "whitelisted_ext_idefs.json"
data/pipe2.json:
	python3 wikidatarefisland/run.py --step pipe2 --input "pipe1.json" --output "pipe2.json"
