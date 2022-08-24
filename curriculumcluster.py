# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 19:04:17 2022


Script to map and compare all student routes.
@author: marti
"""
import os
from scipy.cluster.hierarchy import linkage,dendrogram
from matplotlib import pyplot as plt
import MRS

SLTpath = 's:' # put path to SLT here

# get module list for level 3 and 4 in 21/22

modyear = '2223'

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
    
    path = os.path.join(SLTpath, y, "SLSLT Teaching Admin")
    allmods = MRS.find_modules(path)
    for a in allmods:
        if a.count(' '):
            allmods[a.split()[0]]=allmods[a]
    for m in modlist:
        mp = allmods.get(m, None)
        if m is None:
            continue
        student_list = MRS.extractStudents(allmods[m])
        
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
        distance = distance - (val >>1)
        val = val>>1
    return distance/maximum

# can calculate a distance now for every student. 
# hierarchical clustering.

studentlist = list(students.keys())
distarray =[]
#1D dist 
for n in range(len(studentlist)-1):
    for m in range(n+1, len(studentlist)):
        distarray.append(distance(students[studentlist[n]]['routeval'],students[studentlist[m]]['routeval']))

# now have a distancearray
clusters =  linkage(distarray)
plt.clf()
plt.ioff()
dendrogram(clusters,no_label=True)

plt.show()
#plt.savefig('dendro.pdf')



