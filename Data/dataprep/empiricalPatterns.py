"""
  calculate the empirical pattern distribution for a corpus as a function of its prefix-size
"""


import re,sys

multiplestresses_rex = re.compile(r"[*].*[*]")

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

patterns = "init peninit ult penult antepenult init_unamb penult_unamb peninit_unamb ult_unamb antepenult_unamb poly1 poly2 poly3 poly4pl nostress monostress multiplestresses".split()

patterns2 = "poly1 poly2 poly3 poly4pl nostress monostress".split()

def inc(hm,k):
    try:
        hm[k]+=1
    except KeyError:
        hm[k]=1

def newType(w,hm):
    return not hm.has_key(w)

if __name__=="__main__":
    sizes = [int(x) for x in sys.argv[1].split()]
    seen = 0
    tokens = 0
    patCountTok = {}
    patCountTyp = {}
    patCountUnambTok = {}
    patCountUnambTyp = {}
    seenWords = {}
    sys.stdout.write("size,pattern,tokens,tokensTotal,tokRatio,types,typesTotal,typRatio\n")
    for l in sys.stdin:
        if seen>sizes[-1]:
            break
        words = l.strip().split("| ")
        seen += 1
        for w in words:
           for p in patterns:
               if eval(p+"_rex").search(w) is not None:
                   inc(patCountTok,p)
                   if newType(w,seenWords):
                       inc(patCountTyp,p)
#               matchedPenIn = False
#               matchedPenUlt = False
#               if eval(p+"_unamb_rex").search(w) is not None:
#                   if p=="peninit":
#                       matchedPenIn = True
#                   if p=="penult":
#                       matchedPenUlt = True
#                   inc(patCountUnambTok,p)
                   if newType(w,seenWords):
                       inc(patCountUnambTyp,p)
#               if matchedPenIn != matchedPenUlt:
#                   sys.stderr.write("%s, penin=%s, penult=%s\n"%(w,matchedPenIn,matchedPenUlt))
           seenWords[w]=1
           tokens += 1
        if seen in sizes: #print info
            totTypes = len(seenWords)
            for p in patterns:
                pTok = patCountTok.get(p,0)
                pTyp = patCountTyp.get(p,0)
#                pUnambTok = patCountUnambTok.get(p,0)
#                pUnambTyp = patCountUnambTyp.get(p,0)
#                sys.stdout.write("%s,%s,%s,%s,%s,%.3f,%.3f,%s,%s,%s,%.3f,%.3f\n"%(seen,p,pTok,pUnambTok,tokens,pTok/float(tokens),pUnambTok/float(tokens),pTyp,pUnambTyp,totTypes,pTyp/float(totTypes),pUnambTyp/float(totTypes)))
                sys.stdout.write("%s,%s,%s,%s,%.3f,%s,%s,%.3f\n"%(seen,p,pTok,tokens,pTok/float(tokens),pTyp,totTypes,pTyp/float(totTypes)))
            pTok = patCountTok.get("monostress",0)+patCountTok.get("poly1",0)
            pTyp = patCountTyp.get("monostress",0)+patCountTyp.get("poly1",0)
            sys.stdout.write("%s,%s,%s,%s,%.3f,%s,%s,%.3f\n"%(seen,"stress1",pTok,tokens,pTok/float(tokens),pTyp,totTypes,pTyp/float(totTypes)))

