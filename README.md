# pd-helper
 
 A helpful package to streamline Pandas DataFrame optimization.
 
 Save 50-75% on DataFrame memory usage by running the optimizer. 
 
 Auto configure dtypes for appropriate data types in each column. 

## Basic Usage to Iterate over DataFrame
```python
from pd_helper.helper import optimize

if __name__ == "__main__":
   # some DataFrame, df
   df = optimize(df)
```
## Better Usage With Multiprocessing
```python
from pd_helper.helper import optimize

if __name__ == "__main__":
   # some DataFrame, df
   df = optimize(df, enable_mp=True)
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


### TODO

* Improve efficiency of iterating on DataFrame.

* Allow user to toggle logging.

* Provide tools for imputing missing data.