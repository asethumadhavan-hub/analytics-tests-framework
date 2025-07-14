#  In-memory cache so tables are read only once per file
_table_cache = {}

def get_table_df(spark, table_name, filter_expr=None):
    cache_key = (table_name, filter_expr)

    if cache_key not in _table_cache:
        #print(f"[LOAD] Reading table: {table_name}")
        df = spark.read.table(table_name)

        if filter_expr:
            #print(f"[FILTER] Applying filter on {table_name}: {filter_expr}")
            df = df.filter(filter_expr)
        _table_cache[cache_key] = df

    else:
        print(f"[CACHE] Using cached table: {table_name}")
    return _table_cache[cache_key]



