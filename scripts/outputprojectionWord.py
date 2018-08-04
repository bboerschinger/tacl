"""input / output projections as defined in Daland (2013)

collect a distribution over the output-projections of specific words, given
a sequence of samples

author: benjamin boerschinger

an output-projection is 
  "the minimal sequence of segmented words containing the entire input word. For example, 
   if 'the#kitty' were segmented as 'thekitty', then 'thekitty' would be the output pro-
   jection for both 'the' and 'kitty'"
"""


import doctest,segUtils,sys


def outputprojections(goldseg,predseg):
    """calculate outputprojections for all the words in goldseg given predseg
    
    @goldseg  the goldsegmentation, a white-space separated string, e.g. "the kitty"
    @predseg  the predicted segmentation, a white-space separated string, e.g. "th e kitty"

    >>> outputprojections("the kitty","thekitty")
    [("the","thekitty"),("kitty","thekitty")]

    >>> outputprojections("the kitty","thek itty")
    [("the","thek"),("kitty","thek itty")]
    """
    inWords = segUtils.words(goldseg)
    goldtext = goldseg.replace(" ","").replace(".","")
    predVector = segUtils.getBVec(predseg)
    res = []
    for (l,r) in sorted(inWords,lambda x,y:cmp(x[0],y[0])):
        inpP = goldtext[l:r]
        lp = l-1 if l>0 else l
        while lp>-1 and predVector[lp]!="b":
            lp-=1
        rp = r-1
        while rp<len(goldtext)-1 and predVector[rp]!="b":
            rp+=1
        outP = segUtils.segment(goldtext[lp+1:rp+1],predVector[lp+1:rp])
        res.append((inpP,outP))
    return res

def inc(hm,k1,k2):
    try:
        hm.setdefault(k1,{})[k2]+=1
    except KeyError:
        hm.setdefault(k1,{})[k2]=1

def inc1(hm,k):
    try:
        hm[k]+=1
    except KeyError:
        hm[k]=1

if __name__=="__main__":
    gold = open(sys.argv[1]).readlines()
    words = sys.argv[2].split()
    loutps = []
    pred = []
    for l in sys.stdin:
        l = l.strip()
        if len(l)>0:
            pred.append(l)
        else:
            loutps.append({})
            outps = loutps[-1]
            for (p,g) in zip(pred,gold):
                p = p.strip()
                g = g.strip()
                outs = outputprojections(g,p)
                for (a,b) in outs:
                    if a in words:
                        inc(outps,a,b)
            pred = []

    for outs in loutps:
        for w in words:
            sys.stdout.write("%s\n"%w)
            norm = float(sum(outs[w].values()))
            for o in outs[w].keys():
                sys.stdout.write("  %.3f  %s\n"%(outs[w][o]/norm,o))
