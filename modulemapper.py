from flask import Flask, render_template, request
import sys
from CurriculumDB.Modelsn4j import *
from neo4j import GraphDatabase
app = Flask(__name__)

URI = "bolt://localhost:7687"
AUTH = ("curriculum", "mycurriculum")

driver = GraphDatabase.driver(URI, auth=AUTH)
try:
    driver.verify_connectivity()
except:
    print('Connection Failed')
factory = CurriculumFactory(driver, 'curriculumdb')

@app.route("/")
def index():
    '''
    Basic Flask app for handling module mapping

    Returns
    -------
    Rendered template

    '''
    progs = factory.get_all_elements('Programme')
    print('Progs',len(progs), file=sys.stderr)
    mods = factory.get_all_elements('Module')
    
    return render_template('index.html', programmes=progs, modules=mods)
    
@app.route("/module/<modcode>", methods=['GET', 'POST'])
def module(modcode):
    '''
    Generate page for a module.

    Parameters
    ----------
    modcode : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    try:
        module=factory.get_or_create_Element('Module', code=modcode)
    except:
        return render_template('not_found.html')
    if request.method=='POST':
        # Do the updates
        pass
    #get the necessary data lists
    ilos={}
    for i in module.ILO:
        ilos[i] ={}
        ilos[i].update(module.ILO[i][0])
        ilos[i].update(module.ILO[i][1])
        ilos[i]['endyear']=ilos[i].get('endyear','')
    
    return render_template('module.html', module=module, ilos=ilos)

@app.route("/programme/<prog>", methods=['GET', 'POST'])

def programme(prog):
    '''
    Generate page for a programme

    Parameters
    ----------
    prog : string
        programme code.

    Returns
    -------
    rendered programme template

    '''
   
    try:
        programme=factory.get_or_create_Element('Programme', code=prog)
    except:
        return render_template('not_found.html')
    if request.method=='POST':
        # Do the updates
        pass
    levels = {}
    for m in programme.modules:
        for item in programme.modules[m]:
            level= item['target']['params']['shelevel']
            semester = item['target']['params']['semester']
            code=m
            name = item['target']['params']['name']
            credits =item['target']['params']['credits']
            core = item['relation']['type']
            startyear = item['relation']['params']['startyear']
            endyear = item['relation']['params'].get('endyear','')
            if level not in levels:
                levels[level]={}
            if semester not in levels[level]:
                levels[level][semester]={}
            if core not in levels[level][semester]:
                levels[level][semester][core]={}
            if code not in levels[level][semester][core]:
                levels[level][semester][core][code]=[]
            levels[level][semester][core][code].append({"name":name, "credits":credits, "sy":startyear, "ey":endyear})
    ilos={}     
    for i in programme.ILO:
        ilos[i] ={}
        ilos[i].update(programme.ILO[i][0])
        ilos[i].update(programme.ILO[i][1])
        ilos[i]['endyear']=ilos[i].get('endyear','')
    
    return render_template('programme.html', modules=levels, ilos=ilos, programme=programme)

        
    