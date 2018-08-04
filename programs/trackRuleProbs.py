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
    cat = sys.argv[6]
    epochs = int(sys.argv[7])
    burnin = float(sys.argv[8])
    rate = int(sys.argv[9])
    nskip = int(burnin*epochs/rate)
#    nskip=0
    nsample = 0
    sys.stdout.write("#corpus,fold,nsample,grammar,setting,size,prob,rule\n")
    d = {} #temporary count
    for l in sys.stdin:
        l = l.strip()
        if len(l)==0: #write
            if nskip<=0:
                norm = float(sum(d.values()))
                for (rh,c) in sorted(d.iteritems(),lambda x,y:-cmp(x[1],y[1])):
                    sys.stdout.write("%s,%s,%s,%s,%s,%s,%.3f,\"%s\"\n"%(corpus,fold,nsample,g,condition,s,c/norm,rh))
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
            if lh==cat:
                d[rh] = d.get(rh,0)+float(c)

