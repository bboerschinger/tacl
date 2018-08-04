# AGWS/Makefile
#  modified by ben boerschinger, 15/11/13
#
#  (c) Mark Johnson, 20th July 2012
#
#
# Makefile for Adaptor Grammar word segmentation
# using stress cues

# set default shell
#
SHELL=/bin/bash

# CORPUS is the name of the corpus we are using
CORPUS=alex

# CONDITION is the condition we are looking at, primaryreduced, primaryseconday, nostress, primaryall
# primaryreduced corresponds to a setting where only primary stresses are transcribed and function words are not stress
# primaryall also has stressed function words
# nostress is lacking stress completely from its input
CONDITION=primaryonly


# DIR is the base directory in which we work (all files produced are
# relative to this directory)
#
DIR:=./runs/$(CORPUS)/$(CONDITION)

# SIZE is the length of the prefix of the corpus used as input for inference
SIZE=50

# GRAMMAR is the name of the grammar we are looking at
GRAMMAR=colloc3syllIFstress

# SOURCE is the gold data file
SOURCE=Data/$(CORPUS)_all_$(CONDITION)_0.phon

# the folders where the outputs reside
EVALDIR:=$(DIR)/$(GRAMMAR)_$(SIZE)_Eval
TMPDIR:=$(DIR)/$(GRAMMAR)_$(SIZE)_Tmp

# a test-set
TESTIN=Data/$(CORPUS)_test_$(CONDITION).phon
TESTINNOVEL=Data/$(CORPUS)_testnovel_$(CONDITION).phon

# OUTPUTPREFIX is a prefix prepended to all temporary and output run
# files (change this for a new run)
#
OUTPUTPREFIX=x1.0

# BURNINSKIP is the fraction of the sample to be discarded before collecting 
# samples for evaluation
BURNINSKIP=0.8

# PYFLAGS specify flags to be given to py-cfg, e.g., -P (predictive filter)
PYFLAGS=-d 101

# which rule is to be tracked...
RULETRACK=GenWord

# Each fold is a different chain; to do 8 runs set FOLDS=0 1 2 3 4 5 6 7
#FOLDS=00 01 02 03 04 05 06 07
FOLDS=01 02 03 04

# OUTS is a list of types of output files we're going to produce
OUTS=trscore_all $(foreach f,$(FOLDS),trscore_$(f)) testwordscore_all $(foreach f,$(FOLDS),testwordscore_$(f)) testscore_all $(foreach f,$(FOLDS),testscore_$(f)) trwordscore_all $(foreach f,$(FOLDS),trwordscore_$(f)) testnovelscore_all $(foreach f,$(FOLDS),testnovelscore_$(f)) testnovelwordscore_all $(foreach f,$(FOLDS),testnovelwordscore_$(f))

PYTHON=/usr/local/bin/python2.7

# PYCFG is the py-cfg program (including its path)
#
PYCFG=~/software/py-cfg/py-cfg

PYAS=1e-4
PYES=2
PYFS=1

PYBS=1e4
PYGS=100
PYHS=0.01

PYWS=1

PYTS=1
PYMS=0

# PYNS is the number of iterations
PYNS=1000

# PYRS controls how long we do table label resampling for (-1 = forever)
PYRS=-1

PYD=D_
PYE=E_

# rate at which model's output is evaluated
TRACEEVERY=10

# EXEC is the prefix used to execute the py-cfg command
EXEC=time

# EVALREGEX is the regular expression given to eval.py in the evaluation script (may depend on grammar)
# Beware of spurios matches --- note that adapted non-terminals have a #-in each of their occurence, so you can match ^Word# to exclude matching Words, e.g.
EVALREGEX=^Word

# IGNORETERMINALREGEX is the regular expression given to eval.py in the evaluation script
IGNORETERMINALREGEX=^[$$]{3}$$

# WORDSPLITREGEX is the regular expression given to eval.py in the evaluation script
WORDSPLITREGEX=[\\t]+

################################################################################
#                                                                              #
#                     everything below this should be generic                  #
#                                                                              #
################################################################################

# INPUTFILE is the file that contains the adaptor grammar input
#
INPUTFILE:=$(TMPDIR)/AGinput.txt
TESTINPUT:=$(TMPDIR)/AGtestinput.txt
TESTINPUTNOVEL:=$(TMPDIR)/AGtestnovelinput.txt

# GOLDFILE is the file that contains word and syllable boundaries that will be used to
#  evaluate the adaptor grammar word segmentation
#
GOLDFILE:=$(TMPDIR)/AGgold.txt
TESTGOLD:=$(TMPDIR)/AGtestgold.txt
TESTNOVELGOLD:=$(TMPDIR)/AGtestnovelgold.txt

# The list of files we will make
FILENAMEBASE=$(OUTPUTPREFIX)_G$(GRAMMAR)_$(PYD)$(PYE)n$(PYNS)_m$(PYMS)_t$(PYTS)_w$(PYWS)_a$(PYAS)_b$(PYBS)_e$(PYES)_f$(PYFS)_g$(PYGS)_h$(PYHS)_R$(PYRS)
OUTPUTS=$(foreach out,$(OUTS),$(EVALDIR)/$(FILENAMEBASE).$(out))

TARGETS=$(OUTPUTS)

# the grammarfile to be built
GRAMMARFILE=$(TMPDIR)/$(GRAMMAR).gr

.PHONY: top
top: $(TARGETS)

.SECONDARY:
#.DELETE_ON_ERROR:


# HELPERS defined by Mark to take apart the filenames
getarg=$(patsubst $(1)%,%,$(filter $(1)%,$(subst _, ,$(2))))

keyword=$(patsubst $(1),-$(1),$(filter $(1),$(subst _, ,$(2))))

$(EVALDIR)/$(FILENAMEBASE).trscore_%: $(TMPDIR)/$(FILENAMEBASE).travprs_% programs/evaluate.py
	@mkdir -p $(EVALDIR)
	$(PYTHON) programs/evaluate.py $(GOLDFILE) < $< > $@

$(TMPDIR)/$(FILENAMEBASE).travprs_all: programs/mbr.py $(foreach fold,$(FOLDS),$(TMPDIR)/$(FILENAMEBASE)_$(fold).syllables)
	$(PYTHON) $^ > $@

$(TMPDIR)/$(FILENAMEBASE).testavprs_all: programs/mbr.py $(foreach fold,$(FOLDS),$(TMPDIR)/$(FILENAMEBASE)_$(fold).testsyllables)
	$(PYTHON) $^ > $@

$(TMPDIR)/$(FILENAMEBASE).testnovelavprs_all: programs/mbr.py $(foreach fold,$(FOLDS),$(TMPDIR)/$(FILENAMEBASE)_$(fold).testnovelsyllables)
	$(PYTHON) $^ > $@

$(TMPDIR)/$(FILENAMEBASE).travprs_%: $(TMPDIR)/$(FILENAMEBASE)_%.syllables programs/mbr.py $(TMPDIR)/$(FILENAMEBASE).travprs_all $(TMPDIR)/$(FILENAMEBASE).testavprs_all
	$(PYTHON) programs/mbr.py $< > $@


$(TMPDIR)/$(FILENAMEBASE).testavprs_%: $(TMPDIR)/$(FILENAMEBASE)_%.testsyllables programs/mbr.py $(TMPDIR)/$(FILENAMEBASE).testavprs_all $(TMPDIR)/$(FILENAMEBASE).travprs_all
	$(PYTHON) programs/mbr.py $< > $@

$(TMPDIR)/$(FILENAMEBASE).testnovelavprs_%: $(TMPDIR)/$(FILENAMEBASE)_%.testnovelsyllables programs/mbr.py $(TMPDIR)/$(FILENAMEBASE).testnovelavprs_all $(TMPDIR)/$(FILENAMEBASE).travprs_all
	$(PYTHON) programs/mbr.py $< > $@

$(EVALDIR)/$(FILENAMEBASE).testscore_%: $(TMPDIR)/$(FILENAMEBASE).testavprs_% programs/evaluate.py
	@mkdir -p $(EVALDIR)
	$(PYTHON) programs/evaluate.py $(TESTGOLD) < $< > $@


$(EVALDIR)/$(FILENAMEBASE).testnovelscore_%: $(TMPDIR)/$(FILENAMEBASE).testnovelavprs_% programs/evaluate.py
	@mkdir -p $(EVALDIR)
	$(PYTHON) programs/evaluate.py $(TESTNOVELGOLD) < $< > $@

$(EVALDIR)/$(FILENAMEBASE).trwordscore_%: $(TMPDIR)/$(FILENAMEBASE).travprs_% $(TMPDIR)/$(FILENAMEBASE).travprs_all $(foreach f,$(FOLDS),$(TMPDIR)/$(FILENAMEBASE)_$(f).syllables) scripts/resultfiles.sh programs/eval-words.py
	@mkdir -p $(EVALDIR)
#	@echo "scripts/resultfiles.sh $(GOLDFILE) $< > $@"
#	I don't know what's going on here, brute-force error-message handling...
	-scripts/resultfiles.sh $(GOLDFILE) $< > $@ || scripts/resultfiles.sh $(GOLDFILE) $< > $@ && true


$(EVALDIR)/$(FILENAMEBASE).testwordscore_%: $(TMPDIR)/$(FILENAMEBASE).testavprs_% $(TMPDIR)/$(FILENAMEBASE).testavprs_all $(foreach f,$(FOLDS),$(TMPDIR)/$(FILENAMEBASE)_$(f).testsyllables) scripts/resultfiles.sh programs/eval-words.py
	@mkdir -p $(EVALDIR)
#	@echo "scripts/resultfiles.sh $(TESTGOLD) $< > $@"
	-scripts/resultfiles.sh $(TESTGOLD) $< > $@ || -scripts/resultfiles.sh $(TESTGOLD) $< > $@ && true

$(EVALDIR)/$(FILENAMEBASE).testnovelwordscore_%: $(TMPDIR)/$(FILENAMEBASE).testnovelavprs_% $(TMPDIR)/$(FILENAMEBASE).testnovelavprs_all $(foreach f,$(FOLDS),$(TMPDIR)/$(FILENAMEBASE)_$(f).testnovelsyllables) scripts/resultfiles.sh
	@mkdir -p $(EVALDIR)
#	@echo "scripts/resultfiles.sh $(TESTGOLD) $< > $@"
	-scripts/resultfiles.sh $(TESTNOVELGOLD) $< > $@ || -scripts/resultfiles.sh $(TESTNOVELGOLD) $< > $@ && true


$(TMPDIR)/$(FILENAMEBASE)_%.syllables $(TMPDIR)/$(FILENAMEBASE)_%.testsyllables $(TMPDIR)/$(FILENAMEBASE)_%.testnovelsyllables: $(PYCFG) $(GRAMMARFILE) $(GOLDFILE) $(INPUTFILE) $(TESTGOLD) $(TESTINPUT) $(TESTNOVELGOLD) $(TESTINPUTNOVEL)
	@mkdir -p $(TMPDIR)
	echo "Starting $@"
	date
	$(EXEC) $(PYCFG) $(PYFLAGS) \
		-A $(basename $@).prs \
		-F $(basename $@).trace \
		-G $(basename $@).wlt \
		$(call keyword,D,$(FILENAMEBASE)) \
		$(call keyword,E,$(FILENAMEBASE)) \
		-r $$RANDOM$$RANDOM \
		-a $(call getarg,a,$(FILENAMEBASE)) \
		-b $(call getarg,b,$(FILENAMEBASE)) \
		-e $(call getarg,e,$(FILENAMEBASE)) \
		-f $(call getarg,f,$(FILENAMEBASE)) \
		-g $(call getarg,g,$(FILENAMEBASE)) \
		-h $(call getarg,h,$(FILENAMEBASE)) \
		-w $(call getarg,w,$(FILENAMEBASE)) \
		-T $(call getarg,t,$(FILENAMEBASE)) \
		-m $(call getarg,m,$(FILENAMEBASE)) \
		-n $(call getarg,n,$(FILENAMEBASE)) \
		-R $(call getarg,R,$(FILENAMEBASE)) \
		-x $(TRACEEVERY) \
		-u $(TESTINPUT) \
                -U "$(PYTHON) programs/collectTreeSyllables.py --noLabel --segSep=\"\" --sylSep=\".\" --wordSep=\" \" --category=\"^Word\" --sylCategory=\"^(Syll[SU]?|Syll[SU]?I|Syll[SU]?F|Syll[SU]?IF)$$\" | $(PYTHON) programs/evaluate.py $(TESTGOLD) > $(basename $@).testseval" \
                -U "$(PYTHON) programs/collectTreeSyllables.py --noLabel --segSep=\"\" --sylSep=\".\" --wordSep=\" \" --category=\"^Word\" --sylCategory=\"^(Syll[SU]?|Syll[SU]?I|Syll[SU]?F|Syll[SU]?IF)$$\" --nepochs $(call getarg,n,$(FILENAMEBASE)) --rate $(TRACEEVERY) --ignore $(BURNINSKIP) > $(basename $@).testsyllables" \
		-X "$(PYTHON) programs/collectTreeSyllables.py --noLabel --segSep=\"\" --sylSep=\".\" --wordSep=\" \" --category=\"^Word\" --sylCategory=\"^(Syll[SU]?|Syll[SU]?I|Syll[SU]?F|Syll[SU]?IF)$$\" | $(PYTHON) programs/evaluate.py $(GOLDFILE) > $(basename $@).trseval" \
		-X "$(PYTHON) programs/collectTreeSyllables.py --noLabel --segSep=\"\" --sylSep=\".\" --wordSep=\" \" --category=\"^Word\" --sylCategory=\"^(Syll[SU]?|Syll[SU]?I|Syll[SU]?F|Syll[SU]?IF)$$\" --nepochs $(call getarg,n,$(FILENAMEBASE)) --rate $(TRACEEVERY) --ignore $(BURNINSKIP) > $(basename $@).syllables" \
		-Y "$(PYTHON) programs/trackRuleProbs.py $(CORPUS) $(GRAMMAR) $(SIZE) $(CONDITION) $* $(RULETRACK) $(call getarg,n,$(FILENAMEBASE)) $(BURNINSKIP) $(TRACEEVERY) > $(basename $@).grammarsamples" \
		-v $(TESTINPUTNOVEL) \
		-V "$(PYTHON) programs/collectTreeSyllables.py --noLabel --segSep=\"\" --sylSep=\".\" --wordSep=\" \" --category=\"^Word\" --sylCategory=\"^(Syll[SU]?|Syll[SU]?I|Syll[SU]?F|Syll[SU]?IF)$$\" | $(PYTHON) programs/evaluate.py $(TESTNOVELGOLD) > $(basename $@).testnovelseval" \
		-V "$(PYTHON) programs/collectTreeSyllables.py --noLabel --segSep=\"\" --sylSep=\".\" --wordSep=\" \" --category=\"^Word\" --sylCategory=\"^(Syll[SU]?|Syll[SU]?I|Syll[SU]?F|Syll[SU]?IF)$$\" --nepochs $(call getarg,n,$(FILENAMEBASE)) --rate $(TRACEEVERY) --ignore $(BURNINSKIP) > $(basename $@).testnovelsyllables" \
		$(TMPDIR)/$(call getarg,G,_$(FILENAMEBASE)).gr \
		< $(INPUTFILE)

# additional testfile
#		-v $(TESTINPUTNOVEL) \
#               -V "$(PYTHON) programs/collectTreeSyllables.py --noLabel --segSep=\"\" --sylSep=\".\" --wordSep=\" \" --category=\"^Word\" --sylCategory=\"^(Syll[SU]?|Syll[SU]?I|Syll[SU]?F|Syll[SU]?IF)$$\" | $(PYTHON) programs/evaluate.py $(TESTNOVELGOLD) > $(basename $@).testnovelseval" \
#               -V "$(PYTHON) programs/collectTreeSyllables.py --noLabel --segSep=\"\" --sylSep=\".\" --wordSep=\" \" --category=\"^Word\" --sylCategory=\"^(Syll[SU]?|Syll[SU]?I|Syll[SU]?F|Syll[SU]?IF)$$\" --nepochs $(call getarg,n,$(FILENAMEBASE)) --rate $(TRACEEVERY) --ignore $(BURNINSKIP) > $(basename $@).testnovelsyllables" \

$(TMPDIR)/%.gr: programs/input2grammar_stress.py
	mkdir -p $(TMPDIR)
	$(PYTHON) $^ --grammar $(*F) > $@

$(INPUTFILE): programs/source2AGinput.py $(SOURCE)
	mkdir -p $(TMPDIR)
	head -n$(SIZE) $(SOURCE) | $(PYTHON) programs/source2AGinput.py -s0 -b "\.\||\." | head -n$(SIZE) > $@ 

$(TESTINPUT): programs/source2AGinput.py $(TESTIN)
	mkdir -p $(TMPDIR)
	$(PYTHON) $^ -s0 -b "\.\||\." > $@

$(TESTINPUTNOVEL): programs/source2AGinput.py $(TESTINNOVEL)
	mkdir -p $(TMPDIR)
	$(PYTHON) $^ -s0 -b "\.\||\." > $@

$(GOLDFILE): $(SOURCE)
	mkdir -p $(TMPDIR)
	echo "	head -n$(SIZE) $(SOURCE) | sed 's/ //g; s/\.|/ /g; s/\.$$//g' > $@"
	head -n$(SIZE) $(SOURCE) | sed 's/ //g; s/\.|/ /g; s/\.$$//g' > $@

$(TESTGOLD): $(TESTIN)
	mkdir -p $(TMPDIR)
	sed 's/ //g; s/\.|/ /g; s/\.$$//g' $(TESTIN) > $@

$(TESTNOVELGOLD): $(TESTINNOVEL)
	mkdir -p $(TMPDIR)
	sed 's/ //g; s/\.|/ /g; s/\.$$//g' $(TESTINNOVEL) > $@

.PHONY: clean
clean: 
#	rm -fr $(TMP)

.PHONY: real-clean
real-clean: clean
#	rm -fr $(OUTPUTDIR)
