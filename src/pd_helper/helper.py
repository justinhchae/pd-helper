import pandas as pd
import multiprocessing as mp
from tqdm import tqdm
from functools import partial
import logging


from pd_helper.utils._mem_usage import _mem_usage
from pd_helper.utils._parse_cols import _parse_cols
from pd_helper.utils._reduce_precision import _reduce_precision
from pd_helper.utils._configuration import _configuration


def optimize(df
             , parse_col_names=True
             , enable_mp=False
             , mp_processors=None
             , date_strings=None
             , exclude_cols=None
             , special_mappings=None
             , bool_types=None
             , categorical_ratio=.1
             , categorical_threshold=20
             , final_default_dtype='string'
             , echo=False
             ):
    """
    Optimize a Pandas DataFrame by applying least precision to column dtypes.

    :params
    ----------
    df: DataFrame, Required
        a pandas dataframe that needs optimization
    parse_col_names: bool, default True
        If passed, returns columns as lower case without spaces
    enable_mp: bool, default to False
        If passed, runs optimization on columns in parallel with multiprocessing
    mp_processors: integer, default to None
        If None, default to half of available processes from mp.cpu_count(), only effective if mp is enabled.
    date_strings: list of string, default to None
        If None, default to a list of strings that indicate date columns -> ['_date', 'date_']
    exclude_cols: list of string, default to None
        If None, default to a list of strings that indicate columns to exclude from optimization -> ['exclude_this_col', 'exclude_another_col'].
        Note, excluded columns are returned, just not run through the optimizer.
    special_mappings: dictionary of {string: list of strings}, default to None
        Optional. If provided indicate a special mapping for col types with a dictionary, these are excluded from auto optimization.
        Note, the key is the desired dtype and the value is a list of column names.
    bool_types: list of string, default to None
        If None, default to a list of bool and semantic string values that indicate there is a boolean dtype such
        as True False, etc. -> [True, False, 'true', 'True', 'False', 'false']
    categorical_ratio: float, default to None
        If None, default to .1 (10%). Evaluates the ratio of unique values in the column to determine if categorical dtype is worthwhile.
        Note, if cat ratio less than 10%, then, the column is assigned categorical.
    categorical_threshold: integer, default to None
        If None, default to 20. Evaluates the len() of unique values in a column to determine if categorical dtype is worthwhile.
        Note, if the number of unique values is less than 20, categorical dtype is assigned.
    final_default_dtype: string, default to None
        If None, default to "string" dtype. This is the catch all dtype to assign if optimizer does not assign one by rule.
    echo: bool, default to False.
        If True, echo progress, show progress, and display metrics.

    *Note when calling function with multiprocessing enabled, ensure that the function is called from a module such as:

        if __name__ == "__main__":
            df = pd.DataFrame(<Some data here>)

            df = optimize(df)

    """
    _configuration(echo=echo)

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

    def f(s, c):
        """
        A Helper Function to assigning special mappings
        :param s: Pandas Series
        :param c: String
        :return: Pandas Series
        """
        logging.info(f'Applying special mappings for {c}')
        if c == 'category':
            s = pd.Categorical(s)
        elif c == 'datetime':
            s = pd.to_datetime(s, errors='coerce')
        else:
            s = s.astype(c)
        return s

    special_exclusions = []

    if special_mappings is not None:
        for k, v in special_mappings.items():
            for i in v:
                df[i] = f(df[i], k)
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
    else:
        CPUs = mp_processors
    # by default, enable multiprocessing to run optimizations in parallel
    if enable_mp:
        logging.info('Starting optimization process with multiprocessor.')
        # break out the dataframe into a list of series to be worked on in parallel
        lst_of_series = [df[d] for d in cols_to_convert]

        pool = mp.Pool(CPUs)

        if echo:
            # run with progress bar in terminal
            pbar = tqdm(lst_of_series, desc='Running DataFrame Optimization with multiprocessing')
        else:
            # use the same pbar object but iterate over a list with no progress bar
            pbar = lst_of_series

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
        logging.info('Optimization can be run in parallel with multiprocessing'
                     ', set enable_mp to True and see function params.')

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
    logging.info(f'Completed DataFrame Optimization. Ending with {end_mem} memory.')

    return df








