from pyspark.sql.functions import col
from utils.get_table_df import get_table_df


#  NOT NULL TEST

def test_not_null(spark, table_name, column):
    df = get_table_df(spark, table_name)
    null_count = df.filter(f"{column} IS NULL").count()
    assert null_count == 0, f" Nulls found in {table_name}.{column}"

#  DUPLICATE TEST

def test_duplicate(spark, table_name, column):
    df = get_table_df(spark, table_name)
    keys = column if isinstance(column, list) else [column]

    dup_count = (
        df.groupBy(*keys)
          .count()
          .filter("count > 1")
          .count()
    )

    assert dup_count == 0, f" Duplicates found in {table_name} on columns {keys}"

# COLUMN PRESENCE

def test_column_presence(spark, table, columns):
    df = spark.read.table(table)
    actual_columns = set(df.columns)
    expected = set(columns.keys())

    missing = expected - actual_columns
    unexpected = actual_columns - expected
    assert not missing, f"Missing columns in {table}: {missing}"
    assert not unexpected, f"Unexpected columns in {table}: {unexpected}"

# DATA TYPE CHECK

def test_data_type(spark, table, columns):
    df = spark.read.table(table)
    df_schema = {field.name: field.dataType.simpleString() for field in df.schema.fields}
    for col, expected_type in columns.items():
        actual_type = df_schema.get(col)
        assert actual_type == expected_type

# ROW COUNT CHECK

def test_row_count(spark, source_table, target_table, client):
    source_df = get_table_df(spark, source_table)
    target_df = get_table_df(spark, target_table)
    if client:
        source_df = source_df.filter(col("databasename").like(f"{client}%"))
        target_df = target_df.filter(col("client_name")  == client)

    source_count = source_df.count()
    target_count = target_df.count()
    assert source_count == target_count, f"Row count mismatch for client {client}: source={source_count}, target={target_count}"


