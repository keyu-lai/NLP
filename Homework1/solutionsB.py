import sys
import nltk
import math
import time

START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
RARE_SYMBOL = '_RARE_'
RARE_WORD_MAX_FREQ = 5
LOG_PROB_OF_ZERO = -1000


# TODO: IMPLEMENT THIS FUNCTION
# Receives a list of tagged sentences and processes each sentence to generate a list of words and a list of tags.
# Each sentence is a string of space separated "WORD/TAG" tokens, with a newline character in the end.
# Remember to include start and stop symbols in yout returned lists, as defined by the constants START_SYMBOL and STOP_SYMBOL.
# brown_words (the list of words) should be a list where every element is a list of the tags of a particular sentence.
# brown_tags (the list of tags) should be a list where every element is a list of the tags of a particular sentence.
def split_wordtags(brown_train):
    brown_words = []
    brown_tags = []

    for sentence in brown_train:
        words = [START_SYMBOL, START_SYMBOL]
        tags = [START_SYMBOL, START_SYMBOL]
        for token in sentence.split(" ")[:-1]:
            i = token.rindex('/')
            words.append(token[:i])
            tags.append(token[i+1:])
        words.append(STOP_SYMBOL);
        tags.append(STOP_SYMBOL)
        brown_words.append(words)
        brown_tags.append(tags)
    return brown_words, brown_tags


# TODO: IMPLEMENT THIS FUNCTION
# This function takes tags from the training data and calculates tag trigram probabilities.
# It returns a python dictionary where the keys are tuples that represent the tag trigram, and the values are the log probability of that trigram
def calc_trigrams(brown_tags):
    tuples = []
    for item in brown_tags:
        tuples.extend(list(nltk.trigrams(item)))
    bigram_count = dict()
    trigram_count = dict()
    for item in set(tuples):
        trigram_count[item] = 0
        bigram_count[item[:2]] = 0
    for item in tuples:
        trigram_count[item] += 1
        bigram_count[item[:2]] += 1
    q_values = {item: math.log(trigram_count[item]/float(bigram_count[item[:2]]), 2) for item in trigram_count.keys()}
    return q_values

# This function takes output from calc_trigrams() and outputs it in the proper format
def q2_output(q_values, filename):
    outfile = open(filename, "w")
    trigrams = q_values.keys()
    trigrams.sort()  
    for trigram in trigrams:
        output = " ".join(['TRIGRAM', trigram[0], trigram[1], trigram[2], str(q_values[trigram])])
        outfile.write(output + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Takes the words from the training data and returns a set of all of the words that occur more than 5 times (use RARE_WORD_MAX_FREQ)
# brown_words is a python list where every element is a python list of the words of a particular sentence.
# Note: words that appear exactly 5 times should be considered rare!
def calc_known(brown_words):
    known_words = set()
    for sentence in brown_words:
        for word in sentence:
            known_words.add(word)
    words_count = dict()
    for word in known_words:
        words_count[word] = 0
    for sentence in brown_words:
        for word in sentence:
            words_count[word] += 1
    for key in words_count.keys():
        if words_count[key] <= RARE_WORD_MAX_FREQ:
            known_words.remove(key)
    return known_words

# TODO: IMPLEMENT THIS FUNCTION
# Takes the words from the training data and a set of words that should not be replaced for '_RARE_'
# Returns the equivalent to brown_words but replacing the unknown words by '_RARE_' (use RARE_SYMBOL constant)
def replace_rare(brown_words, known_words):
    brown_words_rare = []
    for sentence in brown_words:
        sentence_rare = list(sentence)
        for i in range(len(sentence)):
            if sentence[i] not in known_words:
                sentence_rare[i] = RARE_SYMBOL
        brown_words_rare.append(sentence_rare)
    return brown_words_rare

# This function takes the ouput from replace_rare and outputs it to a file
def q3_output(rare, filename):
    outfile = open(filename, 'w')
    for sentence in rare:
        outfile.write(' '.join(sentence[2:-1]) + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Calculates emission probabilities and creates a set of all possible tags
# The first return value is a python dictionary where each key is a tuple in which the first element is a word
# and the second is a tag, and the value is the log probability of the emission of the word given the tag
# The second return value is a set of all possible tags for this data set
def calc_emission(brown_words_rare, brown_tags):
    tuples = []
    for i in range(len(brown_words_rare)):
        for j in range(len(brown_words_rare[i])):
            tuples.append((brown_words_rare[i][j], brown_tags[i][j]))
    tuples_count = dict()
    for item in set(tuples):
        tuples_count[item] = 0
    for item in tuples:
        tuples_count[item] += 1
    tags_count = dict()
    for sentence in brown_tags:
        for item in sentence:
            tags_count[item] = 0
    for sentence in brown_tags:
        for item in sentence:
            tags_count[item] += 1
    e_values = {item: math.log(tuples_count[item]/float(tags_count[item[1]]) ,2) for item in tuples}
    taglist = set()
    for sen in brown_tags:
        for item in sen:
            taglist.add(item)
    return e_values, taglist

# This function takes the output from calc_emissions() and outputs it
def q4_output(e_values, filename):
    outfile = open(filename, "w")
    emissions = e_values.keys()
    emissions.sort()  
    for item in emissions:
        output = " ".join([item[0], item[1], str(e_values[item])])
        outfile.write(output + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# This function takes data to tag (brown_dev_words), a set of all possible tags (taglist), a set of all known words (known_words),
# trigram probabilities (q_values) and emission probabilities (e_values) and outputs a list where every element is a tagged sentence 
# (in the WORD/TAG format, separated by spaces and with a newline in the end, just like our input tagged data)
# brown_dev_words is a python list where every element is a python list of the words of a particular sentence.
# taglist is a set of all possible tags
# known_words is a set of all known words
# q_values is from the return of calc_trigrams()
# e_values is from the return of calc_emissions()
# The return value is a list of tagged sentences in the format "WORD/TAG", separated by spaces. Each sentence is a string with a 
# terminal newline, not a list of tokens. Remember also that the output should not contain the "_RARE_" symbol, but rather the
# original words of the sentence!
def viterbi(brown_dev_words, taglist, known_words, q_values, e_values):
    # Replace a word with RARE_SYMBOL when it is not in know_words
    def get_rare(word):
        if word in known_words:
            return word
        else:
            return RARE_SYMBOL

    # If the transition probability of a trigram doesn't exist, return LOG_PROB_OF_ZERO
    def get_q_values(trigram):
        try:
            return q_values[trigram]
        except KeyError:
            return LOG_PROB_OF_ZERO

    tagged = []
    taglist = list(taglist)
    N = len(taglist)
    # Get the index of NOUN in taglist
    noun = taglist.index('NOUN')
    #Get the index of START_SYMBOL in taglist
    start = taglist.index(START_SYMBOL)
    minus_inf = LOG_PROB_OF_ZERO * 100

    for words in brown_dev_words:
        T = len(words)
        viterbi_matrix = [[[minus_inf for _ in range(T)] for _ in range(N)] for _ in range(N)]
        backpointer = [[[noun for _ in range(T)] for _ in range(N)] for _ in range(N)]

        # Initialization step for first word
        word = get_rare(words[0])
        for s2 in range(N):
            try:
                viterbi_matrix[start][s2][0] = e_values[(word, taglist[s2])] + get_q_values((START_SYMBOL, START_SYMBOL, taglist[s2]))
            except KeyError:
                pass

        # Initialization step for second word
        word = get_rare(words[1])
        for s1 in range(N):
            for s2 in range(N):
                if viterbi_matrix[start][s1][0] == minus_inf:
                    continue
                try:
                    tmp = viterbi_matrix[start][s1][0] + e_values[(word, taglist[s2])] + get_q_values((START_SYMBOL, taglist[s1], taglist[s2]))
                    if tmp > viterbi_matrix[s1][s2][1]:
                        viterbi_matrix[s1][s2][1] = tmp
                except KeyError:
                    pass

        # Recursion step
        for t in range(2, T):
            word = get_rare(words[t])
            for s1 in range(N):
                for s2 in range(N):
                    for s in range(N):
                        if viterbi_matrix[s][s1][t - 1] == minus_inf:
                            continue
                        try:
                            tmp = viterbi_matrix[s][s1][t - 1] + e_values[(word, taglist[s2])] + get_q_values((taglist[s], taglist[s1], taglist[s2]))
                            if tmp > viterbi_matrix[s1][s2][t]:
                                viterbi_matrix[s1][s2][t] = tmp
                                backpointer[s1][s2][t] = s
                        except KeyError:
                            pass

        # Termination step
        viterbi_final = minus_inf
        for s1 in range(N):
            for s2 in range(N):
                if viterbi_matrix[s1][s2][T - 1] == minus_inf:
                    continue
                tmp = viterbi_matrix[s1][s2][T - 1] + get_q_values((taglist[s1], taglist[s2], STOP_SYMBOL))
                if tmp > viterbi_final:
                    viterbi_final = tmp
                    backpointer_final = (s1, s2)

        # Get the index of every word from backpointers 
        tags_num = [0 for _ in range(T)]
        i = T
        (s1, s2) = backpointer_final
        while i > 0:
            i -= 1
            tags_num[i] = s2
            tmp = backpointer[s1][s2][i]
            s2 = s1
            s1 = tmp

        sentence_output = words[0] + '/' + taglist[tags_num[0]]
        for i in range(1, T):
            sentence_output += (' ' + words[i] + '/' + taglist[tags_num[i]])
        sentence_output += '\n'
        tagged.append(sentence_output)
    return tagged

# This function takes the output of viterbi() and outputs it to file
def q5_output(tagged, filename):
    outfile = open(filename, 'w')
    for sentence in tagged:
        outfile.write(sentence)
    outfile.close()

# TODO: IMPLEMENT THIS FUNCTION
# This function uses nltk to create the taggers described in question 6
# brown_words and brown_tags is the data to be used in training
# brown_dev_words is the data that should be tagged
# The return value is a list of tagged sentences in the format "WORD/TAG", separated by spaces. Each sentence is a string with a 
# terminal newline, not a list of tokens. 
def nltk_tagger(brown_words, brown_tags, brown_dev_words):
    # Hint: use the following line to format data to what NLTK expects for training
    training = [ zip(brown_words[i],brown_tags[i]) for i in xrange(len(brown_words)) ]

    # IMPLEMENT THE REST OF THE FUNCTION HERE
    default_tagger = nltk.DefaultTagger('NOUN')
    bigram_tagger = nltk.BigramTagger(training, backoff=default_tagger)
    trigram_tagger = nltk.TrigramTagger(training, backoff=bigram_tagger)

    tagged = []
    for line in brown_dev_words:
        tuples = trigram_tagger.tag(line)
        output = tuples[0][0] + '/' + tuples[0][1]
        for i in tuples[1:]:
            output += (' ' + i[0] + '/' + i[1])
        output += '\n'
        tagged.append(output)
    return tagged

# This function takes the output of nltk_tagger() and outputs it to file
def q6_output(tagged, filename):
    outfile = open(filename, 'w')
    for sentence in tagged:
        outfile.write(sentence)
    outfile.close()

DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'

def main():
    # start timer
    time.clock()

    # open Brown training data
    infile = open(DATA_PATH + "Brown_tagged_train.txt", "r")
    brown_train = infile.readlines()
    infile.close()

    # split words and tags, and add start and stop symbols (question 1)
    brown_words, brown_tags = split_wordtags(brown_train)

    # calculate tag trigram probabilities (question 2)
    q_values = calc_trigrams(brown_tags)

    # question 2 output
    q2_output(q_values, OUTPUT_PATH + 'B2.txt')

    # calculate list of words with count > 5 (question 3)
    known_words = calc_known(brown_words)

    # get a version of brown_words with rare words replace with '_RARE_' (question 3)
    brown_words_rare = replace_rare(brown_words, known_words)

    # question 3 output
    q3_output(brown_words_rare, OUTPUT_PATH + "B3.txt")

    # calculate emission probabilities (question 4)
    e_values, taglist = calc_emission(brown_words_rare, brown_tags)

    # question 4 output
    q4_output(e_values, OUTPUT_PATH + "B4.txt")

    # delete unneceessary data
    del brown_train
    del brown_words_rare

    # open Brown development data (question 5)
    infile = open(DATA_PATH + "Brown_dev.txt", "r")
    brown_dev = infile.readlines()
    infile.close()

    # format Brown development data here
    brown_dev_words = []
    for sentence in brown_dev:
        brown_dev_words.append(sentence.split(" ")[:-1])

    # do viterbi on brown_dev_words (question 5)
    viterbi_tagged = viterbi(brown_dev_words, taglist, known_words, q_values, e_values)

    # question 5 output
    q5_output(viterbi_tagged, OUTPUT_PATH + 'B5.txt')

    # do nltk tagging here
    nltk_tagged = nltk_tagger(brown_words, brown_tags, brown_dev_words)

    # question 6 output
    q6_output(nltk_tagged, OUTPUT_PATH + 'B6.txt')

    # print total time to run Part B
    print "Part B time: " + str(time.clock()) + ' sec'

if __name__ == "__main__": main()
