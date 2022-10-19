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
    if m[2] not in '34' or m[2:4] == '41':
        continue
    modlist.append(m.split()[0])

students = {}

yearlist = []
for d in os.listdir(SLTpath):
    if d[0] in '12' and len(d) ==4:
        yearlist.append(d)

for y in yearlist:
    if y <'14' or y >'22':
        continue
    print('Extracting data for ', y)
    path = os.path.join(SLTpath, y, "SLSLT Teaching Admin")
    allmods = MRS.find_modules(path)
    shortmods ={}
    for a in allmods:
        modcode = a.split()[0]
        print('reading',modcode)
        shortmods[modcode]=allmods[a]
        if a[2] in '34' and modcode not in modlist and modcode[2:4] !='41':
            modlist.append(modcode)

   
        mp = shortmods.get(modcode, None)
        
        if mp is None:
            print('No path for ', modcode)
            continue
        if modcode not in shortmods:
            continue
        student_list = MRS.extractStudents(mp)
        
        for s in student_list:
            if s not in students:
                students[s]=student_list[s]
            students[s]['route'] = student_list[s]['route']
            if modcode[2:4]=='41':
                students[s]['year']=y
            else:
                students[s][modcode]=1
    
def calcroute(student):
    routenum = 0
    for m in modlist:
        if m[2:4]!='41':
            routenum = (routenum <<1) + student.get(m,0)
    bitcount=routenum
    modules=0
    while bitcount:
        modules += (bitcount &1)
        bitcount = bitcount >>1
    if modules !=12:
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


# can calculate a distance now for every student. 
# hierarchical clustering.

studentlist = [ x for x in list(students.keys()) if 'routeval' in students[x] and students[x]['routeval']>0]
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
        parts =[]
        for k in nodes[nodenumbers[n]]:
            parts.append(f"{k} {nodes[nodenumbers[n]][k]}")
        nodelabel = " ".join(parts)
    
    return nodelabel
    

def compareroutes(route1,route2):
    shared = []
    mods1 = []
    mods2 = []
    for p in range(len(modlist)):
        if route1 &route2 &1:
            shared.append(modlist[-(p+1)])
        elif route1 & 1:
            mods1.append(modlist[-(p+1)])
        elif route2 & 1:
            mods2.append(modlist[-(p+1)])
        route1 = route1>>1
        route2 = route2>>1
    return (mods1,shared, mods2)
#for n in range(len(studentlist)-1):
#    for m in range(n+1, len(studentlist)):
#        distarray.append(distance(students[studentlist[n]]['routeval'],students[studentlist[m]]['routeval']))

for n in range(len(nodenumbers)-1):
    for m in range(n+1, len(nodenumbers)):
        distarray.append(distance(nodenumbers[n], nodenumbers[m]))
        

routecores = {}
for s in studentlist:
    if students[s]['route'] not in routecores:
        routecores[students[s]['route']] = students[s]['routeval']
    routecores[students[s]['route']] = students[s]['routeval'] & routecores[students[s]['route']]



def viewset (rv):
    coremods = []
    for p in range(len(modlist)):
        if rv & 1:
            coremods.append(modlist[len(modlist)-p-1])
        rv = rv >>1
    return coremods

coremodules = {}
for rv in routecores:
    coremodules[rv] = viewset(routecores[rv])

def setscore (arr):
    score = 0
    for m in modlist:
        if m in arr:
            score = score+1
        score = score <<1
    return score

routecompare={}

routes = ['BIMS',
 'NEUR',
 'PHAR',
 'PHSC',
 'BIOLOGSCI',
 'BIOC',
 'BSBI',
 'BSPS',
 'MBIO',
 'MOLG',
 'MOLB',
 'BCDD']

routecomparevals = [['']+routes]
for r in range(len(routes)):
    routecomparevals.append([routes[r]])
    routecompare[routes[r]] = {}
    for p in range(len(routes)):
        routecompare[routes[r]][routes[p]] = compareroutes(routecores[routes[r]], routecores[routes[p]])
        if p >r:
            routecomparevals[-1].append(len(routecompare[routes[r]][routes[p]][0]))
        elif p< r:
            routecomparevals[-1].append(len(routecompare[routes[r]][routes[p]][0]))
        else:
            routecomparevals[-1].append(0)

ofh = open('routes.txt', 'w')
for r in routecomparevals:
    print('\t'.join([str(x) for x in r]), file=ofh)
ofh.close()
        
    


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


#Analyse BS32007

chemlist = []
for s in students:
    if 'BS32003' in students[s] and (('year' in students[s] and students[s]['year'] >'17') ) :
        chemlist.append(s)
chemstud ={}     
for s in chemlist:
    optmod =0
    if 'BS12009' in students[s]:
        optmod += 1
    optmod <<1
    if 'BS21008' in students[s]:
        optmod += 1
    chemstud[optmod] = chemstud.get(optmod, 0) +1

BS12009 = 0
BS32007 = 0
for s in students:
    if 'BS12009' in students[s]:
        BS12009 +=1
        if 'BS32007' in students[s]:
            BS32007 +=1

BS21008 = 0
BS12009 =0
lastyear =[]
for p in [s for s in students if students[s].get('year')== None and 'BS32007' in students[s]]:
    lastyear.append(p)
    if 'BS21008' in students[p]:
        BS21008 +=1
    if 'BS12009' in students[p]:
        BS12009 +=1
        
ty = '''190005425
180009134
190007502
190004336
190008401
190011105
190009741
180010321
2482731
190016774
190005462
190006798
190000099
190007244
190013371
190004204
190005385
190010063
2465271'''.split('\n')

tys =[]
for s in students:
    if s[:9] in ty or ( s[0]=='2' and s[:7] in ty):
        tys.append(s)

tyg ={}
for s in tys:
    modscore = 0
    if 'BS12009' in students[s]:
        modscore +=1
    if 'BS21008' in students[s]:
        modscore +=2
    tyg[modscore] = tyg.get(modscore,0)+1

# check cancer biology module choices

counts = {}
for s in students:
    if 'BS42007' in students[s]:
        for m in students[s]:
            if m.startswith('BS3') or m.startswith('BS4'):
                counts[m] = counts.get(m,0)+1
                

countsboth = {}
for s in students:
    if 'BS42007' in students[s] and 'BS42027' in students[s] and students[s]['route']=='BIMS':
        for m in students[s]:
            if m.startswith('BS3') or m.startswith('BS4'):
                countsboth[m] = countsboth.get(m,0)+1

#Check for cardiovascular
countsboth = {}
for s in students:
    if 'BS42019' in students[s] and 'BS42021' in students[s] and students[s]['route']=='BIMS':
        for m in students[s]:
            if m.startswith('BS3') or m.startswith('BS4'):
                countsboth[m] = countsboth.get(m,0)+1

# Check for metabolic disease
countsboth = {}
for s in students:
    if 'BS42014' in students[s] and 'BS42028' in students[s] and students[s]['route']=='BIMS':
        for m in students[s]:
            if m.startswith('BS3') or m.startswith('BS4'):
                countsboth[m] = countsboth.get(m,0)+1
                
routecounts={}
for r in routecores:
    routecounts[r] = {}
    for s in students:
        if routecores[r] == routecores[r] & students[s].get('routeval',0):
            routecounts[r][students[s]['route']] = routecounts[r].get(students[s]['route'],0)+1

hiddenroutes =[]
hiddenroutes.append(routes[:])
for r in routes:
    hiddenroutes.append([r])
    for c in routes:
        hiddenroutes[-1].append(routecounts[r].get(c,0))
        
for a in hiddenroutes:
    print('\t'.join([str(x) for x in a]))        
    


