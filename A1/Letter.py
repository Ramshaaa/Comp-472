import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import plot_confusion_matrix

# Read the file
data1_Train = pd.read_csv('../input/Assig1-Dataset/train_1.csv')
data2_Train = pd.read_csv('../input/Assig1-Dataset/train_2.csv')
data1_Val = pd.read_csv('../input/Assig1-Dataset/val_1.csv')
data2_Val = pd.read_csv('../input/Assig1-Dataset/val_2.csv')
data1_Test = pd.read_csv('../input/Assig1-Dataset/test_with_label_1.csv')
data2_Test = pd.read_csv('../input/Assig1-Dataset/test_with_label_2.csv')
data1_Test_no_label = pd.read_csv('../input/Assig1-Dataset/test_no_label_1.csv')
data2_Test_no_label = pd.read_csv('../input/Assig1-Dataset/test_no_label_2.csv')

# split the data_1 into training, validation, and test sets
X_train = data1_Train.iloc[:, 0:-1]
y_train = data1_Train.iloc[:, 1024]  # index 1024 aka col 1025
X_val = data1_Val.iloc[:, 0:-1]
y_val = data1_Val.iloc[:, 1024]
X_test = data1_Test.iloc[:, 0:-1]
y_test = data1_Test.iloc[:, 1024]
# yy_test = data1_Test.values[:, -1].ravel()
yy_test = data1_Test.values[:, 1024]
print(yy_test)

# # Make the data
# names1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
#           'W', 'X', 'Y', 'Z']
# values1 = data1_Train['letter'].value_counts().sort_index()
# df = pd.DataFrame({'Alphabet Letters': names1, 'number of instances in each class': values1})
# df.plot.bar(x='Alphabet Letters', y='number of instances in each class', figsize=(12, 4), rot=0)
# plt.show()
#
# Make the data
names2 = ['π', 'α', 'β', 'σ', 'γ', 'δ', 'λ', 'ω', 'µ', 'ξ']
values2 = data2_Train['letter'].value_counts().sort_index()
df = pd.DataFrame({'Greek Letters': names2, 'number of instances in each class': values2})
df.plot.bar(x='Greek Letters', y='number of instances in each class', figsize=(12, 4), rot=0)
plt.show()

#
#
def gnb(X_train, y_train, X_test, y_test):
    # train the model
    gnb = GaussianNB()
    gnb.fit(X_train, y_train)
    # print('gnb accuracy : ', gnb.score(X_test, y_test))

    # use the model to predict the labels of the test data
    y_predicted = gnb.predict(X_test)
    y_expected = y_test
    print('Predicted Value:', y_predicted)
    print()
    print('Expected Value:', y_expected)
    print()

    # Confusion matrix
    print(metrics.classification_report(y_expected, y_predicted))
    print(metrics.confusion_matrix(y_expected, y_predicted))

    # submission = pd.DataFrame(y_predicted, columns=['alphabet letter'])
    # submission.to_csv('[GNB]-[dataset 1].csv')


gnb(X_train, y_train, X_test, y_test)
#
#
# def basedt(X_train, y_train, X_test, y_test):
#     dt = DecisionTreeClassifier(criterion='entropy')
#     dt.fit(X_train, y_train)
#     print('dt accuracy : ', dt.score(X_test, y_test))
#
#     # Confusion matrix
#     y_predicted = dt.predict(X_test)
#     y_expected = y_test
#     print('Predicted Value:', y_predicted)
#     print()
#     print('Expected Value:', y_expected)
#     print()
#
#     # Confusion matrix
#     print(metrics.classification_report(y_expected, y_predicted))
#     print(metrics.confusion_matrix(y_expected, y_predicted))
#     # submission = pd.DataFrame(y_predicted, columns=['alphabet letter'])
#     # submission.to_csv('[GNB]-[dataset 3].csv')
#
#
# basedt(X_train, y_train, X_test, y_test)
#
# def BestDt(X_train, y_train, X_val, y_val, X_test, y_test):
#     dtc = DecisionTreeClassifier()
#     parameter_space = {
#         'criterion': ['gini', 'entropy'],
#         'max_depth': [None, 10],
#         'min_samples_split': [0.1, 0.2, 3],
#         'min_impurity_decrease': [0.0, 1.0, 2.0],
#         'class_weight': ['balanced', None]
#     }
#
#     model1 = GridSearchCV(dtc, parameter_space, n_jobs=-1)
#     model1.fit(X_train, y_train)
#     print(model1.best_params_)
#
#     y_predict = model1.predict(X_val)
#     score = metrics.accuracy_score(y_val, y_predict)
#     print(f'BestDt DS1 Score: {score}')
#
#     X = data1_Test_no_label.values[:, :]
#     y_predict = model1.predict(X)
#     df = pd.DataFrame(y_predict)
#     df.to_csv("BestDt-DS1.csv", mode='w')
#
#     y_predict = model1.predict(X_test)
#     plot_confusion_matrix(model1, X_test, y_test)
#     plt.savefig("BestDt-DS1.png")
#     df.to_csv("BestDt-DS1.csv", mode='a')
#
#
# BestDt(X_train, y_train, X_val, y_val, X_test, y_test)