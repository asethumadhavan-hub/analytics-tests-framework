import pandas.testing as pdt
import pytest
from pyspark.errors.exceptions.connect import NumberFormatException
from dev_transform_code.some_transform import transform_user_loc


@pytest.mark.parametrize(
    "source_file, target_file, sheet_name", [("source_user_location.xlsx", "expected_user_location.xlsx", "test_positive")]
)
def test_transform_user_loc(load_source_and_expected, spark, source_file, target_file, sheet_name):
    source_df, expected_df = load_source_and_expected(source_file, target_file, sheet_name)
    # Convert source Pandas → Spark
    spark_df = spark.createDataFrame(source_df)

    # Call transformation
    transformed_df = transform_user_loc(spark_df)

    # Convert result back to Pandas
    actual_df = transformed_df.toPandas()

    # Normalize data types for comparison
    for col in ["user_id", "zip"]:
        actual_df[col] = actual_df[col].astype("int64")
        expected_df[col] = expected_df[col].astype("int64")

    try:
        pdt.assert_frame_equal(actual_df.reset_index(drop=True), expected_df.reset_index(drop=True))
    except AssertionError as e:
        print("Assertion failed:\n", e)
        print("\nACTUAL DATAFRAME:")
        print(actual_df)
        print("\nEXPECTED DATAFRAME:")
        print(expected_df)
        raise


@pytest.mark.parametrize(
    "source_file, sheet_name",
    [("source_user_location.xlsx", "test_negative_1")]
)
def test_neg_transform_user_loc(load_source_and_expected, spark, source_file, sheet_name):
    source_df, _ = load_source_and_expected(source_file, None, sheet_name)
    spark_df = spark.createDataFrame(source_df.astype(str))
    with pytest.raises(NumberFormatException):
        transform_user_loc(spark_df).collect()
