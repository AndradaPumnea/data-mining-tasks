# http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/
import time

import classifier
import inverted_index
from inv_index_dataset import inv

inv_test=["i love dudette bess",  "i love liz", "i love mark", 'you hate hitler']

def test_query_fancy():
    inverted_index.create_index(inv_test)
    print inverted_index.process_query("love and dudette and not mark")

def main():
    # ngram, classifier, feat_reduct, dup_letter, remove_punct
    clf=1
    print "SENTIMENT ANALYSIS"
    print "no preprocessing"
    classifier.run_classifier(1,clf, False, False, False)
    classifier.run_classifier(2, clf, False, False, False)
    classifier.run_classifier(12, clf, False, False, False)
    classifier.run_classifier(3, clf, False, False, False)

    print "preprocessing"
    classifier.run_classifier(1, clf, True, False, False)
    classifier.run_classifier(2, clf, True, False, False)
    classifier.run_classifier(12, clf, True, False, False)
    classifier.run_classifier(3, clf, True, False, False)

    print "repeated letters"
    classifier.run_classifier(1, clf, False, True, False)
    classifier.run_classifier(2, clf, False, True, False)
    classifier.run_classifier(12, clf, False, True, False)
    classifier.run_classifier(3, clf, False, True, False)

    print "pre+rep lett"
    classifier.run_classifier(1, clf, True, True, False)
    classifier.run_classifier(2, clf, True, True, False)
    classifier.run_classifier(12, clf, True, True, False)
    classifier.run_classifier(3, clf, True, True, False)

    print "punctuation"
    classifier.run_classifier(1, clf, False, False, True)
    classifier.run_classifier(2, clf, False, False, True)
    classifier.run_classifier(12, clf, False, False, True)
    classifier.run_classifier(3, clf, False, False, True)

    print "pre+punct"
    classifier.run_classifier(1, clf, True, False, True)
    classifier.run_classifier(2, clf, True, False, True)
    classifier.run_classifier(12, clf, True, False, True)
    classifier.run_classifier(3, clf, True, False, True)

    print "pre+rep.let+punct"
    classifier.run_classifier(1, clf, True, True, True)
    classifier.run_classifier(2, clf, True, True, True)
    classifier.run_classifier(12, clf, True, True, True)
    classifier.run_classifier(3, clf, True, True, True)

    print "INVERTED INDEX"
    start = time.time()
    inverted_index.create_index(inv)
    end = time.time()
    print("Build index:" + str(end - start))

    start = time.time()
    inverted_index.process_query("hate")
    end = time.time()
    print("Basic search:" + str(end - start))

    start = time.time()
    inverted_index.process_query("library and book")
    end = time.time()
    print("AND query:" + str(end - start))

    start = time.time()
    inverted_index.process_query("library or book")
    end = time.time()
    print("OR query:" + str(end - start))

    start = time.time()
    inverted_index.process_query("library and not book")
    end = time.time()
    print("AND NOT query:" + str(end - start))

    start = time.time()
    inverted_index.process_query("library or not book")
    end = time.time()
    print("OR NOT query:" + str(end - start))

    start = time.time()
    inverted_index.process_query("library or engineering and not book")
    end = time.time()
    print("Sophisticated query:" + str(end - start))

    inverted_index.create_index(inv)
    inverted_index.process_query("hate and work or go")
    test_query_fancy()




