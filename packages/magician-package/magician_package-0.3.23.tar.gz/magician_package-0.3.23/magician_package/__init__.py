import sys 
import os
#sys.path.insert(0,os.getcwd() + '/src')
from . import LDA
from . import LDADE
from .ML import DT, SVM, RF, FFT1
import warnings
from . import DE_ML
#first_arg = sys.argv[1]
#second_arg = sys.argv[2]


def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

def _LDA(file_name = '',MLS = [DT, RF, SVM,FFT1],file_path = '',features = [10]):
    print("The Program started============================================================= ")
    result_ = LDA._test(file_name,MLS,file_path)
    print("Program completed")
    return result_

def _LDADE(file_name = '',MLS = [DT, RF, SVM,FFT1],file_path = ''):
    print("The Program started============================================================= ")
    result_ = LDADE._test(file_name,MLS,file_path)
    print("Program completed")
    return result_

def learner(file_name,second_arg,file_path,features):
    MLS = []
    if second_arg == '1':
        MLS = [DT]
    elif second_arg == '2':
        MLS = [RF]
    elif second_arg == '3':
        MLS = [SVM]
    elif second_arg == '4':
        MLS = [FFT1]
    elif second_arg == '5':
        MLS = [DT, RF, SVM,FFT1]
    else:
        print('Invalid Argument')
        sys.exit()
    result_x = _LDA(file_name,MLS,file_path,features)
    return result_x

def semi_auto_learner(file_name,second_arg,file_path):
    MLS = []
    if second_arg == '1':
        MLS = [DT]
    elif second_arg == '2':
        MLS = [RF]
    elif second_arg == '3':
        MLS = [SVM]
    elif second_arg == '4':
        MLS = [FFT1]
    elif second_arg == '5':
        MLS = [DT, RF, SVM,FFT1]
    else:
        print('Invalid Argument')
        sys.exit()
    result_x = _LDADE(file_name,MLS,file_path)
    return result_x

def auto_learner(file_name,second_arg,file_path,tune_for):
    MLS = []
    if second_arg == '1':
        MLS = [DT]
    elif second_arg == '2':
        MLS = [RF]
    elif second_arg == '3':
        MLS = [SVM]
    elif second_arg == '4':
        MLS = [DT, RF, SVM]
    if tune_for == 'accuracy' or tune_for == 'precision' or tune_for == 'recall' or tune_for == 'f1':
        goal = 'Max'
    else:
        goal = 'Min'
    result_x = DE_ML._test(file_name,MLS,file_path,tune_for,goal)
    return result_x