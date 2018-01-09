import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer


# unigram, bigram, trigram etc.
def ngrams(tweet, n):
  tweet = tweet.split(' ')
  ngramVector = []
  for i in range(len(tweet)-n+1):
      ngramVector.append(tweet[i:i+n])
  return ngramVector

# pos tagging for unigrams
def pos_tag(tweet):
    tweet = nltk.word_tokenize(tweet)
    pos = nltk.pos_tag(tweet)
    return pos

def stemming(tweet):
    stemmer = SnowballStemmer("english")
    stemmed_text = [stemmer.stem(i) for i in word_tokenize(tweet)]
    return stemmed_text

def lemmatizing(tweet):
    lmtzr = WordNetLemmatizer()
    lemmatized_text = [lmtzr.lemmatize(i) for i in word_tokenize(tweet)]
    return lemmatized_text
