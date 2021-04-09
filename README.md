# pd-helper
 
 A helpful package to streamline Pandas DataFrame optimization.
 
 Save 50-75% on DataFrame memory usage by running the optimizer. 
 
 Autoconfigure dtypes for appropriate data types in each column with **helper**.

 Generate a random DataFrame of controlled random variables for testing with **maker**.

## Install
 ```bash
 pip install pd-helper
 ```

## Basic Usage to Iterate over DataFrame
```python
from pd_helper.maker import MakeData 
from pd_helper.helper import optimize
faker = MakeData()

if __name__ == "__main__":
   # MakeData() generates a fake dataframe, convenient for testing
   df = faker.make_df()
   df = optimize(df)
```
## Better Usage With Multiprocessing
```python
from pd_helper.maker import MakeData 
from pd_helper.helper import optimize
faker = MakeData()

if __name__ == "__main__":
   # MakeData() generates a fake dataframe, convenient for testing
   df = faker.make_df()
   df = optimize(df, enable_mp=True)
```

## Specify Special Mappings
```python
from pd_helper.maker import MakeData 
from pd_helper.helper import optimize
faker = MakeData()

if __name__ == "__main__":
   # MakeData() generates a fake dataframe, convenient for testing
   df = faker.make_df()
   special_mappings = {'string': ['object_id'],
                       'category': ['item_name']}
   
   # special mappings will be applied instead of by optimize ruleset, they will be returned.
   df = optimize(df
                 , enable_mp=True,
                 special_mappings=special_mappings
                 )
```


## Sample Results with Helper

```bash
Starting with 175.63 MB memory.

After optmization. 

Ending with 65.33 MB memory.
```

## Generating a Randomly Imperfect DataFrame with Maker

 Maker provides a class, MakeData(), to generate a table of made-up records. 
 
 Each row is an event where an item was retrieved. 
 
 Options to make the table imperfectly random in various ways. 
 
 Sample table below:

|  | Retrieved Date  | Item Name | Retrieved | Condition | Sector |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| Example | 2019-01-01, 2019-03-4  | Toaster, Lighter  | True, False  | Junk, Excellent  | 1, 2 |
| Data Type | String  | String  | String  | String | Integer |


## References

* Pandas Categorical: <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Categorical.html>

* Pandas Pickle: <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_pickle.html>

* Pandas CSV: <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html>

* Pandas Datetime: <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html>

### TODO

* Improve efficiency of iterating on DataFrame.

* Allow user to toggle logging.

* Provide tools for imputing missing data.
