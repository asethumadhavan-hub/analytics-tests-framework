from databricks.connect import DatabricksSession
from utils.assertions import assert_dataframes_equal_spark

spark = DatabricksSession.builder.serverless(True).profile("dbc-2f8c933b-7d38").getOrCreate()

def test_dim_subscriber_activity():

    df_actual = spark.read.table("bizinsights_dev.silver.subscriber_activity")\
          .filter("databasename = 'AnalyticsDemoCo_Kubradoc40'")\
          .select("activity").withColumnRenamed("activity", "activity_desc").distinct()

    df_expected = spark.read.table("bizinsights_dev.silver.dim_subscriber_activity")\
                   .select("activity_desc")

    print(f"ACTUAL_COUNT {df_actual.count()}")
    print(f"EXPECTED_COUNT {df_expected.count()}")

    assert_dataframes_equal_spark(df_actual, df_expected)

