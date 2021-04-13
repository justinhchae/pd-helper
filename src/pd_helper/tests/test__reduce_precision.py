from unittest import TestCase

import pandas as pd

class Test(TestCase):
    from src.pd_helper.maker import MakeData
    from src.pd_helper.utils._reduce_precision import _reduce_precision
    faker = MakeData()
    df = faker.make_df()

    # function params passed by parent
    date_strings = ['_date', 'date_']
    bool_types = [True, False, 'true', 'True', 'False', 'false']
    categorical_ratio = .1
    categorical_threshold = 20
    final_default_dtype = 'string'
    enable_mp = False

    def test__reduce_precision_string(self):

        s = Test._reduce_precision(Test.df["Object ID"]
                              , date_strings=Test.date_strings
                              , bool_types=Test.bool_types
                              , categorical_ratio=Test.categorical_ratio
                              , categorical_threshold=Test.categorical_threshold
                              , final_default_dtype=Test.final_default_dtype
                              , enable_mp=Test.enable_mp
                              )
        data_type = str(s.dtype)
        self.assertEqual(data_type, 'string')

    def test__reduce_precision_category(self):
        s = Test._reduce_precision(Test.df['Item Name']
                              , date_strings=Test.date_strings
                              , bool_types=Test.bool_types
                              , categorical_ratio=Test.categorical_ratio
                              , categorical_threshold=Test.categorical_threshold
                              , final_default_dtype=Test.final_default_dtype
                              , enable_mp=Test.enable_mp
                              )
        data_type = str(s.dtype)
        self.assertEqual(data_type, 'category')

    def test__reduce_precision_datetime(self):
        s = Test._reduce_precision(Test.df["Retrieved Date"]
                              , date_strings=Test.date_strings
                              , bool_types=Test.bool_types
                              , categorical_ratio=Test.categorical_ratio
                              , categorical_threshold=Test.categorical_threshold
                              , final_default_dtype=Test.final_default_dtype
                              , enable_mp=Test.enable_mp
                              )

        data_type = str(s.dtype)
        self.assertEqual(data_type, 'datetime64[ns]')

    def test__reduce_precision_boolean(self):
        s = Test._reduce_precision(Test.df['Retrieved']
                              , date_strings=Test.date_strings
                              , bool_types=Test.bool_types
                              , categorical_ratio=Test.categorical_ratio
                              , categorical_threshold=Test.categorical_threshold
                              , final_default_dtype=Test.final_default_dtype
                              , enable_mp=Test.enable_mp
                              )
        data_type = str(s.dtype)
        self.assertEqual(data_type, 'boolean')

    def test__reduce_precision_int8(self):
        s = Test._reduce_precision(Test.df["Sector"]
                              , date_strings=Test.date_strings
                              , bool_types=Test.bool_types
                              , categorical_ratio=Test.categorical_ratio
                              , categorical_threshold=Test.categorical_threshold
                              , final_default_dtype=Test.final_default_dtype
                              , enable_mp=Test.enable_mp
                              )
        data_type = str(s.dtype)
        self.assertEqual(data_type, 'int8')

    def test__reduce_precision_float16(self):
        s = Test._reduce_precision(Test.df["Weight"]
                              , date_strings=Test.date_strings
                              , bool_types=Test.bool_types
                              , categorical_ratio=Test.categorical_ratio
                              , categorical_threshold=Test.categorical_threshold
                              , final_default_dtype=Test.final_default_dtype
                              , enable_mp=Test.enable_mp
                              )
        data_type = str(s.dtype)
        self.assertEqual(data_type, 'float16')






