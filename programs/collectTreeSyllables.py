#!/usr/local/bin/python


import sys,tb,optparse,re

usage="""
    extracts both word-segmentation and syllabification from an (adaptor-grammar) tree
"""


def visitTree(tree,words,wCat,sCat,segSep,sylSep,noLabel):
    """
        Performs a pre-order traversal of tree, and collects syllable and word boundaries
    """
    def buildSyllable(sTree,segments,noLabel):
        c = tb.tree_category(sTree)
        if c=="C0" or c=="C1" or c=="C2" or c=="C3" or c=="C4" or c=="C5" or c=="Consonant" or c=="Stress":
            if noLabel:
                segments.append(tb.tree_children(sTree)[0])
            else:
                segments.append(tb.tree_children(sTree)[0]+"_C")
        elif tb.tree_category(sTree)=="Vowel":
            if noLabel:
                segments.append(tb.tree_children(sTree)[0])
            else:
                segments.append(tb.tree_children(sTree)[0]+"_V")
        else:
            for child in tb.tree_children(sTree):
                buildSyllable(child,segments,noLabel)

    def buildWord(wTree,sCat,syllables,segSep,sylSep,noLabel):
        try:
            if sCat.search(tb.tree_category(wTree)):#=="Syllable" or tb.tree_category(wTree)=="SyllableIF" or tb.tree_category(wTree)=="SyllableI" or tb.tree_category(wTree)=="SyllableF":
                segments = []
                buildSyllable(wTree,segments,noLabel)
                syllables.append(segSep.join(segments))
            else:
                for child in tb.tree_children(wTree):
                    buildWord(child,sCat,syllables,segSep,sylSep,noLabel)
        except:
            print "%s\n"%wTree
            sys.exit()
            for child in tb.tree_children(wTree):
                buildWord(child,sCat,syllables,segSep,sylSep,noLabel)

    
#    print("VisitT %s"%tb.tree_category(tree))
    if wCat.search(tb.tree_category(tree)):
        syllables = []
        buildWord(tree,sCat,syllables,segSep,sylSep,noLabel)
        words.append(sylSep.join(syllables))
    else:
        for child in tb.tree_children(tree):
            visitTree(child,words,wCat,sCat,segSep,sylSep,noLabel)

def getAnalysis(sTree, wCat, sCat, wordSep, segSep, sylSep,noLabel):
    """
        Stores the yield of a tree with syllabic and segmental information
        each segment is indexed with "_C" or "_V" (consonant or vowel) if
        noLabel == FALSE
        each syllable is separated by sylSep
        each word is separated by wordSep
        each segment is separated by segSep
    """
    tree = tb.string_trees(sTree)
    tree.insert(0,'ROOT')
    words = []
    visitTree(tree,words,wCat,sCat,segSep,sylSep,noLabel)
    return wordSep.join(words)

if __name__=="__main__":
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-n","--nepochs", type="int", dest="nepochs", default=1000,help="total number of epochs")
    parser.add_option("-i","--ignore",type="float",dest="skip",default=0,help="fraction of epochs to skip")
    parser.add_option("-r","--rate",type="int",dest="rate",default=1,help="input provides sample every rate epochs")
    parser.add_option("-s","--segSep",dest="segSep",
                      help="separator between segments (possibly empty)")
    parser.add_option("-S","--sylSep",dest="sylSep",
                      help="separator between syllables")
    parser.add_option("-w","--wordSep",dest="wordSep",
                      help="separator between words")
    parser.add_option("-c","--category",dest="category",
                      help="which non-terminal counts as word, regular-expression to match categories")
    parser.add_option("-C","--sylCategory",dest="sylCategory",
                      help="which non-terminal counts as syllable, regular-expression to match categories")
    parser.add_option("--noLabel",dest="noLabel",action="store_true",default=False)
    (options,args) = parser.parse_args()  
    nskip=int(options.skip*options.nepochs/options.rate)
    out = sys.stdout
    for l in sys.stdin:
        if len(l.strip())==0:
            if nskip<=0:
                out.write("\n")
            out.flush()
            nskip-=1
        else:
            if nskip<=0:
                out.write(getAnalysis(l.strip(),re.compile(options.category),re.compile(options.sylCategory),options.wordSep,options.segSep,options.sylSep,options.noLabel))
                out.write("\n")
            else:
                continue
