from pyspark.sql.functions import sha2, concat_ws, col
from utils.get_table_df import get_table_df


def compare_dataframes_by_row_hash(spark, prod_table, preprod_table, filter_expr=None, exclude_cols=None):

    df1 = get_table_df(spark, prod_table, filter_expr)
    df2 = get_table_df(spark, preprod_table, filter_expr)
    df1 = df1.select([col(c) for c in df1.columns if c not in exclude_cols])
    df2 = df2.select([col(c) for c in df2.columns if c not in exclude_cols])

    df1_hashed = df1.withColumn("row_hash", sha2(concat_ws("||", *df1.columns), 256))
    df2_hashed = df2.withColumn("row_hash", sha2(concat_ws("||", *df2.columns), 256))

    diff1 = df1_hashed.select("row_hash").subtract(df2_hashed.select("row_hash"))
    diff2 = df2_hashed.select("row_hash").subtract(df1_hashed.select("row_hash"))

    count_diff1 = diff1.count()
    count_diff2 = diff2.count()

    if count_diff1 == 0 and count_diff2 == 0:
        print("DataFrames match exactly based on row hash")
        return True

    if count_diff1 > 0:
        print(f"Rows present in {prod_table} but missing in {preprod_table}  ({count_diff1}):")
        #df1_hashed.join(diff1, on="row_hash").show(truncate=False)

    if count_diff2 > 0:
        print(f"Rows present in {preprod_table} but missing in {prod_table} ({count_diff2}):")
        # df2_hashed.join(diff2, on="row_hash").show(truncate=False)
        return None
    return None


