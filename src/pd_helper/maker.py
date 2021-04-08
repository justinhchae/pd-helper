import pandas as pd
import numpy as np
import numpy.lib.recfunctions as rfn

import os
import uuid
import shortuuid
import random


class MakeData:
    """
    MakeData is a class of functions that returns a perfectly imperfect dataframe of various dtypes for testing.
    """
    def __init__(self):
        self.hourly = np.timedelta64(1, 'h')
        self.daily = np.timedelta64(1, 'D')
        self.today = pd.Timestamp.now()

    def make_random_dates(self, start, end, n):
        """

        :param start: A string date like '2010-01-01', should be less than end date
        :param end: A string date like '2020-01-01', should be greater than start date
        :param n: number of records to return
        :return: a series of random datetime stamps in a given range

        works cited: https://stackoverflow.com/questions/50559078/generating-random-dates-within-a-given-range-in-pandas
        """
        start = pd.to_datetime(start)
        end = pd.to_datetime(end)
        start_u = start.value // 10 ** 9
        end_u = end.value // 10 ** 9
        return pd.DatetimeIndex((10 ** 9 * np.random.randint(start_u, end_u, n, dtype=np.int64)).view('M8[ns]'))

    def make_df(self, make_default=True, perfect=False, size=100000, col_names=None, values=None):
        """
        :param make_default: make a Pandas Dataframe of imperfect data types
        :param perfect: no purposeful mistakes in data
        :param size: number of rows in dataframe
        :param col_names: optional col names, or default
        :param values: optional col values, or default
        :return: a dataframe of randomly generated data
        """
        df_out = pd.DataFrame()

        if make_default:

            columns = ['Object ID', 'Item Name', 'Retrieved Date', 'Retrieved', 'Condition', 'Sector', 'Status',
                       'Status Date', 'Weight']
            n_cols = len(columns)
            n_sectors = 8
            sectors = [x for x in range(n_sectors)]

            if perfect:
                conditions = ['Excellent', 'Poor', 'Good', 'Spare Parts', 'Trash']
                items = ['Lighter', 'Toaster', 'YoYo']
            else:
                conditions = ['Excellent', 'excellent', 'excelent', 'Poor', 'poor', 'Good', 'good', 'Spare Parts',
                              'Trash', 'trsh']
                items = ['lighter', 'Lighter', 'toster', 'Toaster', 'YoYo', 'yo-yo']

            statuses = ['Inventoried', 'Inventoried', 'Repaired', 'Repaired', 'Pending Repair', 'Pending Repair',
                        'Pending Repair', 'Pending Repair', 'Pending Inventory', 'Pending Inventory',
                        'Pending Inventory', 'Missing']

            def filler():
                arr = np.zeros((size, n_cols))

                dtype = str(arr.dtype)
                dtypes = np.dtype([(n, dtype) for n in columns])

                structured = rfn.unstructured_to_structured(arr, dtypes)
                df = pd.DataFrame.from_records(data=structured)

                df['Object ID'] = df.apply(lambda x: shortuuid.uuid(), axis=1)

                df['Retrieved Date'] = self.make_random_dates('2010-01-01', '2020-12-31', size)

                # https://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python
                df['Retrieved'] = df.apply(lambda x: bool(random.getrandbits(1)), axis=1)

                df['Sector'] = df.apply(lambda x: np.random.choice(sectors, 1, replace=True)[0], axis=1)

                df['Condition'] = df.apply(lambda x: np.random.choice(conditions, 1, replace=True)[0], axis=1)

                df['Status'] = df.apply(lambda x: np.random.choice(statuses, 1, replace=True)[0], axis=1)

                df['Status Date'] = self.make_random_dates('2020-01-01', '2020-12-31', size)

                df['Item Name'] = df.apply(lambda x: np.random.choice(items, 1, replace=True)[0], axis=1)

                def lighters():
                    return np.random.uniform(low=1, high=11)

                def toasters():
                    return np.random.uniform(low=20, high=48)

                def yoyos():
                    return np.random.uniform(low=5, high=16)

                cond1 = ['lighter', 'Lighter']
                cond2 = ['Toaster', 'toster']
                cond3 = ['YoYo', 'yo-yo']

                df['Weight'] = df.apply(lambda x: lighters(), axis=1)

                df['Weight'] = np.where(df['Item Name'].isin(cond1), df.apply(lambda x: lighters(), axis=1),
                                        np.where(df['Item Name'].isin(cond2), df.apply(lambda x: toasters(), axis=1),
                                                 np.where(df['Item Name'].isin(cond3),
                                                          df.apply(lambda x: yoyos(), axis=1), 0.0)))

                best = ['Excellent', 'excellent', 'excelent', 'Good', 'good']
                mid = ['Good', 'good', 'Spare Parts']
                worst = ['Poor', 'poor', 'Trash', 'trsh']

                def rand_bool(percent=50):
                    # https://stackoverflow.com/questions/14324472/random-boolean-by-percentage
                    return random.randrange(100) < percent

                df['Retrieved'] = np.where(df['Condition'].isin(best),
                                           df.apply(lambda x: rand_bool(percent=70), axis=1),
                                           np.where(df['Condition'].isin(mid),
                                                    df.apply(lambda x: rand_bool(percent=40), axis=1),
                                                    np.where(df['Condition'].isin(worst),
                                                             df.apply(lambda x: rand_bool(percent=10), axis=1), False)))

                df['Status'] = np.where((df['Retrieved'] == False & df['Condition'].isin(worst)),
                                        'Compacted Trash Pile', df['Status'])
                df['Status'] = np.where((df['Retrieved'] == False & df['Condition'].isin(mid)),
                                        'Left in Sector', df['Status'])
                df['Status'] = np.where((df['Retrieved'] == False & df['Condition'].isin(best)),
                                        'Left in Sector', df['Status'])

                df = df.sort_values(by='Retrieved Date').reset_index(drop=True)

                def shuffle(yr):
                    full = (list(str(yr)))
                    inner = full[1:3]
                    inner.reverse()
                    full[1:3] = inner
                    yr = int(''.join(full))
                    return yr

                if not perfect:
                    n_samples = int(size * .002)

                    if n_samples < 1:
                        n_samples = 1

                    s1 = df.sample(n=n_samples, replace=False, random_state=0)
                    s1['Retrieved Date'] = s1['Retrieved Date'].astype('object')
                    s1['Retrieved Date'] = s1['Retrieved Date'].apply(lambda x: x.replace(year=shuffle(x.year), day=np.random.randint(1, 25)))
                    df['Retrieved Date'].update(s1['Retrieved Date'])

                    s2 = df.sample(n=n_samples, replace=False, random_state=21)
                    s2['Retrieved Date'] = s2['Retrieved Date'].apply(lambda x: '')
                    df['Retrieved Date'].update(s2['Retrieved Date'])

                    df['Retrieved Date'] = pd.to_datetime(df['Retrieved Date'])

                    s3 = df.sample(n=n_samples, replace=False, random_state=42)
                    s3['Retrieved'] = s3['Retrieved'].apply(lambda x: '')
                    df['Retrieved'].update(s3['Retrieved'])

                    n_samples = int(size * .1)

                    if n_samples < 1:
                        n_samples = 1

                    s4 = df.sample(n=n_samples, replace=False, random_state=42)
                    s4['Item Name'] = s4['Item Name'].apply(lambda x: '')
                    df['Item Name'].update(s4['Item Name'])

                return df

            df_out = filler()

        return df_out
