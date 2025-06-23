from databricks.connect import DatabricksSession
from dbc_integration_tests.utils.assertions import assert_dataframes

spark = DatabricksSession.builder.serverless(True).profile("dbc-2f8c933b-7d38").getOrCreate()

def test_dim_subscriber_activity():

    expected_df = spark.read.table("bizinsights_dev.silver.subscriber_activity")\
          .filter("databasename = 'AnalyticsDemoCo_Kubradoc40'")\
          .select("activity").withColumnRenamed("activity", "activity_desc").distinct().orderBy("activity_desc")

    actual_df = spark.read.table("bizinsights_dev.silver.dim_subscriber_activity")\
                   .select("activity_desc").orderBy("activity_desc")

    print(f"EXPECTED_COUNT {expected_df.count()}")
    print(f"ACTUAL_COUNT {actual_df.count()}")

    print(f"EXPECTED {expected_df.show()}")
    print(f"ACTUAL {actual_df.show()}")

    assert_dataframes(expected_df, actual_df)

