from pyspark.sql import DataFrame
from pyspark.sql.functions import col

def assert_dataframes(expected_df, actual_df):
#    schema_match = df_actual.schema == df_expected.schema
#    if not schema_match:
#        raise AssertionError(f"Schema mismatch:\n{df_actual.schema}\n!=\n{df_expected.schema}")

    # Check if actual has any rows not in expected
    diff_actual = actual_df.subtract(expected_df)
    extra_actual = diff_actual.count()
    if extra_actual > 0:
        print("Extra rows in actual:")
        diff_actual.show(truncate=False)
        raise AssertionError(f"Actual DataFrame has {extra_actual} extra rows.")

    # Check if expected has any rows not in actual
    diff_expected = expected_df.subtract(actual_df)
    extra_expected = diff_expected.count()
    if extra_expected > 0:
        print("Missing rows in actual (present in expected):")
        diff_expected.show(truncate=False)
        raise AssertionError(f"Expected DataFrame has {extra_expected} extra rows.")
