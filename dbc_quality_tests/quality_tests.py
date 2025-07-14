from utils.get_table_df import get_table_df

#  NOT NULL TEST

def test_not_null(spark, table_name, column, filter_expr):
    df = get_table_df(spark, table_name, filter_expr)
    null_rows = df.filter(f"{column} IS NULL")
    null_count = null_rows.count()
    if null_count > 0:
        print(f"\nNulls found in {table_name}.{column}. Sample rows:")
        null_rows.select(*df.columns).limit(50).show(truncate=False)

    assert null_count == 0, f" Nulls found in {table_name}.{column}"

#  DUPLICATE TEST

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




