from unittest import TestCase
import pandas as pd
import numpy as np

class Test(TestCase):
    def test__mem_usage(self):
        from src.pd_helper.tests.test__config import BigDF
        df = BigDF(num_cols=1000, num_rows=10000, num_size=1000).a_dataframe()
        from src.pd_helper.utils._mem_usage import _mem_usage
        result = _mem_usage(df)
        print(result)
        result_split = result.split(" ")
        result_num = float(result_split[0])
        result_unit = result_split[1]

        assert isinstance(result, str)
        assert isinstance(result_num, float)
        assert result_num > 70.0
        assert result_unit == 'MB'
