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

# iloc : 行を番号で指定する
# loc : 行をindexで指定する

reviews.discription.iloc[0]
reviews.discription[0]
reviews.discription.loc[0]

reviews.iloc[0]
reviews.loc[0]
# not reviews[0]

reviews.iloc[:10]
reviews.head(10)

reviews.loc[[1,2,3,5,8], ['country', 'province', 'region_1', 'region_2']]
reviews.loc[:99, ['country', 'variety']]

italian_wines = reviews[reviews.country == 'Italy']

top_oceania_wines = reviews.loc[(reviews.country.isin(['Australia', 'New Zealand'])) & (reviews.points >= 95)
top_oceania_wines = reviews[(reviews.points >= 95) & ((reviews.country == 'New Zealand') | (reviews.country == 'Australia'))]
# use &, | instead of 'and', 'or'

# Summary functions
reviews.points.describe()
reviews.points.mean()
reviews.taster_name.unique()
reviews.taster_name.value_counts()
reviews.points.map(lambda p: p - review.points.mean()) # changes points

def remean_points(row):
    row.points = row.points - review_points_mean
    return row
reviews.apply(remean_points, axis='columns')

reviews.points - reviews.points.mean() # faster way
reviews.country + " - " + reviews.region_1

bargain_idx = (reviews.points / reviews.price).idxmax()
bargain_wine = reviews.loc[bargain_idx, 'title']

n_trop = reviews.description.map(lambda desc: "tropical" in desc).sum()
n_fruity = reviews.description.map(lambda desc: "fruity" in desc).sum()
descriptor_counts = pd.Series([n_trop, n_fruity], index=['tropical', 'fruity'])

def stars(row):
    if row.country == 'Canada':
        return 3
    elif row.points >= 95:
        return 3
    elif row.points >= 85:
        return 2
    else:
        return 1
star_ratings = reviews.apply(stars, axis='columns')

reviews.groupby('points').points.count()
reviews.groupby('points').price.min()
reviews.groupby('winery').apply(lambda df: df.title.iloc[0])
reviews.groupby(['country', 'province']).apply(lambda df: df.loc[df.points.idxmax()])
reviews.groupby(['country']).price.agg([len, min, max])

countries_reviewed.sort_values(by='len')
countries_reviewed.sort_values(by='len', ascending=False)
countries_reviewed.sort_index()
countries_reviewed.reset_index()
countries_reviewed.sort_values(by=['country', 'len'])

reviews.points.dtype
reviews.points.astype('float64')

reviews[pd.isnull(reviews.country)]
reviews.region_2.fillna('Unknown')
reviews.taster_twitter_handle.replace('@kerinokeefe', '@kernio')

reviews[reviews.price.isnull()]
reviews.price.isnull().sum()
pd.isnull(reviews.price.sum())

# Renaming and Combining
renamed = reviews.rename(columns=dict(region_1='region', region_2='locale'))
reindexed = reviews.rename_axis('wines', axis='rows')

combined_products = pd.concat([gaming_products, movie_products])
powerlifting_combined = powerlifting_meets.set_index('MeetID').join(powerlifting_competitors.set_index('MeetID'))
