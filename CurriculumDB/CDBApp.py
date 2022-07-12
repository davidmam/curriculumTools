# -*- coding: utf-8 -*-
"""

Flask application for curriculum DB

Created on Mon Jul 11 14:05:28 2022

@author: dmamartin
"""

from flask import Flask
import mysql.connector
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
    return 'Hello World'

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

@app.route('/ajax/programme/add', methods=['POST'])
def add_programme():
    '''
    AJAX call to add a programme to the database

    Returns
    -------
    JSON with programme ID

    '''

@app.route('/ajax/module/add', methods=['POST'])
def add_module():
    '''
    AJAX call to add a module to the database

    Returns
    -------
    JSON with module ID

    '''

@app.route('/ajax/activity/add', methods=['POST'])
def add_activity():
    '''
    AJAX call to add an activity to the database

    Returns
    -------
    JSON with programme ID

    '''

@app.route('/ajax/programmeILO/add', methods=['POST'])
@app.route('/ajax/moduleILO/add', methods=['POST'])
@app.route('/ajax/activityILO/add', methods=['POST'])
@app.route('/ajax/programmes')
@app.route('/ajax/modules')
@app.route('/ajax/activities')
@app.route('/ajax/programmeILOs')
@app.route('/ajax/moduleILOs')
@app.route('/ajax/activitieILOs')

    
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()