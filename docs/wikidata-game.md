# Introduction
In order to measure the quality fo the pipeline, and to add references to Wikidata we implemented a version of the distributed game.

The main page of the game platform can be found: [here](https://tools.wmflabs.org/wikidata-game/distributed/)

The code for the platform that the games runs on can be found: [here](https://bitbucket.org/magnusmanske/wikiata-game/src/master/public_html/distributed/)

The version of the game deployed in May 2020 by the Reference Island team can be found: [here](https://tools.wmflabs.org/wikidata-game/distributed/#game=73)

# Hosting our Game
The platform requires an api to be provided that:
1. serves "tiles" that can then be shown to users.
1. receives sent feedback about user actions. e.g. accepted or rejected tiles
1. provides a small summary for inclusion on the main page of the game (logo, description etc..)

The API must be accessible by the platform over http(s). We therefore chose to host our game on toolforge.

Documentation for toolforge can be found: [here](https://wikitech.wikimedia.org/wiki/Help:Toolforge)

It is hosted under the tool name: `wd-ref-island`. Current maintainers can be found [here](https://tools.wmflabs.org/admin/tool/wd-ref-island).
You can get in touch with them to request access.

The tool was setup manually and includes code to keep the game scripts updated when new commits are made to the master
branch of this repository on github.

It also provides a staging environment to test new versions of the api.

Scripts for the game are found in the wikidata_game subfolder.

For more details see [corresponding section](../README.md#making-changes-to-the-wikidata-game) in the main README.

# Loading data into the game
Load data using `wikidata_game/populator.php` which should be run with the env variable `REFS_PATH` set to a JSON file
containing the references in one large array.

```bash
RAFS_PATH="<path-to-refs.json>" php wikidata_game/populator.php
```
