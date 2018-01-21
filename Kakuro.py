from utils import *
from csp import *
from KakuroClass import *
import math, random, sys, time, bisect, string
from search import *
import itertools, re



def Kakuro2(neighbors,numbers):
        counter=0
        #Arxikopoihsh twn sums mazi me autous pou summetexoun se auto
        for i in neighbors:
            counter=counter+1
            counter3=0
            for j in i:
                counter3=counter3+1
                if(len(j)==2 and "w" not in j):
                    counter5=0
                    for o in j:
                        counter5=counter5+1
                        counter2=0
                        d=[]
                        d.append(o)
                        if(o!=0):
                            flag=0
                            if(counter5==1): 
                                for k in neighbors:
                                    counter2=counter2+1
                                    counter4=0
                                    if (counter2>counter):
                                        for l in k:
                                            counter4=counter4+1
                                            if(counter4==counter3 and flag==0):
                                                if(("w" in l) and flag==0):
                                                    d.append(l)
                                                elif("b"==l or (len(l)==2 and "w" not in l)):
                                                    flag=1
                                sums.append(d)
                            elif(counter5==2):
                                for k in neighbors:
                                    counter2=counter2+1
                                    counter4=0
                                    if (counter2==counter):
                                        for l in k:
                                            counter4=counter4+1
                                            if(counter4>counter3 and flag==0):
                                                if(("w" in l) and flag==0):
                                                    d.append(l)
                                                elif("b"==l or (len(l)==2 and "w" not in l)):
                                                    flag=1
                                sums.append(d)
        #enas pinakas toso 8esewn oses exei to sums meion tis 8eseis pou kratiountai ta sum
        for i in sums:
                counter1=0
                while(counter1<len(i)-1):
                        nsum.append(0)
                        counter1=counter1+1
        #arxikopoihsh twn neighbors se dict wste na perasei sto csp
        domain = {}
        for i in neighbors:
                for j in i:
                        if("w" in j):
                                domain.setdefault(j,[])
                                counter=1
                                while(counter<=9):
                                        domain[j].append(counter)
                                        counter=counter+1
        neighbors = parse_neighbors(neighbors)
        return CSP(neighbors.keys(),domain,neighbors,kakuzo_constraints)
                    
def parse_neighbors(neighbors, vars=[]):
    dict = DefaultDict([])
    for var in vars:
        dict[var] = []
    counter=0
    for i in neighbors:
        counter=counter+1
        counter3=0
        for j in i:
            counter3=counter3+1
            if("w" in j):
                counter2=0
                d=j
                op=[]
                op2=[]
                flag=0
                #parsing stous neighbours pou briskontai apo katw tou
                for k in neighbors:
                    counter2=counter2+1
                    counter4=0
                    if (counter2<counter):
                        for l in k:
                            counter4=counter4+1
                            if(counter4==counter3):
                                op.append(l)
                    if (counter2>counter):
                        for l in k:
                            counter4=counter4+1
                            if(counter4==counter3 and flag==0):
                                if(("w" in l) and flag==0):
                                    dict.setdefault(d,[])
                                    dict[d].append(l)
                                elif("b"==l or (len(l)==2 and ("w" not in l))):
                                    flag=1
                flag=0
                counter2=0
                #parsing stous neighbours pou briskontai de3ia tou
                for k in neighbors:
                    counter2=counter2+1
                    counter4=0
                    if (counter2==counter):
                        for l in k:
                            counter4=counter4+1
                            if (counter4<counter3):
                                op2.append(l)
                            if(counter4>counter3 and flag==0):
                                if(("w" in l) and flag==0):
                                    dict.setdefault(d,[])
                                    dict[d].append(l)
                                elif("b"==l or (len(l)==2 and ("w" not in l))):
                                    flag=1
                #parsing tous neighbours pou briskontai aristera tou
                temp = []
                for i in op:
                    if("w" in i):
                        temp.append(i)
                    else:
                        temp = []
                if(len(temp)>0):
                    for i in temp:
                        dict.setdefault(d,[])
                        dict[d].append(i)
                for i in op2:
                    if("w" in i):
                        temp.append(i)
                    else:
                        temp = []
                if(len(temp)>0):
                    for i in temp:
                        dict.setdefault(d,[])
                        dict[d].append(i)
    return dict

def kakuzo_constraints(A,a,B,b,variaty=0):
    #amesws elenxws an geitonas idios ari8mos
    #Elenxos oti oi air8moi den einai sto idio column h line
        if(type(b) is not int):
                for i in b[A]:
                        if i in B:
                                if B[i] == a:
                                        return False
                for i in sums:
                        s=0
                        counter=0
                        counter1=0
                        if A in i:
                                for j in i:
                                        if j in B and counter1>0:
                                                s=s+B[j]
                                                counter=counter+1
                                        counter1=counter1+1
                                if(counter==len(i)-1 and s!=i[0]):
                                        return False
                                if(counter<len(i)-1 and s>=i[0]):
                                        return False
        else:
                l = []
                counter1=0
                for i in sums:
                        counter2=0
                        for j in i:
                                if(A==j and counter2>0):
                                        l.append(counter1)
                                        nsum[counter1]=int(a)
                                if(counter2>0):
                                        counter1=counter1+1
                                counter2=counter2+1
                counter1=0
                for i in sums:
                        counter2=0
                        if(A in i):
                                for j in i:
                                        if(A!=j and counter2>0 and int(a)==nsum[counter1]):
                                                for k in l:
                                                        nsum[k]=0
                                                return False
                                        if(counter2>0):
                                                counter1=counter1+1
                                        counter2=counter2+1
                        else:
                                for j in i:
                                        if(counter2>0):
                                                counter1=counter1+1
                                        counter2=counter2+1
                counter1=0
                for i in sums:
                        counter2=0
                        nsums2=0
                        csum=0
                        if(A in i):
                                counter3=0
                                for j in i:
                                        if(A==j and counter2>0):
                                                nsums2=nsums2+int(a)
                                                counter3=counter3+1
                                        elif(counter2>0 and nsum[counter1]!=0):
                                                nsums2=nsums2+nsum[counter1]
                                                counter3=counter3+1
                                        if(counter2>0):
                                                counter1=counter1+1
                                        elif(counter2==0):
                                                csum=j
                                        counter2=counter2+1
                                if(counter3==len(i)-1 and nsums2!=csum):
                                        for k in l:
                                                nsum[k]=0
                                        return False
                                if(counter3<len(i)-1 and nsums2>=csum):
                                        for k in l:
                                                nsum[k]=0
                                        return False
                        else:
                                for j in i:
                                        if(counter2>0):
                                                counter1=counter1+1
                                        counter2=counter2+1
        return True


#ta puzzle einai 9x9
easy = [["b",[4,0],[3,0],"b",[6,0],[13,0],"b",[24,0],[4,0]],
        [[0,4],"w1","w2",[15,4],"w3","w4",[0,3],"w5","w6"],
        [[0,15],"w7","w8","w9","w10","w11",[34,7],"w12","w13"],
        ["b",[4,0],[16,21],"w14","w15","w16","w17","w18",[16,0]],
        [[0,6],"w19","w20","w21","b",[0,24],"w22","w23","w24"],
        [[0,8],"w25","w26","w27",[22,0],[24,23],"w28","w29","w30"],
        ["b",[4,34],"w31","w32","w33","w34","w35",[17,0],[16,0]],
        [[0,4],"w36","w37",[0,34],"w38","w39","w40","w41","w42"],
        [[0,3],"w43","w44",[0,16],"w45","w46",[0,16],"w47","w48"]]

intermediate = [["b",[8,0],[11,0],"b",[19,0],[6,0],"b",[17,0],[9,0]],
               [[0,13],"w1","w2",[21,14],"w3","w4",[17,3],"w5","w6"],
               [[0,40],"w7","w8","w9","w10","w11","w12","w13","w14"],
               ["b",[11,0],[23,11],"w15","w16",[0,14],"w17","w18",[12,0]],
               [[0,10],"w19","w20","w21","w22",[11,0],[13,13],"w23","w24"],
               [[0,14],"w25","w26",[16,0],[0,11],"w27","w28","w29","w30"],
               ["b",[15,10],"w31","w32",[4,12],"w33","w34",[9,0],[17,0]],
               [[0,38],"w36","w37","w38","w39","w40","w41","w42","w43"],
               [[0,16],"w44","w45",[0,6],"w46","w47",[0,14],"w48","w49"]]

hard = [["b","b","b",[7,0],[10,0],[15,0],[12,0],"b","b"],
        ["b","b",[28,11],"w1","w2","w3","w4",[21,0],[35,0]],
        ["b",[16,28],"w5","w6","w7","w8","w9","w10","w11"],
        [[0,14],"w12","w13",[12,4],"w14","w15",[12,15],"w16","w17"],
        [[0,13],"w18","w19","w20",[25,20],"w21","w22","w23","w24"],
        [[0,15],"w25","w26","w27","w28",[18,19],"w29","w30","w31"],
        [[0,13],"w32","w33",[11,17],"w34","w35",[16,13],"w36","w37"],
        [[0,42],"w38","w39","w40","w41","w42","w43","w44","b"],
        ["b","b",[0,14],"w45","w46","w47","w48","b","b"]]

expert = [["b","b","b",[15,0],[9,0],"b",[19,0],[30,0],[8,0]],
        ["b",[12,0],[41,7],"w1","w2",[0,13],"w3","w4","w5"],
        [[0,25],"w6","w7","w8","w9",[19,24],"w10","w11","w12"],
        [[0,9],"w13","w14","b",[21,14],"w15","w16","w17",[26,0]],
        [[0,10],"w18","w19",[29,18],"w20","w21","w22","w23","w24"],
        [[0,34],"w25","w26","w27","w28","w29",[0,16],"w29","w30"],
        ["b",[9,23],"w31","w32","w33",[4,0],[12,4],"w34","w35"],
        [[0,23],"w36","w37","w38",[0,13],"w39","w40","w41","w42"],
        [[0,10],"w43","w44","w45",[0,11],"w46","w47","b","b"]]

example = [["b","b",[4,0],[10,0],"b","b","b"],
           ["b",[0,4],"w1","w2","b",[3,0],[4,0]],
           ["b",[0,3],"w3","w4",[11,4],"w5","w6"],
           ["b",[3,0],[4,10],"w7","w8","w9","w10"],
           [[0,11],"w11","w12","w13","w14",[4,0],"b"],
           [[0,4],"w15","w16",[0,4],"w17","w18","b"],
           ["b","b","b",[0,3],"w19","w20","b"]]

#Oles oi parakatw leitourgies ektws apo to example pernoun wra epomenws ama 8elete na epibebaiwsete swsth leitourgia protinw to example me FC

print "Please Press a Number from 1-4"
print "Press 1 for easy"
print "Press 2 for immediate"
print "Press 3 for hard"
print "Press 4 for Expert"
print "Press 5 for Example"
choice=input()
if(choice==1):
    print "You chose Easy"
    man = easy
elif(choice==2):
    print "You chose Immediate"
    man = intermediate
elif(choice==3):
    print "You chose Hard"
    man = hard
elif(choice==4):
    print "You chose Expert"
    man = expert
elif(choice==5):
    print "You chose Example"
    man = example
print "Please press a Number from 1-4"
print "Press 1 for BT"
print "Press 2 for BT+MRV"
print "Press 3 for FC"
print "Press 4 for FC+MRV"
choice=input()
if(choice==1):
    print "Also you chose Backtracking"
    mode = Kakuro2(man,list("123456789"))
    start_time = time.time()
    k = backtracking_search(mode,first_unassigned_variable,unordered_domain_values,no_inference)
elif(choice==2):
    print "Also you chose Backtracking with MRV"
    mode = Kakuro2(man,list("123456789"))
    start_time = time.time()
    k = backtracking_search(mode,mrv)
elif(choice==3):
    print "Also you chose FC"
    mode = Kakuro(man,list("123456789"))
    start_time = time.time()
    k = backtracking_search2(mode,first_unassigned_variable,unordered_domain_values,forward_checking)
elif(choice==4):
    print "Also you chose FC with MRV"
    mode = Kakuro(man,list("123456789"))
    start_time = time.time()
    k = backtracking_search2(mode,mrv,unordered_domain_values,forward_checking)
elapsed_time = time.time() - start_time
print "elapsed_time = ",elapsed_time,"secs"
print k
print"done"

