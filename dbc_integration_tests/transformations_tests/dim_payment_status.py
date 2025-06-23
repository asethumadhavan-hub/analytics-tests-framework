from pyspark.sql.functions import col
from dbc_integration_tests.utils.assertions import assert_dataframes

def test_dim_payment_status(spark):

    df = spark.read.table("bizinsights_dev.silver.payment").filter(col("databasename") == "AnalyticsDemoCo_Kubradoc40")

    #print(df.show(5))

    expected_df = (df.select(
        col("paymentstatus").alias("payment_status"),
        col("transactionstatus").alias("transaction_status"))
                   .fillna("-1", subset=["transaction_status"]).distinct().orderBy("payment_status", "transaction_status"))

    actual_df = (spark.read.table("bizinsights_dev.silver.dim_payment_status")).select("payment_status", "transaction_status").orderBy("payment_status", "transaction_status")

    print(f"EXPECTED_COUNT {expected_df.count()}")
    print(f"ACTUAL_COUNT {actual_df.count()}")

    print(f"EXPECTED {expected_df.show()}")
    print(f"ACTUAL {actual_df.show()}")

    assert_dataframes(expected_df, actual_df)

