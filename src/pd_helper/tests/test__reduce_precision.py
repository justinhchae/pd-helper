from unittest import TestCase

import pandas as pd

class Test(TestCase):

    def test__reduce_precision(self):
        from src.pd_helper.maker import MakeData
        from src.pd_helper.utils._reduce_precision import _reduce_precision
        faker = MakeData()
        df = faker.make_df()
        df_cols = list(df.columns)

        # function params passed by parent
        date_strings = ['_date', 'date_']
        bool_types = [True, False, 'true', 'True', 'False', 'false']
        categorical_ratio = .1
        categorical_threshold = 20
        final_default_dtype = 'string'
        enable_mp = False

        s = _reduce_precision(df["Object ID"]
                              , date_strings=date_strings
                              , bool_types=bool_types
                              , categorical_ratio=categorical_ratio
                              , categorical_threshold=categorical_threshold
                              , final_default_dtype=final_default_dtype
                              , enable_mp=enable_mp
                              )
        data_type = str(s.dtype)
        assert data_type == 'string'

        s = _reduce_precision(df['Item Name']
                              , date_strings=date_strings
                              , bool_types=bool_types
                              , categorical_ratio=categorical_ratio
                              , categorical_threshold=categorical_threshold
                              , final_default_dtype=final_default_dtype
                              , enable_mp=enable_mp
                              )
        data_type = str(s.dtype)
        assert data_type == 'category'

        s = _reduce_precision(df["Retrieved Date"]
                              , date_strings=date_strings
                              , bool_types=bool_types
                              , categorical_ratio=categorical_ratio
                              , categorical_threshold=categorical_threshold
                              , final_default_dtype=final_default_dtype
                              , enable_mp=enable_mp
                              )

        data_type = str(s.dtype)
        assert data_type == 'datetime64[ns]'

        s = _reduce_precision(df['Retrieved']
                              , date_strings=date_strings
                              , bool_types=bool_types
                              , categorical_ratio=categorical_ratio
                              , categorical_threshold=categorical_threshold
                              , final_default_dtype=final_default_dtype
                              , enable_mp=enable_mp
                              )
        data_type = str(s.dtype)
        assert data_type == 'boolean'

        s = _reduce_precision(df["Sector"]
                              , date_strings=date_strings
                              , bool_types=bool_types
                              , categorical_ratio=categorical_ratio
                              , categorical_threshold=categorical_threshold
                              , final_default_dtype=final_default_dtype
                              , enable_mp=enable_mp
                              )
        data_type = str(s.dtype)
        assert data_type == 'int8'

        s = _reduce_precision(df["Weight"]
                              , date_strings=date_strings
                              , bool_types=bool_types
                              , categorical_ratio=categorical_ratio
                              , categorical_threshold=categorical_threshold
                              , final_default_dtype=final_default_dtype
                              , enable_mp=enable_mp
                              )
        data_type = str(s.dtype)
        assert data_type == 'float16'






