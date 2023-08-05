from __future__ import print_function, division

__author__ = 'amrit'

import sys
from .demo import cmd
#sys.dont_write_bytecode = True
from .DE import DE
from .ldavem import *
from collections import OrderedDict
import os
from collections import Counter
from .featurization import *
from .ML import DT, SVM, RF, FFT1
from sklearn.model_selection import StratifiedKFold
import pickle
import time

learners=[main]
learners_para_dic=[OrderedDict([("n_components",10),("doc_topic_prior",0.1), ("topic_word_prior",0.01)])]
learners_para_bounds=[[(10,100), (0.1,1), (0.01,1)]]
learners_para_categories=[[ "integer", "continuous", "continuous"]]
ROOT=os.getcwd()
files=["pitsA", "pitsB", "pitsC", "pitsD", "pitsE", "pitsF"]
MLS=[DT,RF, SVM,  FFT1]
MLS_para_dic = {'DT':OrderedDict([("min_samples_split", 2), ("min_impurity_decrease", 0.0), ("max_depth", None),
                             ("min_samples_leaf", 1)]), 
                'RF': OrderedDict([("min_samples_split", 2),("max_leaf_nodes", None), ("min_samples_leaf", 1),
                                   ("min_impurity_decrease", 0.0),("n_estimators", 10)]),
                'SVM': OrderedDict([("C", 1.0), ("kernel", 'linear'),
                             ("degree", 3)]), 
                'FFT1':OrderedDict()}

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

def _test(res='',_MLS = [DT, RF, SVM,FFT1],file_path = ''):
    seed(1)
    np.random.seed(1)
    #path=ROOT+"/data/preprocessed/"+res+".txt"
    path = file_path + res + ".txt"
    raw_data,labels=readfile1(path)
    temp={}
    MLS = _MLS
    for i in range(5):
        ranges=range(len(labels))
        shuffle(ranges)
        raw_data=raw_data[ranges]
        labels=labels[ranges]
        #print(raw_data)
        start_time=time.time()
        de = DE(Goal="Max", GEN=5, NP=10,termination="Early")
        v, _ = de.solve(learners[0], OrderedDict(learners_para_dic[0]),
                        learners_para_bounds[0], learners_para_categories[0],
                        file=res, term=7, data_samples=raw_data)
        corpus,_=LDA_(raw_data,**v.ind)
        end_time = time.time()-start_time

        skf = StratifiedKFold(n_splits=5)
        for train_index, test_index in skf.split(corpus, labels):
            train_data, train_labels = corpus[train_index], labels[train_index]
            test_data, test_labels = corpus[test_index], labels[test_index]

            for j, le in enumerate(MLS):
                if le.__name__ not in temp:
                    temp[le.__name__]={}
                start_time1=time.time()
                _,val=MLS[j](MLS_para_dic[le.__name__], train_data, train_labels, test_data, test_labels, 'recall')
                end_time1=time.time()-start_time1
                for m in metrics:
                    if m not in temp[le.__name__]:
                        temp[le.__name__][m]=[]
                    temp[le.__name__][m].append(val[0][m])
                if 'times' not in temp[le.__name__]:
                    temp[le.__name__]['times']=[]
                else:
                    temp[le.__name__]['times'].append(end_time1+end_time)
                if 'features' not in temp[le.__name__]:
                    temp[le.__name__]['features'] = []
                else:
                    temp[le.__name__]['features'].append(val[1])

    return temp

if __name__ == '__main__':
    eval(cmd ())
