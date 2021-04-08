def _mem_usage(df):
    """ iterate through all the columns of a dataframe and modify the data type
        to reduce memory usage.
        source: https://gist.github.com/enamoria/fa9baa906f23d1636c002e7186516a7b
    """
    mem = df.memory_usage().sum() / 1024 ** 2

    return '{:.2f} MB'.format(mem)
