from databricks.connect import DatabricksSession
from pyspark.sql.connect.functions import coalesce
from pyspark.sql.functions import from_xml, col, when, lit, lower
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

spark = DatabricksSession.builder.serverless(True).profile("dbc-2f8c933b-7d38").getOrCreate()

def test_dim_payment_mode():

    df = spark.read.table("bizinsights_dev.silver.payment").filter("databasename = 'Reliance_KubraDoc40'")

    xml_schema = StructType([
        StructField("CARDTYPE", StringType(), True),
        StructField("DIVISION", IntegerType(), True),
        StructField("ISCOMMERCIAL", IntegerType(), True),
        StructField("PDMOP", StringType(), True),
        StructField("PROCESSOR", StringType(), True)
    ])

    df_parsed = df.withColumn("parsed", from_xml(col("paymentdata"), xml_schema))
    df_flat = df_parsed \
        .withColumn("card_type", coalesce(col("parsed.CARDTYPE"), col("paymentmode"), lit("-1")))\
        .withColumn("division_id", coalesce(col("parsed.DIVISION"), lit(-1)))\
        .withColumn("is_commercial", when(lower(col("parsed.ISCOMMERCIAL")) == "TRUE", lit(1))
                                            .when(lower(col("parsed.ISCOMMERCIAL")) == "FALSE", lit(0))
                                            .otherwise(lit(-1)))\
        .withColumn("pd_network", coalesce(col("parsed.PDMOP"), lit("-1")))\
        .withColumn("processor", coalesce(col("parsed.PROCESSOR"), lit("-1")))\
        .withColumn("api", when(col("paymentnote").like("%API%"), 1).otherwise(0)) \
        .withColumn("csr", when(col("paymentnote").like("CSR%"), col("paymentnote"))
                                   .otherwise("-1"))\
        .withColumn("payment_mode", coalesce(col("paymentmode"), lit("-1")))\
        .drop("parsed")

    columns_to_select = ["api", "card_type", "csr", "division_id", "is_commercial", "payment_mode", "pd_network", "processor"]
    expected_df =  df_flat.select(*columns_to_select)\
                 .fillna(-1, subset=["division_id"])\
                 .fillna("-1", subset=["api", "card_type", "csr", "payment_mode", "pd_network", "processor"])\
                 .distinct()\
                 .orderBy(*columns_to_select)


    actual_df =  spark.read.table("bizinsights_dev.silver.dim_payment_mode")\
                   .select(*columns_to_select)\
                   .orderBy(*columns_to_select)

    print(f"EXPECTED_COUNT {expected_df.show()}")
    print(f"ACTUAL_COUNT {actual_df.show()}")


    print(f"EXPECTED_COUNT {expected_df.count()}")
    print(f"ACTUAL_COUNT {actual_df.count()}")

    print(expected_df.filter(col("division_id") != lit(-1)).count())
    #assert_dataframes(expected_df, actual_df)

