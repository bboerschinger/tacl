#!/home/bborschi/local/bin/python2.7

"""
  ensure that every word has at least one stressed syllable --> for mono-syllabic words lacking a stress, introduce one
  input format:
    seg1 seg2. seg3.| seg4.

  where "|" indicates a word-boundary and "." a syllable boundary, and " " indicates a segment boundary
"""

import sys


def hasStress(w):
    for c in w:
        if c=="*":
            return True
    return False


if __name__=="__main__":
    outF = open(sys.argv[1],"w")
    stressDict = {}
    for l in open(sys.argv[2],"r"):
        l=l.strip().rstrip(".")
        words=[]
        for w in l.split(".| "):
            if not hasStress(w):
                if stressDict.has_key(w):
                    words.append(stressDict[w])
                else:
                    stressDict[w]=raw_input("%s - "%w)
                    words.append(stressDict[w])
            else:
                words.append(w)
        sys.stdout.write("%s.\n"%".| ".join(words))
        outF.write("%s.\n"%".| ".join(words))
