"""get the distribution over right-hand-sides of a given non-terminal

for the allpatterns-grammar, get Word
for the finitenostress, get WordGen
"""


import sys,re,glob


grammar = re.compile(r"/([^/_]+)_[0-9]")
size = re.compile(r"_([0-9]+)_Tmp")
cond = re.compile(r"(nostress|primaryonly|fullstress)")
run = re.compile(r"_([0-9]+).wlt")


if __name__=="__main__":
    for f in sys.argv[1:]:
        g = grammar.search(f).groups()[0]
        s = size.search(f).groups()[0]
        condition = cond.search(f).groups()[0]
        if g.endswith("allpatterns"):
            cat = "Word"
        elif g.endswith("finitestress"):
            cat = "GenWord"
        elif g.endswith("stresspos"):
            cat = "GenWord"
        else:
            continue
        
        d = {}
        dind = {}
        for wlt in glob.glob(f+"/*.wlt"):
            r = run.search(wlt).groups()[0]
            dind[r]={}
            for l in open(wlt):
                l = l.strip()
                if len(l)==0:
                    continue
                if l[0]=="(":
                    continue
                c,ls = l.split("\t",1)
                lh,rh = ls.split(" --> ")
                if lh==cat:
                    d[rh] = d.get(rh,0)+float(c)
                    dind[r][rh] = dind[r].get(rh,0)+float(c)
        norm = float(sum(d.values()))
        for (rh,c) in sorted(d.iteritems(),lambda x,y:-cmp(x[1],y[1])):
            print "all,%s,%s,%s,%.3f,\"%s\""%(g,s,condition,c/norm,rh)

        for i in dind.keys():
            d = dind[i]
            norm = float(sum(d.values()))
            for (rh,c) in sorted(d.iteritems(),lambda x,y:-cmp(x[1],y[1])):
                print "%s,%s,%s,%s,%.3f,\"%s\""%(i,g,s,condition,c/norm,rh)

