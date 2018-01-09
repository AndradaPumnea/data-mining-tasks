import nltk
import sklearn
import feature_reduction
from sklearn import svm
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.model_selection import train_test_split

from positive_dataset import pos_sent
from negative_dataset import neg_sent

def prepare_sets(feat_reduct, dup_letter,remove_punct):
    data = []
    target = []
    for row in pos_sent:
        if row[0] and row[1]:
            if feat_reduct == True:
                lst = list(row)
                lst[0] = feature_reduction.process_tweet(row[0])
                row = tuple(lst)
            if dup_letter == True:
                lst = list(row)
                lst[0] = feature_reduction.replaceTwoOrMore(row[0])
                row = tuple(lst)
            if remove_punct == True:
                lst = list(row)
                lst[0] = feature_reduction.remove_punctuation(row[0])
                row = tuple(lst)
            data.append(row[0])
            target.append(row[1])
    for row in neg_sent:
        if row[0] and row[1]:
            if feat_reduct == True:
                lst = list(row)
                lst[0] = feature_reduction.process_tweet(row[0])
                row = tuple(lst)
            if dup_letter == True:
                lst = list(row)
                lst[0] = feature_reduction.replaceTwoOrMore(row[0])
                row = tuple(lst)
            if remove_punct == True:
                lst = list(row)
                lst[0] = feature_reduction.remove_punctuation(row[0])
                row = tuple(lst)
            data.append(row[0])
            target.append(row[1])
    return data, target

stemmer = nltk.SnowballStemmer("english")
analyzer = CountVectorizer().build_analyzer()

def stemmed_words(doc):
    stemmed_text=[stemmer.stem(w) for w in analyzer(doc)]
    ngramVector = []
    for i in range(len(stemmed_text) - 2 + 1):
        ngramVector.append(stemmed_text[i:i + 2])
    return ngramVector

def ngram_preprocess(n,feat_reduct, dup_letter,remove_punct):
    data, target = prepare_sets(feat_reduct, dup_letter,remove_punct)
    if n==1:
        count_vectorizer = CountVectorizer(min_df=1, stop_words='english')
    elif n==2:
        count_vectorizer = CountVectorizer(analyzer='char_wb', ngram_range=(2, 2), min_df=1, stop_words='english')
    elif n==3:
        count_vectorizer = CountVectorizer(analyzer='char_wb', ngram_range=(3, 3), min_df=1, stop_words='english')
    elif n==12:
        count_vectorizer = CountVectorizer(ngram_range=(1, 2), token_pattern=r'\b\w+\b', min_df=1, stop_words='english')
    data = count_vectorizer.fit_transform(data)
    tfidf_data = TfidfTransformer(use_idf=False).fit_transform(data)
    return tfidf_data

def evaluate_model(target_true,target_predicted):
    print classification_report(target_true,target_predicted)
    print "The accuracy score is {:.2%}".format(accuracy_score(target_true,target_predicted))

def cross_validate_model(model, data_train, target_train):
    seed = 7
    kfold = sklearn.model_selection.KFold(n_splits=10, random_state=seed)
    scoring = 'accuracy'
    results = sklearn.model_selection.cross_val_score(model, data_train, target_train, cv=kfold, scoring=scoring)
    print("%.3f %.3f") % (results.mean()*100, results.std()*100)

def learn_model(data,target,x):
    # preparing data for split validation. 60% training, 20% test
    data_train,data_test,target_train,target_test = train_test_split(data,target,test_size=0.2,random_state=43)

    if (x == 1):
        classifier = BernoulliNB().fit(data_train,target_train)
    elif (x == 2):
        classifier = MultinomialNB().fit(data_train, target_train)
    elif (x == 3):
        classifier = RandomForestClassifier().fit(data_train, target_train)
    elif (x == 4):
        classifier =  AdaBoostClassifier().fit(data_train, target_train)
    elif (x == 5):
        classifier = svm.LinearSVC().fit(data_train, target_train)
    predicted = classifier.predict(data_test)
    #evaluate_model(target_test, predicted)
    cross_validate_model(classifier, data_train, target_train)

def run_classifier(n,x, feat_reduct, dup_letter,remove_punct):
    data,target = prepare_sets(feat_reduct, dup_letter,remove_punct)
    tf_idf = ngram_preprocess(n, feat_reduct, dup_letter,remove_punct)
    learn_model(tf_idf,target,x)

