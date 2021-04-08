import pandas as pd
import numpy as np


class BigDF:
    def __init__(self, num_cols, num_size, num_rows):
        self.num_rows = num_rows
        self.lst_of_cols = [f'Col {i}' for i in range(num_cols)]
        self.lst_of_nums = list(np.random.randint(num_rows, size=num_size)) * num_cols

        self.data = {k: v for (k, v) in zip(self.lst_of_cols, self.lst_of_nums)}

    def a_dataframe(self):
        df = pd.DataFrame(self.data, index=list(range(self.num_rows)))
        return df