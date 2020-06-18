data.describe()
data.info()
data['feature'].mean()
# max(), min(), ...
data.columns

data = pd.read_csv(file_path)
data.SalesPrice # one of the columns

feature_names = ['asdf', 'asdf']
X = data[feature_names]

# DecisionTreeRegressor
model = DecisionTreeRegressor(random_state=1)
model.fit(X,y)
preds = model.predict(X_dash)

# Validation
from sklearn.model_selection import train_test_split
train_X, train_y, val_X, val_y = train_test_split(X, y, random_state=1)
model.fit(train_X, train_y)
val_predictions = model.predict(val_X)

from sklearn.metrics import mean_absolute_error
val_mae = mean_absolute_error(val_predictions, val_y)

def get_mae(max_leaf_node, train_X, train_y, val_X, val_y):
    model = DecisionTreeRegressor(max_leaf_node=max_leaf_node, random_state=0)
    model.fit(train_X, train_y)
    preds_val = model.predict(val_X)
    mae = mean_absolute_error(val_y, preds_val)
    return mae

candidate_max_leaf_nodes = [5, 25, 50, 100, 250, 500]
mae_values = []
for node in candidate_max_leaf_nodes:
    mae_values.append(get_mae(node, train_X, train_y, val_X, val_y))
best_tree_size = candidate_max_leaf_nodes[mae_values.index(min(mae_values))]

from sklearn.ensemble import RandomForestRegressor
rf_model = RandomForestRegressor(random_state=1)
rf_model.fit(train_X, train_y)
rf_val_mae = mean_absolute_error(val_y, rf_model.predict(val_X))
