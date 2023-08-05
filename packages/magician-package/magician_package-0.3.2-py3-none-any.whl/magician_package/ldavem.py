from __future__ import print_function, division

__author__ = 'amrit'

import sys

#sys.dont_write_bytecode = True
from random import shuffle, seed
import numpy as np
import os
from sklearn.feature_extraction.text import CountVectorizer
import copy
from sklearn.decomposition import LatentDirichletAllocation

ROOT=os.getcwd()
seed(1)
np.random.seed(1)

def calculate(topics=[], lis=[], count1=0):
    count = 0
    for i in topics:
        if i in lis:
            count += 1
    if count >= count1:
        return count
    else:
        return 0


def recursion(topic=[], index=0, count1=0):
    count = 0
    global data
    # print(data)
    # print(topics)
    d = copy.deepcopy(data)
    d.pop(index)
    for l, m in enumerate(d):
        # print(m)
        for x, y in enumerate(m):
            if calculate(topics=topic, lis=y, count1=count1) != 0:
                count += 1
                break
                # data[index+l+1].pop(x)
    return count


data = []


def jaccard(a, score_topics=[], term=0):
    labels = []  # ,6,7,8,9]
    labels.append(term)
    global data
    l = []
    data = []
    file_data = {}
    for doc in score_topics:
        l.append(doc.split())
    for i in range(0, len(l), int(a)):
        l1 = []
        for j in range(int(a)):
            l1.append(l[i + j])
        data.append(l1)
    dic = {}
    for x in labels:
        j_score = []
        for i, j in enumerate(data):
            for l, m in enumerate(j):
                sum = recursion(topic=m, index=i, count1=x)
                if sum != 0:
                    j_score.append(sum / float(9))
                '''for m,n in enumerate(l):
                    if n in j[]'''
        dic[x] = j_score
        if len(dic[x]) == 0:
            dic[x] = [0]
    file_data['citemap'] = dic
    X = range(len(labels))
    Y_median = []
    Y_iqr = []
    for feature in labels:
        Y = file_data['citemap'][feature]
        Y = sorted(Y)
        return Y[int(len(Y) / 2)]


def get_top_words(model, path1, feature_names, n_top_words, i=0, file1=''):
    topics = []
    fo = open(path1, 'a+')
    fo.write("Run: " + str(i) + "\n")
    for topic_idx, topic in enumerate(model.components_):
        str1 = ''
        fo.write("Topic " + str(topic_idx) + ": ")
        for j in topic.argsort()[:-n_top_words - 1:-1]:
            str1 += feature_names[j] + " "
            fo.write(feature_names[j] + " ")
        str1=str(str1.encode('ascii', 'ignore'))
        topics.append(str1)
        fo.write("\n")
    fo.close()
    return topics


def readfile1(filename=''):
    dict = []
    with open(filename, 'r') as f:
        for doc in f.readlines():
            try:
                row = doc.lower().strip()
                dict.append(row)
            except:
                pass
    return dict


def _test_LDA( path1, file='', data_samples=[], term=7, **l):
    topics = []
    for i in range(10):
        shuffle(data_samples)

        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
        tf = tf_vectorizer.fit_transform(data_samples)

        lda1 = LatentDirichletAllocation(max_iter=100,learning_method='online',**l)

        lda1.fit_transform(tf)

        # print("done in %0.3fs." % (time() - t0))
        tf_feature_names = tf_vectorizer.get_feature_names()
        topics.extend(get_top_words(lda1, path1, tf_feature_names, term, i=i, file1=file))
    return topics

## main(k,alpha,beta,tune='tuned',file='',term='',data_samples='')

def main(*x, **r):

    base = ROOT+"/../temp/"
    path = os.path.join(base, r['file'], str(r['term']))
    if not os.path.exists(path):
        os.makedirs(path)
    l = np.asarray(x)
    n_components = l[0]['n_components']
    doc_topic_prior=l[0]['doc_topic_prior']
    topic_word_prior=l[0]['topic_word_prior']
    path1 = path + "/K_" + str(n_components) + "_a_" + str(doc_topic_prior) + "_b_" + str(topic_word_prior) + ".txt"
    with open(path1, "w") as f:
        f.truncate()

    topics = _test_LDA(path1, file=r['file'],data_samples=r['data_samples'],term=int(r['term']),n_components=n_components,
                       doc_topic_prior=doc_topic_prior,topic_word_prior=topic_word_prior)

    a = jaccard(n_components, score_topics=topics, term=int(r['term']))
    fo = open(path1, 'a+')
    fo.write("\nScore: " + str(a))
    fo.close()
    return a, [{},[]]
