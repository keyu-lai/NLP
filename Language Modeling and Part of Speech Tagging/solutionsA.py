import math
import nltk
import time

# Constants to be used by you when you fill the functions
START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
MINUS_INFINITY_SENTENCE_LOG_PROB = -1000

# TODO: IMPLEMENT THIS FUNCTION
# Calculates unigram, bigram, and trigram probabilities given a training corpus
# training_corpus: is a list of the sentences. Each sentence is a string with tokens separated by spaces, ending in a newline character.
# This function outputs three python dictionaries, where the keys are tuples expressing the ngram and the value is the log probability of that ngram
def calc_probabilities(training_corpus):

    tokens = []
    for item in training_corpus:
        tokens.extend(item.split(' ')[:-1] + [STOP_SYMBOL])
    logn = math.log(len(tokens), 2)
    unigram_count = dict()
    for item in set(tokens):
        unigram_count[(item, )] = 0
    for item in tokens:
        unigram_count[(item, )] += 1
    unigram_count = {item: math.log(unigram_count[item], 2) for item in unigram_count.keys()}
    unigram_p = {item: unigram_count[item] - logn for item in unigram_count.keys()}

    tuples = []
    for item in training_corpus:
        tuples.extend(list(nltk.bigrams([START_SYMBOL] + item.split(' ')[:-1] + [STOP_SYMBOL])))
    unigram_count[(START_SYMBOL, )] = math.log(len(training_corpus), 2)
    bigram_count = dict()
    for item in set(tuples):
        bigram_count[item] = 0
    for item in tuples:
        bigram_count[item] += 1
    bigram_count = {item: math.log(bigram_count[item], 2) for item in bigram_count.keys()}
    bigram_p = {item: bigram_count[item] - unigram_count[item[:1]] for item in bigram_count.keys()}

    tuples = []
    for item in training_corpus:
        tuples.extend(list(nltk.trigrams([START_SYMBOL, START_SYMBOL] + item.split(' ')[:-1] + [STOP_SYMBOL])))
    bigram_count[(START_SYMBOL, START_SYMBOL)] = math.log(len(training_corpus), 2)
    trigram_count = dict()
    for item in set(tuples):
        trigram_count[item] = 0
    for item in tuples:
        trigram_count[item] += 1
    trigram_count = {item: math.log(trigram_count[item], 2) for item in trigram_count.keys()}
    trigram_p = {item: trigram_count[item] - bigram_count[item[:2]] for item in trigram_count.keys()}

    return unigram_p, bigram_p, trigram_p

# Prints the output for q1
# Each input is a python dictionary where keys are a tuple expressing the ngram, and the value is the log probability of that ngram
def q1_output(unigrams, bigrams, trigrams, filename):
    # output probabilities
    outfile = open(filename, 'w')

    unigrams_keys = unigrams.keys()
    unigrams_keys.sort()
    for unigram in unigrams_keys:
        outfile.write('UNIGRAM ' + unigram[0] + ' ' + str(unigrams[unigram]) + '\n')

    bigrams_keys = bigrams.keys()
    bigrams_keys.sort()
    for bigram in bigrams_keys:
        outfile.write('BIGRAM ' + bigram[0] + ' ' + bigram[1]  + ' ' + str(bigrams[bigram]) + '\n')

    trigrams_keys = trigrams.keys()
    trigrams_keys.sort()    
    for trigram in trigrams_keys:
        outfile.write('TRIGRAM ' + trigram[0] + ' ' + trigram[1] + ' ' + trigram[2] + ' ' + str(trigrams[trigram]) + '\n')

    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Calculates scores (log probabilities) for every sentence
# ngram_p: python dictionary of probabilities of uni-, bi- and trigrams.
# n: size of the ngram you want to use to compute probabilities
# corpus: list of sentences to score. Each sentence is a string with tokens separated by spaces, ending in a newline character.
# This function must return a python list of scores, where the first element is the score of the first sentence, etc. 
def score(ngram_p, n, corpus):
    scores = []
    
    ngram_keys = set(ngram_p.keys())
    for sentence in corpus:
        if n == 1:
            tokens = sentence.split(' ')[:-1] + [STOP_SYMBOL]
            tuples = [(item, ) for item in tokens]
        elif n == 2:
            tuples = nltk.bigrams([START_SYMBOL] + sentence.split(' ')[:-1] + [STOP_SYMBOL])
        elif n == 3:
            tuples = nltk.trigrams([START_SYMBOL, START_SYMBOL] + sentence.split(' ')[:-1] + [STOP_SYMBOL])
        sen_score = 0
        try:
            for item in tuples:
                    sen_score += ngram_p[item]
        except KeyError:
            sen_score = MINUS_INFINITY_SENTENCE_LOG_PROB
        scores.append(sen_score)   
    return scores

# Outputs a score to a file
# scores: list of scores
# filename: is the output file name
def score_output(scores, filename):
    outfile = open(filename, 'w')
    for score in scores:
        outfile.write(str(score) + '\n')
    outfile.close()

# TODO: IMPLEMENT THIS FUNCTION
# Calculates scores (log probabilities) for every sentence with a linearly interpolated model
# Each ngram argument is a python dictionary where the keys are tuples that express an ngram and the value is the log probability of that ngram
# Like score(), this function returns a python list of scores
def linearscore(unigrams, bigrams, trigrams, corpus):
    from math import pow
    scores = []

    tmp = math.log(3, 2)
    for sentence in corpus:
        tuples = nltk.trigrams([START_SYMBOL, START_SYMBOL] + sentence.split(' ')[:-1] + [STOP_SYMBOL])
        sen_score = 0
        try:
            for item in tuples:
                sen_score += (math.log(pow(2.0, unigrams[item[2:]]) + pow(2.0, bigrams[item[1:]]) + pow(2.0, trigrams[item]), 2) - tmp)
        except KeyError:
            sen_score = MINUS_INFINITY_SENTENCE_LOG_PROB
        scores += [sen_score]
    return scores

DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'

# DO NOT MODIFY THE MAIN FUNCTION
def main():
    # start timer
    time.clock()

    # get data
    infile = open(DATA_PATH + 'Brown_train.txt', 'r')
    corpus = infile.readlines()
    infile.close()

    # calculate ngram probabilities (question 1)
    unigrams, bigrams, trigrams = calc_probabilities(corpus)

    # question 1 output
    q1_output(unigrams, bigrams, trigrams, OUTPUT_PATH + 'A1.txt')

    # score sentences (question 2)
    uniscores = score(unigrams, 1, corpus)
    biscores = score(bigrams, 2, corpus)
    triscores = score(trigrams, 3, corpus)

    # question 2 output
    score_output(uniscores, OUTPUT_PATH + 'A2.uni.txt')
    score_output(biscores, OUTPUT_PATH + 'A2.bi.txt')
    score_output(triscores, OUTPUT_PATH + 'A2.tri.txt')

    # linear interpolation (question 3)
    linearscores = linearscore(unigrams, bigrams, trigrams, corpus)

    # question 3 output
    score_output(linearscores, OUTPUT_PATH + 'A3.txt')

    # open Sample1 and Sample2 (question 5)
    infile = open(DATA_PATH + 'Sample1.txt', 'r')
    sample1 = infile.readlines()
    infile.close()
    infile = open(DATA_PATH + 'Sample2.txt', 'r')
    sample2 = infile.readlines()
    infile.close() 

    # score the samples
    sample1scores = linearscore(unigrams, bigrams, trigrams, sample1)
    sample2scores = linearscore(unigrams, bigrams, trigrams, sample2)

    # question 5 output
    score_output(sample1scores, OUTPUT_PATH + 'Sample1_scored.txt')
    score_output(sample2scores, OUTPUT_PATH + 'Sample2_scored.txt')

    # print total time to run Part A
    print "Part A time: " + str(time.clock()) + ' sec'

if __name__ == "__main__": main()
