import pytest
import pandas as pd
import os

# READ DATA DIRECTLY FROM EXCEL
@pytest.fixture
def load_source_and_expected():
    def _loader(source_file=None, expected_file=None, sheet_name=None):
        base_path = os.path.dirname(__file__)
        source, expected = None, None

        if source_file:
            source_path = os.path.join(base_path, "source_data", source_file)
            source = pd.read_excel(source_path, sheet_name, dtype=str) if sheet_name else pd.read_excel(source_path, dtype=str)

        if expected_file:
            target_path = os.path.join(base_path, "target_data", expected_file)
            expected = pd.read_excel(target_path, sheet_name, dtype=str) if sheet_name else pd.read_excel(target_path, dtype=str)

        return source, expected

    return _loader


# READ DATA DIRECTLY FROM SANDBOX TEST TABLES
@pytest.fixture
def load_sandbox_and_expected(load_source_and_expected, spark):
    def _loader(table_name, expected_file=None, sheet_name=None):
        source_df = spark.read.table(table_name)  # Spark DataFrame
        _, expected_df = load_source_and_expected(None, expected_file, sheet_name)  # Pandas DataFrame
        return source_df, expected_df
    return _loader
