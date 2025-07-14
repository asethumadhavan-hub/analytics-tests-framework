import pandas.testing as pdt
import pytest
from dev_transform_code.dim_csr_transform import transform_dim_csr
from pyspark.sql.utils import AnalysisException

@pytest.mark.parametrize(
    "source_file, target_file, sheet_name", [("source_csr_dim.xlsx", "expected_csr_dim.xlsx", "test_positive")]
)
def test_dim_csr(load_source_and_expected, spark, source_file, target_file, sheet_name):
    source_df, expected_df = load_source_and_expected(source_file, target_file, sheet_name)

    # Convert source Pandas to Spark
    spark_df = spark.createDataFrame(source_df)

    # Call transformation
    transformed_df = transform_dim_csr(spark_df)

    # Convert result back to Pandas
    actual_df = transformed_df.toPandas()
    actual_df = actual_df[["csr", "client_name"]]

    # Force string type for all columns to ensure exact match
    actual_df = actual_df.sort_values(by=["csr", "client_name"]).reset_index(drop=True)
    expected_df = expected_df.sort_values(by=["csr", "client_name"]).reset_index(drop=True)

    pdt.assert_frame_equal(actual_df, expected_df)


@pytest.mark.parametrize(
    "source_file, sheet_name, expected_exception", [("source_csr_dim.xlsx", "test_negative_case_1", AnalysisException)]
)
def test_negative_customer_dim(load_source_and_expected, source_file, sheet_name, expected_exception, spark):
    source_df, _ = load_source_and_expected(source_file, expected_file=None, sheet_name=sheet_name)
    source_df = spark.createDataFrame(source_df)

    with pytest.raises(expected_exception):
        print(transform_dim_csr(source_df))