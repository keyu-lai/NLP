1)
----------------------------------------------------------------------------------------------
b. 
For every arc in the dependency graph, the head and the dependent of a certain arc define an open range. If there is another arc with one end lying outside the range and the other end lying inside the range, then this dependency graph is not projective. Otherwise, this dependency graph is projective.
----------------------------------------------------------------------------------------------
c.
Projective:
Failure is not the end of the world.
Not Projective:
I saw him yesterday with his new laptop.
----------------------------------------------------------------------------------------------

2)
----------------------------------------------------------------------------------------------
b.
UAS: 0.229038040231 
LAS: 0.125473013344
The badfeatures.model uses only very few features to describe a configuration, which include FORM, FEATS and left/right dependencies of the top token in the stack and first token in the buffer. It lacks the necessary information to make a good prediction. For example, POS is needed to predict the dependency relationship. As a result, it has a bad performance.
----------------------------------------------------------------------------------------------

3)
----------------------------------------------------------------------------------------------
a. 
The features I added include:
POS of the top token in the stack
POS of the top token in the stack
POS of the second token in the buffer
FORM of the second token in the buffer
Number of left children of top token in the stack
Number of right children of top token in the stack
Number of left children of first token in the buffer
Number of right children of the first token in the buffer

POS:
POS is the part-of-speech tag of a certain word inside a sentence. This feature can be got from the "tag" field of a token inside a DependencyGraph class. Thus, it takes constant time to get this feature.
POSs contain information about the dependency relationship of two tokens. Furthemore, since the token on the top of stack and first token in the buffer are the two to be immediately manipulated, POSs of these two give a significant boost to both UAS and LAS.
The POS of the second token in the buffer is not the one to be directly manipulated in a certain step. Thus, its contribution to the performance is less than the other two POS features. But it also have a fair improvement on both UAS and LAS.

FORM:
FORM is the basic word(or the alphabetical form) of a token. This feature can be got from the "word" field of a token inside a DependencyGraph class. Thus, it takes constant time to get this feature.
FORM is the basic form of a token. Since the second token of the buffer is not that important as mentioned above, it has a fair contribution to the improvement of performance. Since it don't explicitly contain information about dependency relationship of two tokens. Its improvement to UAS is higher than that of LAS.

Number of left/right children:
This feature can be got from the "deps" field of a token inside a DependencyGraph class. The number of left children is the number of dependents with indices smaller than the token. In contrast, the number of right children the number of dependents with indices larger than it. Thus, it takes linear time, which is O(n), to get this feature.
The number of left/right children contains information about a token's function in a sentence. Also, the tokens we choose are the ones to be immediately manipulated in a step. Thus, these features have a significant contribution on the performance of the system.
----------------------------------------------------------------------------------------------
c.
Swedish
UAS: 0.887870942043 
LAS: 0.750049790878

Danish
UAS: 0.871856287425 
LAS: 0.778443113772
----------------------------------------------------------------------------------------------
d. 
The arc-eager shift-reduce parser trains a classifier to predict the best transition given a certain configuration. Then a greedy deterministic procedure is applied to derive the dependency graph. Thus, it results in linear-time parsing provided that each transition can be predicted and executed in constant time. 
The arc-eager shift-reduce parser employs a greedy strategy, which make it among the most efficient systems available for syntactic parsing. However, It's efficiency comes with the sacrifice of performance. It prediction is only based on a certain configuration, which make it inherently suffer from prediction errors and subsequent error propagation.
----------------------------------------------------------------------------------------------



