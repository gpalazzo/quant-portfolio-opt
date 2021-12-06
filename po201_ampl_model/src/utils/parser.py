import pandas as pd


def ampl_list_to_pandas_df(ampl_list, n_stocks: int = 21, cols_as_index: bool = False):
    _stocks = []
    _values = []
    df = pd.DataFrame()

    for i, elem in enumerate(ampl_list, 1):

        if i % n_stocks == 0:
            _stocks.append(elem[1])
            _values.append(elem[2])
            _aux_dict = {"stocks": _stocks, "values": _values}
            _tmp_df = pd.DataFrame.from_dict(_aux_dict)
            _cols = _tmp_df.T.values[0].tolist()
            _tmp_df = _tmp_df.T.reset_index(drop=True).drop([0])
            _tmp_df.columns = _cols

            df = df.append(_tmp_df, ignore_index=True)

            _stocks = []
            _values = []

        else:
            _stocks.append(elem[1])
            _values.append(elem[2])

    if cols_as_index:
        df.index = df.columns.tolist()

    df = df.apply(pd.to_numeric)

    return df


def pandas_df_to_indexed_ampl_format(df: pd.DataFrame) -> pd.DataFrame:

    data_values = {}

    for i, row in df.iterrows():
        for k in range(0, len(row)):
            _key = (i, row.index[k])
            data_values[_key] = row[k + 1]

    return pd.DataFrame.from_dict(data_values, orient="index", columns=["value"])
