
def _parse_cols(df):
    # logging.info('Parsing column headers to lower case and replacing spaces with underscore.')
    df.columns = map(str.lower, df.columns)
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace('-', '_')
    return df