def pandas_to_spark(spark, pandas_df):
    return spark.createDataFrame(pandas_df)
