import numpy as np
import pandas as pd


def _reduce_precision(x
                      , date_strings
                      , bool_types
                      , categorical_ratio
                      , categorical_threshold
                      , final_default_dtype
                      , enable_mp
                      ):
    """
    :params x: a pandas series (a column) to convert for dtype precision reduction
    """
    col_name = x.name
    col_type = x.dtype
    # return a unique list of non-na values in the current series
    unique_data = list(x.dropna().unique())

    n_unique = float(len(unique_data))
    n_records = float(len(x))
    cat_ratio = n_unique / n_records

    if 'int' in str(col_type):
        # if integer, make it the smallest possible type of integer
        c_min = x.min()
        c_max = x.max()

        if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
            x = x.astype(np.int8)
        elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
            x = x.astype(np.int16)
        elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
            x = x.astype(np.int32)
        elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
            x = x.astype(np.int64)
            # TODO: set precision to unsigned integers with nullable NA

    elif 'float' in str(col_type):
        # if float, make it the smallest possible type of float
        c_min = x.min()
        c_max = x.max()
        if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                x = x.astype(np.float16)
        elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
            x = x.astype(np.float32)
        else:
            x = x.astype(np.float64)

    elif 'datetime' in col_type.name or any(i in str(x.name).lower() for i in date_strings):
        # if datetime, make it datetime or if the col name matches default date strings
        try:
            x = pd.to_datetime(x, errors='coerce')
        except:
            # TODO: conform to PEP and avoid naked except statement
            pass

    elif any(i in bool_types for i in unique_data):
        unique_vals = x.unique().tolist()

        blank_char = ''
        blank_space = ' '

        if blank_char in unique_vals:
            x = x.replace({blank_char: pd.NA})
        if blank_space in unique_vals:
            x = x.replace({blank_space: pd.NA})

        x = x.astype('boolean')

    elif cat_ratio < categorical_ratio or n_unique < categorical_threshold:
        # if the category ratio is smaller than default thresholds, then make the column a categorical
        # a high level attempt to strike a balance when making columns categorical or not
        try:
            # return normal categories, i.e. avoid "dog" and "Dog" as different categories
            x = x.str.title()
        except:
            # TODO: conform to PEP and avoid naked except statement
            pass

        x = pd.Categorical(x)

    elif all(isinstance(i, str) for i in unique_data):
        # if all else fails, provide a final dtype as default
        x = x.astype(final_default_dtype)

    if enable_mp:
        return col_name, x
    else:
        return x