python2.7 ~/research/Syllabification/programs/eval-words.py --syllInd . --match-template All --match-re "" -g $1 $2
python2.7 ~/research/Syllabification/programs/eval-words.py --syllInd . --match-template NoStress --match-re "^[^*]*$" -g $1 $2 | grep -v "^#"
python2.7 ~/research/Syllabification/programs/eval-words.py --syllInd . --match-template Stress --match-re "[*]" -g $1 $2 | grep -v "^#"
python2.7 ~/research/Syllabification/programs/eval-words.py --syllInd . --match-template MonoSyllables --match-re "^[^.]*$" -g $1 $2 | grep -v "^#"
python2.7 ~/research/Syllabification/programs/eval-words.py --syllInd . --match-template MultiSyllables --match-re "^[^.]*[.].*$" -g $1 $2 | grep -v "^#"
python2.7 ~/research/Syllabification/programs/eval-words.py --syllInd . --match-template StressFirstAll --match-re "^[^*.]*[*]" -g $1 $2 | grep -v "^#"
python2.7 ~/research/Syllabification/programs/eval-words.py --syllInd . --match-template StressFirstMono --match-re "^[^*.]*[*][^.]*$" -g $1 $2 | grep -v "^#"
python2.7 ~/research/Syllabification/programs/eval-words.py --syllInd . --match-template StressFirstMulti --match-re "^[^*.]*[*][^.]*[.].*$" -g $1 $2 | grep -v "^#"
python2.7 ~/research/Syllabification/programs/eval-words.py --syllInd . --match-template StressSecondAll --match-re "^[^*.]*[.][^.]*[*]" -g $1 $2 | grep -v "^#"
