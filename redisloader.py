# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 09:41:18 2022
Load module information into the redis DB
@author: dmamartin

"""

import openpyxl
import redis
import os
from redisgraph import Node, Edge, Graph, Path

r = redis.Redis(host='redis-19330.c226.eu-west-1-3.ec2.cloud.redislabs.com', port=19330, username='default', password=open('redispassword.txt').read())

redis_graph = Graph('curriculum', r)

wb=openpyxl.open("zz MASTER MODULE MANAGERS LIST Office 2022-23.xlsx")
sheet=wb['Master']
nodes=[]
headers = [ str(x.value).strip().replace(' ','_').replace('C/','') for x in sheet[3]]
nodedata = []    

for row in range(4,90):
    params = {}
    for c in range(12):
        val = sheet.cell(row=row, column=c+1).value
        if val:
            params[headers[c]] = val
    print(params)
    params['name'] = params['Module_code']+" "+params['Module_Name']
    nodedata.append(params)
    nodes.append(Node(label='Module', properties=params))

for n in nodes:
    redis_graph.add_node(n)    
redis_graph.commit()

graphnodes={}

for n in redis_graph.nodes:
    graphnodes[redis_graph.nodes[n].properties['Module_code']] = redis_graph.nodes[n]
coremodules={}
for m in nodedata:
    if m.get('Optonal_Modules','') == 'C':
        if m['Level'] not in coremodules:
            coremodules[m['Level']] ={}
        if m['Semester'] not in coremodules[m['Level']]:
            coremodules[m['Level']][m['Semester']]=[]
        coremodules[m['Level']][m['Semester']].append(m)

for l in range(1,5):
    level1 = int((l)/2)+1
    level2 = int((l+1)/2)
    semester1 = l%2 +1
    semester2 = (l+1)%2+1
    for m in coremodules[level1][semester1]:
        for n in coremodules[level2][semester2]:
            redis_graph.add_edge(Edge(graphnodes[m['Module_code']], 'HAS_PREREQUISITE', graphnodes[n['Module_code']]))
    print(F'L{level1} S{semester1} L{level2} S{semester2}')
    