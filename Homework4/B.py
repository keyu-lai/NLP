import nltk
import A
from collections import defaultdict
from nltk.align import AlignedSent
from nltk.align import Alignment

class BerkeleyAligner():

    def __init__(self, align_sents, num_iter):
        self.t, self.q = self.train(align_sents, num_iter)

    # TODO: Computes the alignments for align_sent, using this model's parameters. Return
    #       an AlignedSent object, with the sentence pair and the alignments computed.
    def align(self, aligned_sent):

        best_alignment = []
        out_sent = AlignedSent(aligned_sent.words, aligned_sent.mots)
        l = len(aligned_sent.mots)
        m = len(aligned_sent.words)

        for i, t_word in enumerate(aligned_sent.words):
            best_prob = (self.t[t_word][None] * self.q[0][i + 1][l][m])
            best_alig = None

            for j, s_word in enumerate(aligned_sent.mots):
                alig_prob = (self.t[t_word][s_word] * self.q[j + 1][i + 1][l][m])
                if alig_prob > best_prob:
                    best_prob = alig_prob
                    best_alig = j

            if best_alig != None:
                best_alignment.append((i, best_alig))

        out_sent.alignment = Alignment(best_alignment)
        return out_sent
    
    # TODO: Implement the EM algorithm. num_iters is the number of iterations. Returns the 
    # translation and distortion parameters as a tuple.
    def train(self, aligned_sents, num_iters):

        transitions_f = defaultdict(lambda: defaultdict(lambda: 0.0))
        distortions_f = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0))))

        transitions_b = defaultdict(lambda: defaultdict(lambda: 0.0))
        distortions_b = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0))))

        # initilize the transition table
        En_words = set()
        Ge_words = set()

        for aligned_sent in aligned_sents:
            En_words.update(aligned_sent.mots)
            Ge_words.update(aligned_sent.words)

        En_words.add(None);

        En_words = list(En_words)
        Ge_words = list(Ge_words)

        transitions_f, transitions_b = self._train_ibm1(aligned_sents, num_iters, En_words, Ge_words)

        # initilize the alignment table
        for aligned_sent in aligned_sents:

            l = len(aligned_sent.mots)
            m = len(aligned_sent.words)

            initial_value_f = 1.0 / (l + 1)
            initial_value_b = 1.0 / m
            for i in range(1, m + 1):
                for j in range(0, l + 1):
                    distortions_f[j][i][l][m] = initial_value_f
                    distortions_b[i][j][m][l] = initial_value_b

        # actual training
        for _ in range(num_iters):

            count_t_given_s_f = defaultdict(lambda: defaultdict(lambda: 0.0))
            count_any_t_given_s_f = defaultdict(lambda: 0.0)
            alignment_count_f = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0))))
            alignment_count_for_any_j_f = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

            count_t_given_s_b = defaultdict(lambda: defaultdict(lambda: 0.0))
            count_any_t_given_s_b = defaultdict(lambda: 0.0)
            alignment_count_b = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0))))
            alignment_count_for_any_j_b = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

            for aligned_sent in aligned_sents:

                En_sent = [None] + aligned_sent.mots
                Ge_sent = ['UNUSED'] + aligned_sent.words

                l = len(aligned_sent.mots) 
                m = len(aligned_sent.words)

                total_count_f = defaultdict(lambda: 0.0)
                total_count_b = defaultdict(lambda: 0.0)

                # E step
                for i in range(1, m + 1):
                    t = Ge_sent[i]
                    total_count_f[i] = 0.0
                    for j in range(0, l + 1):
                        s = En_sent[j]
                        total_count_f[i] += transitions_f[t][s] * distortions_f[j][i][l][m]
                        total_count_b[j] += transitions_b[s][t] * distortions_b[i][j][m][l]

                for i in range(1, m + 1):
                    t = Ge_sent[i]
                    for j in range(0, l + 1):
                        s = En_sent[j]
                        count_f = transitions_f[t][s] * distortions_f[j][i][l][m]
                        count_b = transitions_b[s][t] * distortions_b[i][j][m][l]
                        normalized_count_f = count_f / total_count_f[i]
                        normalized_count_b = count_b / total_count_b[j]
                        count_t_given_s_f[t][s] += normalized_count_f
                        count_any_t_given_s_f[s] += normalized_count_f
                        alignment_count_f[j][i][l][m] += normalized_count_f
                        alignment_count_for_any_j_f[i][l][m] += normalized_count_f
                        count_t_given_s_b[s][t] += normalized_count_b
                        count_any_t_given_s_b[t] += normalized_count_b
                        alignment_count_b[i][j][m][l] += normalized_count_b
                        alignment_count_for_any_j_b[j][m][l] += normalized_count_b

            # M step:
            for t in Ge_words:
                for s in En_words:
                    transitions_f[t][s] = (count_t_given_s_f[t][s] + count_t_given_s_b[s][t]) / (count_any_t_given_s_f[s] + count_any_t_given_s_b[t])
                    transitions_b[s][t] = transitions_f[t][s]

            for aligned_sent in aligned_sents:

                l = len(aligned_sent.mots)
                m = len(aligned_sent.words)

                for j in range(0, l + 1):
                    for i in range(1, m + 1):
                        distortions_f[j][i][l][m] = (alignment_count_f[j][i][l][m] + alignment_count_b[i][j][m][l]) / (alignment_count_for_any_j_f[i][l][m] + alignment_count_for_any_j_b[j][m][l])
                        distortions_b[i][j][m][l] = distortions_f[j][i][l][m]

        return (transitions_f, distortions_f)

    def _train_ibm1(self, aligned_sents, num_iters, En_words, Ge_words):

        transitions_f = defaultdict(lambda: defaultdict(lambda: 0.0))
        transitions_b = defaultdict(lambda: defaultdict(lambda: 0.0))

        init_prob_f = 1.0 / len(En_words)
        init_prob_b = 1.0 / len(Ge_words)
        for t in Ge_words:
            for s in En_words:
                transitions_f[t][s] = init_prob_f
                transitions_b[s][t] = init_prob_b

        # actual training
        for _ in range(num_iters):

            count_t_given_s_f = defaultdict(lambda: defaultdict(lambda: 0.0))
            count_any_t_given_s_f = defaultdict(lambda: 0.0)

            count_t_given_s_b = defaultdict(lambda: defaultdict(lambda: 0.0))
            count_any_t_given_s_b = defaultdict(lambda: 0.0)

            for aligned_sent in aligned_sents:

                En_sent = [None] + aligned_sent.mots
                Ge_sent = ['UNUSED'] + aligned_sent.words

                l = len(aligned_sent.mots) 
                m = len(aligned_sent.words)

                total_count_f = defaultdict(lambda: 0.0)
                total_count_b = defaultdict(lambda: 0.0)

                # E step
                for i in range(1, m + 1):
                    t = Ge_sent[i]
                    total_count_f[i] = 0.0
                    for j in range(0, l + 1):
                        s = En_sent[j]
                        total_count_f[i] += transitions_f[t][s]
                        total_count_b[j] += transitions_b[s][t]

                for i in range(1, m + 1):
                    t = Ge_sent[i]
                    for j in range(0, l + 1):
                        s = En_sent[j]
                        normalized_count_f = transitions_f[t][s] / total_count_f[i]
                        normalized_count_b = transitions_b[s][t] / total_count_b[j]
                        count_t_given_s_f[t][s] += normalized_count_f
                        count_any_t_given_s_f[s] += normalized_count_f
                        count_t_given_s_b[s][t] += normalized_count_b
                        count_any_t_given_s_b[t] += normalized_count_b

            # M step:
            for t in Ge_words:
                for s in En_words:
                    transitions_f[t][s] = count_t_given_s_f[t][s] / count_any_t_given_s_f[s]
                    transitions_b[s][t] = count_t_given_s_b[s][t] / count_any_t_given_s_b[t]

        return transitions_f, transitions_b

def main(aligned_sents):
    ba = BerkeleyAligner(aligned_sents, 10)
    A.save_model_output(aligned_sents, ba, "ba.txt")
    avg_aer = A.compute_avg_aer(aligned_sents, ba, 50)

    print ('Berkeley Aligner')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))
