from pyspark.sql.functions import col, when
from dbc_integration_tests.utils.assertions import assert_dataframes


def test_gold_mat_vw_rcp(spark):
    df1 = (spark.table("bizhq_dev.silver.payment_view_details")
             .select("payment_id", "realm", "client_id", "channel", "account_number", "payment_date", "payment_amount", "fee_amount",
                     "item_incomm_configuration_biller_id", "item_incomm_configuration_currency_code", "item_incomm_context_external_account_id",
                     "item_incomm_context_bar_code", "item_incomm_context_external_payment_id", "item_incomm_context_retailer_id",
                     "item_incomm_context_retailer_name", "item_incomm_context_store_id", "payment_processor_code")
                 .filter("channel = 'RCP'"))
    df2 = spark.table("bizhq_dev.silver.retail_cash_payments").select(
        when(col("Address1").isNull(), col("Address2")).otherwise(col("Address1")).alias("retailer_address"),
        col("city").alias("retailer_city"),
        col("state").alias("retailer_state"),
        col("zip_code").alias("retailer_zip"),
        col("county").alias("retailer_country"),
        col("internal_store_id")
    )

    df_joined = ((df1.join(df2, df1["item_incomm_context_store_id"] == df2["internal_store_id"], how="left")
                 .filter(col("payment_processor_code") == "Incomm"))
                 .select("payment_id", "realm", "client_id", "account_number", "payment_date", "payment_amount",
                         col("fee_amount").alias("conv_fee_amount"),
                         col("item_incomm_context_retailer_id").alias("retailer_id"),
                         col("item_incomm_context_retailer_name").alias("retailer_name"),
                         "retailer_address", "retailer_city", "retailer_state", "retailer_zip", "retailer_country",
                         col("item_incomm_context_bar_code").alias("bar_code")))

    df_target = spark.table("bizhq_dev.gold.mat_vw_retail_cash_payments")
    assert_dataframes(df_joined, df_target)