import sys,re

vwl = re.compile(r"[aeiou].")

def jabberwock(x):
    if x.count("*")>=1:
        return vwl.sub("xx",x)
    else:
        return x

if __name__=="__main__":
    for l in sys.stdin:
        res = []
        for w in l.strip().split("| "):
            res.append(jabberwock(w))
        print "| ".join(res)
