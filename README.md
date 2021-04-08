# pd-helper
 
 A helpful package to streamline Pandas DataFrame optimization.
 
 Save 50-75% on DataFrame memory usage by running the optimizer. 
 
 Auto configure dtypes for appropriate data types in each column. 

## Basic Usage
 
 Given a pandas dataframe, "df":
 ```python3
 from pd_helper.helper import optmize
 
 if __name__ == "__main__":
    # guading function under module is necessary to run multiprocessing (save time).
    # some DataFrame, df
    df = optimize(df)
 ```
 
## Install
 ```bash
 pip install pd-helper
 ```

## Sample Results

```bash
Starting with 175.63 MB memory.

After optmization. 

Ending with 65.33 MB memory.
```
