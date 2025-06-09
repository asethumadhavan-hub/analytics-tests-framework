import yaml
from databricks.connect import DatabricksSession
from pyspark.sql.functions import from_xml, col, schema_of_xml, lit
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

spark = DatabricksSession.builder.serverless(True).profile("dbc-2f8c933b-7d38").getOrCreate()

def test_dim_payment_status():

    df = spark.read.table("bizinsights_dev.silver.payment").filter(col("databasename") == "AnalyticsDemoCo_Kubradoc40")

    #print(df.show(5))

    df_actual = (df.select(
        col("paymentstatus").alias("payment_status"),
        col("transactionstatus").alias("transaction_status"))
                 .fillna("-1", subset=["transaction_status"]).distinct().orderBy("payment_status", "transaction_status"))

    df_expected = (spark.read.table("bizinsights_dev.silver.dim_payment_status")).select("payment_status", "transaction_status").orderBy("payment_status", "transaction_status")

    print(f"ACTUAL_COUNT {df_actual.count()}")
    print(f"EXPECTED_COUNT {df_expected.count()}")

    assert(df_actual, df_expected)

