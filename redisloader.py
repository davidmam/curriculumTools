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

r = redis.Redis(host='redis-19330.c226.eu-west-1-3.ec2.cloud.redislabs.com', port=19330, username='cdev', password=open('redispassword.txt').read())

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
    
routes = {'BIMS': ["BMS","Biomedical Sciences"],
 'NEUR': ["BMS","Neuroscience"],
 'PHAR': ["BMS","Pharmacology"],
 'PHSC': ["BMS","Physiological Sciences"],
 'BIOLOGSCI': ["BIO","Biological Sciences"],
 'BIOC': ["BIO","Biochemistry"],
 'BSBI' : ["BIO","Biological Sciences (Bioinformatics)"],
 'BSPS': ["BIO","Biological Sciences (Plant Sciences)"],
 'MBIO': ["BIO","Microbiology"],
 'MOLG': ["BIO","Molecular Genetics"],
 'MOLB':["BIO","Molecular Biology"],
 'BCDD' : ["BIO","Biological Chemistry and Drug Discovery"]}

prognodes={}

for d in routes:
    prognodes[d] = Node(label='Programme',properties={'name': routes[d][1], 'stream':routes[d][0], 'code':d})
    redis_graph.add_node(prognodes[d])
redis_graph.commit()

wb=openpyxl.open("Tabular programme data - AC 28092022.xlsx")

redis_graph = Graph('curriculum', r)
result=redis_graph.query('''MATCH (m:Module) return m''')
modules = {}
for m in result.result_set:  
    modules[m[0].properties['Module_code']]=m[0]
result=redis_graph.query('''MATCH (p:Programme) return p''')
programmes = {}
for p in result.result_set:  
    programmes[p[0].properties['name']]=m[0]
coreopt = {'C': 'REQUIRED', 'O': 'OPTIONAL'}    
sheet = wb['Program spec']
row = 2
stream = sheet.cell(row=row, column=1).value
while stream:
    #print([x.value for x in sheet[row]])
    try:
        prog=sheet.cell(row=row, column=2).value
        if prog:
            prog = prog.split()[-1][1:-1]
        
        if stream in programmes:
            module=sheet.cell(row=row, column=3).value[:7]
            core = sheet.cell(row=row, column=4).value
            if core not in coreopt:
                print(core, row)
                row=row+1
                stream = sheet.cell(row=row, column=1).value
                continue
            if module in modules:
                params=  {'module':module, 'name':prog,'coreopts':coreopt[core] }
                #print(params)
                if prog:
                    if prog in routes:
                        #pass
                        redis_graph.query("""MATCH (p:Programme {code:$name}) MATCH (m:Module {Module_code:$module})  MERGE (p)-[co:MODULE_TAKING {optional:$coreopts}]->(m)""", params)
                    else:
                        print (F'Unknown route {prog}')
                else:
                    for route in routes:
                        params = {'module':module, 'name':route,'coreopts':coreopt[core] }
                        #print(params)
                        redis_graph.query("""MATCH (p:Programme {code:$name}) MATCH (m:Module {Module_code:$module})  MERGE (p)-[co:MODULE_TAKING {optional:$coreopts}]->(m)""", params)
        else:
            print(F'programme {stream} not found')
        row = row+1
        stream = sheet.cell(row=row, column=1).value
    except Exception as e:
        print(row,module, prog, core, coreopt[core], e)
        row=row+1
            
milos ={}
milocount = 0

sheet = wb['MILO']

row = 2
module = sheet.cell(row=row, column=1).value
while module:
    module = module[:7]
    milo = sheet.cell(row=row, column=2).value
    learning_type = sheet.cell(row=row, column=3).value
    if milo not in milos:
        milocount+=1
        milos[milo]={'milo_id':milocount, 'modules':[], 'type':learning_type}
    milos[milo]['modules'].append(module)
    row = row+1
    module = sheet.cell(row=row, column=1).value
for m in  milos:
    try:
        redis_graph.query("MERGE (milo:MILO {milo_id:$mid, objective:$objective, type:$type})", {'mid':milos[m]['milo_id'], 'objective':m, 'type':milos[m]['type']})
    except:
        print("MERGE (milo:MILO {milo_id:$mid, objective:$objective, type:$type})", {'mid':milos[m]['milo_id'], 'objective':m, 'type':milos[m]['type']})   
    for mod in milos[m]['modules']:
        try:
            redis_graph.query("MATCH (milo:MILO {milo_id:$mid} ) MATCH (m:Module {Module_code:$mod}) MERGE (m) -[:HAS_OBJECTIVE]->(milo)", {'mid':milos[m]['milo_id'], 'mod':mod})
        except:
            print("MATCH (milo:MILO {milo_id:$mid} ) MATCH (m:Module {Module_code:$mod}) MERGE (m) -[:HAS_OBJECTIVE]->(milo)", {'mid':milos[m]['milo_id'], 'mod':mod})   
pilos ={}
pilocount = 0

sheet = wb['PILO']

row = 2
prog = sheet.cell(row=row, column=1).value
while prog:
    
    pilo = sheet.cell(row=row, column=2).value
    learning_type = sheet.cell(row=row, column=3).value
    if pilo not in pilos:
        pilocount+=1
        pilos[pilo]={'pilo_id':milocount, 'programmes':[], 'type':learning_type}
    pilos[pilo]['programmes'].append(prog)
    row = row+1
    prog = sheet.cell(row=row, column=1).value
for p in  pilos:
    redis_graph.query("MERGE (pilo:PILO {pilo_id:$pid, objective:$objective, type:$type})", {'pid':pilos[p]['pilo_id'], 'objective':p, 'type':pilos[p]['type']})
    for pro in pilos[p]['programmes']:
        redis_graph.query("MATCH (pilo:PILO {pilo_id:$pid} ) MATCH (p:Programme {name:$prog}) MERGE (p) -[:HAS_OBJECTIVE]->(pilo)", {'pid':pilos[p]['pilo_id'], 'prog':pro})
     
wb=openpyxl.open("QAA mapping biosciences.xlsx")
wb=openpyxl.open("QAA biomedical benchmarks.xlsx")
sheet = wb['Sheet1']
row = 2
subject = sheet.cell(row=row, column=1).value
while subject:
    data = [str(x.value).strip() for x in sheet[row]]
    params =  {'subject': data[0],
        'section': data[1],
        'subsection': data[2],
        'descriptor': data[3],
        'section_text': data[4],
        'subsection_text': data[5],
        'descriptor_text': data[6]       
        }
    redis_graph.query("MERGE (:QAA_benchmark {subject:$subject, section:$section, subsection:$subsection, descriptor:$descriptor,section_text:$section_text, subsection_text:$subsection_text, descriptor_text:$descriptor_text}) ",params)
    row=row+1
    subject = sheet.cell(row=row, column=1).value

mabfolder = r'S:\Lifesci\LifeSciOff\SLT\2122\SLSLT Teaching Admin\Academic Standards\MAB Structures APP 2122\MABS'

mablist = [x for x in os.listdir(mabfolder) if x.startswith('BS')]

wb=openpyxl.open(os.path.join(mabfolder,mablist[0]))
sheet =wb['MAB']
type(sheet[12][8].value)
for x in mablist[1:]:
    wb=openpyxl.open(os.path.join(mabfolder,x),data_only=True)
    sheet =wb['MAB']
    module = sheet[5][10].value
    credit = sheet[3][13].value
    row=12
    assessment =sheet[row][9].value
    while assessment:
        if type(sheet[row][8].value)==type(1):
            rowdata = [str(v.value) for v in sheet[row]]
            params={'seq':rowdata[8],
                    'name':rowdata[9],
                    'ast':rowdata[10],
                    'type':rowdata[11],
                    'weight':rowdata[12],
                    'credits':str(int(rowdata[12])*credit/100),
                    'module':module,
                    }
            redis_graph.query("MATCH (b:Module {Module_code:$module}) MERGE (a:Assessment {sequence:$seq, name:$name, AST_code:$ast, Assessmnet_type:$type, weight_percent:$weight, credits:$credits,module:$module})  MERGE (b)-[:HAS_ASSESSMENT]->(a)", params)
            #print("MERGE (a:Assessment {sequence:$seq, name:$name, AST_code:$ast, Assessmnet_type:$type, weight_percent:$weight, credits:$credits,module:$module}) MERGE (b) -[:HAS_ASSESSMENT]->(a)", params)
        row +=1
        assessment =sheet[row][9].value
        
            
def make_unique():    
    unique = '''MATCH (p:Module)
    WITH p.id as id, collect(p) AS nodes 
    WHERE size(nodes) >  1
    UNWIND nodes[1..] AS node
    DELETE node'''    
    
    redis_graph.query(unique)
