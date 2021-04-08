from unittest import TestCase


class Test(TestCase):
    def test__parse_cols(self):
        from src.pd_helper.tests.test__config import BigDF
        df = BigDF(num_cols=1000, num_rows=10000, num_size=1000).a_dataframe()
        from src.pd_helper.utils._parse_cols import _parse_cols
        df = _parse_cols(df)
        cols = list(df.columns)
        has_space = False

        if any(' ' in i for i in cols):
            has_space = True

        self.assertFalse(has_space)
