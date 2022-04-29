# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 09:36:32 2022

@author: JM
"""
import numpy as np
import random as rd
import pandas as pd
import math
import matplotlib
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import networkx as nx

#%%

def ERMGen(n=2000, p=0.0001, nameoffile = 'Random.txt'):
    file = open(nameoffile, 'w')
    line = str(n)+'\n'
    file.write(line)
    for x in range(0,n):
        for y in range(x+1,n):
            if rd.random() <= p:
                line =  str(x+1)+' '+str(y+1)+'\n'
                file.write(line)
    file.close()
    return


def BSF(a):
    total = a
    sizeGC = 0
    while total != []:
        something = total.pop(0)
        total,size = BSFqueue(something, total)
        if size > sizeGC:
            sizeGC = size
    return(sizeGC)

def BSFqueue(tocompare,full):
    queue = []
    queue.append(tocompare[0])
    queue.append(tocompare[1])
    i =0
    algo = []
    algo=full.copy()
    while i < len(queue):
        index=0
        n=0
        while n < len(algo):
            if queue[i] == algo[n][0] or queue[i] == algo[n][1]:
                full.pop(index)
                index -=1
                appendable=True
                if queue[i] == algo[n][0]:
                    toapp=algo[n][1]
                else:
                    toapp=algo[n][0]
                for a in queue:
                    if a == toapp:
                        appendable=False
                if appendable==True:
                    queue.append(toapp)  
            n+=1
            index +=1
        algo=full.copy()  
        i+=1
    return(full,len(queue))


def file_to_list(filename='Random.txt'):
    file = open(filename, 'r')
    connections = file.readlines()
    n = connections.pop(0)
    seq = [] #turn a list into a tuple
    for l in connections:
        x = l.replace("\n","")
        seq.append(x.split(' '))
    file.close()
    return(seq, n)

def BA(n, m0, m, nameoffile = 'ba.txt'):
    
    file = open(nameoffile, 'w')
    line = str(n)+'\n'
    file.write(line)
    edgesonnode=[]
    totaledges=m0-1
    #define m0
    for x in range(1,m0):
        line = str(x)+' '+str(x+1)+'\n'
        file.write(line)
    #create a side matrix to check the number of edges on a give node
    for x in range(0,n+1):
        edgesonnode.append(0)
    #adds the edges of the m0 to the graf
    for x in range(1,m0+1):
        edgesonnode[x]+=2

        if x==1 or x==(m0):
            edgesonnode[x]-=1
    #runs through the rest of the N
    for x in range(m0+1,n+1):
        toconnect=0
        toappend=[]
        while toconnect<m:
            for y in range(1,x):
                #goes through all nodes y sequentialy 
                #if the random probability is under the value established by the equation
                #it generates an edge between the node X and Y and adds it to the txt file
                #this model is heavily biased torwards the first elements on the array
                #further increasing the probability of adding a connection
                skip=False
                for i in toappend:
                    if y == i:
                        skip = True
                if rd.random() <= (edgesonnode[y]/totaledges) and skip == False:  
                    edgesonnode[y]+=1
                    edgesonnode[x]+=1
                    line = str(x)+' '+str(y)+'\n'
                    file.write(line)
                    toconnect+=1
                    totaledges+=1
                    toappend.append(y)
                    break
    file.close()
    return(edgesonnode)

def BAnonseq(n, m0, m, nameoffile = 'ba.txt'):
    file = open(nameoffile, 'w')
    line = str(n)+'\n'
    file.write(line)
    edgesonnode=[]
    totaledges=m0-1
    #define m0
    for x in range(1,m0):
        line = str(x)+' '+str(x+1)+'\n'
        file.write(line)
    #create a side matrix to check the number of edges on a give node
    for x in range(0,n+1):
        edgesonnode.append(0)
    #adds the edges of the m0 to the graf
    for x in range(1,m0+1):
        edgesonnode[x]+=2
        if x==1 or x==(m0):
            edgesonnode[x]-=1
    #runs through the rest of the N
    for x in range(m0+1,n+1):
        toconnect=0
        toappend = []
        while toconnect<m:
            #gets a random node Y from the previous generated ones
            #if the random probability is under the value established by the equation
            #it generates an edge between the node X and Y and adds it to the txt file
            y = rd.randint(1,x-1)
            skip=False
            for i in toappend:
                if i == y:
                    skip = True
            if rd.random() <= (edgesonnode[y]/totaledges) and skip == False:  
                edgesonnode[y]+=1
                edgesonnode[x]+=1
                line = str(x)+' '+str(y)+'\n'
                file.write(line)
                toconnect+=1
                totaledges+=1
                toappend.append(y)
    file.close()
    return(edgesonnode)

def CumBin(nodesonedges,n, logscale = 0):
    #cumulative binning
    value = nodesonedges
    value.pop(0)
    dic = {}
    for s in value:
        if s in dic: dic[s] += 1
        else: dic[s] = 1
    sort_dic = sorted(dic.items(), key=lambda x: x[0], reverse=True)
    sumof=[(0)]
    index=0
    values=[(0)]
    for i in sort_dic:
        sumof.append(i[1]+sumof[index])
        values.append(i[0])
        index+=1
    sumof.pop(0)
    values.pop(0)
    
    
    if logscale!=0:
        sumof_log = [math.log(int(x)) for x in sumof]
        values_log = [math.log(int(x)) for x in values]

        data = {'values':  values_log,
                'sumof': sumof_log}

        df = pd.DataFrame(data)   
        model = smf.ols('sumof_log~values_log', data=df)
        model = model.fit()
        variavel = model.predict()
        print(model.params)
        sortcumbin=list(zip(values_log,sumof_log))
        plt.plot(values_log,variavel,'r')   
        plt.scatter(*zip(*sortcumbin))
    else:
        #plt.scatter(*zip(*sort_dic)) # This line will plot the network "unbinned"
        sortcumbin=list(zip(values,sumof))
        plt.yscale("log")
        plt.xscale("log")
        plt.scatter(*zip(*sortcumbin))
    return(sort_dic,sortcumbin)

def RunEx7and8(log=0):
    n=2000
    Edges = BAnonseq(n, 3, 1, 'ba1.txt')
    CumBin(Edges,n,log)
    plt.xlabel("Number of Connections")
    plt.ylabel("Frequency")
    Edges = BAnonseq(n, 5, 2, 'ba2.txt')
    CumBin(Edges,n,log)
    plt.legend(['ba1,txt', 'ba2.txt','ba1,txt', 'ba2.txt'])


def IterERM():
    stepstart = 0.0001
    stepfim = 0.005
    steps = 0.0001
    X = []
    Y = []
    while stepstart<=stepfim:
        X.append(stepstart)
        ERMGen(2000,stepstart,'temp.txt')
        con,n = file_to_list('temp.txt')
        y = BSF(con)
        Y.append(y)
        stepstart+=steps
    plt.plot(X,Y)
    plt.xlabel("p")
    plt.ylabel("Size of Giant Component")
    
    return

def ComputeGC(filename='Random.txt'):
    con,n = file_to_list("teste.txt")
    size = BSF(con)
    return(size)

if __name__ == "__main__":
    print('Compiled')
    

    #For exercise 4 run the following on the console:
    #ERMGen(n, p, nameoffile)
    
    #For exercise 5 run:
    #ComputeGC(filename)
    
    #For exercise 6 run:
    #IterERM()
    #this process takes time since it is poorly optimized

    #For exercise 7 and 8 run:
    #RunEx7and8(log)
    #if the log parameter is 0 it plots a log-log scale
    #if the log parameter is not 0 it plots with a log regression
    
    

#%%

