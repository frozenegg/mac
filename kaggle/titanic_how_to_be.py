import pandas as pd
ntrain = train.shape[0]
ntest = test.shape[0]

y_train = train['Survived'].values
passId = test['PassengerId']

data = pd.concat((train, test))

train['Survived'].value_counts()

import missingno as msno
msno.matrix(data)

data.isnull().sum()
data.Age.isnull()
data.Age.isnull().any()

print(data.corr())

# fig = plt.figure(figsize(10,2))
sns.countplot(y='Survived', data=train)

def piecount(col):
    f, ax = plt.subplots(1, 2, figsize=(15, 6))
    train[col].value_counts().plot.pie(explode=[0.1 for i in range(train[col].nunique())], autopct='%1.1f%%', ax=ax[0], shadow=True)
    ax[0].set_title(col)
    ax[0].set_ylabel('')
    sns.countplot(col, data=train, ax=ax[1])
    ax[1].set_title(col)
    plt.show()

train.groupby(['Pclass', 'Survived'])['Survived'].count()

data.Name.value_counts()

temp = data.copy()
temp['Initial'] = 0
temp['Initial'] = data.Name.str.extract('([A-Za-z0-9]+)¥.')

sns.swarmplot(x=train['Survived'], y=train['Age'])
plt.xlabel('Survived')
plt.ylabel('Age')
plt.show()

temp.groupby('Initial').agg({'Age': ['mean', 'count']})
temp = temp.reset_index(drop=True)
temp['Age'] = temp.groupby('Initial')['Age'].apply(lambda x: x.fillna(x.mean()))

# binning
s_cut = pd.cut(s, 4)
s_cut = pd.cut(s, [0, 10, 50, 100])
s_cut, bins = pd.cut(s, 4, retbins=True)
print(type(bins))

temp['Fare'].fillna(temp['Fare'].mean(), inplace=True)

temp.groupby('NumTicket')['Survived'].mean().to_frame().plot(kind='hist')

# Name to number
temp['Inicab'] = temp['Inicab'].factorize()[0]

# Making ML Models
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.fit_transform(X_test)

ran = RandomForestClassifier(random_state=1)
knn = KNeighborsClassifier()
log = LogisticRegression()
xgb = XGBClassifier()
gbc = GradientBoostingClassifier()
svc = SVC(probability=True)
ext = ExtraTreesClassifier()
ada = AdaBoostClassifier()
gnb = GaussianNB()
gpc = GaussianProcessClassifier()
bag = BaggingClassifier()

models = [ran, knn, log, xgb, gbc, svc, ext, ada, gnb, gpc, bag]
model_names = ['Random Forest', 'K Nearest Neighbor', 'Logistic Regression', 'XGBoost', 'SVC', 'Extra Trees', 'AdaBoost', 'Gaussian Naive Bayes', 'Gaussian Process', 'Bagging Classifier']
scores = {}

for ind, mod in enumerate(models):
    mod.fit(X_train, y_train)
    acc = cross_val_score(mod, X_train, y_train, scoring = 'accuracy', cv=10)
    scores[model_names[ind]] = acc

results = pd.DataFrame(scores).T
results['mean'] = results.mean(1)

results_df = results.sort_values(by='mean', ascending=False)#.reset_index()

results_df = results_df.drop(['mean'], axis=1)
sns.boxplot(data=results_df.T, orient='h')
plt.title('Machine Learning Algorithm Accuracy Score')
plt.xlabel('Accuracy Score (%)')

def importance_plotting(data, xlabel, ylabel, title, n=20):
    sns.set(style='whitegrid')
    ax = data.tail(n).plot(kind='barh')

    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.xaxis.grid(False)
    ax.yaxis.grid(True)
    plt,show()

fi = {'Features': train.columns.tolist(), 'Importance': xgb.feature_importances_}
importance = pd.DataFrame(fi, index=fi['Features']).sort_values('Importance', ascending=True)

title = 'Top 20 most important features in predicting survival on the Titanic: XGB'
importance_plotting(importance, 'Importance', 'Features', title, 20)
