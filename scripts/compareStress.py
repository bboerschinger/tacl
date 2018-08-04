import sys

"""compare induced and dictionary stress

we assume each utterance is prefixed by its id, and that the ids are in incremental order
"""

def getUID(f,uId):
    tmpLine = f.readline()
    tId,phons = tmpLine.strip().split(" ",1)
#    print "in getUID",tId,uId
    while tId != uId:
        tmpLine = f.readline()
        tId,phons = tmpLine.strip().split(" ",1)
#        print "in getUID",tId,uId
    return phons

primaryCorrect=0
primaryPredicted=0
primaryGold=0
secondaryAsPrimary=0
secondaryGold=0
noCorrect=0
noPredicted=0
noGold=0
syllablesGold=0
syllablesPred=0

def comparePair(predicted,gold):
    global primaryCorrect,primaryPredicted,primaryGold,secondaryAsPrimary,secondaryGold,noCorrect,noPredicted,noGold,syllablesGold,syllablesPred
    predSylls = predicted.split(". ")
    goldSylls = gold.split(". ")
    try:
        assert(len(predSylls)==len(goldSylls))
    except AssertionError:
        print predicted, gold
    for (p,g) in zip(predSylls,goldSylls):
        if p.startswith("sil"):
            continue
        syllablesGold+=1
        syllablesPred+=1
        gIsPrimary = g.count("1")==1
        gIsSecondary = g.count("2")==1
        gUnstressed = g.count("0")==1
        pIsPrimary = p.count("1")==1
        pUnstressed = p.count("0")==1
        if not (pIsPrimary | pUnstressed):
            print p,g
        if not (gIsPrimary | gUnstressed | gIsSecondary):
            print g,p
        primaryGold = primaryGold + (1 if gIsPrimary else 0)
        secondaryGold = secondaryGold + (1 if gIsSecondary else 0)
        noGold = noGold + (1 if gUnstressed else 0)
        primaryPredicted = primaryPredicted + (1 if pIsPrimary else 0)
        primaryCorrect = primaryCorrect + (1 if pIsPrimary and gIsPrimary else 0)
        secondaryAsPrimary = secondaryAsPrimary + (1 if pIsPrimary and gIsSecondary else 0)
        noPredicted = noPredicted + (1 if pUnstressed else 0)
        noCorrect = noCorrect + (1 if pUnstressed and gUnstressed else 0)

def fscore(a,b):
    return (2*a*b)/float(a+b)

if __name__=="__main__":
    stressFile = open(sys.argv[1])
    goldFile = open(sys.argv[2])
    for l in stressFile:
        l = l.strip()
        uID,pred = l.split(" ",1)
        lg = getUID(goldFile,uID)
        for (p,g) in zip(pred.split(".| "),lg.split(".| ")):
            #print p,":",g
            comparePair(p,g)
    primaryPrec = primaryCorrect / float(primaryPredicted)
    primaryRec = primaryCorrect / float(primaryGold)
    secRec = secondaryAsPrimary / float(secondaryGold)
    unstressedPrec = noCorrect / float(noPredicted)
    unstressedRec = noCorrect / float(noGold)
    print "PP %.3f (%d/%d) PR %.3f (%d/%d) PF %.3f"%(primaryPrec,primaryCorrect,primaryPredicted,primaryRec,primaryCorrect,primaryGold,fscore(primaryPrec,primaryRec))
    print "SR %.3f (%d/%d)"%(secRec,secondaryAsPrimary,secondaryGold)
    print "UP %.3f (%d/%d) UR %.3f (%d/%d) UF %.3f"%(unstressedPrec,noCorrect,noPredicted,unstressedRec,noCorrect,noGold,fscore(unstressedPrec,unstressedRec))
    print "SyllPred %d SyllGold %d"%(syllablesPred,syllablesGold)
