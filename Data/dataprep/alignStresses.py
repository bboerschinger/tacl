import sys

"""take one of John's stress-string files and add the stresses of that file to a standard gold-file

we assume each utterance is prefixed by its id, and that the ids are in incremental order

john has sp where we have sil
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

if __name__=="__main__":
    stressFile = open(sys.argv[1])
    goldFile = open(sys.argv[2])
    vwls = "a e i o u".split()
    for lStress in stressFile:
        try:
            lStress = lStress.strip()
            uId,phonsStress = lStress.split(": ")
            phonsStress = phonsStress.split("#")
            phonsGold = getUID(goldFile,uId)
            phonPos = 0
#            print "phonsStress=",phonsStress
#            print "goldPhons=",phonsGold
            gstringPos = 0
            nextPhonBuf = []
            utterance = []
            while gstringPos<len(phonsGold):
    #            print utterance
                if phonsGold[gstringPos]=="." or phonsGold[gstringPos]==" ":
                    if len(nextPhonBuf)==0:
                        gstringPos+=1
                        continue
                    nextPhon="".join(nextPhonBuf)
                    nextPhonBuf = []
                elif phonsGold[gstringPos]=="|": #word-boundary
                    gstringPos+=2
                    utterance.append("|")
                    continue
                else:
                    nextPhonBuf.append(phonsGold[gstringPos])
                    gstringPos+=1
                    continue
    #            print "phonPos=",phonPos
                stressPhon = phonsStress[phonPos]
    #            print nextPhon,stressPhon
                if nextPhon[0] in vwls:
                    isStressed = stressPhon.endswith("*")
                    if isStressed:
                        utterance.append(nextPhon[:-1]+"1")
                    else:
                        utterance.append(nextPhon[:-1]+"0")
                else:
                    utterance.append(nextPhon)
                phonPos+=1
                if phonsGold[gstringPos]==".": #syllable
                    utterance.append(".")
                gstringPos+=1
            sys.stdout.write("%s %s\n"%(uId," ".join(utterance).replace(" .",".").replace(" |","|")))
        except:
            continue
