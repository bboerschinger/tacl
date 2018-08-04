"""
  adds a stress to every unstressed word in the corpus
  for mono-syllabic words, stresses are just added to 
  the vowel
  for multi-syllabic words, a text-file is consulted.
  if no pronunciation is found, an exception is thrown
"""

import sys

def addStress(x,m):
    if x.count(".")==1: #monosyllable, just add stress to the vowel
        res = []
        i = 0
        while i < len(x):
            if x[i] in "aeiou":
                res.append("%s%s *"%(x[i],x[i+1]))
                i+=2
            else:
                res.append(x[i])
                i+=1
        return "".join(res)
    else:
        try:
            return m[x]
        except:
            sys.stderr.write("No pronunciation found for '%s'\n"%x)

def readM(f):
    res = {}
    for l in open(f):
        l = l.strip()
        orig,stress = l.split("  ")
        res[orig]=stress
    return res


def ensureStressed(w,m):
    if w.count("*")>=1:
        return w
    else:
        return addStress(w,m)

if __name__=="__main__":
    m = readM(sys.argv[1])
    for l in sys.stdin:
        l = l.strip()
        ut = []
        for w in l.split("| "):
            ut.append(ensureStressed(w,m))
        sys.stdout.write("%s\n"%("| ".join(ut)))
