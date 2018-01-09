import csv
from collections import defaultdict

import nltk
import unicodedata

import feature_reduction
import preprocessing

reserved = ['not','and', 'or']
dict = {}

def create_index(data):
    for i, tokens in enumerate(data):
        tokens = preprocess(tokens)
        for token in tokens:
            if token in dict.keys():
                dict.get(token).append(i)
            else:
                dict[token] = [i]
    write_file("indexed.csv", dict)
    return dict

def write_file(file_name, dict):
        with open(file_name, "w") as csvfile:
            writer = csv.writer(csvfile, delimiter=":")
            for key, value in dict.items():
                writer.writerow([key, '->'.join(str(x) for x in value)])

def preprocess(text):
    text = feature_reduction.process_tweet(text)
    text = feature_reduction.remove_punctuation(text)
    text = feature_reduction.remove_emoticon(text)
    text = feature_reduction.replaceTwoOrMore(text)
    text = preprocessing.stemming(text)
    return text

def get_operators(expr):
    operators = []
    expr = nltk.word_tokenize(expr)  # get operators
    for token in expr:
        if token in reserved:
            operators.append(token)

    return operators

def process_query(expr):
    terms = []
    operators = get_operators(expr)
    expr = preprocess(expr)
    for token in expr:
        if (token not in reserved):
            terms.append(token)
    for i in range(0, len(operators)-1):
        if (operators[i] == "and" or operators[i] == "or") and operators[i+1]=="not":
            operators[i] = operators[i] + " " + operators[i+1]
            operators.pop(i+1)
    result = apply_operator(terms, operators)
    return result

def  apply_operator(terms, operators):
    if len(terms) == 0:
        return set()
    else:
        postings = []
        for i in range(0, len(terms)):
            postings.append(dict.get(terms[i]))
    result = postings[0]
    print operators
    print terms
    for op in operators:
        if op == "and":
            result = set(result).intersection(postings[1])
        elif op == "or":
            result = set(result).union(postings[1])
        elif op == "and not":
            result = set(result).difference(postings[1])
        elif op == "or not":
            result = set(result).union(postings[1])
            result = set(result).difference(postings[1])
        postings.pop(0)
    return result


