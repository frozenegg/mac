import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns
plt.style.use('seaborn-whitegrid')
import missingno

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import VotingClassifier

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_predict
from sklearn import model_selection

def model_assessment(X_train, X_test, y_train, y_test):
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

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

    ns.boxplot(data=results_df.T, orient='h')
    plt.title('Machine Learning Algorithm Accuracy Score')
    plt.xlabel('Accuracy Score (%)')

    # fi = {'Features': train.columns.tolist(), 'Importance': xgb.feature_importances_}
    # importance = pd.DataFrame(fi, index=fi['Features']).sort_values('Importance', ascending=True)
    #
    # title = 'Top 20 most important features in predicting survival on the Titanic: XGB'
    # importance_plotting(importance, 'Importance', 'Features', title, 20)

def importance_plotting(data, xlabel, ylabel, title, n=20):
    sns.set(style='whitegrid')
    ax = data.tail(n).plot(kind='barh')

    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.xaxis.grid(False)
    ax.yaxis.grid(True)
    plt,show()
