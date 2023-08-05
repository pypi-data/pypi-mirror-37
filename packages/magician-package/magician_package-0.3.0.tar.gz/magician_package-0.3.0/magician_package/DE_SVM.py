from __future__ import print_function, division

__author__ = 'amrit'

import sys
from demo import cmd
#sys.dont_write_bytecode = True
from DE import DE
from ldavem import *
from collections import OrderedDict
import os
from collections import Counter
from featurization import *
from ML import SVM
from sklearn.model_selection import StratifiedKFold
import pickle
import time
import pandas as pd

lda=[main]
lds_para_dic=[OrderedDict([("n_components",10),("doc_topic_prior",0.1), ("topic_word_prior",0.01)])]
lda_para_bounds=[[(10,100), (0.1,1), (0.01,1)]]
lda_para_categories=[[ "integer", "continuous", "continuous"]]


learners=[SVM]
learners_para_dic=[OrderedDict([("C", 1.0), ("kernel", 'linear'), ("degree", 3)])]
learners_para_bounds=[[(0.1,100), ("linear","poly","rbf","sigmoid"), (1,20)]]
learners_para_categories=[["continuous", "categorical", "integer"]]
ROOT=os.getcwd()
files=["pitsA", "pitsB", "pitsC", "pitsD", "pitsE", "pitsF"]
features=[LDA_]
topics = ['10']
metrics=['accuracy','recall','precision','false_alarm']

def readfile1(filename=''):
    dict = []
    labels=[]
    with open(filename, 'r') as f:
        for doc in f.readlines():
            try:
                row = doc.lower().split(">>>")
                dict.append(row[0].strip())
                labels.append(row[1].strip())
            except:
                pass
    count=Counter(labels)
    import operator
    key = max(count.iteritems(), key=operator.itemgetter(1))[0]
    labels=map(lambda x: 1 if x == key else 0, labels)
    return np.array(dict), np.array(labels)

def _test(res='',file_path = ''):
    seed(1)
    np.random.seed(1)
    path = file_path + res + ".txt"
    raw_data, labels = readfile1(path)
    temp={}

#    for m in metrics:
#    if m!='false_alarm':
#    if m not in temp:
#        temp[m] = {}
    for i in range(2):
        print('Starting iteration ',i)
        ranges=range(len(labels))
        shuffle(ranges)
        raw_data=raw_data[ranges]
        labels=labels[ranges]
        for fea in features:
            start_time = time.time()
            corpus,_=fea(raw_data)
            end_time = time.time() - start_time

#                    start_time=time.time()
#                    de = DE(Goal="Max", GEN=5, NP=10,termination="Early")
#                    v, _ = de.solve(lda[0], OrderedDict(lds_para_dic[0]),
#                                    lda_para_bounds[0],
#                                    lda_para_categories[0],file=res, term=7, data_samples=raw_data)
#                    corpus,_=LDA_(raw_data,**v.ind)
#                    end_time = time.time()-start_time

            skf = StratifiedKFold(n_splits=2)
            for train_index, test_index in skf.split(corpus, labels):
                print('Starting fold :')
                train_data, train_labels = corpus[train_index], labels[train_index]
                test_data, test_labels = corpus[test_index], labels[test_index]
                
                for DE_train_index, validation_index in skf.split(train_data, train_labels):
                    DE_train_data, DE_train_labels = train_data[DE_train_index], train_labels[DE_train_index]
                    DE_validation_data, DE_validation_labels = corpus[validation_index], labels[validation_index]
                    print('Start DE')
                    ML_de = DE(Goal="Max", GEN=5, NP=10,termination="Early")
                    mlv, _ = ML_de.solve(learners[0], OrderedDict(learners_para_dic[0]),
                            learners_para_bounds[0],
                            learners_para_categories[0],
                            train_data = DE_train_data,train_labels = DE_train_labels, 
                            test_data = DE_validation_data, test_labels = DE_validation_labels, metric = 'recall')
#                            print(mlv.ind)
                    print('End DE')
                    for j, le in enumerate(learners):
                        if le.__name__ not in temp:
                            temp[le.__name__]={}
                        start_time1=time.time()
                        _,val=learners[0](mlv.ind, train_data, train_labels, test_data, test_labels, 'recall')
                        end_time1=time.time()-start_time1
                        print(val)

                        for m in metrics:
                            if m not in temp[le.__name__]:
                                temp[le.__name__][m]=[]
                        if 'times' not in temp[le.__name__]:
                            temp[le.__name__]['times']=[]
                        else:
                            temp[le.__name__]['times'].append(end_time1+end_time)
                        if 'metrices' not in temp[le.__name__]:
                            temp[le.__name__]['metrices'] = []
                        else:
                            temp[le.__name__]['metrices'].append(val[0])

    print(temp)
    return temp

if __name__ == '__main__':
    eval(cmd ())
    
#/Users/suvodeepmajumder/Documents/AI4SE/magician_package/magician_package/data/preprocessed
