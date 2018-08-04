import sys,glob,os,re
"""add stress to nostress-files, then build stress-scores"""

size = re.compile(r"_([0-9]+)_Tmp")
data = "/home/bborschi/research/Syllabification/Data"

if __name__=="__main__":
    if sys.argv[1].count("nostress")==0:
        print "run only with no-stress"
        sys.exit(1)
    for tmpDir in glob.glob(sys.argv[1]):
        child = "lily" if tmpDir.count("lily") >= 1 else "korman" if tmpDir.count("korman")>=1 else "adam" if tmpDir.count("adam")>=1 else "alex" if tmpDir.count("alex")>=1 else "brent" if tmpDir.count("brent")>=1 else sys.exit(1)
        #build the new gold-files which contain stress information from the reduced file
        try:
            s = size.search(tmpDir).groups()[0]
        except:
            sys.stderr.write("ERROR: %s\n"%tmpDir)
            continue
        os.system("head -n%s %s/%s_all_primaryonly.phon | sed 's/ //g; s/\.|/ /g; s/\.$$//g' > %s/trainstress.txt"%(s,data,child,tmpDir))
        os.system("tail -n1000 %s/%s_all_primaryonly.phon | sed 's/ //g; s/\.|/ /g; s/\.$$//g' > %s/teststress.txt"%(data,child,tmpDir))
        os.system("cat %s/%s_testnovel_primaryonly.phon | sed 's/ //g; s/\.|/ /g; s/\.$$//g' > %s/testnovelstress.txt"%(data,child,tmpDir))
        #build the stress-files
        gFtest = tmpDir+"/teststress.txt"
        gFtr = tmpDir+"/trainstress.txt"
	gFtestnovel = tmpDir+"/testnovelstress.txt"
        for i in ["01","02","03","04","all"]:
            for c in ["tr","test","testnovel"]: 
                try:
                    parseFile = glob.glob(tmpDir+"/*%savprs_%s"%(c,i))[0] 
                    parseFileStress = parseFile.replace("avprs","_stress")
                    if c=="tr":
                        gf = gFtr
                    elif c=="test":
                        gf = gFtest
                    elif c=="testnovel":
                        gf = gFtestnovel
                    os.system("python2.7 /home/bborschi/research/Syllabification/scripts/reinsertStress.py %s %s > %s"%(gf,parseFile,parseFileStress))
                    target = parseFile.replace("Tmp","Eval").replace("%savprs"%c,"%swordscore"%c)
                    
                    print parseFileStress,target 
                    os.system("/home/bborschi/research/Syllabification/scripts/resultfiles.sh %s %s > %s"%(gf,parseFileStress,target))
                except:
                    continue
