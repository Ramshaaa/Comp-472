import sklearn
import pandas as pd
import csv
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import GridSearchCV, PredefinedSplit
from pandas import read_csv, DataFrame
from collections import Counter, OrderedDict
from matplotlib.pyplot import savefig, show
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import Perceptron
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import classification_report

train_1 = read_csv('../Assig1-Dataset/train_1.csv', header=None)
val_1 = read_csv('../Assig1-Dataset/val_1.csv', header=None)
test_with_label_1 = read_csv('../Assig1-Dataset/test_with_label_1.csv', header=None)
test_no_label_1 = read_csv('../Assig1-Dataset/test_no_label_1.csv', header=None)

train_2 = read_csv('../Assig1-Dataset/train_2.csv', header=None)
val_2 = read_csv('../Assig1-Dataset/val_2.csv', header=None)
test_with_label_2 = read_csv('../Assig1-Dataset/test_with_label_2.csv', header=None)
test_no_label_2 = read_csv('../Assig1-Dataset/test_no_label_2.csv', header=None)

info_1 = read_csv('../Assig1-Dataset/info_1.csv')
info_2 = read_csv('../Assig1-Dataset/info_2.csv')


def unbox(dataset):
    X = dataset.values[:, :-1]
    Y = dataset.values[:, -1]
    return X, Y


def confusion_matrix(dataset, model, output_file):
    X, y = unbox(dataset)
    y_predict = model.predict(X)
    plot_confusion_matrix(model, X, y)
    savefig(output_file + '.png')
    report = classification_report(y, y_predict, output_dict=True, zero_division=1)
    df = DataFrame(report).transpose()
    return df


def prediction(model, test, filename):
    X = test.values[:, :]
    y_predict = model.predict(X)
    df = pd.DataFrame(y_predict)
    df.to_csv(filename + ".csv", mode='w')


def distribution_plot(dataset, info):
    X, y = unbox(dataset)
    X_axis, y_axis = unbox(info)
    frequency = OrderedDict(sorted(Counter(y).items())).values()
    df = DataFrame({'Letters': y_axis, 'number of instances in each class': frequency})
    ax = df.plot.bar(x='Letters', y='number of instances in each class', figsize=(16, 6), rot=0)
    savefig('distribution.png')
    show()


def GNB():
    X, y = unbox(train_1)
    model1 = GaussianNB().fit(X, y)
    prediction(model1, test_no_label_1, 'GNB-DS1')
    df = confusion_matrix(test_with_label_1, model1, 'GNB-DS1')
    df.to_csv('GNB-DS1.csv', mode='a')

    X, y = unbox(train_2)
    model2 = GaussianNB().fit(X, y)
    prediction(model2, test_no_label_2, 'GNB-DS2')
    df = confusion_matrix(test_with_label_2, model2, 'GNB-DS2')
    df.to_csv('GNB-DS2.csv', mode='a')


def Base_DT():
    X, y = unbox(train_1)
    model1 = DecisionTreeClassifier().fit(X, y)
    prediction(model1, test_no_label_1, 'Base-DT-DS1')
    df = confusion_matrix(test_with_label_1, model1, 'Base-DT-DS1')
    df.to_csv('Base-DT-DS1.csv', mode='a')

    X, y = unbox(train_2)
    model2 = DecisionTreeClassifier().fit(X, y)
    prediction(model2, test_no_label_2, 'Base-DT-DS2')
    df = confusion_matrix(test_with_label_2, model2, 'Base-DT-DS2')
    df.to_csv('Base-DT-DS2.csv', mode='a')


def Best_DT():
    dtc = DecisionTreeClassifier()
    parameter_grid = {
        'criterion': ['gini', 'entropy'],
        'max_depth': [None, 10],
        'min_samples_split': [2, 3, 4, 5, 6],
        'min_impurity_decrease': [0.0, 0.02, 0.05, 0.1, 0.15, 0.2],
        'class_weight': ['balanced', None]
    }
    X_train, y_train = unbox(train_1)
    X_val, y_val = unbox(val_1)

    # Finding best hyperparameters using grid search.
    model1 = GridSearchCV(dtc, parameter_grid, n_jobs=-1)
    model1.fit(X_train, y_train)
    print(model1.best_params_)
    prediction(model1, test_no_label_1, 'Best-DT-DS1')

    # Train Best-DT model with dataset 1, using the hyperparameters found in the previous grid search.
    model1 = DecisionTreeClassifier(criterion=model1.best_params_['criterion'],
                                    max_depth=model1.best_params_['max_depth'],
                                    min_samples_split=model1.best_params_['min_samples_split'],
                                    min_impurity_decrease=model1.best_params_['min_impurity_decrease'],
                                    class_weight=model1.best_params_['class_weight'])
    model1.fit(X_train, y_train)

    # Use validation data to test
    y_val_predict = model1.predict(X_val)

    # Check validation metrics and modify hyper-parameters as needed in previous cell
    print(sklearn.metrics.confusion_matrix(y_val, y_val_predict))
    print(classification_report(y_val, y_val_predict, zero_division=1))

    # When ready, do testing
    X_test, y_test = unbox(test_with_label_1)
    y_predict = model1.predict(X_test)
    score = accuracy_score(y_test, y_predict)
    print(f'Best-DT DS1 Score: {score}')
    print(sklearn.metrics.confusion_matrix(y_test, y_predict))
    print(sklearn.metrics.classification_report(y_test, y_predict, zero_division=1))

    df = confusion_matrix(test_with_label_1, model1, 'Best-DT-DS1')
    df.to_csv('Best-DT-DS1.csv', mode='a')

    X, y = unbox(train_2)
    model2 = GridSearchCV(dtc, parameter_grid, n_jobs=-1)
    model2.fit(X, y)
    print(model2.best_params_)

    X_test, y_test = unbox(test_with_label_2)
    y_predict = model2.predict(X_test)
    score = accuracy_score(y_test, y_predict)
    print(f'Best-DT DS2 Score: {score}')

    df = confusion_matrix(test_with_label_2, model2, 'Best-DT-DS2')
    df.to_csv('Best-DT-DS2.csv', mode='a')


def PER():
    X, y = unbox(train_1)
    model1 = Perceptron().fit(X, y)
    prediction(model1, test_no_label_1, 'PER-DS1')
    df = confusion_matrix(test_with_label_1, model1, 'PER-DS1')
    df.to_csv('PER-DS1.csv', mode='a')

    X, y = unbox(train_2)
    model2 = Perceptron().fit(X, y)
    prediction(model2, test_no_label_2, 'PER-DS2')
    df = confusion_matrix(test_with_label_2, model2, 'PER-DS2')
    df.to_csv('PER-DS2.csv', mode='a')


def Base_MLP():
    mlp = MLPClassifier(hidden_layer_sizes=(100,), activation='logistic', solver='sgd', max_iter=5000)

    X, y = unbox(train_1)
    model1 = mlp.fit(X, y)
    prediction(model1, test_no_label_1, 'Base-MLP-DS1')
    df = confusion_matrix(test_with_label_1, model1, 'Base-MLP-DS1')
    df.to_csv('Base-MLP-DS1.csv', mode='a')

    X, y = unbox(train_2)
    model2 = mlp.fit(X, y)
    prediction(model2, test_no_label_2, 'Base-MLP-DS1')
    df = confusion_matrix(test_with_label_2, model2, 'Base-MLP-DS2')
    df.to_csv('Base-MLP-DS2.csv', mode='a')


def Best_MLP():
    mlp = MLPClassifier(max_iter=200)
    parameter_grid = {
        'hidden_layer_sizes': [(10, 10, 50), (30, 50)],
        'activation': ['identity', 'logistic', 'tanh', 'relu'],
        'solver': ['sgd', 'adam'],
    }
    X, y = unbox(train_1)
    model1 = GridSearchCV(mlp, parameter_grid, n_jobs=-1)
    model1.fit(X, y)
    print(model1.best_params_)

    prediction(model1, test_no_label_1, 'Best-MLP-DS1')
    df = confusion_matrix(test_with_label_1, model1, 'Best-MLP-DS1')
    df.to_csv('Best-MLP-DS1.csv', mode='a')

    X, y = unbox(train_2)
    model2 = GridSearchCV(mlp, parameter_grid, n_jobs=-1)
    model2.fit(X, y)
    print(model2.best_params_)

    prediction(model2, test_no_label_2, 'Best-MLP-DS2')
    df = confusion_matrix(test_with_label_2, model2, 'Best-MLP-DS2')
    df.to_csv('Best-MLP-DS2.csv', mode='a')


# GNB()
# Base_DT()
# Best_DT()
#
# PER()
# Base_MLP()
# Best_MLP()
#
# distribution_plot(train_2, info_2)