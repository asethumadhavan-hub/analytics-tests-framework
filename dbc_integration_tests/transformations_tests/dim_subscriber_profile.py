from databricks.connect import DatabricksSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window

#def test_dim_subscriber_profile():

spark = DatabricksSession.builder.serverless(True).profile("dbc-2f8c933b-7d38").getOrCreate()
w = Window.partitionBy("user_id", "id").orderBy("last_accessed")

df = spark.read.table("bizinsights_dev.silver.subscriber_profile")\
    .filter("databasename = 'AnalyticsDemoCo_Kubradoc40'")

expected_df = df.withColumn("from_date", col("insert_timestamp").cast("date"))\
                .withColumn("to_date", lead("insert_timestamp").over(w).cast("date"))\
                .withColumn("to_date", coalesce(col("to_date"), lit("9999-12-31").cast("date")))\
                .withColumn("current_flag", when(col("to_date") == lit("9999-12-31"), 1).otherwise(0))\
                .select("user_id", "id", "from_date", "to_date", "current_flag")

actual_df = spark.read.table("bizinsights_dev.silver.dim_subscriber_profile")\
                .filter("client_name = 'AnalyticsDemoCo_Kubradoc40'")

#assert_dataframes(expected_df, actual_df)


print(expected_df.filter(col("current_flag") == 0).show())
print(actual_df.filter(col("current_flag") == 0).show())
