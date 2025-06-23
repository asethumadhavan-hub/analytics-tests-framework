from databricks.connect import DatabricksSession
from pyspark.sql.functions import *

spark = DatabricksSession.builder.serverless(True).profile("dbc-2f8c933b-7d38").getOrCreate()