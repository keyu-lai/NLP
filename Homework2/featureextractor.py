from nltk.compat import python_2_unicode_compatible

printed = False

@python_2_unicode_compatible
class FeatureExtractor(object):
    @staticmethod
    def _check_informative(feat, underscore_is_informative=False):
        """
        Check whether a feature is informative
        """

        if feat is None:
            return False

        if feat == '':
            return False

        if not underscore_is_informative and feat == '_':
            return False

        return True

    @staticmethod
    def find_left_right_dependencies(idx, arcs):
        left_most = 1000000
        right_most = -1
        dep_left_most = ''
        dep_right_most = ''
        for (wi, r, wj) in arcs:
            if wi == idx:
                if (wj > wi) and (wj > right_most):
                    right_most = wj
                    dep_right_most = r
                if (wj < wi) and (wj < left_most):
                    left_most = wj
                    dep_left_most = r
        return dep_left_most, dep_right_most

    @staticmethod
    def extract_features(tokens, buffer, stack, arcs):
        """
        This function returns a list of string features for the classifier

        :param tokens: nodes in the dependency graph
        :param stack: partially processed words
        :param buffer: remaining input words
        :param arcs: partially built dependency tree

        :return: list(str)
        """

        """
        Think of some of your own features here! Some standard features are
        described in Table 3.2 on page 31 of Dependency Parsing by Kubler,
        McDonald, and Nivre

        [http://books.google.com/books/about/Dependency_Parsing.html?id=k3iiup7HB9UC]
        """
        # Number of left/right children of a certain token
        def left_right_children(node):
            left_children = 0
            right_children = 0
            index = node['address']
            children = node['deps']
            for i in children:
                for j in children[i]:
                    if j < index:
                        left_children = left_children + 1
                    elif j > index:
                        right_children = right_children + 1
            return left_children, right_children

        result = []

        if stack:
            stack_idx0 = stack[-1]
            token = tokens[stack_idx0]
            if FeatureExtractor._check_informative(token['word'], True):
                result.append('STK_0_FORM_' + token['word'])

            if 'tag' in token and FeatureExtractor._check_informative(token['tag'], True):
                result.append('STK_0_POSTAG_' + token['tag'])

            if 'feats' in token and FeatureExtractor._check_informative(token['feats']):
                feats = token['feats'].split("|")
                for feat in feats:
                    result.append('STK_0_FEATS_' + feat)

            # Left most, right most dependency of stack[0]
            dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(stack_idx0, arcs)

            if FeatureExtractor._check_informative(dep_left_most):
                result.append('STK_0_LDEP_' + dep_left_most)
            if FeatureExtractor._check_informative(dep_right_most):
                result.append('STK_0_RDEP_' + dep_right_most)

            left_children, right_children = left_right_children(token)
            result.append('STK_0_LCHD_' + str(left_children))
            result.append('STK_0_RCHD_' + str(right_children))

        if buffer:
            buffer_idx0 = buffer[0]
            token = tokens[buffer_idx0]
            if FeatureExtractor._check_informative(token['word'], True):
                result.append('BUF_0_FORM_' + token['word'])

            if 'tag' in token and FeatureExtractor._check_informative(token['tag'], True):
                result.append('BUF_0_POSTAG_' + token['tag'])

            if 'feats' in token and FeatureExtractor._check_informative(token['feats']):
                feats = token['feats'].split("|")
                for feat in feats:
                    result.append('BUF_0_FEATS_' + feat)

            dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(buffer_idx0, arcs)

            if FeatureExtractor._check_informative(dep_left_most):
                result.append('BUF_0_LDEP_' + dep_left_most)
            if FeatureExtractor._check_informative(dep_right_most):
                result.append('BUF_0_RDEP_' + dep_right_most)

            left_children, right_children = left_right_children(token)
            result.append('BUF_0_LCHD_' + str(left_children))
            result.append('BUF_0_RCHD_' + str(right_children))

            if len(buffer) > 1:
                buffer_idx1 = buffer[1] 
                token = tokens[buffer_idx1]
                if 'word' in token and FeatureExtractor._check_informative(token['word'], True):
                    result.append('BUF_1_FORM_' + token['word'])
                if 'tag' in token and FeatureExtractor._check_informative(token['tag'], True):
                    result.append('BUF_1_POSTAG_' + token['tag'])

        return result
