import pandas as pd

# two core objects: Dataframe and Series

pd.Dataframe({'Yes': [50,21], 'No': [131,2]})
pd.DataFrame({'Bob': ['I liked it.', 'It was awful.'],
              'Sue': ['Pretty good.', 'Bland.']},
             index=['Product A', 'Product B'])

pd.Series([1, 2, 3, 4, 5])
pd.Series([30, 35, 40], index=['2015 Sales', '2016 Sales', '2017 Sales'], name='Product A')

data = pd.read_csv('file path', index_col=0) # set index array to its index (index column)
animals = pd.DataFrame({'Cows': [12, 20], 'Goats': [22, 19]}, index=['Year 1', 'Year 2'])
animals.to_csv('file name')
