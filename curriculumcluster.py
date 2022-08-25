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
        modcode = a.split()[0]
        shortmods[modcode]=allmods[a]
        if a[2] in '34' and modcode not in modlist:
            modlist.append(modcode)

   
        mp = shortmods.get(modcode, None)
        
        if mp is None:
            continue
        if modcode not in shortmods:
            continue
        student_list = MRS.extractStudents(mp)
        
        for s in student_list:
            if s not in students:
                students[s]=student_list[s]
            
            if m[2:4]=='41':
                students[s]['year']=y
            else:
                students[s][m]=1
    
def calcroute(student):
    routenum = 0
    for m in modlist:
        if m[2:4]!='41':
            routenum = (routenum <<1) | student.get(m,0)
    bitcount=routenum
    modules=0
    while bitcount:
        modules += (bitcount &1)
        bitcount = bitcount >>1
    if bitcount !=12:
        routenum = 0
    return routenum
                
# should now have all students with a dictionary with all their level 3/4 modules and the year in which they graduated.
studentroutes = {}
for s in students:
    routenum =0
    if calcroute(students[s]) ==0:
        continue
    students[s]['routeval']=calcroute(students[s])
    
    



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

def leafname(n):
    if n < len(studentlist):
        return students[studentlist[n]]['route']
    return ''

# can calculate a distance now for every student. 
# hierarchical clustering.

studentlist = [ x for x in list(students.keys()) if 'routeval' in students[x] and students[x]['routeval']>0]
open('data.json','w').write(json.dumps({'modules':modlist,'students':students}))
labels = [students[s]['route'] for s in studentlist]
distarray =[]
#1D dist 
for n in range(len(studentlist)-1):
    for m in range(n+1, len(studentlist)):
        distarray.append(distance(students[studentlist[n]]['routeval'],students[studentlist[m]]['routeval']))

# now have a distancearray
clusters =  linkage(distarray)
#plt.figure(figsize=(100,100), dpi=600)
plt.clf()
#plt.ioff()
matplotlib.rcParams['lines.linewidth'] = 0.1
dendrogram(clusters)
plt.figure( figsize=(11,8), dpi=600)
#plt.show()
plt.savefig('dendro.pdf', bbox_inches='tight')



