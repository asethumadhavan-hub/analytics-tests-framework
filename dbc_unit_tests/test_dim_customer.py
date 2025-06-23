import pandas.testing as pdt
from dev_transform_code.dim_transform_customer import transform_customer_dim
import pytest

@pytest.mark.parametrize(
    "source_file, target_file, sheet_name", [("source_customer_dim.xlsx", "expected_customer_dim.xlsx", "test_positive")]
)

def test_transform_customer_dim(load_source_and_expected, source_file, target_file, sheet_name):
    source_df, expected_df = load_source_and_expected(source_file, target_file, sheet_name)

    actual_df = transform_customer_dim(source_df)
    pdt.assert_frame_equal(actual_df.reset_index(drop=True), expected_df.reset_index(drop=True))

@pytest.mark.parametrize(
    "source_file, sheet_name, expected_exception", [("source_customer_dim.xlsx", "test_negative_1", KeyError)]
)
def test_negative_customer_dim(load_source_and_expected, source_file, sheet_name, expected_exception):
    source_df, _ = load_source_and_expected(source_file, expected_file=None, sheet_name=sheet_name)

    with pytest.raises(expected_exception):
        print(transform_customer_dim(source_df))


