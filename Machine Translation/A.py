import nltk
from nltk.align import AlignedSent
from nltk.align import IBMModel1
from nltk.align import IBMModel2

# TODO: Initialize IBM Model 1 and return the model.
def create_ibm1(aligned_sents):

    return IBMModel1(aligned_sents, 10)

# TODO: Initialize IBM Model 2 and return the model.
def create_ibm2(aligned_sents):

    return IBMModel2(aligned_sents, 10)

# TODO: Compute the average AER for the first n sentences
#       in aligned_sents using model. Return the average AER.
def compute_avg_aer(aligned_sents, model, n):

    avg_aer = 0
    weights = 0

    for aligned_sent in aligned_sents[:50]:

        sent = model.align(aligned_sent)
        avg_aer += aligned_sent.alignment_error_rate(sent)

    avg_aer /= 50
    return avg_aer

# TODO: Computes the alignments for the first 20 sentences in
#       aligned_sents and saves the sentences and their alignments
#       to file_name. Use the format specified in the assignment.
def save_model_output(aligned_sents, model, file_name):

    file = open(file_name, 'w')

    for aligned_sent in aligned_sents[:20]:

        sent = model.align(aligned_sent)
        file.write(str(sent.words) + '\n')
        file.write(str(sent.mots) + '\n')
        file.write(str(sent.alignment) + '\n')
        file.write('\n')

    file.close()

def main(aligned_sents):
    ibm1 = create_ibm1(aligned_sents)
    save_model_output(aligned_sents, ibm1, "ibm1.txt")
    avg_aer = compute_avg_aer(aligned_sents, ibm1, 50)

    print ('IBM Model 1')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))

    ibm2 = create_ibm2(aligned_sents)
    save_model_output(aligned_sents, ibm2, "ibm2.txt")
    avg_aer = compute_avg_aer(aligned_sents, ibm2, 50)
    
    print ('IBM Model 2')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))
