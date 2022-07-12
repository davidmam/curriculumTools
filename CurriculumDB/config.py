# -*- coding: utf-8 -*-
"""
Configurations for FLASK
Created on Tue Jul 12 11:03:37 2022

@author: dmamartin
"""
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

TESTING = True
DEBUG = True
FLASK_ENV = 'development'
SECRET_KEY = environ.get('SECRET_KEY')


# MySQL setup
DATABASE_HOST = 'localhost'
DATABASE_NAME = 'curriculum'
DATABASE_USER = 'curriculum'
DATABASE_PASSWORD = environ.get('DATABASE_PW')
