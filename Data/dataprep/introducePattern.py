"""turn a given corpus into a fixed-stress-pattern corpus"""

import sys

def conformToPattern(w,p,stressAll=False):
    if w.count("*")==0 and not stressAll: #don't treat unstressed
        return w
    w = w.replace("*","")
    res = []
    sylls = w.split(". ")
    if p == "Init":
        sylls[0]=addStress(sylls[0])
    elif p=="PenInit":
        i = min(1,len(sylls)-1)
        sylls[i]=addStress(sylls[i])
    elif p=="Ult":
        sylls[-1]=addStress(sylls[-1])
    elif p=="PenUlt":
        i=max(len(sylls)-2,0)
        sylls[i]=addStress(sylls[i])
    elif p=="AntePenUlt":
        i=max(len(sylls)-3,0)
        sylls[i]=addStress(sylls[i])
    return ". ".join(sylls)

def addStress(s):
    res = []
    i = 0
    while i<len(s):
        res.append(s[i])
        if s[i] in "aeiou":
            res.append(s[i+1])
            res.append(" *")
            i+=1
        i+=1
    return "".join(res)

if __name__=="__main__":
    p = sys.argv[1]
    sall = True if len(sys.argv)>2 and sys.argv[2]=="yes" else False
    for l in sys.stdin:
        l = l.strip()
        words = l.split("| ")
        res = []
        for w in words:
            res.append(conformToPattern(w,p,sall))
        sys.stdout.write("%s\n"%("| ".join(res)))
