import re
import string
from nltk.corpus import stopwords

def process_tweet(tweet):
    # Conver to lower case
    tweet = tweet.lower()
    # Convert https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
    # Convert @username to AT_USER
    tweet = re.sub('@[^\s]+', 'AT_USER', tweet)
    # Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    # Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    # Remove stopwords
    tweet = ' '.join([word for word in tweet.split() if word not in (stopwords.words('english'))])
    # Remove words that contain digits
    tweet = ' '.join(s for s in tweet.split() if not any(c.isdigit() for c in s))
    # Remove hyphen
    tweet.replace('-', ' ').split(' ')
    # trim
    tweet = tweet.strip()
    # remove first/last " or 'at string end
    tweet = tweet.rstrip('\'"')
    tweet = tweet.lstrip('\'"')
    return tweet

def replaceTwoOrMore(tweet):
    # pattern to look for three or more repetitions of any character, including
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", tweet)

def remove_punctuation(tweet):
    tweet = tweet.translate(string.maketrans("", ""), string.punctuation)
    return tweet

def remove_emoticon(tweet):
    if not tweet:
        return tweet
    if not isinstance(tweet, basestring):
        return tweet
    try:
        # UCS-4
        patt = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    except re.error:
        # UCS-2
        patt = re.compile(
            u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
    return patt.sub('', tweet)