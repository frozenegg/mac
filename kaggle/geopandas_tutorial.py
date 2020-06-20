import geopandas as gpd

# use shapefile for easy use
full_data = gpd.read_file('filename.shp')
data = full_data.loc[:, ['CLASS', 'COUNTRY', 'geometry']].copy()

data.CLASS.value_counts()
wild_lands = data.loc[data.CLASS.isin(['WILD FOREST', 'WILDERNESS'])].copy()
wild_lands.plot()
