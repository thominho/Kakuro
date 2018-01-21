from csp2 import *
"""to sum den mporei na perastei san constraint opws to a!=b epomenws prepei na perastei ston constraint
san lista ta a8roismata h deuterh krata ana 8esh to sum pou exoume se ka8e state px 0,0,0 afora to prwto sum
an h prwth lista apo to sums exei treis 8eseis"""
sums = []
nsum= []

class Kakuro(CSP2):
    def __init__(self,neighbors,numbers):
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
        #Arxikopoihsh twn metablhtwn
        self.variables = []
        for i in neighbors:
            for j in i:
                if("w" in j):
                    self.variables.append(j)
        #Arxikopoihsh twn Neighbours
        self.Neighbors = {}
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
                                        self.Neighbors.setdefault(d,[])
                                        self.Neighbors[d].append(l)
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
                                        self.Neighbors.setdefault(d,[])
                                        self.Neighbors[d].append(l)
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
                            self.Neighbors.setdefault(d,[])
                            self.Neighbors[d].append(i)
                    for i in op2:
                        if("w" in i):
                            temp.append(i)
                        else:
                            temp = []
                    if(len(temp)>0):
                        for i in temp:
                            self.Neighbors.setdefault(d,[])
                            self.Neighbors[d].append(i)
        #Arxikopoihsh twn domains
        self.domains = {}
        for i in neighbors:
            for j in i:
                if("w" in j):
                    self.domains.setdefault(j,[])
                    counter=1
                    while(counter<=9):
                        self.domains[j].append(counter)
                        counter=counter+1
        return CSP2.__init__(self,self.variables,self.domains,self.Neighbors,self.has_constraints)

    #Eftiaksa dikia mou constraint wste na pernaw to val pou 8a ginei assign alla kai ola ta assignments gia na meiw8ei o xronos twn iterations
    def has_constraints(self,var,val,assignment):
        #koitaei an uparxei collision me neighbour
        for neighbor in self.Neighbors[var]:
                if neighbor in assignment:
                        if assignment[neighbor] == val:
                                return True
        #tsekarei ta sum pou summetexei to value
        for i in sums:
                if var in i:
                        s=0
                        counter=0
                        for j in i:
                                if j in assignment:
                                        s = s + assignment[j]
                                        counter =counter +1
                        if (counter==len(i)-1 and s!=i[0]):
                                return True
                        if (counter<len(i)-1 and s>=i[0]):
                                return True
        return False
