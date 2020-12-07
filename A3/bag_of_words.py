import csv


def generate_bow(filename, FV=False):
    vocabulary = {}

    with open(filename, encoding="utf-8") as tsv_file:
        read_tsv = csv.reader(tsv_file, delimiter='\t')

        # Building a vocabulary of words from the given tweets
        for header, tweet in enumerate(read_tsv):
            if header != 0:
                for word in tweet[1].lower().split(' '):
                    if word in vocabulary:
                        vocabulary[word] += 1
                    else:
                        vocabulary[word] = 1

    if FV:
        for key in list(vocabulary.keys()):
            if vocabulary[key] == 1:
                del vocabulary[key]

    return vocabulary


if __name__ == '__main__':
    training_set = "covid_training.tsv"
    testing_set = "covid_test_public.tsv"
    original_vocabulary = generate_bow(training_set, False)
    filtered_vocabulary = generate_bow(training_set, True)

    print("Original Vocabulary (size: " + str(len(original_vocabulary)) + "): ", end='')
    print(original_vocabulary)
    print("Filtered Vocabulary (size: " + str(len(filtered_vocabulary)) + "): ", end='')
    print(filtered_vocabulary)
