import sys

"""take a textfile and look up words in pronunciation dictionary"""

def readD(f,sAf):
    d = {}
    for l in open(f):
        try:
            ort,phon = l.strip().split("  ")
        except ValueError:
            raise ValueError("%s doesn't conform to format"%l)
        if sAf:
            d[ort]=phon.replace(":-:",". ").replace(":"," ").replace("1"," *").replace("0","").replace("2","*")
        else:
            d[ort]=phon.replace(":-:",". ").replace(":"," ").replace("1"," *"),replace("0","").replace("2","")
    return d

if __name__=="__main__":
    if len(sys.argv)>2 and sys.argv[2]=="yes":
        secondAsFirst = True
    else:
        secondAsFirst = False
    d = readD(sys.argv[1],secondAsFirst)
    for l in sys.stdin:
        l=l.lower().strip()
        res = []
        skip = False
        for w in l.split():
            try:
                res.append(d[w])
            except KeyError:
                sys.stderr.write("%s\n"%w)
                skip = True
                continue
        if not skip:
            sys.stdout.write("%s.\n"%(".| ".join(res)))
