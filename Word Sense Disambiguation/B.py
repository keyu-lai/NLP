import A
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
from nltk import word_tokenize
from string import punctuation as puncts
import sklearn.feature_selection as se
# from nltk.corpus import wordnet as wn

def build_s(data, stemmer):
    s = {}

    for lexelt in data:
        words = set()
        for instance in data[lexelt]:

            context = word_tokenize(instance[1].strip())[-window_size:] + word_tokenize(instance[3].strip())[:window_size]

            for token in context:
                token = stemmer(token)
                if token not in puncts:
                    words.add(token)
        s[lexelt] = list(words)

    return s

# Get the taager of a certain language
def get_tagger(language):

    def English_tagger():
        import nltk
        from nltk.data import load
        tagger = load('taggers/maxent_treebank_pos_tagger/english.pickle')
        return tagger

    def Spanish_tagger():
        import nltk
        from nltk.corpus import cess_esp
        training = cess_esp.tagged_sents()
        default_tagger = nltk.DefaultTagger('NOUN')
        bigram_tagger = nltk.BigramTagger(training, backoff=default_tagger)
        trigram_tagger = nltk.TrigramTagger(training, backoff=bigram_tagger)
        return trigram_tagger

    def Catalan_tagger():
        import nltk
        from nltk.corpus import cess_cat
        training = cess_cat.tagged_sents()
        default_tagger = nltk.DefaultTagger('NOUN')
        bigram_tagger = nltk.BigramTagger(training, backoff=default_tagger)
        trigram_tagger = nltk.TrigramTagger(training, backoff=bigram_tagger)
        return trigram_tagger

    taggers = {'English': English_tagger, 'Spanish': Spanish_tagger, 'Catalan': Catalan_tagger}

    return taggers[language]()

def get_stemmer(language):

    def free_stemmer(word):
        try:
            word = my_stemmer(word)
        except:
            pass
        return word

    import nltk.stem.snowball
    if language == 'English':
        my_stemmer = nltk.stem.snowball.EnglishStemmer().stem
    else:
        my_stemmer = nltk.stem.snowball.SpanishStemmer().stem
    return free_stemmer

# Get the necessary information for relavence method
def get_relavence_info(data, stemmer):

    words_count = {}
    senses_count = {}

    for instance in data:
        sentence = word_tokenize(instance[1].strip()) + word_tokenize(instance[3].strip())
        if instance[4] not in senses_count:
            senses_count[instance[4]] = {}
        for token in set(sentence):
            token = stemmer(token)
            if token in words_count:
                words_count[token] += 1
            else:
                words_count[token] = 1
            if token in senses_count[instance[4]]:
                senses_count[instance[4]][token] += 1
            else:
                senses_count[instance[4]][token] = 1

    return words_count, senses_count

# You might change the window size
window_size = 17

# B.1.a,b,c,d
def extract_features(data, tagger, words_count, senses_count, stemmer, s):
    '''
    :param data: list of instances for a given lexelt with the following structure:
        {
			[(instance_id, left_context, head, right_context, sense_id), ...]
        }
    :return: features: A dictionary with the following structure
             { instance_id: {f1:count, f2:count,...}
            ...
            }
            labels: A dictionary with the following structure
            { instance_id : sense_id }
    '''
    features = {}
    labels = {}

    # implement your code here

    def get_col_feats(data, tagger, stemmer):

        size = 3

        for instance in data:

            sentence = []
            left_context = word_tokenize(instance[1].strip())[-size:]
            right_context = word_tokenize(instance[3].strip())[:size]
            tuples = tagger.tag(left_context + [instance[2]] + right_context)

            center = len(left_context)
            left = 0 if len(left_context) <= size else center - size
            right = center + len(right_context) if len(right_context) <= size else center + size

            for i in range(left, right):
                features[instance[0]]['POS' + str(i-center)] = tuples[i][1]
                features[instance[0]]['w' + str(i-center)] = stemmer(tuples[i][0]) 

    def get_relavence_feats(data, words_count, senses_count, stemmer):

        size = 3
        for instance in data:
            window = word_tokenize(instance[1].strip())[-size:] + word_tokenize(instance[1].strip())[:size]
            for sense in senses_count:
                max_score = -1000
                for word in window:
                    word = stemmer(word)
                    if word in senses_count[sense]:
                        if words_count[word] == senses_count[sense][word]:
                            tmp_score = words_count[word] * 1000
                        else:
                            tmp_score = float(senses_count[sense][word]) / (words_count[word] - senses_count[sense][word])
                        if tmp_score > max_score:
                            max_score = tmp_score
                            max_word = word
                if max_score > -1:
                    features[instance[0]][sense] = max_word

    def get_bag_of_words(data, s, stemmer):
        for instance in data:
            context = word_tokenize(instance[1].strip())[-window_size:] + word_tokenize(instance[3].strip())[:window_size]
            for token in context:
                token = stemmer(token)
                if token in s:
                    if token in features[instance[0]]:
                        features[instance[0]][token] += 1
                    else:
                        features[instance[0]][token] = 1


    for instance in data:
        labels[instance[0]] = instance[4]
        features[instance[0]] = {}

    get_col_feats(data, tagger, stemmer)
    get_relavence_feats(data, words_count, senses_count, stemmer)
    get_bag_of_words(data, s, stemmer)

    return features, labels

# implemented for you
def vectorize(train_features,test_features):
    '''
    convert set of features to vector representation
    :param train_features: A dictionary with the following structure
             { instance_id: {f1:count, f2:count,...}
            ...
            }
    :param test_features: A dictionary with the following structure
             { instance_id: {f1:count, f2:count,...}
            ...
            }
    :return: X_train: A dictionary with the following structure
             { instance_id: [f1_count,f2_count, ...]}
            ...
            }
            X_test: A dictionary with the following structure
             { instance_id: [f1_count,f2_count, ...]}
            ...
            }
    '''
    X_train = {}
    X_test = {}

    vec = DictVectorizer()
    vec.fit(train_features.values())
    for instance_id in train_features:
        X_train[instance_id] = vec.transform(train_features[instance_id]).toarray()[0]

    for instance_id in test_features:
        X_test[instance_id] = vec.transform(test_features[instance_id]).toarray()[0]

    return X_train, X_test

#B.1.e
def feature_selection(X_train,X_test,y_train):
    '''
    Try to select best features using good feature selection methods (chi-square or PMI)
    or simply you can return train, test if you want to select all features
    :param X_train: A dictionary with the following structure
             { instance_id: [f1_count,f2_count, ...]}
            ...
            }
    :param X_test: A dictionary with the following structure
             { instance_id: [f1_count,f2_count, ...]}
            ...
            }
    :param y_train: A dictionary with the following structure
            { instance_id : sense_id }
    :return:
    '''

    # implement your code here

    data_train = []
    targets_train = []
    for item in X_train:
        data_train.append(X_train[item].tolist())
        targets_train.append(y_train[item])

    data_test = []
    ids_test = []
    for item in X_test:
        data_test.append(X_test[item].tolist())
        ids_test.append(item)


    KBest = se.SelectKBest(se.chi2, len(data_train[0]) * 0.87)
    KBest.fit(data_train, targets_train)
    X_train_new = KBest.transform(data_train)
    X_test_new = KBest.transform(data_test)

    return X_train_new, X_test_new, targets_train, ids_test

# B.2
def classify(X_train, X_test, y_train, ids_test):
    '''
    Train the best classifier on (X_train, and y_train) then predict X_test labels

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

    :return: results: a list of tuples (instance_id, label) where labels are predicted by the best classifier
    '''

    results = []

    # implement your code here
    svm_clf = svm.LinearSVC()

    svm_clf.fit(X_train, y_train)
    targets_svm = svm_clf.predict(X_test)
    results = zip(ids_test, targets_svm)

    return results

# run part B
def run(train, test, language, answer):
    results = {}

    tagger = get_tagger(language)
    stemmer = get_stemmer(language)
    s = build_s(train, stemmer)

    for lexelt in train:

        words_count, senses_count = get_relavence_info(train[lexelt], stemmer)
        train_features, y_train = extract_features(train[lexelt], tagger, words_count, senses_count, stemmer, s[lexelt])
        test_features, _ = extract_features(test[lexelt], tagger, words_count, senses_count, stemmer, s[lexelt])

        X_train, X_test = vectorize(train_features,test_features)
        X_train_new, X_test_new, y_train_new, ids_test = feature_selection(X_train, X_test, y_train)
        results[lexelt] = classify(X_train_new, X_test_new, y_train_new, ids_test)

    A.print_results(results, answer)