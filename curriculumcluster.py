# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 19:04:17 2022


Script to map and compare all student routes.
@author: marti
"""
import os
from scipy.cluster.hierarchy import linkage,dendrogram
from matplotlib import pyplot as plt
import matplotlib
import json
import MRS

SLTpath = r'S:\Lifesci\LifeSciOff\SLT' # put path to SLT here

# get module list for level 3 and 4 in 21/22

modyear = '2122'

path = os.path.join(SLTpath,modyear,"SLSLT Teaching Admin")
allmods = MRS.find_modules(path)

modlist = []
for m in allmods:
    if m[2] not in '34':
        continue
    modlist.append(m.split()[0])

students = {}

yearlist = []
for d in os.listdir(SLTpath):
    if d[0] in '12':
        yearlist.append(d)

for y in yearlist:
    if y <'18':
        continue
    print('Extracting data for ', y)
    path = os.path.join(SLTpath, y, "SLSLT Teaching Admin")
    allmods = MRS.find_modules(path)
    shortmods ={}
    for a in allmods:
        shortmods[a.split()[0]]=allmods[a]
    for m in modlist:
        mp = shortmods.get(m, None)
        if m is None:
            continue
        if m not in shortmods:
            continue
        student_list = MRS.extractStudents(shortmods[m])
        
        for s in student_list:
            if s not in students:
                students[s]=student_list[s]
            
            if m[2:4]=='41':
                students[s]['year']=y
            else:
                students[s][m]=1
                
# should now have all students with a dictionary with all their level 3/4 modules and the year in which they graduated.
studentroutes = {}
for s in students:
    routenum =0
    if len(students[s]) != 16:
        continue
    
    for m in modlist:
        if m[2:4]!='41':
            routenum = (routenum <<1) | students[s].get(m,0)
    students[s]['routeval'] = routenum



def distance(num1, num2, maximum=12):
    val = num1 & num2
    distance = maximum
    while val:
        distance = distance - (val & 1)
        val = val>>1
    try:
        assert distance>=0  
    except:
        print(num1, bin(num1), num2, bin(num2), (num1 & num2), bin(num1 & num2))
    return distance/maximum


# can calculate a distance now for every student. 
# hierarchical clustering.

studentlist = [ x for x in list(students.keys()) if 'routeval' in students[x]]
open('data.json','w').write(json.dumps({'modules':modlist,'students':students}))
labels = [students[s]['route'] for s in studentlist]
distarray =[]
#1D dist 

nodes = {}
for s in studentlist:
    nv = students[s]['routeval']
    if nv not in nodes:
        nodes[nv] = {}
    nodes[nv][students[s]['route']] = nodes[nv].get(students[s]['route'],0)+1

nodenumbers = list(nodes.keys())

def leafname(n):
    nodelabel = ''
    if n < len(nodenumbers):
        for k in nodes[nodenumbers[n]]:
            nodelabel = " ".join([str(x) for x in [nodelabel,k,nodes[nodenumbers[n]][k]]])
    
    return nodelabel
    
    
#for n in range(len(studentlist)-1):
#    for m in range(n+1, len(studentlist)):
#        distarray.append(distance(students[studentlist[n]]['routeval'],students[studentlist[m]]['routeval']))

for n in range(len(nodenumbers)-1):
    for m in range(n+1, len(nodenumbers)):
        distarray.append(distance(nodenumbers[n], nodenumbers[m]))
        

# now have a distancearray
clusters =  linkage(distarray)
#plt.figure(figsize=(100,100), dpi=600)
#plt.clf()
#plt.ioff()
matplotlib.rcParams['lines.linewidth'] = 0.5
dendrogram(clusters, leaf_label_func=leafname)
#plt.figure( figsize=(11,8), dpi=600)
#plt.show()
plt.savefig('dendro.pdf', bbox_inches='tight')



