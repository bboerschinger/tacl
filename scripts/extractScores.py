"""extract scores and get them all into one csv-file"""

import re,sys

grammar = re.compile(r"_G([^_]+)_")
scale = re.compile(r"_([0-9]+)_Eval")
cond = re.compile(r"(nostress|primaryonly|fullstress)")
run = re.compile(r"_([0-9]+|all)$")
setting = re.compile(r"(test|tr|testnovel)score")
name = re.compile(r"(alex|lily|korman|brent)")


if __name__=="__main__":
    print "name,grammar,size,condition,run,setting,bp,br,bf,tp,tr,tf,sbp,sbr,sbf,stp,str,stf,lp,lr,lf,slp,slr,slf"
    for f in sys.argv[1:]:
        g = grammar.search(f).groups()[0]
        sc = scale.search(f).groups()[0]
        c = cond.search(f).groups()[0]
        r = run.search(f).groups()[0]
        se = setting.search(f).groups()[0]
        n = name.search(f).groups()[0]
        scores = open(f).readlines()[-1]
        sys.stdout.write("%s,%s,%s,%s,%s,%s,%s\n"%(n,g,sc,c,r,se,scores.strip().replace(" ",",")))
