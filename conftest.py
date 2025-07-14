from databricks.connect import DatabricksSession
import pytest

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev", help="Environment to test (dev or preprod)")

@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


#  Spark Session Fixture — runs once per test session
@pytest.fixture(scope="session")
def spark(env):
    profile = "dbc-2f8c933b-7d38" if env == "dev" else "dbc-c2d92968-31c6"
    print("\n STARTING SPARK SESSION")

    spark = DatabricksSession.builder.serverless(True).profile(profile).getOrCreate()

    yield spark

    print("\n STOPPING SPARK SESSION")
    spark.stop()