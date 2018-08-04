import sys

"""normalize counts and produce csv-file for a specific rule-distribution"""

if __name__=="__main__":
    cat = sys.argv[1]
    corpus = sys.argv[2]
    condition = sys.argv[3]
    size = sys.argv[4]
    run = sys.argv[5]
    samples = []
    d = {}
    for l in sys.stdin:
        l = l.strip()
        if len(l)==0:
            norm = float(sum(d.values()))
            tmp = []
            for rhs in d.keys():
                tmp.append((rhs,d[rhs]/norm))
            samples.append(tmp)
            d={}
        else:
            counts, rest = l.split("\t")
            x,rhs = rest.split(" --> ")
            if x==cat:
                d[rhs]=float(counts)
    norm = float(sum(d.values()))
    tmp = []
    for rhs in d.keys():
        tmp.append((rhs,d[rhs]/norm))
    samples.append(tmp)
    print "sample,rule,prob"
    for (i,sample) in enumerate(samples):
        for (rhs,prob) in sample:
            print "%s,%s,%s"%(i,"\"%s -> %s\""%(cat,rhs),prob)
        
