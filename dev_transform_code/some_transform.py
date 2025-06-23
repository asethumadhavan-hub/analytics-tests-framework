from pyspark.sql.functions import col, concat_ws, upper
from databricks.connect import DatabricksSession

spark = DatabricksSession.builder.serverless(True).profile("dbc-2f8c933b-7d38").getOrCreate()

df = spark.read.table("bizinsights_dev.silver.subscriber_profile")\
      .filter("databasename = 'AnalyticsDemoCo_Kubradoc40'")

def transform_user_loc(df):
    return (
        df.select("user_id", "city", "zip", "state")
        .filter(col("user_id").isNotNull() & col("zip").isNotNull())
        .withColumn("city", upper(col("city").cast("string")))
        .withColumn("state", upper(col("state").cast("string")))
        .withColumn("zip", col("zip").cast("int").cast("string"))
        .withColumn("location_code", concat_ws("-", col("state"), col("zip")))
    )