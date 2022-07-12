# -*- coding: utf-8 -*-
"""

Flask application for curriculum DB

Created on Mon Jul 11 14:05:28 2022

@author: dmamartin
"""

from flask import Flask, render_template,request
import mysql.connector
import json
import Models
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
app.config.from_pyfile('config.py')
factory = None



def get_factory():
    global factory,app
    if factory is None:
        mydb = mysql.connector.connect(
          host=app.config['DATABASE_HOST'],
          user=app.config['DATABASE_USER'],
          password=app.config['DATABASE_PASSWORD'],
          database=app.config['DATABASE_NAME']
        )
        factory = Models.CurriculumFactory(mydb)
    return factory

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def index():
    
    return render_template('index.html')

@app.route('/Programme/<progammeID>')
def view_programme(programmeID):
    '''
    Returns a view page for a specific programme

    Parameters
    ----------
    programmeID : TYPE
        DESCRIPTION.

    Returns
    -------
    rendered programme template

    '''
    factory = get_factory()
    if programmeID:
        programme = factory.get_programme_by_id(programmeID)
        
        return render_template('programme.html', prog=programme)    
    
@app.route('/Module/<moduleID>')
def view_module(moduleID):
    '''
    Returns a view page for a specific module

    Parameters
    ----------
    moduleID : TYPE
        DESCRIPTION.

    Returns
    -------
    rendered module template

    '''
    factory = get_factory()
    if moduleID:
        module = factory.get_module_by_id(moduleID)
    
    return render_template('module.html', mod=module)    

@app.route('/Activity/<activityID>')
def view_activity(activityID):
    '''
    Returns a view page for a specific Activity

    Parameters
    ----------
    activityID : text identifier
        DESCRIPTION.

    Returns
    -------
    rendered programme template

    '''
    factory = get_factory()
    if activityID:
        act = factory.get_TeachingActivity_by_id(activityID)
    
    return render_template('activity.html', act=act)    


@app.route('/ajax/programme/add', methods=['POST'])
def add_programme():
    '''
    AJAX call to add/update a programme to the database

    Returns
    -------
    JSON with programme ID

    '''
    fields='ID,P_name,P_code,P_version,Previous_P,change,Future_P,approvalEvent,status'.split(',')
    params={}
    for f in fields:
        params[f]=request.form.get(f)
    prog = factory.get_or_create_programme(**params)
    return json.dumps(prog.toDict()) # Need to add this method to each object #TODO

@app.route('/ajax/module/add', methods=['POST'])
def add_module():
    '''
    AJAX call to add/update a module to the database

    Returns
    -------
    JSON with module ID

    '''
    fields='ID,name,code,version,TMlevel,altlevel,Previous_M,future_M,credits,block,change,approvalEvent,status,sqcflevel'.split(',')
    params={}
    for f in fields:
        params[f]=request.form.get(f)
    mod = factory.get_or_create_Module(**params)
    return json.dumps(mod.toDict()) # Need to add this method to each object #TODO

@app.route('/ajax/activity/add', methods=['POST'])
def add_activity():
    '''
    AJAX call to add/update an activity to the database

    Returns
    -------
    JSON with activity ID

    '''
    fields='ID,name,description,duration,TAtype,version,Previous_TA,moduleID'.split(',')
    params={}
    for f in fields:
        params[f]=request.form.get(f)
    ta = factory.get_or_create_TeachingActivity(**params)
    return json.dumps(ta.toDict()) # Need to add this method to each object #TODO

@app.route('/ajax/programmeILO/add', methods=['POST'])
def add_programmeILO():
    '''
    Add programmeILO

    Returns
    -------
    programmeILO ID

    '''
    fields='ID,ILOtext,category'.split(',')
    params={}
    for f in fields:
        params[f]=request.form.get(f)
    pilo = factory.get_or_create_ProgrammeILO(**params)
    return json.dumps(pilo.toDict()) # Need to add this method to each object #TODO


    
@app.route('/ajax/moduleILO/add', methods=['POST'])
def add_moduleILO():
    '''
    Add moduleILO

    Returns
    -------
    moduleILO ID

    '''
    fields='ID,ILOtext,category,programmeILO'.split(',')
    params={}
    for f in fields:
        params[f]=request.form.get(f)
    milo = factory.get_or_create_ModuleILO(**params)
    return milo.toDict() # Need to add this method to each object #TODO

@app.route('/ajax/activityILO/add', methods=['POST'])
def add_activityILO():
    '''
    Add activityILO

    Returns
    -------
    activityILO ID

    '''
    fields='ID,ILOtext,category,moduleILO,bloom'.split(',')
    params={}
    for f in fields:
        params[f]=request.form.get(f)
    ailo = factory.get_or_create_ActivityILO(**params)
    return ailo.toDict() # Need to add this method to each object #TODO

@app.route('/ajax/programmeILO/map', methods=['POST'])
def map_programmeILO():
    '''
    Map or unmap a ProgrammeILO to a programme

    Returns
    -------
    None.

    '''
    pilo = request.form.get('pilo')
    progID = request.form.get('progID')
    remove = request.form.get('remove')
    factory=get_factory()
    prog = factory.get_programme_by_id(progID)
    ilo = factory.get_ProgrammeILO_by_id(pilo)
    prog.map_ilo(ilo, remove=remove)

@app.route('/ajax/activityILO/map', methods=['POST'])
def map_activityILO():
    '''
    Map or unmap a ActivityILO to a programme

    Returns
    -------
    None.

    '''
    ailo = request.form.get('ailo')
    actID = request.form.get('actID')
    remove = request.form.get('remove')
    factory=get_factory()
    act = factory.get_TeachingActivity_by_id(actID)
    ilo = factory.get_ActivityILO_by_id(ailo)
    act.map_ilo(ilo, remove=remove)

@app.route('/ajax/ModuleILO/map', methods=['POST'])
def map_moduleILO():
    '''
    Map or unmap a ModuleILO to a programme

    Returns
    -------
    None.

    '''
    milo = request.form.get('milo')
    modID = request.form.get('modID')
    remove = request.form.get('remove')
    factory=get_factory()
    mod = factory.get_module_by_id(modID)
    ilo = factory.get_ModuleILO_by_id(milo)
    mod.map_ilo(ilo, remove=remove)

@app.route('/ajax/programmes')
def get_programmes():
    '''
    Return all programmes

    Returns
    -------
    JSON containing programme details

    '''
    factory = get_factory()
    proglist = factory.get_all_programmes()
    
    
@app.route('/ajax/modules')
def get_modules():
    '''
    return all modules

    '''
@app.route('/ajax/activities')
def get_activities():
    '''
    Retrieve all activities

    Returns
    -------
    list of activities

    '''
@app.route('/ajax/programmeILOs')
def get_programmeILOs():
    '''
    retrieve all programmeILO
    '''
@app.route('/ajax/moduleILOs')
def get_moduleILOs():
    '''
    Retreive all moduleILOs
    
    Returns
    -------
    list of ILOs

    '''

@app.route('/ajax/activityILOs')
def get_activityILOs():
    '''
    Retreive a lsit of all activityILOs

    Returns
    -------
    None.

    '''
    
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()