import pickle
from sys import argv

with open(argv[1], 'rb') as fin:
  print(pickle.load(fin))