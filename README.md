# DE DBT Example

This repository is a showcase for the usage of [dbt (data build tool)](https://docs.getdbt.com/)

Be sure to checkout this guide from gitlab [Gitlab DBT Guide](https://about.gitlab.com/handbook/business-technology/data-team/platform/dbt-guide)
## Usage

The usage section was written and tested for Windows WSL2 using Ubuntu (see the installation guide in the [CI Confluence](https://cologne-intelligence.atlassian.net/wiki/spaces/CIDD/pages/49676386/Setup+DE+Entwicklungsumgebung)). If you're using another system, some commands may vary.

**Clone the Bitbucket repository to your local machine**

`git clone https://bitbucket.cgn.co-in.de:8443/scm/cidd/de-dbt-example.git`

**Setup a venv and install the required packages via poetry**

See [Poetry Installation](https://python-poetry.org/docs/#installation) and [Poetry Usage](https://python-poetry.org/docs/basic-usage/) in case you do not have experience with it.

Open another shell and setup poetry:

```bash
# Install the required dependencies via poetry
poetry install

# Enter the poetry sub-shell to access the newly installed python packages
# This allows you to use e.g. dbt from the CLI
poetry shell

# Start the postgres backend using docker compose in detached mode
# I.e. the container ouputs are not shown in the terminal and you can continue to use the same terminal
# NOTE: Make sure you started Docker Desktop, otherwise you'll get an error saying docker-compose command is not known
docker-compose up -d
```

**Refresh Postgres Jaffle Shop schema**

In order to setup the Postgres database with the example Jaffle Shop data, run `python demo.py -o reset`.
This can also be used to reset the database at a later point in development.

**Run dbt for the first time**

Re-enter the shell and run dbt for the first time:

```bash
cd jaffle_shop

# Install the dbt dependecies specified in jaffle_shop/packages.yml.
# This is used for dbt tests. See the "Tests" section for more information
dbt deps

# This is necessary to avoid errors with the other components of this showcase
# For a more detailed explanation on what this does and why it's necessary,
# see the "Snapshots" section
dbt snapshot

dbt run --full-refresh
```

**What did just happen?**

You used dbt to orchestrate and execute a series of CREATE TABLE and CREATE VIEW statements against your Postgres backend. To see the results, connect to your local Postgres instance using a database client of your choice, e.g. Azure Data Studio or DBeaver:

```
Host: localhost
Port: 5432
User: postgres
Password: postgres
Database (or Schema): jaffle_shop
```

You should find various tables in the `raw` and `dbt_postgres` schemas as well as some views under `dbt_postgres_staging`. You can now start to develop new models and execute them via the dbt CLI ([dbt command overview](https://docs.getdbt.com/reference/dbt-commands)). If you want to reset the database, use `poetry run demo.py -o reset`.

**Create and show docs**

With following commands you can create and serve the docs to the browser

```bash
dbt docs generate
dbt docs serve
```

**Example command order**

```bash
dbt source freshness            #check the freshness of all sources
dbt test -s source:*            #run tests on sources
dbt run                         #build models
dbt test --exclude source:*     #test builded models
```

---

For the explanation of other dbt features see the following README files:
- [Snapshots.md](docs/snapshots.md)
- [Tests.md](docs/tests.md)
- [Incremental_Models.md](docs/incremental_models.md)
