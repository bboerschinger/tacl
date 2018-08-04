"""
  processes a csv-forced-alignment file to extract a phonemic transcript,
  using an additional dictionary
  (really, all we use the forced alignment for is ensure that we only
   consider words which we also will have alignments for at some stage)
"""

import sys,optparse

WORD=2
PHON=3
UTT=0
ORT=4

def readDict(f):
    res = {}
    for l in open(f):
        word,pron = l.strip().split("  ")
        res[word]=pron.replace(":-",".").replace(":"," ")
    return res
    

if __name__=="__main__":
    parser = optparse.OptionParser(usage="")
    parser.add_option("-w","--word",dest="word",action="store_true",default=False)
    (options,args) = parser.parse_args()
    curWord = -1
    curOrt = ""
    curUtt = -1
    wordBuff = []
    uttBuff = []
    d = readDict(sys.argv[1])
    for l in sys.stdin:
        l = l.strip().split(",")
        if l[0]=="uttNum": #first line
            continue
        if curUtt != l[UTT]:
            curUtt=l[UTT]
            if len(wordBuff)>0:
                if options.word:
                    uttBuff.append("%s, %s"%(curOrt,d[curOrt.lower()]))#" ".join(wordBuff)))
                else:
                    uttBuff.append(d[curOrt.lower()])#" ".join(wordBuff))
            if len(uttBuff)>0:
                sys.stdout.write("%s\n"%(".| ".join(uttBuff)+"."))
            uttBuff=[]
            wordBuff=[]
        if curWord != l[WORD]:
            curWord=l[WORD]
            if len(wordBuff)>0:
                if options.word:
                    uttBuff.append("%s, %s"%(curOrt,d[curOrt.lower()]))#" ".join(wordBuff)))
                else:
                    uttBuff.append(d[curOrt.lower()]) #" ".join(wordBuff))
            curOrt = l[ORT]
            wordBuff = []
        wordBuff.append(l[PHON])
    if options.word:
        uttBuff.append("%s, %s"%(curOrt,d[curOrt.lower()])) #" ".join(wordBuff)))
    else:
        uttBuff.append(d[curOrt.lower()]) #" ".join(wordBuff))
    sys.stdout.write("%s\n"%(".| ".join(uttBuff)+"."))
