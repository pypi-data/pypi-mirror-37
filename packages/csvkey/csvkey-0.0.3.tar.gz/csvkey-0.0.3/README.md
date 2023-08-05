## csvkey
For a very limited situation such that you don't need performance and 
want to use CSV as database.

## Example
```python
from csvkey import Connection
import pandas as pd
import numpy as np


# prepare DataFrame
data = pd.DataFrame()
data['A'] = pd.Series([1,2,3], dtype='int')
data['B'] = pd.Series([4,5,6], dtype='float32')
data['C'] = pd.Series([7,8,9], dtype='float64')


# register database
conn = Connection()
conn.initialize(data, r'C:\TEST\database.csv',
                primary=['A', 'B'],
                unique=['C'],
                notnull=['C'])
# database.csv and the configuration file (default: csv.conf) are generated in C:\TEST\
# set 'A' and 'B' columns as a primary key
# values in 'C' column must be unique and not NaN

 
# connect to database.csv
conn.connect(r'C:\TEST\database.csv')
conn.df.dtypes # dtypes are preserved


# change values in conn.df
conn.df.loc[0, 'C'] = 8
conn.commit() # raise ValueError because 8 is not unique
conn.df.loc[0, 'C'] = np.nan 
conn.commit() # raise ValueError because NaN is not allowed in 'C'
conn.df.loc[0, 'C'] = -1
conn.commit() # OK
conn.df.loc[2, ['A', 'B']] = [1, 4]
conn.commit() # raise ValueError because primary keys are duplicated
```

## Installation
```
pip install csvkey
```

## Requirements
pandas  
pyyaml
