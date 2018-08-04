#!/bin/python

"""
  lower-cases entries and combines dictionaries  
  outputs cmudict-format as follows

  orthographicform  seg1:seg2:-:seg3

  where :-: indicates a syllableboundary
"""
import sys

if __name__=="__main__":
    d = {}
    #first file cmu...
    for l in open(sys.argv[1]):
        word,pron = l.strip().split("  ")
        d[word.lower()]=pron.lower()
    
    #second file, handlist
    for l in open(sys.argv[2]):
        try:
            word,pron = l.strip().split("  ")
        except:
            print l
            sys.exit()
        d[word.lower()]=pron.lower()
    
    for word in sorted(d.keys()):
        print "%s  %s"%(word,d[word])
    
