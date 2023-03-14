import scipy.io
import sys
from Levenshtein import *
import pandas
import numpy as np
#pathToParticipants = sys.argv[1]
#subject = sys.argv[2]
#conditionIndex = sys.argv[3]


sequence1 = scipy.io.loadmat('D:/Dissertation/Participants/sub-01/moduleResults/allBrainData__1.mat', matlab_compatible=True)['allBrainData'][0][0]
sequence2 = pandas.read_csv(
    'C:/Users/Reece/Documents/Dissertation/Main/Batch_Scripts/sequence2.csv', header=None)

functionalMap = sequence1.astype(
    int).applymap(lambda x: chr(ord('`')+x+1)).to_string(header=False, index=False, col_space=0).strip().replace(' ', '')
structuralMap = sequence2.astype(
    int).applymap(lambda x: chr(ord('`')+x+1)).to_string(header=False, index=False, col_space=0).strip().replace(' ', '')

x = distance(structuralMap, functionalMap, weights=(1, 1, 1))
y = ratio(structuralMap, functionalMap)
z = hamming(structuralMap, functionalMap)
x_ = distance(functionalMap, structuralMap, weights=(1, 1, 1))
y_ = ratio(functionalMap, structuralMap)
z_ = hamming(functionalMap, structuralMap)
print(x)
print(x_)
print(x_/len(structuralMap))

print(y)
print(y_)
print(y_/len(structuralMap))
print(z)
print(z_)
print(z_/len(structuralMap))
