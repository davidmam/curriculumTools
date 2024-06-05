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
    progs ={'core':module.getEdges(relation='IS_CORE'),
            'elective': module.getEdges(relation='IS_ELECTIVE')}
    ilos={}
    for i in module.ILO:
        ilos[i] ={}
        ilos[i].update(module.ILO[i][0])
        ilos[i].update(module.ILO[i][1])
        ilos[i]['endyear']=ilos[i].get('endyear','')
        ilos[i]['id']=i.replace(':','_')
    milos=sorted(ilos.values(), key=lambda x:x.get('rank', x['id']))

    
    return render_template('module.html', module=module, ilos=milos,progs=progs)

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
    except Exception as e:
        return render_template('not_found.html',exception=e)
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
        ilos[i]['id']=i.replace(':','_')
    pilos=sorted(ilos.values(), key=lambda x:x.get('rank', x['id']))
    return render_template('programme.html', modules=levels, ilos=pilos, programme=programme)

@app.route('/moduleilo/<iloid>', methods=['GET', 'POST'])     
def moduleilo(iloid):
    '''
    Show/map ModuleILO

    Parameters
    ----------
    iloid : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    
    try:
        milo=factory.get_element_by_ID(iloid.replace('_',':'))
    except:
        return render_template('not_found.html')
    if request.method=='POST':
        # Do the updates
        pass
    edges=milo.getEdges()
    edgesbytype = {}
    for e in edges:
        et = e['edge'].type
        if et not in edgesbytype:
            edgesbytype[et]=[]
        edgesbytype[et].append(e)
    mods = [(dict(m['target'])['code'], dict(m['target'])['name']) for m in edgesbytype['HAS_ILO']]  
    maps={}
    for q in edgesbytype.get('MAPS_TO',[]):
        crit=q['target'].element_id
        if crit not in maps:
            maps[crit]=[] 
        maps[crit].append((q['target'], q['edge']))
    rsb = factory.get_all_elements('RSBCriterion')   
    qaa=factory.get_all_elements('QAABenchmark')   
    pilo=factory.get_all_elements('ProgrammeILO')
    nibs=factory.get_all_elements('NIBLSEcompetency')
    
    
    return render_template('moduleilo.html', milo=milo, rsbs=rsb,qaas=qaa,pilos=pilo, nibs=nibs, mods=mods, maps=maps)

@app.route('/programmeilo/<iloid>', methods=['GET', 'POST'])     
def programmeilo(iloid):
    '''
    Show/map ModuleILO

    Parameters
    ----------
    iloid : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    
    try:
        pilo=factory.get_element_by_ID(iloid.replace('_',':'))
    except:
        return render_template('not_found.html')
    if request.method=='POST':
        # Do the updates
        pass
    edges=pilo.getEdges()
    edgesbytype = {}
    for e in edges:
        et = e['edge'].type
        if et not in edgesbytype:
            edgesbytype[et]=[]
        edgesbytype[et].append(e)
    progs = [(dict(m['target'])['code'], dict(m['target'])['name']) for m in edgesbytype['HAS_ILO'] if 'code' in dict(m['target'])]  
    maps={}
    for q in edgesbytype.get('MAPS_TO',[]):
        crit=q['target'].element_id
        if crit not in maps:
            maps[crit]=[] 
        maps[crit].append((q['target'], q['edge']))
    rsb = factory.get_all_elements('RSBCriterion')   
    qaa=factory.get_all_elements('QAABenchmark')   
    nibs=factory.get_all_elements('NIBLSEcompetency')
    
    
    return render_template('programmeilo.html', pilo=pilo, rsbs=rsb,qaas=qaa, nibs=nibs, progs=progs, maps=maps)

@app.route('/ajax/moduleilo', methods=['POST'])
def ajax_module_ilo():
   '''
    Ordering/change/delete of module ILO

    Returns
    -------
    None.

    '''   
@app.route('/ajax/benchmarkilo', methods=['POST'])
def ajax_ilo_benchmark():
    '''
    Map or change mapping for an ilo set against a benchmark.

    Post parameters are Benchmark type, benchmark IDs for mapping, ILO id.
    Returns
    -------
    None.

    '''