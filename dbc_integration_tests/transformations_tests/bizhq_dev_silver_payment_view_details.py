from pyspark.sql.functions import col, lower
from dbc_integration_tests.utils.assertions import assert_dataframes


def test_silver_payment_view_details(spark):
    df = spark.read.table("bizhq_dev.bronze.payment_transaction")\
           .select("_id", "Realm", "ClientId", "Channel", "Account", "PaymentDate", "PaymentAmount", "FeeAmount", "ItemIncommConfiguration", "ItemIncommContext", "PaymentProcessorCode")\
           .filter("Channel = 'RCP'")

    df_flat = df.select(
        col("_id").alias("payment_id"),
        lower(col("Realm")).alias("realm"),
        col("ClientId").alias("client_id"),
        col("Channel").alias("channel"),
        col("Account.AccountNumber").alias("account_number"),
        col("PaymentDate").alias("payment_date"),
        col("PaymentAmount").alias("payment_amount"),
        col("FeeAmount").alias("fee_amount"),
        col("ItemIncommConfiguration.BillerId").alias("item_incomm_configuration_biller_id"),
        col("ItemIncommConfiguration.CurrencyCode").alias("item_incomm_configuration_currency_code"),
        col("ItemIncommContext.ExternalAccountId").alias("item_incomm_context_external_account_id"),
        col("ItemIncommContext.Barcode").alias("item_incomm_context_bar_code"),
        col("ItemIncommContext.ExternalPaymentId").alias("item_incomm_context_external_payment_id"),
        col("ItemIncommContext.RetailerId").alias("item_incomm_context_retailer_id"),
        col("ItemIncommContext.RetailerName").alias("item_incomm_context_retailer_name"),
        col("ItemIncommContext.StoreId").alias("item_incomm_context_store_id"),
        col("PaymentProcessorCode").alias("payment_processor_code")
    )

    df_target = (spark.table("bizhq_dev.silver.payment_view_details")
             .select("payment_id", "realm", "client_id", "channel", "account_number", "payment_date", "payment_amount", "fee_amount",
                     "item_incomm_configuration_biller_id", "item_incomm_configuration_currency_code", "item_incomm_context_external_account_id",
                     "item_incomm_context_bar_code", "item_incomm_context_external_payment_id", "item_incomm_context_retailer_id",
                     "item_incomm_context_retailer_name", "item_incomm_context_store_id", "payment_processor_code")
                 .filter("channel = 'RCP'"))

    df1 = df_flat.dropDuplicates()
    df2 = df_target.dropDuplicates()

    print(f"Actual data count {df1.count()} \nTarget data count {df2.count()}")
    assert_dataframes(df1, df2)

