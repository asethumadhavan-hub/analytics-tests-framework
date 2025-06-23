from databricks.connect import DatabricksSession
import pytest

#  Spark Session Fixture — runs once per test session
@pytest.fixture(scope="session")
def spark():
    print("\n STARTING SPARK SESSION")
    spark = DatabricksSession.builder.serverless(True).profile("dbc-2f8c933b-7d38").getOrCreate()
    yield spark
    print("\n STOPPING SPARK SESSION")
    spark.stop()