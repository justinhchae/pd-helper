import pandas as pd
import numpy as np
import multiprocessing as mp
from tqdm import tqdm
from functools import partial
import logging

from pd_helper.utils._parse_cols import _parse_cols
from pd_helper.utils._mem_usage import _mem_usage
from pd_helper.utils._reduce_precision import _reduce_precision


def optimize(df
             , parse_col_names=True
             , enable_mp=True
             , mp_processors=None
             , date_strings=None
             , exclude_cols=None
             , special_mappings=None
             , bool_types=None
             , categorical_ratio=.1
             , categorical_threshold=20
             , final_default_dtype='string'
             ):
    """
    :args: Consumes a dataframe, returns an optimized dataframe.
    :params df: a pandas dataframe that needs optimization
    :params parse_col_names: Default to True; returns columns as lower case without spaces
    :params enable_mp: Default to True; runs optimization on columns in parallel. Set to false to run in series.
    :params date_strings: If None, default to a list of strings that indicate date columns -> ['_date', 'date_']
    :params exclude_cols: Default to None. A list of strings that indicate columns to exclude
    :params special_mappings: Default to None.
            A dictionary where each key is the desired dtype and the value are a list of strings that indicate columns
            to make that dtype.
    :params bool_types: If None, default to a list of values that indicate there is a boolean dtype such
            as True False, etc. -> [True, False, 'true', 'True', 'False', 'false']
    :params categorical_ratio: If None, default to .1 (10%). Evaluates the ratio of unique values in the column
            , if less than 10%, then, categorical.
    :params categorical_threshold: If None, default to 20. If the number of unique values is less than 20
            , make it a categorical column.
    :params final_default_dtype: If None, default to "string" dtype.
    """
    start_mem = _mem_usage(df)
    logging.info(f'Starting DataFrame Optimization. Starting with {start_mem} memory.')
    if parse_col_names:
        logging.info('Converting Column Names to Lower Case and Removing Spaces')
        df = _parse_cols(df)
    cols_to_convert = []
    # a default of strings that indicate the column is some kind of datetime column
    if date_strings is None:
        date_strings = ['_date', 'date_']
    # make a list of strings from all available dataframe columns
    cols_to_convert = [i for i in df.columns]
    # accommodate any special user-defined mappings
    special_exclusions = []
    if special_mappings is not None:
        for k, v in special_mappings.items():
            for i in v:
                df[i] = df[i].astype(k)
                special_exclusions.append(i)

    # exclude columns if a list is provided
    if exclude_cols is not None:
        cols_to_convert = [i for i in cols_to_convert if i not in exclude_cols]
    # by default, if special mappings are provided, exclude them from auto optimization
    if special_exclusions:
        cols_to_convert = [i for i in cols_to_convert if i not in special_exclusions]
    # by default, a list of values to be explicitly treated as bools
    if bool_types is None:
        bool_types = [True, False, 'true', 'True', 'False', 'false']
        # TODO: account for only T or only F or 1/0 situations
    if mp_processors is None:
        CPUs = mp.cpu_count() // 2
    # by default, enable multiprocessing to run optimizations in parallel
    if enable_mp:
        logging.info('Starting optimization process with multiprocessor.')
        # break out the dataframe into a list of series to be worked on in parallel
        lst_of_series = [df[d] for d in cols_to_convert]

        pool = mp.Pool(CPUs)
        pbar = tqdm(lst_of_series, desc='Running DataFrame Optimization with multiprocessing')
        _reduce_precision_ = partial(_reduce_precision
                                     , date_strings=date_strings
                                     , bool_types=bool_types
                                     , categorical_ratio=categorical_ratio
                                     , categorical_threshold=categorical_threshold
                                     , final_default_dtype=final_default_dtype
                                     , enable_mp=enable_mp
                                     )
        list_of_converted = list(pool.imap(_reduce_precision_, pbar))
        pool.close()
        pool.join()

        # update the dataframe based on the converted records
        for (col_name, col_series) in list_of_converted:
            df[col_name] = col_series
    else:
        logging.info('Starting optimization process in series.')
        # un comment below to do conversion without MP
        df[cols_to_convert] = df[cols_to_convert].apply(lambda x: _reduce_precision(x
                                                                                    , date_strings=date_strings
                                                                                    , bool_types=bool_types
                                                                                    , categorical_ratio=categorical_ratio
                                                                                    , categorical_threshold=categorical_threshold
                                                                                    , final_default_dtype=final_default_dtype
                                                                                    , enable_mp=enable_mp
                                                                                    ))

    logging.info(f'Converted DF with new dtypes as follows:\n{df.dtypes}')
    end_mem = _mem_usage(df)
    mem_delta = start_mem - end_mem
    pct_saving = (mem_delta / start_mem) * 100
    logging.info(f'Completed DataFrame Optimization. Ending with {end_mem} memory, saving {pct_saving}%.')

    return df








