import pandas as pd
from collections import Counter
import collections
import matplotlib.pyplot as plt
import sklearn
from sklearn.metrics import accuracy_score
import sklearn.metrics
from sklearn.linear_model import Perceptron
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import classification_report
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

train_1 = pd.read_csv('Assig1-Dataset/Assig1-Dataset/train_1.csv', header=None)
val_1 = pd.read_csv('Assig1-Dataset/Assig1-Dataset/val_1.csv', header=None)
test_with_label_1 = pd.read_csv('Assig1-Dataset/Assig1-Dataset/test_with_label_1.csv', header=None)
test_no_label_1 = pd.read_csv('Assig1-Dataset/Assig1-Dataset/test_no_label_1.csv', header=None)

train_2 = pd.read_csv('Assig1-Dataset/Assig1-Dataset/train_2.csv', header=None)
val_2 = pd.read_csv('Assig1-Dataset/Assig1-Dataset/val_2.csv', header=None)
test_with_label_2 = pd.read_csv('Assig1-Dataset/Assig1-Dataset/test_with_label_2.csv', header=None)
test_no_label_2 = pd.read_csv('Assig1-Dataset/Assig1-Dataset/test_no_label_2.csv', header=None)

info_1 = pd.read_csv('Assig1-Dataset/Assig1-Dataset/info_1.csv')
info_2 = pd.read_csv('Assig1-Dataset/Assig1-Dataset/info_2.csv')


def unbox(dataset):
    X = dataset.values[:, :-1]
    Y = dataset.values[:, -1]
    return X, Y


def Score(y_test, y_predict):
    return sklearn.metrics.accuracy_score(y_test, y_predict)


def Save(filename, file, mode='w'):
    file.to_csv(filename + ".csv", mode=mode)


def confusionmatrix(DS, model, output_file):
    X, y = unbox(DS)
    y_predict = model.predict(X)
    plot_confusion_matrix(model, X, y)
    plt.savefig(output_file + '.png')
    report = classification_report(y, y_predict, output_dict=True, zero_division=1)
    df = pd.DataFrame(report).transpose()
    return df


def prediction(model, test, filename):
    X = test.values[:, :]
    y_predict = model.predict(X)
    df = pd.DataFrame(y_predict)
    Save(filename, df)


def distribution_plot(dataset, info):
    X, y = unbox(dataset)
    X_axis, y_axis = unbox(info)
    frequency = collections.OrderedDict(sorted(Counter(y).items())).values()
    df = pd.DataFrame({'Letters': y_axis, 'number of instances in each class': frequency})
    ax = df.plot.bar(x='Letters', y='number of instances in each class', figsize=(16, 6), rot=0)
    plt.savefig('distribution.png')
    plt.show()


def GNB():

    X, y = unbox(train_1)

    model1 = GaussianNB().fit(X, y)

    df = confusionmatrix(test_with_label_1, model1, "GNB-DS1")

    Save("GNB-DS1", df, mode='a')


    X, y = unbox(train_2)

    model2 = GaussianNB().fit(X, y)

    df = confusionmatrix(test_with_label_2, model2, "GNB-DS2")

    Save("GNB-DS2", df, mode='a')


def BaseDt():

    X, y = unbox(train_1)

    model1 = DecisionTreeClassifier().fit(X, y)

    df = confusionmatrix(test_with_label_1, model1, "BaseDt-DS1")

    Save("BaseDt-DS1", df, mode='a')


    X, y = unbox(train_2)

    model2 = DecisionTreeClassifier().fit(X, y)

    df = confusionmatrix(test_with_label_2, model2, "BaseDt-DS2")

    Save("BaseDt-DS2", df, mode='a')



GNB()
BaseDt()
# distribution_plot(train_2, info_2)
