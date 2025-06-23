import pytest
import pandas as pd
import os


@pytest.fixture
def load_source_and_expected():
    def _loader(source_file=None, expected_file=None, sheet_name=None):
        base_path = os.path.dirname(__file__)
        source, expected = None, None

        if source_file:
            source_path = os.path.join(base_path, "source_data", source_file)
            source = pd.read_excel(source_path, sheet_name) if sheet_name else pd.read_excel(source_path)

        if expected_file:
            target_path = os.path.join(base_path, "target_data", expected_file)
            expected = pd.read_excel(target_path, sheet_name) if sheet_name else pd.read_excel(target_path)

        return source, expected

    return _loader