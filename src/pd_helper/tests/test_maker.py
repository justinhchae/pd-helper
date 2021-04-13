from unittest import TestCase


class TestMakeData(TestCase):
    from src.pd_helper.maker import MakeData
    fake_df = MakeData().make_df

    def test_make_df_size(self):
        size = 5
        df = TestMakeData.fake_df(size=size)
        self.assertEqual(len(df), size)

    def test_make_df_dates(self):
        start_year = "2021"
        datetime_start = f"{start_year}-01-01"
        end_month = "02"
        datetime_end = f"2021-{end_month}-15"
        perfect = True
        size = 1000
        df = TestMakeData.fake_df(perfect=perfect, datetime_start=datetime_start, datetime_end=datetime_end, size=size)

        min_date = str(df["Retrieved Date"].min().year)
        self.assertEqual(start_year, min_date)
        max_date = df["Retrieved Date"].max().month
        self.assertEqual(int(end_month), max_date)
