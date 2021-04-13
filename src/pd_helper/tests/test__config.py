import pandas as pd
import numpy as np
from functools import partial


class BigDF:
    def __init__(self, num_cols, num_size, num_rows):
        self.num_rows = num_rows
        self.lst_of_cols = [f'Col {i}' for i in range(num_cols)]

        lst_of_floats = [np.random.uniform(0, 100) for i in range(num_cols//2)]
        lst_of_ints = list(np.random.randint(num_rows, size=num_size)) * (num_cols//2)

        self.lst_of_nums = lst_of_ints + lst_of_floats

        self.data = {k: v for (k, v) in zip(self.lst_of_cols, self.lst_of_nums)}

    def a_dataframe(self):
        df = pd.DataFrame(self.data, index=list(range(self.num_rows)))
        return df


class FakeDF:
    def __init__(self):
        from src.pd_helper.maker import MakeData
        from src.pd_helper.utils._reduce_precision import _reduce_precision
        faker = MakeData()
        self.df = faker.make_df()

        # function params currently passed by parent by default
        date_strings = ['_date', 'date_']
        bool_types = [True, False, 'true', 'True', 'False', 'false']
        categorical_ratio = .1
        categorical_threshold = 20
        final_default_dtype = 'string'
        enable_mp = False

        self._reduce_precision_ = partial(_reduce_precision
                                          , date_strings=date_strings
                                          , bool_types=bool_types
                                          , categorical_ratio=categorical_ratio
                                          , categorical_threshold=categorical_threshold
                                          , final_default_dtype=final_default_dtype
                                          , enable_mp=enable_mp
                                          )
