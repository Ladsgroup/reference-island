# Reference Hunt Wikidata Game

This document describes various aspects of the Reference Hunt Wikidata Game: from updating the game's data to deploying new versions.

## Background

The development team for the Reference Island data pipeline implemented a [Wikidata Distributed Game](https://tools.wmflabs.org/wikidata-game/distributed/) to measure the quality of the pipeline, and add references to Wikidata. For more information about the Wikidata Distributed Game and the Reference Hunt implementation, see the following:

- [Wikidata Distributed Game API documentation](https://bitbucket.org/magnusmanske/wikidata-game/src/master/public_html/distributed/?at=master)

- [Reference Hunt Distributed Game](https://tools.wmflabs.org/wikidata-game/distributed/#game=73)

### Distributed Game Requirements

The platform requires an api to be provided that:

1. serves "tiles" that can then be shown to users.
1. receives sent feedback about user actions. e.g. accepted or rejected tiles
1. provides a small summary for inclusion on the main page of the game (logo, description etc..)

### Game API Hosting

The API must be accessible by the platform over http(s). We therefore chose to host our game on toolforge.

Documentation for toolforge can be found: [here](https://wikitech.wikimedia.org/wiki/Help:Toolforge)

It is hosted under the tool name: `wd-ref-island`. Current maintainers can be found [here](https://tools.wmflabs.org/admin/tool/wd-ref-island).
You can get in touch with them to request access.

## Updating The Game Data
Load data using `wikidata_game/populator.php` which should be run with the env variable `REFS_PATH` set to a JSON file
containing the references in one large array.

```bash
RAFS_PATH="<path-to-refs.json>" php wikidata_game/populator.php
```

## Development workflow

Scripts for the game are found in the wikidata_game subfolder.

### Running a copy of the game locally

There is a docker-compose setup to simulate running the game api. It should work out of the box with `docker-compose
 up` in the root of this repository.

The service will be available on http://localhost:8100

To customise please look in docker-compose.yml.

Note: a custom docker image derived from the official php 7.3 apache image was used to enable the PDO extension.

The Dockerfiles and simulated config files are available in `./docker_config`

### Installing composer dependencies

To install the project's dependencies, run the following command from the `wikidata_game` directory:

```bash
php bin/composer install
```

### Running phpunit

To run the phpunit tests locally, run the following command from the `wikidata_game` directory:

```bash
php bin/composer run-script test
```

## Deployment

The tool was setup manually and includes code to keep the game scripts updated when new commits are made to the master
branch of this repository on github.

It also provides a staging environment to test new versions of the api.

### Staging and automatic deployment to toolforge

1. Make sure to prefix your branch name with `game-` otherwise automatic deployment and staging would not work
2. Once you would like to preview your changes, create a WIP pull request to this repository. This will create a staged api version from your branch.
3. To preview your changes go to `https://tools.wmflabs.org/wd-ref-island/test.php?branch=<your branch name>` to see a live test of the game on your branch.
4. Once your pull request is merged, the game will be automatically deployed to https://tools.wmflabs.org/wikidata-game/distributed/#game=73 .

[Refer to above for depenedency install]