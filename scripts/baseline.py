"""Base-line segmenter for syllabified data"""

import sys

def segmentSyll(x):
    """simply treat each syllable as a word"""
    return " ".join(x.split())

def segmentStress(x):
    """posit a boundary in front of every stressed-syllable, unless there isn't a stressed-syllable in the current span (can only happen at the beginning of a word"""
    res = []
    tmp = []
    hasStress=False
    for s in x.split():
        if s.count("*")==1:
            if hasStress:
                res.append(tmp)
                hasStress=True
                tmp=[s]
            else:
                tmp.append(s)
                hasStress=True
        else:
            tmp.append(s)
    res.append(tmp)
    return " ".join(["".join(q) for q in res])

if __name__=="__main__":
    if sys.argv[1]=="stress":
        segmenter=segmentStress
    elif sys.argv[1]=="syll":
        segmenter=segmentSyll
    else:
        print "has to be 'stress' or 'syll'"
        sys.exit(1)
    for l in sys.stdin:
        l = l.strip()
        print segmenter(l)
    print
