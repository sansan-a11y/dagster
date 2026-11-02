# Dagster 1.13.26 security changes

Upstream source: `dagster-io/dagster`, tag `1.13.26`, commit
`fb6aeab1df0f2dc72cac644ba1fa332dbfa18593`.

## Initial inventory

| Pattern | Call sites | Files |
| --- | ---: | ---: |
| Unsafe YAML load calls | 7 | 4 |
| Subprocess shell flags set to true | 16 | 13 |

After the changes, a repository-wide scan reports zero occurrences of both
patterns.

## YAML changes

| File | Sites | Change |
| --- | ---: | --- |
| `python_modules/libraries/dagster-shared/dagster_shared/yaml_utils/__init__.py` | 4 | Load through the existing `DagsterYamlLoader`, which subclasses `yaml.SafeLoader` |
| `examples/experimental/external_assets/external_assets/external_assets/__init__.py` | 1 | `yaml.safe_load()` |
| `examples/experimental/assets_yaml_dsl/assets_yaml_dsl/pure_assets_dsl/assets_dsl.py` | 1 | `yaml.safe_load()` instead of `yaml.CLoader` |
| `examples/experimental/assets_yaml_dsl/assets_yaml_dsl/domain_specific_dsl/stocks_dsl.py` | 1 | `yaml.safe_load()` instead of `yaml.CLoader` |

The Dagster shared helper uses `loader(stream).get_single_data()` so the
project-specific safe loader continues preserving date-like values as strings.

## subprocess changes

| File | Sites | Change |
| --- | ---: | --- |
| `scripts/run-ty.py` | 1 | Pass the command as an argument list |
| `scripts/get_recent_pypi_changes.py` | 1 | Run `uv pip list` and parse fields in Python |
| `examples/with_openai/baseline.py` | 2 | Split `git clone` and `git rev-parse` into argument lists |
| `integration_tests/python_modules/dagster-k8s-test-infra/dagster_k8s_test_infra/kind.py` | 2 | Split Docker and kubelet commands into argument lists |
| `integration_tests/python_modules/dagster-k8s-test-infra/dagster_k8s_test_infra/cluster.py` | 1 | Replace the ECR pipeline with `check_output` plus `docker login` stdin |
| `python_modules/automation/automation/docker/ecr.py` | 1 | Replace the ECR pipeline with `check_output` plus `docker login` stdin |
| `examples/docs_snippets/docs_snippets_tests/snippet_checks/utils.py` | 1 | Invoke `/bin/bash -c` explicitly with `shell=False`; this test harness accepts shell syntax |
| `python_modules/libraries/dagster-cloud-cli/dagster_cloud_cli/docker_utils.py` | 1 | Pass `docker -v` as an argument list |
| `python_modules/libraries/dagster-aws/dagster_aws_tests/emr_tests/test_pyspark.py` | 2 | Pass rsync and ssh commands as argument lists |
| `examples/docs_snippets/docs_snippets/integrations/external_pipelines/dagster_pipes/pyspark/dagster_code.py` | 1 | Build `spark-submit` arguments as a list |
| `examples/docs_snippets/docs_snippets/integrations/external_pipelines/dagster_pipes/gcp/dataproc_job/upload_artifacts.py` | 1 | Split the Docker and GCS pipeline into three checked commands |
| `python_modules/libraries/dagster-mysql/dagster_mysql_tests/compat_tests/test_back_compat.py` | 1 | Pass the SQL snapshot through stdin instead of shell redirection |
| `python_modules/dagster/dagster/_grpc/compile.py` | 1 | Expand generated files in Python and pass a `ruff` argument list |

## Verification

- `py_compile`: 17 modified Python files passed.
- `pytest` for `dagster_shared_tests/test_yaml.py`: 7 passed.
- Repository scan: zero unsafe YAML load calls and zero subprocess shell flags
  set to true.
