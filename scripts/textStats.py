import sys, optparse, re

usage = """calculate simple summary statistics for text-file
-w  wordseparator, e.g. ".| "
-s  segmentseparator, e.g. " "
-S  syllableseparator, e.g. ". "
"""

def incr(hm,k):
    try:
        hm[k]+=1
    except KeyError:
        hm[k]=1

if __name__=="__main__":	
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-s", "--seg", dest="segBound", default=r" ")
    parser.add_option("-w", "--word", dest="wBound", default=r"\.\| ")
    parser.add_option("-S", "--syl", dest="sylBound", default=r"\. ")
    parser.add_option("-p", "--points", dest="points", default="1 2 5 10 20 50 100 200 500 1000 2000 5000 9790")
    options, args = parser.parse_args()
    segBound = re.compile(options.segBound)
    wBound = re.compile(options.wBound)
    sylBound = re.compile(options.sylBound)
    sizes = [int(x) for x in options.points.split()]
    print "sample,types,tokens,typtokratio,utterances,uttlenwords,uttlenphones,uttlensylls,toklenphones,toklensylls,typlenphones,typlensylls"
    files = [open(f) for f in args]
    seen = 0
    wordCounts = [{} for i in args]
    uttLenWords = [[] for i in args]
    uttLenPhones = [[] for i in args]
    uttLenSylls = [[] for i in args]
    while seen < sizes[-1]:
        seen+=1
        for i in range(len(files)):
            l = files[i].readline().strip().rstrip(options.sylBound).rstrip(options.wBound)
            words = wBound.split(l)
            uttLenWords[i].append(len(words))
            syllables = [sylBound.split(w) for w in words]
            phones = [[segBound.split(s) for s in sylBound.split(w)] for w in words]
            uttLenSylls[i].append(sum([len(w) for w in syllables]))
            uttLenPhones[i].append(sum([sum([len(s) for s in w]) for w in phones]))
            for w in words:
                incr(wordCounts[i],"".join(w))
            if seen in sizes:
                totalPhonsTok = 0
                totalPhonsTyp = 0
                totalSyllsTok = 0
                totalSyllsTyp = 0
                for (w,c) in wordCounts[i].iteritems():
                    sylls = sylBound.split(w)
                    totalSyllsTyp += len(sylls)
                    totalSyllsTok += len(sylls)*c
                    phons = segBound.split(w)
                    totalPhonsTyp += len(phons)
                    totalPhonsTok += len(phons)*c
                tokens = sum(wordCounts[i].values())
                types = len(wordCounts[i])
                print "%d,%d,%d,%.3f,%d,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f"%(i,len(wordCounts[i]),sum(wordCounts[i].values()),float(sum(wordCounts[i].values()))/len(wordCounts[i]),len(uttLenWords[i]),sum(uttLenWords[i])/float(len(uttLenWords[i])),sum(uttLenPhones[i])/float(len(uttLenPhones[i])),sum(uttLenSylls[i])/float(len(uttLenSylls[i])),float(totalPhonsTok)/tokens,float(totalSyllsTok)/tokens,float(totalPhonsTyp)/types,float(totalSyllsTyp)/types)
