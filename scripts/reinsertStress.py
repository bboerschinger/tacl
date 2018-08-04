"""
  add back stress-information to segmented data that lacks the stress information
"""
import sys

def getBVec(t):
    """get a vector-representation of a segmentation, 's' indicates syllable, 'b' a word-boundary, 'n' absence of a boundary"""
    res = []
    pos = 1
    while pos<len(t):
        if t[pos]==".":
            res.append("s")
            pos+=2
        elif t[pos]==" ":
            res.append("b")
            pos+=2
        else:
            res.append("n")
            pos+=1
    return res

def addStress(seg,stressed,vec):
    """given a vectorial segmentation of the unstressed text, add the missing stress-indicators"""
    s1pos=1
    s2pos=1
    vecpos = 0
    res = []
    seg = seg.replace(".","").replace(" ","")
    stressed = stressed.replace(".","").replace(" ","")
    while s1pos<len(seg):
        if seg[s1pos]==stressed[s2pos]:
            s1pos+=1
            s2pos+=1
            res.append(vec[vecpos])
            vecpos+=1
        elif stressed[s2pos]=="*":
            res.append("str")
            s2pos+=1
        else:
            sys.stderr.write("strings don't match: \n%s\n%s"%(seg[:s1pos]+"!"+seg[s1pos:],stressed[:s2pos]+"!"+stressed[s2pos:]))
            sys.exit(1)
    if stressed[-1]=="*":
        res.append("str")
    return res

def segment(text,vec):
    """given a vectorial segmentation of text, generate the segmented string"""
    text = text.replace(".","").replace(" ","")
    res = []
    buf = [text[0]]
    spos=1
    for b in vec:
        if b=="n":
            buf.append(text[spos])
            spos+=1
        elif b=="s":
            buf.append(".")
            buf.append(text[spos])
            spos+=1
        elif b=="b":
            res.append(''.join(buf))
            buf=[text[spos]]
            spos+=1
        elif b=="str":
            buf.append("*")
    res.append(''.join(buf))
    return " ".join(res)
    

if __name__=="__main__":
    goldseg = zip(open(sys.argv[1]).readlines(),open(sys.argv[2]).readlines())
    for (g,s) in goldseg:
        s=s.strip()
        g=g.strip()
        origSeg = getBVec(s)
        strSeg = addStress(s,g,origSeg)
        strS = segment(s,strSeg)
        if strS.replace("*","")!=s:
            sys.stderr.write("no match for\n%s\n%s\n"%(s,strS))
            sys.exit(1)
        sys.stdout.write("%s\n"%segment(s,strSeg))
        
