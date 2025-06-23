import pandas as pd
from datetime import datetime
from dev_transform_code.dim_calendar import generate_calendar_df
import pandas.testing as pdt
import pytest


@pytest.mark.parametrize("start_date, end_date, expected_file", [("2020-01-01", "2020-01-10", "expected_calendar_jan.xlsx"),
                                                                  ("2020-02-25", "2020-02-29", "expected_calendar_feb.xlsx"),
                                                                  ("2020-12-25", "2021-01-02", "expected_calendar_yearend.xlsx")
                                                                  ])

def test_generate_calendar_df(start_date, end_date, expected_file, load_source_and_expected):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    actual = generate_calendar_df(start, end).toPandas()
    _, expected = load_source_and_expected(None, expected_file, None)
    actual["date"] = actual["date"].dt.normalize()
    expected["date"] = expected["date"].dt.normalize()

    datetime_columns = ["date", "first_day_of_month", "last_day_of_month"]
    for col in datetime_columns:
        actual[col] = pd.to_datetime(actual[col]).dt.tz_localize(None).dt.normalize()
        expected[col] = pd.to_datetime(expected[col]).dt.tz_localize(None).dt.normalize()

    int_columns = [
        "date_key", "year", "month", "day", "week", "day_of_week", "quarter"
    ]

    for col in int_columns:
        actual[col] = actual[col].astype("int64")
        expected[col] = expected[col].astype("int64")

    pdt.assert_frame_equal(actual.reset_index(drop=True), expected.reset_index(drop=True))
