import pytest
import yaml
from functools import lru_cache
from databricks.connect import DatabricksSession


#  Spark Session Fixture — runs once per test session
@pytest.fixture(scope="session")
def spark():
    print("STARTING SPARK SESSION")
    spark = DatabricksSession.builder.serverless(True).profile("dbc-2f8c933b-7d38").getOrCreate()
    yield spark
    print("STOPPING SPARK SESSION")
    spark.stop()


#  Load YAML metadata (cached)
@lru_cache()
def load_metadata():
    with open("../metadata/metadata.yaml") as f:
        raw = yaml.safe_load(f)


    not_null_params = [
        (entry["table"], col)
        for entry in raw.get("not_null", [])
        for col in entry.get("columns", [])
    ]

    duplicate_params = [
        (entry["table"], col_group)
        for entry in raw.get("duplicate", [])
        for col_group in entry.get("columns", [])
    ]

    schema_params = []
    for entry in raw.get("schema_check", []):
        table = entry["table"]
        columns = {}
        for col_entry in entry["columns"]:
            for col_name, expected_type in col_entry.items():
                columns[col_name] = expected_type
        schema_params.append((table, columns))

    row_count_params = [
        (entry["source_table"], entry["target_table"], entry.get("client"))
        for entry in raw.get("row_count", [])
    ]

    return {
        "test_not_null": not_null_params,
        "test_duplicate": duplicate_params,
        "test_data_type": schema_params,
        "test_column_presence": schema_params,
        "test_row_count": row_count_params
    }

#  Pytest hook to parametrize tests
def pytest_generate_tests(metafunc):
    test_map = load_metadata()
    test_name = metafunc.function.__name__

    print(f"Test Name: {test_name}")
    print(f"Param Keys: {test_map.keys()}")


    if test_name in test_map:
        params = test_map[test_name]

        if test_name == "test_row_count":
            metafunc.parametrize(("source_table", "target_table", "client"), params)

        elif test_name in ["test_column_presence", "test_data_type"]:
            metafunc.parametrize(("table", "columns"), params)

        else:
            metafunc.parametrize(("table_name", "column"), params)
    else:
        print(f"No parameters found for {test_name}")
