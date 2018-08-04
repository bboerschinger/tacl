"""get the distribution over right-hand-sides of a given non-terminal

for the allpatterns-grammar, get Word
for the finitenostress, get WordGen
"""


import sys,re,glob

if __name__=="__main__":
    corpus = sys.argv[1]
    g = sys.argv[2]
    s = sys.argv[3]
    condition = sys.argv[4]
    fold = sys.argv[5]
    epochs = int(sys.argv[6])
    burnin = float(sys.argv[7])
    rate = int(sys.argv[8])
    nskip = int(burnin*epochs/rate)
    nsample = 0
    sys.stdout.write("#corpus,fold,nsample,grammar,setting,size,prob,lhs,rhs\n")
    d = {} #temporary count
    for l in sys.stdin:
        l = l.strip()
        if len(l)==0: #write
            if nskip<=0:
                for (lh,dl) in sorted(d.iteritems()):
                    for (rh,c) in sorted(dl.iteritems(),lambda x,y:-cmp(x[1],y[1])):
                        norm = float(sum(dl.values()))
                        sys.stdout.write("%s,%s,%s,%s,%s,%s,%.3f,\"%s\",\"%s\"\n"%(corpus,fold,nsample,g,condition,s,c/norm,lh,rh))
                nsample+=1
                d = {}
                sys.stdout.flush()
            else:
                d = {}
                nskip-=1
        else:             
            if l[0]=="(":
                continue
            c,ls = l.split("\t",1)
            lh,rh = ls.split(" --> ")
            try:
                ccs = d[lh]
            except KeyError:
                d[lh]={}
                ccs = d[lh]
            try:
                ccs[rh]+=float(c)
            except KeyError:
                ccs[rh]=float(c)
