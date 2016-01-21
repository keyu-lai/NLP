import sys
from providedcode.transitionparser import TransitionParser
from providedcode.evaluate import DependencyEvaluator
from featureextractor import FeatureExtractor
from providedcode.dependencygraph import DependencyGraph
from transition import Transition

if __name__ == '__main__':
	sentences = []
	try:
		while 1:
			sentence = raw_input().strip()
			sentences.append(DependencyGraph.from_sentence(sentence))
	except EOFError:
		pass

	tp = TransitionParser.load(sys.argv[1])
	parsed = tp.parse(sentences)

	for p in parsed:
		print p.to_conll(10).encode('utf-8')