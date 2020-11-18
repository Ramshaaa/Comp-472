from collections import Counter, OrderedDict
from pandas import read_csv, DataFrame
from numpy import concatenate
from matplotlib.pyplot import savefig, show
from sklearn.metrics import plot_confusion_matrix, classification_report, f1_score
from sklearn.model_selection import GridSearchCV, PredefinedSplit
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import Perceptron
from sklearn.neural_network import MLPClassifier

# Dataset 1
info_1 = read_csv('./Assig1-Dataset/info_1.csv')
train_1 = read_csv('./Assig1-Dataset/train_1.csv', header=None)
val_1 = read_csv('./Assig1-Dataset/val_1.csv', header=None)
test_no_label_1 = read_csv('./Assig1-Dataset/test_no_label_1.csv', header=None)
test_with_label_1 = read_csv('./Assig1-Dataset/test_with_label_1.csv', header=None)

# Dataset 2
info_2 = read_csv('./Assig1-Dataset/info_2.csv')
train_2 = read_csv('./Assig1-Dataset/train_2.csv', header=None)
val_2 = read_csv('./Assig1-Dataset/val_2.csv', header=None)
test_no_label_2 = read_csv('./Assig1-Dataset/test_no_label_2.csv', header=None)
test_with_label_2 = read_csv('./Assig1-Dataset/test_with_label_2.csv', header=None)

# Demoset 2
Demo_test_no_label_2 = read_csv('./Assig1-Dataset/47.csv')


def unbox(dataset):
    X = dataset.values[:, :-1]
    Y = dataset.values[:, -1]
    return X, Y


def confusionmatrix(testWithLabel, model, output_file):
    X_test, y_test = unbox(testWithLabel)
    y_predict = model.predict(X_test)
    f1_score_w = f1_score(y_test, y_predict, average='weighted')
    plot_confusion_matrix(model, X_test, y_test)
    savefig(output_file + '.png')
    show()
    report = classification_report(y_test, y_predict, output_dict=True, zero_division=1)
    df = DataFrame(report).transpose()
    return df, f1_score_w


def prediction(testNoLabel, model, output_file):
    X_test = testNoLabel.values[:, :]
    y_predict = model.predict(X_test)
    df = DataFrame(y_predict)
    df.to_csv(output_file + '.csv', mode='w')


def distribution_plot(info, dataset, output_file):
    X, y = unbox(dataset)
    X_axis, y_axis = unbox(info)
    frequency = OrderedDict(sorted(Counter(y).items())).values()
    # print(frequency)
    df = DataFrame({'Letters': y_axis, 'number of instances in each class': frequency})
    ax = df.plot.bar(x='Letters', y='number of instances in each class', figsize=(16, 6), rot=0)
    savefig(output_file + '.png')
    show()


def Best_Model(info, train, val, test_no_label, test_with_label, suffix):
    distribution_plot(info, train, './Output Files/Distribution' + suffix)

    X_train, y_train = unbox(train)
    X_valid, y_valid = unbox(val)
    X_dev = concatenate((X_train, X_valid), axis=0)
    y_dev = concatenate((y_train, y_valid), axis=0)

    model_params = {
        'GNB': {
            'model': GaussianNB(),
            'params': {}
        },
        'Base-DT': {
            'model': DecisionTreeClassifier(criterion='entropy'),
            'params': {}
        },
        'Best-DT': {
            'model': DecisionTreeClassifier(),
            'params': {
                'class_weight': ['balanced', None],
                'criterion': ['gini', 'entropy'],
                'max_depth': [10, None],
                'min_impurity_decrease': [0.0, 0.1],
                'min_samples_split': [2, 3, 4, 5, 6]
            }
        },
        'PER': {
            'model': Perceptron(),
            'params': {}
        },
        'Base-MLP': {
            'model': MLPClassifier(activation='logistic', hidden_layer_sizes=(100,), solver='sgd'),
            'params': {}
        },
        'Best-MLP': {
            'model': MLPClassifier(),
            'params': {
                'activation': ['identity', 'logistic', 'tanh', 'relu'],
                'hidden_layer_sizes': [(10, 10, 50), (30, 50)],
                'solver': ['sgd', 'adam']
            }
        }
    }

    scores = []

    for model_name, mp in model_params.items():

        global f1_score_w

        if model_name == 'Best-DT' or model_name == 'Best-MLP':
            ps = PredefinedSplit(test_fold=([-1] * len(X_train) + [0] * len(X_valid)))
            model = GridSearchCV(mp['model'], mp['params'], cv=ps, n_jobs=-1).fit(X_dev, y_dev)
            prediction(test_no_label, model, './Output Files/' + model_name + '/' + model_name + suffix)
            df = confusionmatrix(test_with_label, model, './Output Files/' + model_name + '/' + model_name + suffix)
            df[0].to_csv('./Output Files/' + model_name + '/' + model_name + suffix + '.csv', mode='a')

            scores.append({
                'model': model_name,
                'best_score (F1-score weighted)': df[1],
                'best_params': model.best_params_
            })
        else:
            model = mp['model'].fit(X_train, y_train)
            prediction(test_no_label, model, './Output Files/' + model_name + '/' + model_name + suffix)
            df = confusionmatrix(test_with_label, model, './Output Files/' + model_name + '/' + model_name + suffix)
            df[0].to_csv('./Output Files/' + model_name + '/' + model_name + suffix + '.csv', mode='a')

            scores.append({
                'model': model_name,
                'best_score (F1-score weighted)': df[1],
                'best_params': mp['params']
            })

            # This is to output the file '47' given during the demo
            if model_name == 'PER' and suffix == '-DS2':
                prediction(Demo_test_no_label_2, model, './Output Files/' + model_name + suffix + '-Demo')

    df = DataFrame(scores, columns=['model', 'best_score (F1-score weighted)', 'best_params'])
    df.to_csv('./Output Files/Best-Model' + suffix + '.csv', mode='w')


Best_Model(info_1, train_1, val_1, test_no_label_1, test_with_label_1, '-DS1')
Best_Model(info_2, train_2, val_2, test_no_label_2, test_with_label_2, '-DS2')