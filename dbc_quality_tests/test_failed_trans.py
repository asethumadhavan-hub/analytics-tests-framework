import pytest
from dbc_quality_tests.data_quality_utils import compare_tables_sql
from dbc_quality_tests.data_quality_utils.df_compare_row_hash import compare_dataframes_by_row_hash
from utils.get_table_df import get_table_df


def test_data_comparison_row_hash(spark):
    df_src = spark.read.table("bizhq_preprod.gold.payment_daily_deposit_fees_summary")
    df_tgt = spark.read.table("bizhq.gold.payment_daily_deposit_fees_summary")

    cols_to_compare = ["client_id", "realm", "report_date_from", "TD", "FTI", "category", "net_deposit"]
    joined_df = compare_dataframes_by_row_hash(df_src, df_tgt, cols_to_compare)

    mismatches = joined_df.filter("src.client_id != tgt.client_id OR src.realm != tgt.realm OR src.report_date_from != tgt.report_date_from OR src.TD != tgt.TD OR src.FTI != tgt.FTI OR src.category != tgt.category OR src.net_deposit != tgt.net_deposit")
    assert mismatches.count() == 0, "Found mismatches in data!"



'''
@pytest.mark.order(1)
def test_duplicate(spark, table_name, column, filter_expr):
    df = get_table_df(spark, table_name, filter_expr)
    keys = column if isinstance(column, list) else [column]

    dup_count = (
        df.groupBy(*keys)
          .count()
          .filter("count > 1")
          .count()
    )

    assert dup_count == 0, f" Duplicates found in {table_name} on columns {keys}"

@pytest.mark.order(2)
@pytest.mark.parametrize(
    "table_name", ["payment_aggregated","payment_batch_orchestrator_post_validation", "payment_batch_orchestrator_post_validation_status", "payment_daily_deposit_fees_summary",
                   "payment_daily_deposit_financial_summary", "payment_daily_deposit_transfer_summary", "payment_daily_financial_activity", "payment_returns",
                   "payment_summarized_daily_financial_activity", "payment_summary"])

def test_row_count_failed_aggregated(spark, table_name):

    pre_df = spark.read.table(f"bizhq_preprod.gold.{table_name}").drop("insert_timestamp")
    prod_df = spark.read.table(f"bizhq.gold.{table_name}").drop("insert_timestamp")

    if "transaction_date" in pre_df.columns and "transaction_date" in prod_df.columns:
        pre_filtered = pre_df.filter("DATE(transaction_date) < current_date() - 2")
        prod_filtered = prod_df.filter("DATE(transaction_date) < current_date() - 2")
        pre_count = pre_filtered.count()
        prod_count = prod_filtered.count()

        print(f"\n Table: {table_name}")
        print(f"Pre-prod row count (t-2): {pre_count}")
        print(f"Prod row count (t-2):    {prod_count}")
        diff = pre_count - prod_count
        print(f"Difference: {diff}")

    else:
        pre_count = pre_df.count()
        prod_count = prod_df.count()

        print(f"\n{table_name} (No transaction_date column — full row count)")
        print(f" Pre-Prod Row Count: {pre_count}")
        print(f" Prod     Row Count: {prod_count}")
        diff = pre_count - prod_count
        print(f"Difference: {diff}")
    assert diff == 0, f"Row count mismatch for client {table_name}: pre_prod={pre_count}, prod={prod_count}"


@pytest.mark.parametrize(
    "table_name", ["payment_aggregated", "payment_summary"])
def test_table1_match(spark, table_name):
    prod_table = f"bizhq.gold.{table_name}"
    pre_prod_table = f"bizhq_preprod.gold.{table_name}"
    cols_prod = [c.lower() for c in spark.table(prod_table).columns]
    cols_preprod = [c.lower() for c in spark.table(pre_prod_table).columns]

    if 'transaction_date' in cols_prod and 'transaction_date' in cols_preprod:
        filter_expr = "transaction_date < date_sub(current_date(), 2)"
    else:
        filter_expr = None  # no filter if column missing in either table

    df_prod_only, df_preprod_only = compare_tables_sql(
        spark,
        prod_table,
        pre_prod_table,
        excluded_col="insert_timestamp",
        filter_expr=filter_expr
    )

    assert df_prod_only.count() == 0 and df_preprod_only.count() == 0, (
        f"\nRows in PROD not in PREPROD:\n{df_prod_only.limit(5).toPandas().to_string(index=False)}"
        f"\n\nRows in PREPROD not in PROD:\n{df_preprod_only.limit(5).toPandas().to_string(index=False)}"
    )


'''
