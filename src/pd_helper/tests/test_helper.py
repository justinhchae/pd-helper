from unittest import TestCase


class Test(TestCase):

    from src.pd_helper.maker import MakeData
    fake_df = MakeData().make_df

    def test_optimize(self):
        df = Test.fake_df(size=1000)
        # df = Test.optimize(df, enable_mp=False)
