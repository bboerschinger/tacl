FOLDER=~/research/Syllabification

cat ${FOLDER}/Data/$1_all_$2.phon | python2.7 ${FOLDER}/Data/dataprep/introducePattern.py $3 no > ${FOLDER}/Data/$1_all_$2$3.phon
tail -n1000 ${FOLDER}/Data/$1_all_$2$3.phon > ${FOLDER}/Data/$1_test_$2$3.phon
sed 's/[aeiou]./xx/g' ${FOLDER}/Data/$1_test_$2$3.phon > ${FOLDER}/Data/$1_testnovel_$2$3.phon
