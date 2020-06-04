# Reference Hunt Wikidata Game

This document describes various aspects of the Reference Hunt Wikidata Game: from updating the game's data to deploying new versions.

## Background

The development team for the Reference Island data pipeline implemented a [Wikidata Distributed Game](https://tools.wmflabs.org/wikidata-game/distributed/) to measure the quality of the pipeline, and add references to Wikidata.

For more information about the Wikidata Distributed Game and the Reference Hunt implementation, see the following:
- [Wikidata Distributed Game API documentation](https://bitbucket.org/magnusmanske/wikidata-game/src/master/public_html/distributed/?at=master)
- [Reference Hunt Distributed Game](https://tools.wmflabs.org/wikidata-game/distributed/#game=73)

### Distributed Game Requirements

The Distributed Game platform requires developers to expose an api which provides:
* Serves "tiles" that can then be shown to users.
* Receives sent feedback about user actions. e.g. accepted or rejected tiles
* Provides a small summary for inclusion on the main page of the game (logo, description etc.)

### Game API Hosting

The API must be accessible by the Distributed Game platform over http(s). The development team chose to host the
Reference Hunt game API on [ToolForge](https://gerrit.wikimedia.org/r/admin/projects).

For more information about ToolForge and the specific tool see:
- [ToolForge Documentation](https://wikitech.wikimedia.org/wiki/Help:Toolforge)
- [wd-ref-island Tool Admin Panel](https://tools.wmflabs.org/admin/tool/wd-ref-island)

_**Note**: In order to gain access to the Game API and ToolForge tool, please get in touch with one of the maintainers listed  in the tool's admin panel_

## Updating The Game Data
The Reference Hunt Game API reads potential matches from a mysql database hosted on ToolForge. For an overview of the database schema
please see: [`wikidata_game/game.sql`](../wikidata_game/game.sql).

In order to obtain the potential matches and update the game database, make sure you are listed as a tool maintainer on ToolForge, and follow the steps below:

1. Run the Reference Island [Data Pipeline](pipeline.md) (see: [Production Pipeline Documentation](production-pipeline.md)).

2. Log into ToolForge via ssh.

3. Run the following command to use ToolForge as the `wd-ref-island` tool:

   ```bash
   become wd-ref-island
   ```

4. Upload the potential matches dump (the file called `refernces.jsonl`) to a path under the tool's home directory. 

5. Run the following command ***from the tool's home directory*** to populate the game's database:

   ```bash
   REFS_PATH="<path to references.jsonl>" php -f populator/populator.php
   ```

   _**Note:** don't forget to replace `<path to references.jsonl>` with the actual path to the potential matches dump file._

## Development workflow

Scripts for the game are found in the `wikidata_game` subfolder.

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