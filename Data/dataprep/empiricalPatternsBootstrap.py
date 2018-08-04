"""
  calculate the empirical pattern distribution for a corpus as a function of its prefix-size, using bootstrape-resampled versions of the corpora
"""


import re,sys,random

init_rex = re.compile(r"^[^.]+[*][^*]*")
init_unamb_rex = re.compile(r"^[^.]+[*][^*]*[.]([^.*]+[.]){3,}")
peninit_rex = re.compile(r"(^[^.]+[*][^.]*[.]$|^[^.*]+[.][^.]+[*][^*]*$)")
peninit_unamb_rex = re.compile(r"^[^.*]+[.][^.]+[*][^*]*")
ult_rex = re.compile(r"^[^*]+[*][^.]*[.]$")
ult_unamb_rex = re.compile(r"^[^*]+[.].+[*][^.]*[.]$")
penult_rex = re.compile(r"(^[^.]+[*][^.]*[.]$|^[^*]+[*][^.]*[.][^.]+[.]$)")
penult_unamb_rex = re.compile(r"^[^*]+[*][^.]+[.][^.]+[.]$")
antepenult_rex = re.compile(r"(^[^.]+[*][^.]*[.]([^.]*[.]){0,2}$|^[^*]+[*][^.]*[.]([^.]+[.]){2,2}$)")
antepenult_unamb_rex = re.compile(r"^[^*]+[*][^.]*[.]([^.]+[.]){2,2}$")

monostress_rex = re.compile(r"^[^.]+[*][^.]*[.]$")
nostress_rex = re.compile(r"^[^*]+$")
poly1_rex = re.compile(r"^[^.]+[*][^*.]*[.][^*]+$")
poly2_rex = re.compile(r"^[^.*]+[.][^.]+[*][^*]+$")
poly3_rex = re.compile(r"^[^.*]+[.][^.*]+[.][^.]+[*][^*]+$")
poly4pl_rex = re.compile(r"^([^.*]+[.]){3,}[^.*]+[*][^*]+$")


patterns = "init peninit ult penult antepenult init_unamb penult_unamb peninit_unamb ult_unamb antepenult_unamb poly1 poly2 poly3 poly4pl nostress monostress".split()


def inc(hm,k):
    try:
        hm[k]+=1
    except KeyError:
        hm[k]=1

def newType(w,hm):
    return not hm.has_key(w)

def sampleFromWithRepl(l,n):
    """sample n items with replacement from the list l"""
    upper = len(l)-1
    res = []
    for i in range(n):
        res.append(l[random.randint(0,upper)])
    return res

if __name__=="__main__":
    sizes = [int(x) for x in sys.argv[1].split()]
    nbootstraps = int(sys.argv[2])
    seen = 0
    tokens = [0 for x in range(nbootstraps)]
    patCountTok = [{} for x in range(nbootstraps)]
    patCountTyp = [{} for x in range(nbootstraps)]
#    patCountUnambTok = {}
#    patCountUnambTyp = {}
    seenWords = [{} for x in range(nbootstraps)]
    sys.stdout.write("size,pattern,tokens,tokensTotal,tokRatio,types,typesTotal,typRatio\n")

    #generate bootstraps
    corpus = []
    for l in sys.stdin:
        l = l.strip()
        if len(l)==0:
            continue
        corpus.append(l)
    
    bootstraps = [[] for x in range(nbootstraps)]
    upper = sizes[-1]
    for i in range(nbootstraps):
        bootstraps[i] = sampleFromWithRepl(corpus,upper)

    for i in range(len(bootstraps[0])):
        if seen>sizes[-1]:
            break
        seen+=1
        for c in range(nbootstraps):
            words = bootstraps[c][i].strip().split("| ")
            for w in words:
               for p in patterns:
                   if eval(p+"_rex").search(w) is not None:
                       inc(patCountTok[c],p)
                       if newType(w,seenWords[c]):
                           inc(patCountTyp[c],p)
               seenWords[c][w]=1
               tokens[c] += 1
        if seen in sizes: #print info
            for c in range(nbootstraps):
                totTypes = len(seenWords[c])
                for p in patterns:
                    pTok = patCountTok[c].get(p,0)
                    pTyp = patCountTyp[c].get(p,0)
                    sys.stdout.write("%s,%s,%s,%s,%.3f,%s,%s,%.3f\n"%(seen,p,pTok,tokens[c],pTok/float(tokens[c]),pTyp,totTypes,pTyp/float(totTypes)))
                pTok = patCountTok[c].get("monostress",0)+patCountTok[c].get("poly1",0)
                pTyp = patCountTyp[c].get("monostress",0)+patCountTyp[c].get("poly1",0)
                sys.stdout.write("%s,%s,%s,%s,%.3f,%s,%s,%.3f\n"%(seen,"stress1",pTok,tokens[c],pTok/float(tokens[c]),pTyp,totTypes,pTyp/float(totTypes)))
