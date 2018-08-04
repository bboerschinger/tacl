# finds lexicon entries which do not have the gold syllabification
# but match otherwise

import sys

if __name__=="__main__":
  goldwordsSyl = set()
  predwordsSyl = set()
  predwords = set()
  for l in open(sys.argv[1]):
    goldwordsSyl.update([x.strip(".") for x in l.strip().split()])

  for l in sys.stdin:
    predwordsSyl.update([x for x in l.strip().split()])
    predwords.update([x.replace(".","") for x in l.strip().split()])

  mismatch = [x for x in goldwordsSyl if x.replace(".","") in predwords and not x in predwordsSyl]
  pairs = []
  for x in mismatch:
    for y in predwordsSyl:
      if y.replace(".","")==x.replace(".",""):
        pairs.append((x,y))
  for (gold,pred) in pairs:
    print "%s as %s"%(gold,pred)
  print predwordsSyl
