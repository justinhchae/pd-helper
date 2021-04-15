def _parse_cols(df):
    """A helper function to standardize column names.

    :param df: A Pandas DataFrame.
    :return: A DataFrame with lowercase column names and spaces as underscore separators.
    """
    # logging.info('Parsing column headers to lower case and replacing spaces with underscore.')
    df.columns = map(str.lower, df.columns)
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace('-', '_')
    return df
