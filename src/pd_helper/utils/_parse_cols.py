def _parse_cols(df):
    """
    :param df: A Pandas DataFrane
    :return: A DataFrame with lowercase columne names and spaces as underscore seperators
    """
    # logging.info('Parsing column headers to lower case and replacing spaces with underscore.')
    df.columns = map(str.lower, df.columns)
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace('-', '_')
    return df