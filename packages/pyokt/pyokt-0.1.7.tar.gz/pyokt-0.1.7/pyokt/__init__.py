import jpype
from pyokt.util import init_jvm, load_okt, java_bool


class KoreanToken(object):
    def __init__(self, kt_java):
        self.text = kt_java.getText()
        self.pos = kt_java.getPos().name()
        self.offset = kt_java.getOffset()
        self.length = kt_java.getLength()
        self.unknown = kt_java.isUnknown()

    def __str__(self):
        return self.pos

    def __repr__(self):
        return '{}({}: {}, {})'.format(self.text, self.pos, self.offset, self.length)


class KoreanPhrase(object):
    def __init__(self, kp_scala):
        self.offset = kp_scala.offset()
        self.text = kp_scala.text()
        self.length = kp_scala.length()
        self.pos = kp_scala.pos()

    def __str__(self):
        return self.text

    def __repr__(self):
        return '{}({}: {}, {})'.format(self.text, self.pos, self.offset, self.length)


def normalize(text):
    okt = load_okt()
    return okt.normalize(text)


def tokenize(text, nomalize=False, stem=False):
    okt = load_okt()
    tokenized = okt.tokenize(text, java_bool(nomalize), java_bool(stem))

    return [KoreanToken(t) for t in tokenized]


def split_sentences(text):
    okt = load_okt()
    return list(okt.splitSentences(text))


def add_nouns_to_dictionary(nouns):
    okt = load_okt()
    okt.addNounsToDictionary(nouns)


def extract_phrases(text, filter_spam=True, add_hash_tags=True):
    okt = load_okt()
    phrases = okt.extractPhrases(text, java_bool(filter_spam), java_bool(add_hash_tags))

    return [KoreanPhrase(p) for p in phrases]


def close():
    jpype.shutdownJVM()
