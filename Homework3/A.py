from main import replace_accented
from sklearn import svm
from sklearn import neighbors
from nltk import word_tokenize
from string import punctuation as puncts
import codecs

# don't change the window size
window_size = 10

# A.1
def build_s(data):
    '''
    Compute the context vector for each lexelt
    :param data: dic with the following structure:
        {
			lexelt: [(instance_id, left_context, head, right_context, sense_id), ...],
			...
        }
    :return: dic s with the following structure:
        {
			lexelt: [w1,w2,w3, ...],
			...
        }

    '''
    s = {}

    # implement your code here

    for lexelt in data:
        words = set()
        for instance in data[lexelt]:

            left_context = word_tokenize(instance[1].strip())
            for token in left_context[-window_size:]:
                if token not in puncts:
                    words.add(token)

            right_context = word_tokenize(instance[3].strip())
            for token in right_context[:window_size]:
                if token not in puncts:
                    words.add(token)
        s[lexelt] = list(words)

    return s


# A.1
def vectorize(data, s):
    '''
    :param data: list of instances for a given lexelt with the following structure:
        {
			[(instance_id, left_context, head, right_context, sense_id), ...]
        }
    :param s: list of words (features) for a given lexelt: [w1,w2,w3, ...]
    :return: vectors: A dictionary with the following structure
            { instance_id: [w_1 count, w_2 count, ...],
            ...
            }
            labels: A dictionary with the following structure
            { instance_id : sense_id }

    '''
    vectors = {}
    labels = {}

    # implement your code here

    index = {}
    i = 0
    for word in s:
        index[word] = i
        i += 1

    for instance in data:

        feat = [0] * len(s)

        left_context = word_tokenize(instance[1].strip())
        for token in left_context[-window_size:]:
            if token in index:
                feat[index[token]] += 1

        right_context = word_tokenize(instance[3].strip())
        for token in right_context[:window_size]:
            if token in index:
                feat[index[token]] += 1

        vectors[instance[0]] = feat
        labels[instance[0]] = instance[4]

    return vectors, labels


# A.2
def classify(X_train, X_test, y_train):
    '''
    Train two classifiers on (X_train, and y_train) then predict X_test labels

    :param X_train: A dictionary with the following structure
            { instance_id: [w_1 count, w_2 count, ...],
            ...
            }

    :param X_test: A dictionary with the following structure
            { instance_id: [w_1 count, w_2 count, ...],
            ...
            }

    :param y_train: A dictionary with the following structure
            { instance_id : sense_id }

    :return: svm_results: a list of tuples (instance_id, label) where labels are predicted by LinearSVC
             knn_results: a list of tuples (instance_id, label) where labels are predicted by KNeighborsClassifier
    '''

    svm_clf = svm.LinearSVC()
    knn_clf = neighbors.KNeighborsClassifier()

    # implement your code here

    data_train = []
    targets_train = []
    for item in X_train:
        data_train.append(X_train[item])
        targets_train.append(y_train[item])

    data_test = []
    ids_test = []
    for item in X_test:
        data_test.append(X_test[item])
        ids_test.append(item)

    svm_clf.fit(data_train, targets_train)
    targets_svm = svm_clf.predict(data_test)
    svm_result = zip(ids_test, targets_svm)

    knn_clf.fit(data_train, targets_train)
    targets_knn = knn_clf.predict(data_test)
    knn_result = zip(ids_test, targets_knn)

    return svm_result, knn_result


# A.3, A.4 output
def print_results(results, output_file):
    '''

    :param results: A dictionary with key = lexelt and value = a list of tuples (instance_id, label)
    :param output_file: file to write output

    '''

    # implement your code here
    # don't forget to remove the accent of characters using main.replace_accented(input_str)
    # you should sort results on instance_id before printing

    from main import replace_accented

    outfile = codecs.open(output_file, encoding='utf-8', mode='w')
    for lexelt, instances in sorted(results.iteritems(), key=lambda d: replace_accented(d[0].split('.')[0])):
        for instance in sorted(instances, key=lambda d: int(d[0].split('.')[-1])):
            outfile.write(replace_accented(lexelt + ' ' + instance[0] + ' ' + instance[1] + '\n'))
    outfile.close()


# run part A
def run(train, test, language, knn_file, svm_file):
    s = build_s(train)
    svm_results = {}
    knn_results = {}
    for lexelt in s:
        X_train, y_train = vectorize(train[lexelt], s[lexelt])
        X_test, _ = vectorize(test[lexelt], s[lexelt])
        svm_results[lexelt], knn_results[lexelt] = classify(X_train, X_test, y_train)

    print_results(svm_results, svm_file)
    print_results(knn_results, knn_file)



