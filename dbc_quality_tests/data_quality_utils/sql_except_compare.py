
def compare_tables_sql(spark, table1, table2, excluded_col="insert_timestamp", filter_expr=None):
    where_clause = f"WHERE {filter_expr}" if filter_expr else ""

    query1 = f"""
    SELECT * EXCEPT({excluded_col})
    FROM {table1}
    {where_clause}
    EXCEPT
    SELECT * EXCEPT({excluded_col})
    FROM {table2}
    {where_clause}
    """

    query2 = f"""
    SELECT * EXCEPT({excluded_col})
    FROM {table2}
    {where_clause}
    EXCEPT
    SELECT * EXCEPT({excluded_col})
    FROM {table1}
    {where_clause}
    """

    df1 = spark.sql(query1)
    df2 = spark.sql(query2)

    c1 = df1.count()
    c2 = df2.count()

    if c1 > 0:
        print(f"\nRows in {table1} but not in {table2} ({c1})")
        df1.show(truncate=False)

    if c2 > 0:
        print(f"Rows in {table2} but not in {table1} ({c2})")
        df2.show(truncate=False)

    if c1 == 0 and c2 == 0:
        print(f"\n {table1} and {table2} match (excluding {excluded_col})")

    return c1, c2
