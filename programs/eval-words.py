#! /bin/env python

description = """
eval-words.py version of 10th September, 2013

starting from Mark Johnson's version of the 8th September, 2011

Evaluates the accuracy of specific words in word segmentation output
(e.g., the *.sws or *.avprs files produced by py-cfg).

When the corpus is read, each word is first transformed by matching
it with --match-re, and generating the pattern specified by 
--match-pattern.  Then the resulting word is looked up in
--rename-file to generate the actual key scored.

Example: to aggregate word scores by frequency:

eval-words.py --renamer-file br-phono.wc.txt <filenames.sws>

Example: if phono-text.txt maps pronunciations to their orthographic forms
this will aggregate scores by orthographic forms.

eval-words.py --renamer-file phono-text.txt <filenames.sws>

To compute the average word f-score, run

eval-words.py --match-template Word <filenames.sws>
"""

import optparse, collections, csv, re, sys

def readparses(inf):
    parses = []
    for line in inf:
        line = line.strip()
        if len(line) == 0:
            if len(parses) > 0:
                yield parses
                parses = []
        else:
            parses.append(line)
    if len(parses) > 0:
        yield parses

def argmax(keyvals):
    return max(keyvals, key=lambda keyval: keyval[1])[0]

def most_frequent_parse(*parses):
    """Counts the number of times each parse appears, and returns the
    one that appears most frequently"""
    parsecounts = collections.defaultdict(int)
    for parse in parses:
        parsecounts[parse] += 1
    return argmax(parsecounts.iteritems())

def read_data(inf, match_rex, match_template, renamer, goldlines=None,syllInd=''):
    parses = list(readparses(inf))
    if len(parses) == 0:
        sys.stderr.write("**Error: file %s has no lines\n"%inf.name)
	return goldlines,-1
#    assert(len(parses) > 0)
    data = map(most_frequent_parse, *parses)
    if goldlines:
        if len(goldlines) != len(data):
            sys.stderr.write("** Error: %s has %s lines, while gold data has %s lines, so results are bogus\n" % (inf.name, len(data), len(goldlines)))
            sys.exit(1)
        for lineno, (goldline,line) in enumerate(zip(goldlines,data)):
            if goldline.replace(syllInd,'') != ''.join(line.replace(syllInd,'').split()):
                print goldline.replace(syllInd,'')
                sys.stderr.write("** Error: line %s in %s differs from gold line, so results are bogus\n** data: %s\n** gold: %s\n\n" %
                                 (lineno+1, inf.name, line, goldline))
                sys.exit(1)
    else:
        goldlines = [''.join(line.split()) for line in data]

    tuples = collections.defaultdict(set)
    pos = 0
    if renamer:
        for line in data:
            for word in line.split():
                oldpos = pos
                pos += len(word.replace(syllInd,''))
                mo = match_rex.match(word)
                if mo:
                    word = mo.expand(match_template)
                    if word in renamer:
                        tuples[renamer[word]].add((oldpos,pos))
    else:
        for line in data:
            for word in line.split():
                oldpos = pos
                pos += len(word.replace(syllInd,''))
                mo = match_rex.match(word)
                if mo:
                    word = mo.expand(match_template)
                    tuples[word].add((oldpos,pos))

    return goldlines, tuples
                

if __name__ == '__main__':
    parser = optparse.OptionParser(description=description)
    parser.add_option("--corpus-re",dest="corpus_re",default=r"(alex|lily|korman|brent)",
                        help="regex mapping path to corpus-name")
    parser.add_option("--setting-re",dest="setting_re",default=r"(primaryonly|fullstress|nostress)",
                        help="regex mapping path to corpus type")
    parser.add_option("--condition-re",dest="condition_re",default=r"\.(tr|testnovel|test)",
                        help="regex mapping the filename to the condition, either test or tr(ain)")
    parser.add_option("--grammar-re", dest="grammar_re", default=r"_G([^_]+)_",
                        help="regex mapping test filename to grammar")
    parser.add_option("--scale-re", dest="scale_re", default=r"_([.0-9]+)_Tmp",
                        help="regex mapping test filename to scale")
    parser.add_option("--fullname-re", "-f", dest="fullname_re", 
                        default=r"_([0-9]+|all)$",
                        help="regex mapping test filename to full identifier")
    parser.add_option("--gold", "-g", dest="gold", default="br-phono.txt",
                        help="file containing gold data")
    parser.add_option("--match-re", "-m", dest="match_re", 
                        # default=r"^(yu|D6|6|D&t|WAt|Iz|It|DIs|wan6|bUk|pUt|wIT|d0gi|h&v|bANi|gEt)$",
                        default=r"^(.*)$",
                        help="regex matching words to score")
    parser.add_option("--match-template", "-t", dest="match_template", default=r"\1",
                        help="template used to generate scoring key from match")
    parser.add_option("--renamer-file", "-r", dest="renamer_file",
                        help="file containing <word> <key> pairs (one per line) mapping words to scoring keys")
    parser.add_option("--output-field-separator", 
                        dest="output_field_separator", default=",",
                        help="separator between output fields")
    parser.add_option("--syllInd",dest="syllInd",default=".",
                        help="indicator of syllable boundaries, ignored when empty")
                         
    args,rest = parser.parse_args()

    grammar_rex = re.compile(args.grammar_re)
    scale_rex = re.compile(args.scale_re)
    fullname_rex = re.compile(args.fullname_re)
    match_rex = re.compile(args.match_re)
    syllInd = args.syllInd
    corpus_rex = re.compile(args.corpus_re)
    condition_rex = re.compile(args.condition_re)
    setting_rex = re.compile(args.setting_re)

    renamer = None
    if args.renamer_file:
        renamer = dict(line.split() for line in file(args.renamer_file, "rU"))

    goldlines, gold = read_data(file(args.gold, "rU"), match_rex, args.match_template, renamer,syllInd=syllInd)

    # words is set of all words that match match_re in gold and test data
    words = set(gold.iterkeys())
    
    # eolpositions is set of eol positions
    eolpositions = set((0,))
    pos = 0
    for goldline in goldlines:
        pos += len(goldline)
        eolpositions.add(pos)
    assert(len(eolpositions) == len(goldlines)+1)

    fname_data = dict()
    for fname in rest:
        inf = file(fname)
        try:
            goldlines, data = read_data(inf, match_rex, args.match_template, renamer, goldlines,syllInd=syllInd)
        except:
            sys.stderr.write("# Ignored %s"%(fname))
            continue
        if data == -1:
            continue
        fname_data[fname] = data
        words.update(data.iterkeys())

    os = csv.writer(sys.stdout, 
                    delimiter=args.output_field_separator, 
                    lineterminator='\n')

    os.writerow(('#setting','condition','corpus','run','grammar','size','word',
                 'token_gold','token_test','token_correct','token_fscore',
                 'boundary_gold','boundary_test','boundary_correct','boundary_fscore',
                 'gold_average_length', 'test_average_length'))

    for fname,data in fname_data.iteritems():
        corpusname = fname
        mo = corpus_rex.search(fname)
        if mo:
            corpusname = mo.group(1)
        condition = None
        mo = condition_rex.search(fname)
        if mo:
            condition = mo.group(1)
        setting = None
        mo = setting_rex.search(fname)
        if mo:
            setting = mo.group(1)
        fullname = fname
        mo = fullname_rex.search(fname)
        if mo:
            fullname = mo.group(1)
        grammar = None
        mo = grammar_rex.search(fname)
        if mo:
            grammar = mo.group(1)
        scale = None
        mo = scale_rex.search(fname)
        if mo:
            scale = mo.group(1)
        for word in words:
            testdata = data[word]
            golddata = gold[word]
            token_correct = testdata & golddata
            token_ngold = len(golddata)
            token_ntest = len(testdata)
            token_ncorrect = len(token_correct)
            token_fscore = 2*token_ncorrect/(token_ngold+token_ntest+1e-100)

            testboundaries = (set(b[0] for b in testdata) | set(b[1] for b in testdata))-eolpositions
            goldboundaries = (set(b[0] for b in golddata) | set(b[1] for b in golddata))-eolpositions
            boundary_correct = testboundaries & goldboundaries
            boundary_ngold = len(goldboundaries)
            boundary_ntest = len(testboundaries)
            boundary_ncorrect = len(boundary_correct)
            boundary_fscore = 2*boundary_ncorrect/(boundary_ngold+boundary_ntest+1e-100)

            gold_average_length = sum(d[1]-d[0] for d in golddata)/(1e-100+len(golddata))
            test_average_length = sum(d[1]-d[0] for d in testdata)/(1e-100+len(testdata))

            os.writerow((setting,condition,corpusname,fullname,grammar,scale,word,
                         token_ngold, token_ntest, token_ncorrect, token_fscore,
                         boundary_ngold, boundary_ntest, boundary_ncorrect, boundary_fscore,
                         gold_average_length, test_average_length
                         ))
