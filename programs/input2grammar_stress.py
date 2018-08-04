#!/usr/local/bin/python



usage = """input2grammar_stress.py

  (c) Mark Johnson, 7th August, 2012
  modified by Benjamin Boerschinger, 17th October, 2013

  Builds a grammar for CMUDict style transcriptions [you'll need to modify the phoneme set manually]
  

  settling on an onset-nocoda syllableif-structure
"""

import optparse, re, sys

global vowels, consonants
vowels = "AA AE AH AO AW AY EH ER EY IH IY OW OY UH UW XX".lower().split()
#add XX for unknown vowel
#vowels = "i I e E & a O o U u A 9 Q 7 6 1".split()
glides = "Y W".lower().split()
#glides = "y w".split()
liquids = "L R".lower().split()
#liquids = "l r".split()
nasals = "M N NG".lower().split()
#nasals = "m n N".split()
fricatives = "S Z F V TH DH HH".lower().split()
#fricatives = "s z f v T D h".split()
affricates = "CH JH SH ZH".lower().split()
#affricates = "S G c Z".split()
stops = "B D G K P T".lower().split()
#stops = "b p d t g k".split()

consonants = [stops,affricates,fricatives,nasals,liquids,glides] #indexed with rising sonority

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

"""
  Initial-Final syllable structure (Mark 2009)
"""

"""
  onset-nocoda syllIF header
"""
nostress_if_syll_header_onset_nocoda = """1 1 Wrds --> Word
1 1 Wrds --> Word Wrds
Word --> SyllIF
Word --> Syllables
1 1 Syllables --> SyllI SyllablesR
1 1 SyllablesR --> SyllF
1 1 SyllablesR --> Syll SyllablesR
2 1 SyllIF --> OnsetI RhymeF
1 1 SyllIF --> RhymeF
2 1 SyllI --> OnsetI Rhyme
1 1 SyllI --> Rhyme
2 1 SyllF --> Onset RhymeF
1 1 SyllF --> RhymeF
2 1 Syll --> Onset Rhyme
1 1 Syll --> Rhyme
OnsetI --> ConsO
Onset --> ConsO
2 1 RhymeF --> Vowel Stress
2 1 RhymeF --> Vowel
1 1 RhymeF --> Vowel CodaF
1 1 RhymeF --> Vowel Stress Coda
2 1 Rhyme --> Vowel
2 1 Rhyme --> Vowel Stress
1 1 Rhyme --> Vowel Coda
1 1 Rhyme --> Vowel Stress Coda
CodaF --> ConsC
Coda --> ConsC
1 1 Stress --> *
"""

"""
  generic syllable structure with stress
"""
syll_header_onset_nocoda = """2 1 SyllSIF --> OnsetI RhymeSF
1 1 SyllSIF --> RhymeSF
2 1 SyllUIF --> OnsetI RhymeUF
1 1 SyllUIF --> RhymeUF
2 1 SyllSI --> OnsetI RhymeS
1 1 SyllSI --> RhymeS
2 1 SyllUI --> OnsetI RhymeU
1 1 SyllUI --> RhymeU
2 1 SyllUF --> Onset RhymeUF
1 1 SyllUF --> RhymeUF
2 1 SyllSF --> Onset RhymeSF
1 1 SyllSF --> RhymeSF
2 1 SyllS --> Onset RhymeS
1 1 SyllS --> RhymeS
2 1 SyllU --> Onset RhymeU
1 1 SyllU --> RhymeU
OnsetI --> ConsO
Onset --> ConsO
2 1 RhymeSF --> Vowel Stress
2 1 RhymeUF --> Vowel
1 1 RhymeUF --> Vowel CodaF
1 1 RhymeSF --> Vowel Stress Coda
2 1 RhymeU --> Vowel
2 1 RhymeS --> Vowel Stress
1 1 RhymeU --> Vowel Coda
1 1 RhymeS --> Vowel Stress Coda
CodaF --> ConsC
Coda --> ConsC
1 1 Stress --> *
"""


"""
  generic syllable structure without stress
"""
syll_header_onset_nocoda_nostress = """2 1 SyllIF --> OnsetI RhymeF
1 1 SyllIF --> RhymeF
2 1 SyllI --> OnsetI Rhyme
1 1 SyllI --> Rhyme
2 1 SyllF --> Onset RhymeF
1 1 SyllF --> RhymeF
2 1 Syll --> Onset Rhyme
1 1 Syll --> Rhyme
OnsetI --> ConsO
Onset --> ConsO
2 1 RhymeF --> VX
1 1 RhymeF --> VX CodaF
2 1 Rhyme --> VX
1 1 Rhyme --> VX Coda
CodaF --> ConsC
Coda --> ConsC
1 1 VX --> Vowel
1 1 VX --> Vowel Stress
1 1 Stress --> *
"""

finitenostress_if_syll_header_onset_nocoda = """1 1 Wrds --> Word
1 1 Wrds --> Word Wrds
Word --> SyllIF
Word --> SyllI SyllF
Word --> SyllI Syll SyllF
Word --> SyllI Syll Syll SyllF
"""

nostress_if_syll_header_onset_nocoda = """1 1 Wrds --> Word
1 1 Wrds --> Word Wrds
Word --> SyllIF
Word --> SyllI Syllables
1 1 Syllables --> SyllF
1 1 Syllables --> Syll Syllables
"""

"""
  onset-nocoda syllIF header, weak stress knowledge,
  binary syllables
"""
weakstress_if_syll_header_onset_nocoda = """1 1 Wrds --> Word
1 1 Wrds --> Word Wrds
Word --> SyllSIF
Word --> SyllUIF
Word --> SyllSI SyllablesS
Word --> SyllUI SyllablesU
1 1 SyllablesS --> SyllUF
1 1 SyllablesS --> SyllSF
1 1 SyllablesS --> SyllU SyllablesU
1 1 SyllablesS --> SyllS SyllablesS
1 1 SyllablesU --> SyllUF
1 1 SyllablesU --> SyllSF
1 1 SyllablesU --> SyllU SyllablesU
1 1 SyllablesU --> SyllS SyllablesS
"""


"""
  onset-nocoda syllIF header with stress
  five possibilities - sparse prior, pick one
  also low pseudo-count on unstressed function words,
  shouldn't need to generate lots of those
"""
stressfinite_if_syll_header_onset_nocoda = """1 1 Wrds --> GenWord
1 1 Wrds --> GenWord Wrds
0.1 GenWord --> WordInit
0.1 GenWord --> WordPenInit
0.1 GenWord --> WordUlt
0.1 GenWord --> WordPenUlt
0.1 GenWord --> WordAntePenUlt
0.1 GenWord --> WordNoStress
1 1 WordNoStress --> SyllUIF
1 1 WordNoStress --> SyllUI SyllUF
1 1 WordNoStress --> SyllUI SyllU SyllUF
1 1 WordNoStress --> SyllUI SyllU SyllU SyllUF
1 1 WordInit --> SyllSIF
1 1 WordInit --> SyllSI SyllUF
1 1 WordInit --> SyllSI SyllU SyllUF
1 1 WordInit --> SyllSI SyllU SyllU SyllUF
1 1 WordPenInit --> SyllSIF
1 1 WordPenInit --> SyllUI SyllSF
1 1 WordPenInit --> SyllUI SyllS SyllUF
1 1 WordPenInit --> SyllUI SyllS SyllU SyllUF
1 1 WordUlt --> SyllSIF
1 1 WordUlt --> SyllUI SyllSF
1 1 WordUlt --> SyllUI SyllU SyllSF
1 1 WordUlt --> SyllUI SyllU SyllU SyllSF
1 1 WordPenUlt --> SyllSIF
1 1 WordPenUlt --> SyllSI SyllUF
1 1 WordPenUlt --> SyllUI SyllS SyllUF
1 1 WordPenUlt --> SyllUI SyllU SyllS SyllUF
1 1 WordAntePenUlt --> SyllSIF
1 1 WordAntePenUlt --> SyllSI SyllUF
1 1 WordAntePenUlt --> SyllSI SyllU SyllUF
1 1 WordAntePenUlt --> SyllUI SyllS SyllU SyllUF
"""


"""

"""
stresspos_if_syll_header_onset_nocoda = """1 1 Wrds --> GenWord
1 1 Wrds --> GenWord Wrds
0.1 GenWord --> Word1
0.1 GenWord --> Word2
0.1 GenWord --> Word3
0.1 GenWord --> Word4
0.1 GenWord --> Word5
0.1 GenWord --> Word6
0.1 GenWord --> Word0
1 1 Syllables5 --> SyllUF
1 1 Syllables5 --> SyllU Syllables4
1 1 Syllables4 --> SyllUF
1 1 Syllables4 --> SyllU Syllables3
1 1 Syllables3 --> SyllUF
1 1 Syllables3 --> SyllU Syllables2
1 1 Syllables2 --> SyllUF
1 1 Syllables2 --> SyllU SyllUF
1 1 Word0 --> SyllUIF
1 1 Word0 --> SyllUI Syllables5
1 1 Word1 --> SyllSIF
1 1 Word1 --> SyllSI Syllables5
1 1 Word2 --> SyllUI SyllSF
1 1 Word2 --> SyllUI SyllS Syllables4
1 1 Word3 --> SyllUI SyllU SyllSF
1 1 Word3 --> SyllUI SyllU SyllS Syllables3
1 1 Word4 --> SyllUI SyllU SyllU SyllSF
1 1 Word4 --> SyllUI SyllU SyllU SyllS Syllables2
1 1 Word5 --> SyllUI SyllU SyllU SyllU SyllSF
1 1 Word5 --> SyllUI SyllU SyllU SyllU SyllS SyllUF
1 1 Word6 --> SyllUI SyllU SyllU SyllU SyllU SyllSF
"""



"""
  onset-nocoda syllIF header with stress
  five possibilities - sparse prior, pick one
  also low pseudo-count on unstressed function words,
  shouldn't need to generate lots of those
"""
stress_if_syll_header_onset_nocoda = """1 1 Wrds --> GenWord
1 1 Wrds --> GenWord Wrds
0.005 GenWord --> WordInit
0.005 GenWord --> WordPenInit
0.005 GenWord --> WordUlt
0.005 GenWord --> WordPenUlt
0.005 GenWord --> WordAntePenUlt
0.005 GenWord --> WordNoStress
1 1 WordNoStress --> SyllUIF
1 1 WordNoStress --> SyllUI Syllables_U
1 1 WordInit --> SyllSIF
1 1 WordInit --> SyllSI Syllables_U
1 1 WordPenInit --> SyllSIF
1 1 WordPenInit --> SyllUI SyllablesS_U
1 1 WordUlt --> SyllSIF
1 1 WordUlt --> SyllUI Syllables_S
1 1 WordPenUlt --> SyllSIF
1 1 WordPenUlt --> SyllSI SyllUF
1 1 WordPenUlt --> SyllUI Syllables_SU
1 1 WordAntePenUlt --> SyllSIF
1 1 WordAntePenUlt --> SyllSI Syllables_UU
1 1 WordAntePenUlt --> SyllUI Syllables_SUU
1 1 Syllables_U --> SyllUF
1 1 Syllables_U --> SyllU Syllables_U
1 1 SyllablesS_U --> SyllSF
1 1 SyllablesS_U --> SyllS Syllables_U
1 1 Syllables_S --> SyllU Syllables_S
1 1 Syllables_S --> SyllSF
1 1 Syllables_SU --> SyllU SyllablesSU
1 1 Syllables_SU --> SyllS SyllUF
1 1 Syllables_UU --> SyllUF
1 1 Syllables_UU --> SyllU SyllUF
1 1 Syllables_SUU --> SyllU Syllables_SUU
1 1 Syllables_SUU --> SyllS SyllU SyllUF
"""


def noUSCHeader(n,outf,sparsity=1.0):
    """
      generate all patterns up to length n of Strong/Weak-Syllables
    """
    outf.write("1 1 Wrds --> Word\n")
    outf.write("1 1 Wrds --> Word Wrds\n")
    outf.write("%f Word --> SyllSIF\n"%sparsity)
    outf.write("%f Word --> SyllUIF\n"%sparsity)
    for l in range(2,n+1):
        outf.write("%f Word --> "%sparsity+" ".join(["SyllUI"]+["SyllU" for j in range(l-2)]+["SyllUF"])+"\n")
        for i in range(1,2**l):
            pat = bin(i)[2:]
            if len(pat)!=l: #pad it with vacuous zeros
                pat = "0"*(l-len(pat))+pat
            res = ["%f Word"%sparsity,"-->"]
            for (pos,c) in enumerate(pat):
                if c=="0":
                    if pos==0:
                        res.append("SyllUI")
                    else:
                        res.append("SyllU")
                elif c=="1":
                    if pos==0:
                        res.append("SyllSI")
                    else:
                        res.append("SyllS")
            # final syllable has to be final
            res[-1] = "SyllSF" if res[-1]=="SyllS" else "SyllUF"
            outf.write(" ".join(res)+"\n")
    outf.write(syll_header_onset_nocoda)

"""
  Sonority sequencing for consonants
  if unbiased=True, then all sequences are apriori considered to be equal
"""
def consSonor(outf,unbiased=False,scale=10.0):
    sonConsOns(outf,unbiased,scale)
    sonConsCod(outf,unbiased,scale)
    sonCons(outf)

"""
  Sonority sequencing in onsets --- from low to high
  that is, disprefer going from higher to lower sonority
  if unbiased=True, then all sequences are apriori considered to be equal
"""
def sonConsOns(outf,unbiased=False,scale=10):
    for i in range(len(consonants)):
        outf.write("1 1 ConsO --> ConsO%s\n"%i)
        outf.write("1 1 ConsO%s --> C%s\n"%(i,i))
        for j in range(len(consonants)):
            prior = 1 if unbiased else scale*(j-i+1) if j>i else 1.0 if i==j else 1/(scale*(i-j+1))
            outf.write("%s 1 ConsO%s --> C%s ConsO%s\n"%(prior,i,i,j))


"""
  Sonority sequencing in codas --- from high to low
  that is, disprefer going from lower to higher
  if unbiased=True, then all sequences are apriori considered to be equal
"""
def sonConsCod(outf,unbiased=False,scale=10):
    for i in range(len(consonants)):
        outf.write("1 1 ConsC --> ConsC%s\n"%i)
        outf.write("1 1 ConsC%s --> C%s\n"%(i,i))
        for j in range(len(consonants)):
            prior = 1 if unbiased else scale*(i-j+1) if j<i else 1 if i==j else 1/(scale*(j-i+1))
            outf.write("%s 1 ConsC%s --> C%s ConsC%s\n"%(prior,i,i,j))

"""
  the consonants in their respective classes
"""
def sonCons(outf):
    for i in range(len(consonants)):
        for c in consonants[i]:
            outf.write("1 1 C%s --> %s\n"%(i,c))

"""
  all consonants without classes
"""
def cons(outf):
    outf.write("1 1 ConsC --> Consonants\n")
    outf.write("1 1 ConsO --> Consonants\n")
    outf.write("1 1 Consonants --> Consonant\n")
    outf.write("1 1 Consonants --> Consonant Consonants\n")
    for conses in consonants:
        for c in conses:
            outf.write("1 1 Consonant --> %s\n"%c)

"""
  all vowels
  special high count for xx because unseen at test-time might lead to underflow problems
"""
def vwls(outf):
    for v in vowels:
        if v=="xx":
            outf.write("1 1 Vowel --> xx\n")
        else:
            outf.write("1 1 Vowel --> %s\n"%v)

def syllIFnostress(sonor=False,noBiasSonor=False):
    def inner(outf):
        outf.write(nostress_if_syll_header_onset_nocoda)
        outf.write(syll_header_onset_nocoda_nostress)
        if sonor:
            consSonor(outf,noBiasSonor)
        else:
            cons(outf)
        vwls(outf)
    return inner


def syllIFfinitenostress(sonor=False,noBiasSonor=False):
    def inner(outf):
        outf.write(finitenostress_if_syll_header_onset_nocoda)
        outf.write(syll_header_onset_nocoda_nostress)
        if sonor:
            consSonor(outf,noBiasSonor)
        else:
            cons(outf)
        vwls(outf)
    return inner

def syllIFstress(sonor=False,noBiasSonor=False):
    def inner(outf):
        outf.write(stress_if_syll_header_onset_nocoda)
        outf.write(syll_header_onset_nocoda)
        if sonor:
            consSonor(outf,noBiasSonor)
        else:
            cons(outf)
        vwls(outf)
    return inner




def syllIFstresspos(sonor=False,noBiasSonor=False):
    def inner(outf):
        outf.write(stresspos_if_syll_header_onset_nocoda)
        outf.write(syll_header_onset_nocoda)
        if sonor:
            consSonor(outf,noBiasSonor)
        else:
            cons(outf)
        vwls(outf)
    return inner

def syllIFfinitestress(sonor=False,noBiasSonor=False):
    def inner(outf):
        outf.write(stressfinite_if_syll_header_onset_nocoda)
        outf.write(syll_header_onset_nocoda)
        if sonor:
            consSonor(outf,noBiasSonor)
        else:
            cons(outf)
        vwls(outf)
    return inner


def syllIFweakstress(sonor=False,noBiasSonor=False):
    def inner(outf):
        outf.write(weakstress_if_syll_header_onset_nocoda)
        outf.write(syll_header_onset_nocoda)
        if sonor:
            consSonor(outf,noBiasSonor)
        else:
            cons(outf)
        vwls(outf)
    return inner

def syllIFallpatterns(sonor=False,noBiasSonor=False):
    def inner(outf):
        noUSCHeader(6,outf)
        outf.write(syll_header_onset_nocoda)
        if sonor:
            consSonor(outf,noBiasSonor)
        else:
            cons(outf)
        vwls(outf)
    return inner

def collocsyllIFallpatterns(n=1,sonor=False,noBiasSonor=False):
    def inner(outf):
        if n==1:
            outf.write(colloc_header)
            syllIFallpatterns(sonor,noBiasSonor)(outf)
        elif n==2:
            outf.write(colloc2_header)
            collocsyllIFallpatterns(n-1,sonor,noBiasSonor)(outf)
        elif n==3:
            outf.write(colloc3_header)
            collocsyllIFallpatterns(n-1,sonor,noBiasSonor)(outf)
    return inner


def collocsyllIFstresspos(n=1,sonor=False,noBiasSonor=False):
    def inner(outf):
        if n==1:
            outf.write(colloc_header)
            syllIFstresspos(sonor,noBiasSonor)(outf)
        elif n==2:
            outf.write(colloc2_header)
            collocsyllIFstresspos(n-1,sonor,noBiasSonor)(outf)
        elif n==3:
            outf.write(colloc3_header)
            collocsyllIFstresspos(n-1,sonor,noBiasSonor)(outf)
    return inner

def collocsyllIFnostress(n=1,sonor=False,noBiasSonor=False):
    def inner(outf):
        if n==1:
            outf.write(colloc_header)
            syllIFnostress(sonor,noBiasSonor)(outf)
        elif n==2:
            outf.write(colloc2_header)
            collocsyllIFnostress(n-1,sonor,noBiasSonor)(outf)
        elif n==3:
            outf.write(colloc3_header)
            collocsyllIFnostress(n-1,sonor,noBiasSonor)(outf)
    return inner

def collocsyllIFfinitenostress(n=1,sonor=False,noBiasSonor=False):
    def inner(outf):
        if n==1:
            outf.write(colloc_header)
            syllIFfinitenostress(sonor,noBiasSonor)(outf)
        elif n==2:
            outf.write(colloc2_header)
            collocsyllIFfinitenostress(n-1,sonor,noBiasSonor)(outf)
        elif n==3:
            outf.write(colloc3_header)
            collocsyllIFfinitenostress(n-1,sonor,noBiasSonor)(outf)
    return inner

def collocsyllIFstress(n=1,sonor=False,noBiasSonor=False):
    def inner(outf):
        if n==1:
            outf.write(colloc_header)
            syllIFstress(sonor,noBiasSonor)(outf)
        elif n==2:
            outf.write(colloc2_header)
            collocsyllIFstress(n-1,sonor,noBiasSonor)(outf)
        elif n==3:
            outf.write(colloc3_header)
            collocsyllIFstress(n-1,sonor,noBiasSonor)(outf)
    return inner


def collocsyllIFfinitestress(n=1,sonor=False,noBiasSonor=False):
    def inner(outf):
        if n==1:
            outf.write(colloc_header)
            syllIFfinitestress(sonor,noBiasSonor)(outf)
        elif n==2:
            outf.write(colloc2_header)
            collocsyllIFfinitestress(n-1,sonor,noBiasSonor)(outf)
        elif n==3:
            outf.write(colloc3_header)
            collocsyllIFfinitestress(n-1,sonor,noBiasSonor)(outf)
    return inner


def collocsyllIFweakstress(n=1,sonor=False,noBiasSonor=False):
    def inner(outf):
        if n==1:
            outf.write(colloc_header)
            syllIFweakstress(sonor,noBiasSonor)(outf)
        elif n==2:
            outf.write(colloc2_header)
            collocsyllIFweakstress(n-1,sonor,noBiasSonor)(outf)
        elif n==3:
            outf.write(colloc3_header)
            collocsyllIFweakstress(n-1,sonor,noBiasSonor)(outf)
    return inner


# grammar_writer maps the grammar's name to
# the program that writes that grammar

grammar_writer = { 'syllIFnostress':syllIFnostress(False,True),
                   'syllIFnostresssonor':syllIFnostress(True,True),
                   'syllIFnostresssonorBias':syllIFnostress(True,False),
                   'collocsyllIFnostress':collocsyllIFnostress(1,False,True),
                   'collocsyllIFnostresssonor':collocsyllIFnostress(1,True,True),
                   'collocsyllIFnostresssonorBias':collocsyllIFnostress(1,True,False),
                   'colloc2syllIFnostress':collocsyllIFnostress(2,False,True),
                   'colloc2syllIFnostresssonor':collocsyllIFnostress(2,True,True),
                   'colloc2syllIFnostresssonorBias':collocsyllIFnostress(2,True,False),
                   'colloc3syllIFnostress':collocsyllIFnostress(3,False,True),
                   'colloc3syllIFnostresssonor':collocsyllIFnostress(3,True,True),
                   'colloc3syllIFnostresssonorBias':collocsyllIFnostress(3,True,False),
                   'syllIFstresspos':syllIFstresspos(False,True),
                   'syllIFstresspossonor':syllIFstresspos(True,True),
                   'syllIFstresspossonorBias':syllIFstresspos(True,False),
                   'collocsyllIFstresspos':collocsyllIFstresspos(1,False,True),
                   'collocsyllIFstresspossonor':collocsyllIFstresspos(1,True,True),
                   'collocsyllIFstresspossonorBias':collocsyllIFstresspos(1,True,False),
                   'colloc2syllIFstresspos':collocsyllIFstresspos(2,False,True),
                   'colloc2syllIFstresspossonor':collocsyllIFstresspos(2,True,True),
                   'colloc2syllIFstresspossonorBias':collocsyllIFstresspos(2,True,False),
                   'colloc3syllIFstresspos':collocsyllIFstresspos(3,False,True),
                   'colloc3syllIFstresspossonor':collocsyllIFstresspos(3,True,True),
                   'colloc3syllIFstresspossonorBias':collocsyllIFstresspos(3,True,False),
                   'syllIFfinitenostress':syllIFfinitenostress(False,True),
                   'syllIFfinitenostresssonor':syllIFfinitenostress(True,True),
                   'syllIFfinitenostresssonorBias':syllIFfinitenostress(True,False),
                   'collocsyllIFfinitenostress':collocsyllIFfinitenostress(1,False,True),
                   'collocsyllIFfinitenostresssonor':collocsyllIFfinitenostress(1,True,True),
                   'collocsyllIFfinitenostresssonorBias':collocsyllIFfinitenostress(1,True,False),
                   'colloc2syllIFfinitenostress':collocsyllIFfinitenostress(2,False,True),
                   'colloc2syllIFfinitenostresssonor':collocsyllIFfinitenostress(2,True,True),
                   'colloc2syllIFfinitenostresssonorBias':collocsyllIFfinitenostress(2,True,False),
                   'colloc3syllIFfinitenostress':collocsyllIFfinitenostress(3,False,True),
                   'colloc3syllIFfinitenostresssonor':collocsyllIFfinitenostress(3,True,True),
                   'colloc3syllIFfinitenostresssonorBias':collocsyllIFfinitenostress(3,True,False),
                   'syllIFstress':syllIFstress(False,True),
                   'syllIFstresssonor':syllIFstress(True,True),
                   'syllIFstresssonorBias':syllIFstress(True,False),
                   'collocsyllIFstress':collocsyllIFstress(1,False,True),
                   'collocsyllIFstresssonor':collocsyllIFstress(1,True,True),
                   'collocsyllIFstresssonorBias':collocsyllIFstress(1,True,False),
                   'colloc2syllIFstress':collocsyllIFstress(2,False,True),
                   'colloc2syllIFstresssonor':collocsyllIFstress(2,True,True),
                   'colloc2syllIFstresssonorBias':collocsyllIFstress(2,True,False),
                   'colloc3syllIFstress':collocsyllIFstress(3,False,True),
                   'colloc3syllIFstresssonor':collocsyllIFstress(3,True,True),
                   'colloc3syllIFstresssonorBias':collocsyllIFstress(3,True,False),
                   'syllIFweakstress':syllIFweakstress(False,True),
                   'syllIFweakstresssonor':syllIFweakstress(True,True),
                   'syllIFweakstresssonorBias':syllIFweakstress(True,False),
                   'collocsyllIFweakstress':collocsyllIFweakstress(1,False,True),
                   'collocsyllIFweakstresssonor':collocsyllIFweakstress(1,True,True),
                   'collocsyllIFweakstresssonorBias':collocsyllIFweakstress(1,True,False),
                   'colloc2syllIFweakstress':collocsyllIFweakstress(2,False,True),
                   'colloc2syllIFweakstresssonor':collocsyllIFweakstress(2,True,True),
                   'colloc2syllIFweakstresssonorBias':collocsyllIFweakstress(2,True,False),
                   'colloc3syllIFweakstress':collocsyllIFweakstress(3,False,True),
                   'colloc3syllIFweakstresssonor':collocsyllIFweakstress(3,True,True),
                   'colloc3syllIFweakstresssonorBias':collocsyllIFweakstress(3,True,False),
                   'syllIFallpatterns':syllIFallpatterns(False,True),
                   'syllIFallpatternssonor':syllIFallpatterns(True,True),
                   'syllIFallpatternssonorBias':syllIFallpatterns(True,False),
                   'collocsyllIFallpatterns':collocsyllIFallpatterns(1,False,True),
                   'collocsyllIFallpatternssonor':collocsyllIFallpatterns(1,True,True),
                   'collocsyllIFallpatternssonorBias':collocsyllIFallpatterns(1,True,False),
                   'colloc2syllIFallpatterns':collocsyllIFallpatterns(2,False,True),
                   'colloc2syllIFallpatternssonor':collocsyllIFallpatterns(2,True,True),
                   'colloc2syllIFallpatternssonorBias':collocsyllIFallpatterns(2,True,False),
                   'colloc3syllIFallpatterns':collocsyllIFallpatterns(3,False,True),
                   'colloc3syllIFallpatternssonor':collocsyllIFallpatterns(3,True,True),
                   'syllIFfinitestress':syllIFfinitestress(False,True),
                   'syllIFfinitestresssonor':syllIFfinitestress(True,True),
                   'syllIFfinitestresssonorBias':syllIFfinitestress(True,False),
                   'collocsyllIFfinitestress':collocsyllIFfinitestress(1,False,True),
                   'collocsyllIFfinitestresssonor':collocsyllIFfinitestress(1,True,True),
                   'collocsyllIFfinitestresssonorBias':collocsyllIFfinitestress(1,True,False),
                   'colloc2syllIFfinitestress':collocsyllIFfinitestress(2,False,True),
                   'colloc2syllIFfinitestresssonor':collocsyllIFfinitestress(2,True,True),
                   'colloc2syllIFfinitestresssonorBias':collocsyllIFfinitestress(2,True,False),
                   'colloc3syllIFfinitestress':collocsyllIFfinitestress(3,False,True),
                   'colloc3syllIFfinitestresssonor':collocsyllIFfinitestress(3,True,True),
                   'colloc3syllIFfinitestresssonorBias':collocsyllIFfinitestress(3,True,False),
                   'colloc3syllIFfinitestresssonorBias':collocsyllIFfinitestress(3,True,False),
                   }

if __name__ == '__main__':
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-g", "--grammar", dest="grammar", default="unigram",
                      help="type of grammar to produce")
    parser.add_option("-l", "--list-grammars", dest='list_grammars', action='store_true',
                      help="print out names of grammars that we can generate")
    options, args = parser.parse_args()

    if options.list_grammars:
        sys.stdout.write(' '.join(sorted(grammar_writer.keys())))
        sys.stdout.write('\n')
        sys.exit(0)

    writer = grammar_writer.get(options.grammar)
    if not writer:
        sys.exit("Unknown grammar: {}\nAvailable grammars: {}\n".format(
                options.grammar, ' '.join(sorted(grammar_writer.keys()))))

    if len(args) == 0:
        inf = sys.stdin
    else:
        assert(len(args) == 1)
        inf = open(args[0], "rU")

    writer(sys.stdout)
