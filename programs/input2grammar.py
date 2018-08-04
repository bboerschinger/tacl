usage = """input2grammar_stress.py

  (c) Mark Johnson, 7th August, 2012
  modified by Benjamin Boerschinger, 17th October, 2013

  Builds a grammar for CMUDict style transcriptions [you'll need to modify the phoneme set manually]
"""

import optparse, re, sys, os

global vowels, consonants, wordlevel, syllevel

ONSNOCODABIAS = 10
NOONSCODABIAS = 1

wordlevel = {}
syllevel = {}

#XX is unknown vowel for heldout
vowels = "AA AE AH AO AW AY EH ER EY IH IY OW OY UH UW XX".lower().split()
glides = "Y W".lower().split()
liquids = "L R".lower().split()
nasals = "M N NG".lower().split()
fricatives = "S Z F V TH DH HH".lower().split()
affricates = "CH JH SH ZH".lower().split()
stops = "B D G K P T".lower().split()

consonants = [stops,affricates,fricatives,nasals,liquids,glides] #indexed with rising sonority

"""still learning syllable-phonotactics, but no correlation with wbs"""
onset_coda_pattern = """Onset --> Consonants
Coda --> Consonants
"""

"""don't memorize onsets and codas"""
onset_coda_nolearn_patter = """1 1 Onset --> Consonants
1 1 Coda --> Consonants
"""

consonants_pattern = """2 1 Consonants --> Consonant
1 1 Consonants --> Consonant Consonants
"""

onseti_codaf_pattern = """OnsetI --> Consonants
CodaF --> Consonants
Onset --> Consonants
Coda --> Consonants
"""

colloc_header = """1 1 Collocs --> Colloc
1 1 Collocs --> Colloc Collocs
Colloc --> Wrds
"""

colloc2_header = """1 1 Collocs2 --> Colloc2
1 1 Collocs2 --> Colloc2 Collocs2
Colloc2 --> Collocs
"""
colloc3_header = """1 1 Collocs3 --> Colloc3
1 1 Collocs3 --> Colloc3 Collocs3
Colloc3 --> Collocs2
"""

syllevel["syllables_stress_nophon"] = os.linesep.join([ s for s in ("""{0} 1 SyllS --> Onset RhymeS
{1} 1 SyllS --> RhymeS
{0} 1 SyllU --> Onset RhymeU
{1} 1 SyllU --> RhymeU
{0} 1 RhymeS --> Vowel Stress
{1} 1 RhymeS --> Vowel Stress Coda
{0} 1 RhymeU --> Vowel
{1} 1 RhymeU --> Vowel Coda
1 1 Stress --> *
{2}
{3}
""".format(ONSNOCODABIAS,NOONSCODABIAS,onset_coda_pattern,consonants_pattern)).splitlines() if s])+os.linesep

syllevel["syllables_stress_phon"] = os.linesep.join([ s for s in ("""{0} 1 SyllUI --> OnsetI RhymeU
{1} 1 SyllUI --> RhymeU
{0} 1 SyllUF --> Onset RhymeUF
{1} 1 SyllUF --> RhymeUF
{0} 1 SyllUIF --> OnsetI RhymeUF
{1} 1 SyllUIF --> RhymeUF
{0} 1 SyllU --> Onset RhymeU
{1} 1 SyllU --> RhymeU
{0} 1 SyllSI --> OnsetI RhymeS
{1} 1 SyllSI --> RhymeS
{0} 1 SyllSF --> Onset RhymeSF
{1} 1 SyllSF --> RhymeSF
{0} 1 SyllSIF --> OnsetI RhymeSF
{1} 1 SyllSIF --> RhymeSF
{0} 1 SyllS --> Onset RhymeS
{1} 1 SyllS --> RhymeS
{0} 1 RhymeU --> Vowel
{1} 1 RhymeU --> Vowel Coda
{0} 1 RhymeUF --> Vowel
{1} 1 RhymeUF --> Vowel CodaF
{0} 1 RhymeS --> Vowel Stress
{1} 1 RhymeS --> Vowel Stress Coda
{0} 1 RhymeSF --> Vowel Stress
{1} 1 RhymeSF --> Vowel Stress CodaF
1 1 Stress --> *
{2}
{3}
""".format(ONSNOCODABIAS,NOONSCODABIAS,onseti_codaf_pattern,consonants_pattern)).splitlines() if s])+os.linesep

syllevel["syllables_nostress_nophon"] = os.linesep.join([ s for s in ("""{0} 1 Syll --> Onset Rhyme
{1} 1 Syll --> Rhyme
{0} 1 Rhyme --> Vowel
{1} 1 Rhyme --> Vowel Coda
{2}
{3}
""".format(ONSNOCODABIAS,NOONSCODABIAS,onset_coda_pattern,consonants_pattern)).splitlines() if s])+os.linesep

syllevel["syllables_nostress_phon"] = os.linesep.join([ s for s in ("""{0} 1 SyllI --> OnsetI Rhyme
{1} 1 SyllI --> Rhyme
{0} 1 SyllF --> Onset RhymeF
{1} 1 SyllF --> RhymeF
{0} 1 Syll --> Onset Rhyme
{1} 1 Syll --> Rhyme
{0} 1 Rhyme --> Vowel
{1} 1 Rhyme --> Vowel Coda
{0} 1 RhymeF --> Vowel
{1} 1 RhymeF --> Vowel CodaF
{2}
{3}
""".format(ONSNOCODABIAS,NOONSCODABIAS,onseti_codaf_pattern,consonants_pattern)).splitlines() if s])+os.linesep


wordlevel["allpatterns_nophon"] = """1 1 Wrds --> Word
1 1 Wrds --> Word Wrds
Word --> SyllU
Word --> SyllS
Word --> SyllU SyllU
Word --> SyllU SyllS
Word --> SyllS SyllU
Word --> SyllU SyllU SyllU
Word --> SyllU SyllS SyllU
Word --> SyllU SyllU SyllS
Word --> SyllS SyllU SyllU
Word --> SyllU SyllU SyllU SyllU
Word --> SyllU SyllS SyllU SyllU
Word --> SyllU SyllU SyllS SyllU
Word --> SyllU SyllU SyllU SyllS
Word --> SyllS SyllU SyllU SyllU
Word --> SyllU SyllU SyllU SyllU SyllU
Word --> SyllS SyllU SyllU SyllU SyllU
Word --> SyllU SyllS SyllU SyllU SyllU
Word --> SyllU SyllU SyllS SyllU SyllU
Word --> SyllU SyllU SyllU SyllS SyllU
Word --> SyllU SyllU SyllU SyllU SyllS
Word --> SyllU SyllU SyllU SyllU SyllU SyllU
Word --> SyllS SyllU SyllU SyllU SyllU SyllU
Word --> SyllU SyllS SyllU SyllU SyllU SyllU
Word --> SyllU SyllU SyllS SyllU SyllU SyllU
Word --> SyllU SyllU SyllU SyllS SyllU SyllU
Word --> SyllU SyllU SyllU SyllU SyllS SyllU
Word --> SyllU SyllU SyllU SyllU SyllU SyllS
"""

wordlevel["allpatterns_phon"] = """1 1 Wrds --> Word
1 1 Wrds --> Word Wrds
Word --> SyllUIF
Word --> SyllSIF
Word --> SyllUI SyllUF
Word --> SyllUI SyllSF
Word --> SyllSI SyllUF
Word --> SyllUI SyllU SyllUF
Word --> SyllUI SyllS SyllUF
Word --> SyllUI SyllU SyllSF
Word --> SyllSI SyllU SyllUF
Word --> SyllUI SyllU SyllU SyllUF
Word --> SyllUI SyllS SyllU SyllUF
Word --> SyllUI SyllU SyllS SyllUF
Word --> SyllUI SyllU SyllU SyllSF
Word --> SyllSF SyllU SyllU SyllUF
Word --> SyllUI SyllU SyllU SyllU SyllUF
Word --> SyllSI SyllU SyllU SyllU SyllUF
Word --> SyllUI SyllS SyllU SyllU SyllUF
Word --> SyllUI SyllU SyllS SyllU SyllUF
Word --> SyllUI SyllU SyllU SyllS SyllUF
Word --> SyllUI SyllU SyllU SyllU SyllSF
Word --> SyllUI SyllU SyllU SyllU SyllU SyllUF
Word --> SyllSI SyllU SyllU SyllU SyllU SyllUF
Word --> SyllUI SyllS SyllU SyllU SyllU SyllUF
Word --> SyllUI SyllU SyllS SyllU SyllU SyllUF
Word --> SyllUI SyllU SyllU SyllS SyllU SyllUF
Word --> SyllUI SyllU SyllU SyllU SyllS SyllUF
Word --> SyllUI SyllU SyllU SyllU SyllU SyllSF
"""

wordlevel["nostress_nophon"] = """1 1 Wrds --> Word
1 1 Wrds --> Word Wrds
Word --> Sllbls
1 1 Sllbls --> Syll
1 1 Sllbls --> Syll Sllbls
"""

wordlevel["nostress_phon"] = """1 1 Wrds --> Word
1 1 Wrds --> Word Wrds 
Word --> SyllIF
Word --> SyllI Sllbls
1 1 Sllbls --> SyllF
1 1 Sllbls --> Syll Sllbls
"""

wordlevel["lrcount_nophon"] = """1 1 Wrds --> Pattern
1 1 Wrds --> Pattern Wrds
0.1 Pattern --> WordLB0
0.1 Pattern --> WordLB1
0.1 Pattern --> WordRB0
0.1 Pattern --> WordRB1
0.1 Pattern --> WordNoStress
1 1 WordNoStress --> SllLUs
1 1 WordLB0 --> SyllS
1 1 WordLB0 --> SyllS SllLUs
1 1 WordLB1 --> SyllS
1 1 WordLB1 --> SyllU SllLSUs
1 1 WordRB0 --> SyllS
1 1 WordRB0 --> SllRUs SyllS
1 1 WordRB1 --> SyllS
1 1 WordRB1 --> SllRSUs SyllU
1 1 SllLUs --> SyllU
1 1 SllLUs --> SyllU SllLUs
1 1 SllLSUs --> SyllS
1 1 SllSUs --> SyllS SllLUs
1 1 SllRUs --> SyllU
1 1 SllRUs --> SllRUs SyllU
1 1 SllRSUs --> SyllS
1 1 SllRSUs --> SllRUs SyllS
"""

wordlevel["lrcount_phon"] = """1 1 Wrds --> Pattern
1 1 Wrds --> Pattern Wrds
0.1 Pattern --> WordLB0
0.1 Pattern --> WordLB1
0.1 Pattern --> WordRB0
0.1 Pattern --> WordRB1
0.1 Pattern --> WordNoStress
1 1 WordNoStress --> SyllUIF
1 1 WordNoStress --> SyllUI SllLUs
1 1 WordLB0 --> SyllSIF
1 1 WordLB0 --> SyllSI SllLUs
1 1 WordLB1 --> SyllSIF
1 1 WordLB1 --> SyllUI SllLSUs
1 1 WordRB0 --> SyllSIF
1 1 WordRB0 --> SllRUs SyllSF
1 1 WordRB1 --> SyllSIF
1 1 WordRB1 --> SllRSUs SyllUF
1 1 SllLUs --> SyllUF
1 1 SllLUs --> SyllU SllLUs
1 1 SllLSUs --> SyllSF
1 1 SllSUs --> SyllS SllLUs
1 1 SllRUs --> SyllUI
1 1 SllRUs --> SllRUs SyllU
1 1 SllRSUs --> SyllSI
1 1 SllRSUs --> SllRUs SyllS
"""

def colloc(outf,n=3,stress=True,pattern="lrcount",phon=True,knowSymbols=True):
    global wordlevel,syllevel
#    print n,stress,pattern,phon,knowSymbols
    if n<=1:
        if n==1:
            outf.write("%s"%colloc_header)
        if not stress:
            wkey = "nostress_%s"%("phon" if phon else "nophon")
        else:
            wkey = "%s_%s"%(pattern,"phon" if phon else "nophon")
        outf.write(wordlevel[wkey])
        skey = "syllables_%s_%s"%("stress" if stress else "nostress","phon" if phon else "nophon")
        outf.write(syllevel[skey])
        if knowSymbols:
            writeGoldClasses(outf)
        else:
            writeUnknownClasses(outf)
    else:
        outf.write(eval("colloc%s_header"%n))
        colloc(outf,n-1,stress,pattern,phon,knowSymbols)

def writeGoldClasses(outf):
    global vowels, consonants
    for v in vowels:
        outf.write("1 1 Vowel --> %s\n"%v)
    for cc in consonants:
        for c in cc:
            outf.write("1 1 Consonant --> %s\n"%c)

def writeUnknownClasses(outf):
    global vowels, consonants
    for v in vowels:
        if v != "xx":
            outf.write("0.01 1 Vowel --> %s\n"%v)
            outf.write("0.01 1 Consonant --> %s\n"%v)
        else:
            outf.write("1 1 Vowel --> xx\n")
    for cc in consonants:
        for c in cc:
            outf.write("0.01 1 Vowel --> %s\n"%c)
            outf.write("0.01 1 Consonant --> %s\n"%c)     

grammar_writer = { }

def initGrammarWriter():
    global grammar_writer
    def grammar(n,stress,pattern,phon,gold):
        return lambda x: colloc(x,n,stress,pattern,phon,gold)
    for n in range(0,4):
        for phon in [True,False]:
            for stress in [True,False]:
                for gold in [True,False]:
                    for pattern in ["lrcount","allpatterns"]:
                        name = "colloc%s-"%(n) if n>1 else "colloc-" if n==1 else ""
                        name += "phon" if phon else "nophon"
                        name += "-stress" if stress else "-nostress"
                        name += "-gold" if gold else "-nogold"
                        name += "-%s"%(pattern) if stress else ""
                        grammar_writer[name] = grammar(n,stress,pattern,phon,gold)


if __name__=="__main__":
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-g", "--grammar", dest="grammar", default="unigram",
                      help="type of grammar to produce")
    parser.add_option("-l", "--list-grammars", dest='list_grammars', action='store_true',
                      help="print out names of grammars that we can generate")
    options, args = parser.parse_args()
    initGrammarWriter()
    if options.list_grammars:
        sys.stdout.write('  '+'\n  '.join(sorted(grammar_writer.keys())))
        sys.stdout.write('\n')
        sys.exit(0)
    writer = grammar_writer.get(options.grammar)
    if not writer:
        sys.exit("Unknown grammar: {}\nAvailable grammars:\n  {}\n".format(
                options.grammar, '\n  '.join(sorted(grammar_writer.keys()))))
    writer(sys.stdout)
