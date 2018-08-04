import sys,glob,os

if __name__=="__main__":
    for tmpDir in glob.glob(sys.argv[1]):
        gFtest = tmpDir+"/AGtestgold.txt"
        gFtr = tmpDir+"/AGgold.txt"
        gFtestnovel = tmpDir+"/AGtestnovelgold.txt"
        for i in ["01","02","03","04","all"]:
            for c in ["tr","test","testnovel"]:
                try:
                    parseFile = glob.glob(tmpDir+"/x1*%savprs_%s"%(c,i))[0]
                    target = parseFile.replace("Tmp","Eval").replace("%savprs"%c,"%swordscore"%c)
                    print parseFile,target
                    if c=="tr":
                        gf = gFtr
                    elif c=="test":
                        gf = gFtest
                    elif c=="testnovel":
                        gf = gFtestnovel
                    os.system("/home/bborschi/research/Syllabification/scripts/resultfiles.sh %s %s > %s"%(gf,parseFile,target))
                except:
                    continue
