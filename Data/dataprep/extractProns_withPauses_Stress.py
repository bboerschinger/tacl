"""
  processes a csv-forced-alignment file to extract a phonemic transcript,
  using an additional dictionary
  (really, all we use the forced alignment for is ensure that we only
   consider words which we also will have alignments for at some stage)

  we set a minimum-length for pauses to be considered, otherwise they won't be added to the transcript
"""

import sys,optparse

WORD=1
PHON=2
UTT=0
ORT=3
DUR=8
STRESS=-1

PAUSELENGTH=1000

ignoredPauses=0
addedPauses=0

def addStress(w,p,o=None):
    w = w.replace("1","0").replace("2","0")
    if len(p)==0:
        return w
    else:
        res = []
        for (i,s) in enumerate(w.split(". ")):
            if i in p:
                res.append(addStressSyl(s))
            else:
                res.append(s)
        w = ". ".join(res)
        if w.count("1")==0:
            sys.stderr.write("Couldn't add stress at pos %s to %s, from %s\n"%(p,w,o))
        return w

def addStressSyl(s):
    s = s.replace("1","").replace("2","").replace("0","")
    res = []
    i = 0
    while i < len(s):
        res.append(s[i])
        if s[i] in "aeiou":
            res.append(s[i+1])
            res.append("1")
            i+=1
        i+=1
    return "".join(res)

def stressPos(s):
    res = []
    i = 0
    for c in s.split():
        if c[0] in "aeiou":
            if c.count("*")==1:
                res.append(i)
            i+=1
    return res

def readDict(f):
    res = {}
    for l in open(f):
        word,pron = l.strip().split("  ")
        res[word]=pron.replace(":-",".").replace(":"," ")
    return res
    

if __name__=="__main__":
    parser = optparse.OptionParser(usage="")
    parser.add_option("-w","--word",dest="word",action="store_true",default=False)
    parser.add_option("-u","--utId",dest="utId",action="store_true",default=False)
    (options,args) = parser.parse_args()
    curWord = -1
    curOrt = ""
    curPhon = ""
    curUtt = -1
    curDur = 0
    wordBuff = []
    uttBuff = []
    d = readDict(sys.argv[1])
    if len(sys.argv)>2:
        PAUSELENGTH=float(sys.argv[2])
    for l in sys.stdin:
        l = l.strip().split(",")
        if l[0].startswith("utt"): #first line
            continue
        if curUtt != l[UTT]:
            if len(wordBuff)>0:
                if options.word:
                    uttBuff.append("%s, %s"%(curOrt,d[curOrt.lower()]))#" ".join(wordBuff)))
                else:
                    if curOrt.lower()=="pause" and curPhon=="sp":
                        if curDur>=PAUSELENGTH:
                            uttBuff.append(d["__PAUSE__"])
                        else:
                            pass
                    else:
                        try:
                            uttBuff.append(addStress(d[curOrt.lower()],stressPos(" ".join(wordBuff))," ".join(wordBuff)))#" ".join(wordBuff))
                        except KeyError:
                            sys.stderr.write("%s  %s\n"%(curOrt.lower(), " ".join(wordBuff)))
            if len(uttBuff)>0:
                if options.utId:
                    sys.stdout.write("%s %s\n"%(curUtt,".| ".join(uttBuff)+"."))
                else:
                    sys.stdout.write("%s\n"%(".| ".join(uttBuff)+"."))         
            curUtt = l[UTT]
            uttBuff=[]
            wordBuff=[]
        if curWord != l[WORD]:
            curWord=l[WORD]
            if len(wordBuff)>0:
                if options.word:
                    uttBuff.append("%s, %s"%(curOrt,d[curOrt.lower()]))#" ".join(wordBuff)))
                else:
                    if curOrt.lower()=="pause" and curPhon=="sp":
#                        print curOrt.lower()
                        if curDur>=PAUSELENGTH:
                            uttBuff.append(d["__PAUSE__"])
                            addedPauses+=1
                        else:
                            ignoredPauses+=1
                    else:
#                        print curOrt.lower()
                        try:
                            uttBuff.append(addStress(d[curOrt.lower()],stressPos(" ".join(wordBuff))," ".join(wordBuff)))
                        except KeyError:
                            sys.stderr.write("%s  %s\n"%(curOrt.lower(), " ".join(wordBuff)))
            curOrt = l[ORT].replace(".","'")
            curDur = float(l[DUR])
            wordBuff = []
        curPhon = l[PHON]
        if l[STRESS]=="p":
            wordBuff.append(l[PHON]+"*")
        else:
            wordBuff.append(l[PHON])
    if options.word:
        uttBuff.append("%s, %s"%(curOrt,d[curOrt.lower()])) #" ".join(wordBuff))
    else:
        if curOrt.lower()=="pause" and curPhon=="sp":
#            print curOrt.lower()
            if curDur>=PAUSELENGTH:
                uttBuff.append(d["__PAUSE__"])
                addedPauses+=1
            else:
                ignoredPauses+=1
        else:
#            print curOrt.lower()
            try:
                uttBuff.append(addStress(d[curOrt.lower()],stressPos(" ".join(wordBuff))," ".join(wordBuff)))
            except KeyError:
                sys.stderr.write("%s  %s\n"%(curOrt.lower(), " ".join(wordBuff)))

    if options.utId:
        sys.stdout.write("%s %s\n"%(curUtt,".| ".join(uttBuff)+"."))
    else:
        sys.stdout.write("%s\n"%(".| ".join(uttBuff)+"."))
    sys.stderr.write("added %d pauses, ignored %d pauses\n"%(addedPauses,ignoredPauses))
