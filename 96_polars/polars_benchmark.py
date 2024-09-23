import marimo

__generated_with = "0.8.18"
app = marimo.App()


@app.cell
def __():
    import polars as pl
    import pandas as pd
    from time import time
    return pd, pl, time


@app.cell
def __(time):
    def timeit(fn):
        tic = time()
        ret = fn()
        toc = time()

        return toc-tic, ret
    return (timeit,)


@app.cell
def __(pd, timeit):
    #_tic = time()
    #data = pd.read_csv("all_spots.tsv.xz", sep='\t')
    #_toc = time()

    pandas_import, data = timeit(lambda: pd.read_csv("all_spots_shuffle.tsv", sep='\t'))
    return data, pandas_import


@app.cell
def __(data):
    data
    return


@app.cell
def __(data, timeit):
    pandas_mean, _ = timeit(lambda: data.mean(numeric_only=True))
    return (pandas_mean,)


@app.cell
def __(data, timeit):
    pandas_sort, _ = timeit(lambda: data.sort_values('intensity'))
    return (pandas_sort,)


@app.cell
def __(pl, timeit):
    polars_import, df = timeit(lambda: pl.scan_csv("all_spots_shuffle.tsv", separator='\t').collect())
    return df, polars_import


@app.cell
def __(df, timeit):
    polars_mean, _ = timeit(lambda: df.mean())
    return (polars_mean,)


@app.cell
def __(df, timeit):
    polars_sort, _ = timeit(lambda: df.sort('intensity'))
    return (polars_sort,)


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def __(
    mo,
    pandas_import,
    pandas_mean,
    pandas_sort,
    polars_import,
    polars_mean,
    polars_sort,
):
    mo.md(
        f"""
        # Observation

        - ~~Marimo sucks~~
        - data import {pandas_import:.2f}s : {polars_import:.2f}s
        - mean {pandas_mean:.2f}s : {polars_mean:.2f}s
        - sort {pandas_sort:.2f}s : {polars_sort:.2f}s
        - pandas problem: mean with non-numeric columns causes an error (solution: `numeric_only`)
        - polars problem: reading xz directly does not work out of the box (solution: unpack before), column format guessing does not use enough columns for this dataset (zc column is guessed as int but is actually float, solution: shuffle csv)
        """
    )
    return


if __name__ == "__main__":
    app.run()
