import re, sys

if __name__=="__main__":
    pattern = re.compile(r"%s"%(sys.argv[1]))
    scale_rex = re.compile(r"_([0-9]+)_Tmp")
    name = sys.argv[2]
    for f in sys.argv[3:]:
        mo = scale_rex.search(f)
        if mo is not None:
            scale = mo.group(1)
        else:
            continue
        tokenCount = 0
        patternCount = 0
        patternTypes = {}
        types = {}
        example = None
        for l in open(f):
            l=l.strip()[:-1] #remove last "."
            for w in l.split(".|"):                
                tokenCount+=1
                types[w]=1
                if pattern.search(w):
                    example=w
                    patternTypes[w]=1
                    patternCount+=1
        sys.stdout.write("%s,%s,%s,%.3f,%s,%.3f\n"%(scale,name,patternCount,patternCount/float(tokenCount),len(patternTypes.keys()),len(patternTypes.keys())/float(len(types.keys()))))
