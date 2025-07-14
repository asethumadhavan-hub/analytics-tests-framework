from dbc_quality_tests.data_quality_utils import compare_tables_sql
from dbc_quality_tests.data_quality_utils.df_compare_row_hash import compare_dataframes_by_row_hash
from utils.get_table_df import get_table_df

# ROW COUNT CHECK

def test_row_count(spark, source_table, target_table, filter_expr):
    source_df = get_table_df(spark, source_table, filter_expr)
    target_df = get_table_df(spark, target_table, filter_expr)

    source_count = source_df.count()
    target_count = target_df.count()
    print(f"Count of {source_table}: {source_count}")
    print(f"Count of {target_table}: {target_count}")
    assert source_count == target_count, f"Row count mismatch: {source_table}={source_count}, {target_table}={target_count}"

def test_data_comparison(spark, source_table, target_table, filter_expr, exclude_col="insert_timestamp"):

    c1, c2 = compare_tables_sql(spark, source_table, target_table, exclude_col, filter_expr)
    match = (c1 == 0 and c2 == 0)
    assert match, f"Mismatch: {source_table}->{target_table}: c1={c1}, c2={c2}"
    #compare_dataframes_by_row_hash(spark, source_table, target_table, filter_expr, exclude_col)








