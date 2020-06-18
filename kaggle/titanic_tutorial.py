train_data = pd.read_csv(file_path)
test_data = pd.read_csv(file_path)

women = train_data.loc[train_data.Sex == 'female']['Survived']
rate_women = sum(women)/len(women)

from sklearn.ensemble import RandomForestClassifier
y = train_data['Survived']

features = ['Pclass', 'Sex', 'SibSp', 'Parch']
X = pd.get_dummies(train_data[features])
X_test = pd.get_dummies(test_data[features])

model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
model.fit(X, y)
predictions = model.predict(X_test)
