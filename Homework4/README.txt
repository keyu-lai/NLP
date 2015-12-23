Name: Keyu Lai
UNI: kl2844

---------------------------------------------------------------------------------------------------------------------------
PART A

3)
Average AER for the first 50 sentences:
IBM Model 1: 0.665
IBM Model 2: 0.650

Model 2 outperforms Model 1 for 0.015. The reason is that model 1 assumes that all q(j|i,l,m)=1/(l+1), which is a uniform probability distribution over all l+1 possible words. However, it’s not always the case. Model 2 outperforms Model 1 because it doesn’t treat all the distortion parameters as uniform distribution.


Sentence pair:
[u'Ich', u'bitte', u'Sie', u',', u'sich', u'zu', u'einer', u'Schweigeminute', u'zu', u'erheben', u'.']
[u'Please', u'rise', u',', u'then', u',', u'for', u'this', u'minute', u"'", u's', u'silence', u'.']
Model 1:
0-1 1-1 2-1 3-4 4-10 5-10 6-10 7-10 8-10 9-1
Model 2:
0-0 1-1 2-0 3-2 4-10 5-10 6-10 7-7 8-10 9-0

In this example, model 1 performs with an error rate of 0.75, while model 2 performs with an error rate of 0.67.
I think this is because of the same reason mentioned above. Model 1 assumes that all q(j|i,l,m)=1/(l+1), which is a uniform probability distribution over all l+1 possible words. In contrast, model 2 doesn’t have this kind of assumption. At a result, Model 2 will take the positions of every English word and a German word, as well as the lengths of an English sentence and a German sentence, into account. This information will contribute a lot to the final performance.
Also, another reason is that model 1 initializes the transitions parameters with an uniform distributions. However, model 2 runs the model 1 to get the initializing transitions parameters. Based on the result of model 1, it will have a better performance.



4)
The model 1 achieves the lowest AER 0.626 in 6 iterations, and the model 2 archives the lowest AER 0.642 in 4 iterations. I expect that the two models will achieve a lowest AER in a larger number of iterations, since more iterations will allow the model parameters to better fit into the training data, and at last find convergence. I guess that it has something to do with our average strategy. Because we only examine the first average AER of the first 50 sentence and average them in a naive way, which could not reflect the AER of the whole system. 
However, the tendency of both models is pretty much what we expect. At first, the AER will decrease as the number of iterations increases. When it reaches a certain point, it finds the convergence and few improvement is made as the number of iterations increases. Model 1 begins to converge after 18 iterations, and model 2 begins to converge after 20 iterations. If we only looks that the AER with more than 10 iterations. Model 1 achieves the lowest AER in 40 iterations with an AER of 0.657, and Model 2 achieves the lowest AER in 20 iterations with an AER of 0.648.



---------------------------------------------------------------------------------------------------------------------------
PART B

4)
Average AER for the first 50 sentences:
Berkeley Aligner: 0.53

The Berkeley Aligner outperforms the IBM Model 2 for 0.12, which is big improvement. 


5)
[u'(', u'Das', u'Parlament', u'erhebt', u'sich', u'zu', u'einer', u'Schweigeminute', u'.', u')']
[u'(', u'The', u'House', u'rose', u'and', u'observed', u'a', u'minute', u"'", u's', u'silence', u')']
Model 1:
0-11 1-5 2-5 3-5 4-10 5-10 6-10 7-10 9-11
Model 2:
0-0 1-5 2-3 3-5 4-10 5-9 6-10 7-7 9-11
Berkeley Aligner(BA):
0-0 1-0 2-2 3-5 4-4 5-8 6-6 7-10 9-11

In this example, model 1 performs with an error rate of 0.75, while model 2 performs with an error rate of 0.67, and BA performs with an error rate of 0.2. In this example, the BA is a huge improvement. Compared with model 2, BA doesn’t introduce more parameters. However, it take into account the different training directions. Different issues may arise when two language going from two different ways. The BA addresses these issues by accommodate the parameters of the two models. Thus, it results in a more accurate fit of the training data.

