## Tests

Data tests enable to assess if a model returns the data it is supposed to return. This can be used by developers to during development, but also by users of the models in order to check data quality. Overall, testing in dbt makes sure that certain assumptions for the processed data hold.

There are two types of dbt tests: Singular tests and generic tests. Singular tests are defined under `jaffle_shop/tests`, while generic tests live in `jaffle_shop/tests/generic`. Generic tests use the Jinja markdown language and are used in the `schema.yml` file of the individual stages.

For more information on dbt tests see:
- [getdbt.com - Tests](https://docs.getdbt.com/docs/build/tests)
- [getdbt.com - Writing custom generic tests](https://docs.getdbt.com/guides/best-practices/writing-custom-generic-tests)

**dbt Tests**

In order to test your models run

```bash
# NOTE: This might fail if you have not run `dbt deps` beforehand. See the section `dbt-expectations` for further explanation
dbt test
```

To test a single model run `dbt test -s <model name>`. E.g. to test only the stg_payments model you can run `dbt test -s stg_payments`.

**dbt-expectations**

[dbt-expectations](https://github.com/calogica/dbt-expectations) is a [package for dbt](https://docs.getdbt.com/docs/build/packages) porting the functionality of [Great Expectations](https://greatexpectations.io/) to dbt. To use it, run the following code:

```bash
cd jaffle_shop

# Run dbt tests (dbt-expectations tests are already defined in models/staging/schema.yml)
dbt test
```

In general, dbt-expectations is a collection of common test cases that are already implemented as generic dbt tests. Examples for those test cases are:
- Is a column (not) present in the data
- Is a column conform with a custom regular expression
- Is the sum of a column within a certain range

For a full documentation of the test cases see [dbt-expectations](https://github.com/calogica/dbt-expectations).
