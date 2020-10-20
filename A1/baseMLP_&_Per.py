def PER():
    X, y = unbox(train_1)
    model1 = Perceptron().fit(X, y)

    df = confusion_matrix(test_with_label_1, model1, 'PER-DS1')
    df.to_csv('PER-DS1.csv', mode='w')

    X, y = unbox(train_2)
    model2 = Perceptron().fit(X, y)

    df = confusion_matrix(test_with_label_2, model2, 'PER-DS2')
    df.to_csv('PER-DS2.csv', mode='w')


def Base_MLP():
    mlp = MLPClassifier(hidden_layer_sizes=(100,), activation='logistic', solver='sgd', max_iter=5000)

    X, y = unbox(train_1)
    model1 = mlp.fit(X, y)

    df = confusion_matrix(test_with_label_1, model1, 'Base-MLP-DS1')
    df.to_csv('Base-MLP-DS1.csv', mode='w')

    X, y = unbox(train_2)
    model2 = mlp.fit(X, y)

    df = confusion_matrix(test_with_label_2, model2, 'Base-MLP-DS2')
    df.to_csv('Base-MLP-DS2.csv', mode='w')


# GNB()
# Base_DT()
#
# PER()
# Base_MLP()

# distribution_plot(train_1, info_1)