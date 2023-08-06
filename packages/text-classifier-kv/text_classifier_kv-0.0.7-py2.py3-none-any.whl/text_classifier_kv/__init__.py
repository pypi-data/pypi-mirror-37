from typing import Dict, List, Tuple, Callable
import re
import math
import string


def getwords_std(doc: str) -> Dict[str, int]:
    '''transform text to Dict of uniq words (standart algorythm)'''
    splitter = re.compile('\\W*')
    words: List[str] = []
    for s in splitter.split(doc):
        if len(s) > 2 and len(s) < 20:
            words.append(s.lower())
    return dict([(w, 1) for w in words])


def _delete_punctuation_marks(text: str) -> str:
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator).replace('’', '')


def getwords(text: str) -> Dict[str, int]:
    '''transform text to Dict of uniq words'''
    wc: Dict[str, int] = {}
    text = _delete_punctuation_marks(text).lower()
    for word in text.split(' '):
        if len(word.strip()) > 0:
            wc.setdefault(word, 0)
            wc[word] += 1

    return wc


def generate_text_vector(
    text_list: List[str],
    min_frequency: float=0.1,
    max_frequency: float=0.5,
    getfeatures: Callable[[str], Dict[str, int]] = getwords
) -> Callable[[str], Dict[str, int]]:
    '''
    Get a Dict of words from array of text between max and mix frequency
    '''
    text_list_len: int = len(text_list)
    text_vector: List[str] = []
    # Dict of uniq words for each text
    apcount: Dict[str, int] = {}

    for text in text_list:
        for word, count in getfeatures(text).items():
            apcount.setdefault(word, 0)
            if count > 1:
                apcount[word] += 1

    # Dict of uniq words for all texts
    # all words are between max and mix frequency
    for word, count in apcount.items():
        frac = float(count) / text_list_len
        if frac > min_frequency and frac < max_frequency:
            text_vector.append(word)

    def get_match_words(text: str) -> Dict[str, int]:
        new_dict: Dict[str, int] = {}
        for text, i in getfeatures(text).items():
            if text in text_vector:
                new_dict[text] = i

        return new_dict
    return get_match_words


class classifier:
    '''class for abstract classifier'''

    def __init__(
        self,
        getfeatures: Callable[[str], Dict[str, int]] = getwords
    ) -> None:
        # feachers Dict { word: {category: :number} }
        self.fc: Dict[str, Dict[str, int]] = {}
        # Dict { category: :number of documents }
        self.cc: Dict[str, int] = {}
        self.getfeatures = getfeatures

    def incf(self, word: str, category: str) -> None:
        '''increase feachers Dict for word in category'''
        self.fc.setdefault(word, {})
        self.fc[word].setdefault(category, 0)
        self.fc[word][category] += 1
        return None

    def incc(self, category: str) -> None:
        '''increase categories Dict'''
        self.cc.setdefault(category, 0)
        self.cc[category] += 1
        return None

    def fcount(self, word: str, category: str) -> float:
        '''how many time the word appears in the category'''
        if word in self.fc and category in self.fc[word]:
            return float(self.fc[word][category])
        return 0.0

    def catcount(self, category: str) -> float:
        '''how many documents in the category?'''
        if category in self.cc:
            return float(self.cc[category])
        return 0.0

    def totalcount(self) -> int:
        '''total count of documents'''
        return sum(self.cc.values())

    def categories(self) -> List[str]:
        '''total count of categories'''
        return list(self.cc.keys())

    def train(self, text: str, category: str) -> None:
        '''
        train classifier

        Algorithm:
        1) Transform text to Dict if uniq words
        2) Increase values in Dict of feactures and Dict of categories
        '''
        words_dict: Dict[str, int] = self.getfeatures(text)
        for word in words_dict:
            self.incf(word, category)
        self.incc(category)
        return None

    def fprob(self, word: str, category: str) -> float:
        '''
        find probability after train

        Algorithm:
        1) Take a number how many documents in the category
        2) Set A - how many documents in the category
        3) Set B - hot many times the words appears in the category
        4) Divive A by B
        '''
        cc: float = self.catcount(category)
        if cc == 0:
            return 0.0
        return self.fcount(word, category) / cc

    def weightedprob(
        self,
        word: str,
        category: str,
        prf: Callable[[str, str], float],
        weight: float = 1.0,
        ap: float = 0.5
    ) -> float:
        '''
        find probability for word with weight. use it after train

        Algorithm:
        1) Call .fprob
        2) Find sum of .fcount for all categories
        3) Calculate avegare value
        '''
        basicprob = prf(word, category)
        totals = sum([self.fcount(word, c) for c in self.categories()])
        bp = ((weight*ap)+(totals*basicprob)) / (weight+totals)
        return bp


class naivebayes(classifier):
    '''class for Naive Bayes classifier'''

    def __init__(
        self,
        getfeatures: Callable[[str], Dict[str, int]] = getwords
    ) -> None:
        classifier.__init__(self, getfeatures)
        self.thresholds: Dict[str, float] = {}

    def setthreshold(self, category: str, t: float) -> None:
        '''set thresholds for a category'''
        self.thresholds[category] = t
        return None

    def getthreshold(self, category: str) -> float:
        '''get thresholds for a category'''
        if category not in self.thresholds:
            # default value
            return 1.0
        return self.thresholds[category]

    def classify(self, item: str, default: str = 'unknown') -> str:
        '''classify with getthreshold'''
        probs: Dict[str, float] = {}
        # find category with max probability
        max: float = 0.0
        best: str = ''
        for category in self.categories():
            probs[category] = self.prob(item, category)
            if probs[category] > max:
                max = probs[category]
                best = category
        # Check probability is bigger than threshold * next one
        for cat in probs:
            if cat == best:
                continue
            if probs[cat] * self.getthreshold(best) > probs[best]:
                return default
        return best

    def docprob(self, text: str, category: str) -> float:
        '''probability: Pr(document | category)'''
        features = self.getfeatures(text)
        # multiply the probability for all words
        p: float = 1.0
        for word in features:
            p *= self.weightedprob(word, category, self.fprob)
        return p

    def prob(self, text: str, category: str) -> float:
        '''
        calculate probability for the category and return:
        Pr(document | category) times Pr(category)
        '''
        if self.totalcount() == 0:
            return 0.0
        catprob: float = self.catcount(category) / self.totalcount()
        docprob: float = self.docprob(text, category)
        return docprob * catprob


class fisherclassifier(classifier):
    '''class for Fisher classifier'''

    def __init__(
        self,
        getfeatures: Callable[[str], Dict[str, int]] = getwords
    ) -> None:
        classifier.__init__(self, getfeatures)
        self.minimums: Dict[str, float] = {}

    def setminimum(self, category: str, min: float) -> None:
        '''set minimum for the category'''
        self.minimums[category] = min
        return None

    def getminimum(self, category: str) -> float:
        '''get minimum for the category'''
        if category not in self.minimums:
            return 0
        return self.minimums[category]

    def cprob(self, word: str, category: str) -> float:
        '''probability for the word and the category'''
        clf: float = self.fprob(word, category)
        if clf == 0:
            return 0.0
        # sum of probabilities for all categories
        freqsum: float = sum([self.fprob(word, c) for c in self.categories()])
        # cprob is probability divided by sum of probabilities for all categories
        if freqsum == 0:
            return 0
        else:
            return clf/(freqsum)

    def fisherprob(self, text: str, category: str) -> float:
        '''
        Fisher probability for the word and the category
        '''
        p: float = 1.0
        features = self.getfeatures(text)
        for word in features:
            p *= (self.weightedprob(word, category, self.cprob))
        fscore = -2 * math.log(p)
        return self.invchi2(fscore, len(features) * 2)

    def invchi2(self, chi: float, df: int) -> float:
        '''Chi-squared distribution'''
        m = chi / 2.0
        sum = term = math.exp(-m)
        for i in range(1, df//2):
            term *= m / i
            sum += term
        return min(sum, 1.0)

    def classify(self, item: str, default: str='unknown') -> str:
        '''find best result'''
        best: str = default
        max: float = 0.0
        for c in self.categories():
            p = self.fisherprob(item, c)
            if p > self.getminimum(c) and p > max:
                best = c
                max = p
        return best
