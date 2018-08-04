python2.7 ~/research/Syllabification/programs/eval-words.py --syllInd .  --match-template All --match-re "" -g ~/research/Syllabification/Data/$1 colloc3syllIF*_*_*/*.$2
python2.7 ~/research/Syllabification/programs/eval-words.py --syllInd . --match-template NoStress --match-re "^[^*]*$" -g ~/research/Syllabification/Data/$1 colloc3syllIF*_*_*/*.$2 | grep -v "^file"
python2.7 ~/research/Syllabification/programs/eval-words.py --syllInd . --match-template Stress --match-re "[*]" -g ~/research/Syllabification/Data/$1 colloc3syllIF*_*_*/*.$2 | grep -v "^file"
python2.7 ~/research/Syllabification/programs/eval-words.py --syllInd . --match-template MonoSyllables --match-re "^[^.]*$" -g ~/research/Syllabification/Data/$1 colloc3syllIF*_*_*/*.$2 | grep -v "^file"
python2.7 ~/research/Syllabification/programs/eval-words.py --syllInd . --match-template MultiSyllables --match-re "^[^.]*[.].*$" -g ~/research/Syllabification/Data/$1 colloc3syllIF*_*_*/*.$2 | grep -v "^file"
python2.7 ~/research/Syllabification/programs/eval-words.py --syllInd . --match-template StressFirstAll --match-re "^[^*.]*[*]" -g ~/research/Syllabification/Data/$1 colloc3syllIF*_*_*/*.$2 | grep -v "^file"
python2.7 ~/research/Syllabification/programs/eval-words.py --syllInd . --match-template StressFirstMono --match-re "^[^*.]*[*][^.]*$" -g ~/research/Syllabification/Data/$1 colloc3syllIF*_*_*/*.$2 | grep -v "^file"
python2.7 ~/research/Syllabification/programs/eval-words.py --syllInd . --match-template StressFirstMulti --match-re "^[^*.]*[*][^.][.].*$" -g ~/research/Syllabification/Data/$1 colloc3syllIF*_*_*/*.$2 | grep -v "^file"
python2.7 ~/research/Syllabification/programs/eval-words.py --syllInd . --match-template StressSecondAll --match-re "^[^*.]*[.][^.]*[*]" -g ~/research/Syllabification/Data/$1 colloc3syllIF*_*_*/*.$2 | grep -v "^file"