# pyokt
[open-korean-text](https://github.com/open-korean-text/open-korean-text) wrapper for python

### Install

``` sh
pip install pyokt
```

For windows users: Please install appropriate jpype1 wheel from [http://www.lfd.uci.edu/~gohlke/pythonlibs/](http://www.lfd.uci.edu/~gohlke/pythonlibs/)

### Example

``` python
import pyokt

text = "나는 집에 가서 잠을 자고 싶어. 너도 그러닠ㅋㅋㅋㅋㅋㅋㅋ"

# Normalization
pyokt.normalize(text)
>>> 나는 집에 가서 잠을 자고 싶어. 너도 그러니ㅋㅋㅋ

# Tokenization
pyokt.tokenize(text, nomalize=True, stem=True)
>>> [나(Noun: 0, 1), 는(Josa: 1, 1),  (Space: 2, 1), 집(Noun: 3, 1), 에(Josa: 4, 1),  (Space: 5, 1), 가다(Verb: 6, 2),  (Space: 8, 1), 잠(Noun: 9, 1), 을(Josa: 10, 1),  (Space: 11, 1), 자고(Noun: 12, 2),  (Space: 14, 1), 싶다(Verb: 15, 2), .(Punctuation: 17, 1),  (Space: 18, 1), 너(Noun: 19, 1), 도(Josa: 20, 1),  (Space: 21, 1), 그렇다(Adjective: 22, 3), ㅋㅋㅋ(KoreanParticle: 25, 3)]

# Split sentences
pyokt.split_sentences(text)
>>> ['나는 집에 가서 잠을 자고 싶어.', '너도 그러닠ㅋㅋㅋㅋㅋㅋㅋ']

# Add nouns to the dictionary
pyokt.tokenize("군단숙주가 나타났다")
>>> [군단(Noun: 0, 2), 숙주(Noun: 2, 2), 가(Josa: 4, 1),  (Space: 5, 1), 나타났다(Verb: 6, 4)]
pyokt.add_nouns_to_dictionary(['군단숙주'])
pyokt.tokenize("군단숙주가 나타났다")
>>> [군단숙주(Noun: 0, 4), 가(Josa: 4, 1),  (Space: 5, 1), 나타났다(Verb: 6, 4)]

# Phrase extraction
pyokt.extract_phrases("깊은 잠에 빠지고 말았다.")
>>> [깊은 잠(Noun: 0, 4)]
