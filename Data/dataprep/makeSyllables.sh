##
## turn phonemic representation into syllabic representation, postfixing
## each syllable containing a stressed vowel with a "*"
## 

sed 's/ //g' $1 | sed 's/\(\(^\||\|\.\)[^.]\+[*][^.]*\)/\01/g' | sed 's/[*]//g;s/1/*/g'
