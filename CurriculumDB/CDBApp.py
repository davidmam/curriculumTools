# -*- coding: utf-8 -*-
"""

Flask application for curriculum DB

Created on Mon Jul 11 14:05:28 2022

@author: dmamartin
"""

from flask import Flask
import Models
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

factory = None

def get_factory():
    global factory
    if factory is None:
        factory = Models.CurriculumFactory()
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


    
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()