from datetime import timedelta
from pyspark.sql.functions import col, date_format, year, month, dayofmonth, dayofweek, weekofyear, last_day, trunc
from databricks.connect import DatabricksSession

spark = DatabricksSession.builder.serverless(True).profile("dbc-2f8c933b-7d38").getOrCreate()

def generate_calendar_df(start_date, end_date):
    date_list = [(start_date + timedelta(days=x),) for x in range((end_date - start_date).days + 1)]
    df = spark.createDataFrame(date_list, ["date"])
    return df.withColumn("date_key", date_format(col("date"), "yyyyMMdd").cast("int")) \
        .withColumn("year", year("date")) \
        .withColumn("month", month("date")) \
        .withColumn("day", dayofmonth("date")) \
        .withColumn("week", weekofyear("date")) \
        .withColumn("day_of_week", dayofweek("date")) \
        .withColumn("day_name", date_format(col("date"), "EEEE")) \
        .withColumn("month_name", date_format(col("date"), "MMMM")) \
        .withColumn("quarter", ((month(col("date")) - 1) / 3 + 1).cast("int")) \
        .withColumn("is_weekend", (col("day_of_week").isin([1, 7])).cast("boolean")) \
        .withColumn("first_day_of_month", trunc(col("date"), "month")) \
        .withColumn("last_day_of_month", last_day("date"))