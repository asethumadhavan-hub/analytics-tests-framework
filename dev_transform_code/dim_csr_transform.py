from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when, upper, split

def transform_dim_csr(df):
    df_transformed = (
        df.withColumn(
            'csr',
            when(col('paymentnote').like('CSR%'), upper(col('paymentnote'))).otherwise('-1')
        )
        .withColumn(
            'client_name',
            split(col('databasename'), '_')[0]
        )
        .drop('paymentnote', 'databasename')
        .distinct()
    )
    return df_transformed
