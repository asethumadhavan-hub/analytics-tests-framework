#  In-memory cache so tables are read only once per file
_table_cache = {}

def get_table_df(spark, table_name):
    if table_name not in _table_cache:
        print(f"[LOAD] Reading table: {table_name}")
        _table_cache[table_name] = spark.read.table(table_name)
    else:
        print(f"[CACHE] Using cached table: {table_name}")
    return _table_cache[table_name]


