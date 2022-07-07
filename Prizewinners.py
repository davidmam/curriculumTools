# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 11:29:04 2022

@author: DMAMartin
"""

from tkinter import Tk
from tkinter.filedialog import askdirectory
import os
import openpyxl
from MRS import find_modules

def main():
    root = Tk()
    
    TAdir = askdirectory(title="TA folder")
    root.destroy()
    mrs = find_modules(TAdir)
    mods = list(mrs.keys())
   
    basemod =''
    for m in mods:
        if m[:7]=="BS21001":
            basemod = m
            break
    studentgrades=extractStudents(mrs[basemod]) # should get students from BS11001
    for mod in mods:
        if mod in mrs:
            grades = extractgrades(mrs[mod])
            for s in grades:
                if s in studentgrades:
                    studentgrades[s][mod]=grades[s]
    scores={}
    
    
    for s in studentgrades:
        scores[s]=0
        credittotal=0
        for m in studentgrades[s]:
            if m[:2]=='BS':
                credit=20
                if m.split()[0] in ['BS21001', 'BS21002', 'BS22001', 'BS22002']:
                    credit=10
                try:
                    scores[s] += credit*studentgrades[s][m]
                except:
                    print('could not multiply {} by {}'.format(studentgrades[s][m], credit))
                    scores[s] +=0
                credittotal+=credit
        scores[s]=scores[s]/credittotal
    ofh=open("L2 mean scores.txt ", "w")
    for s in studentgrades:
        g = studentgrades[s]
        print(s, g['firstname'], g['lastname'], g['route'], scores[s], sep="\t", file=ofh)
    ofh.close()
    
def extractgrades(file):
    workbook=openpyxl.load_workbook(filename=file, data_only=True)
    sheet = workbook['OVERALL Results']
    row = 5
    grades={}
    matric = sheet.cell(row=row, column=1).value
    grade = sheet.cell(row=row, column=8).value
    while matric:
        grades[matric]=grade
        row +=1
        matric = sheet.cell(row=row, column=1).value
        grade = sheet.cell(row=row, column=8).value
    return grades

def extractStudents(file):
    workbook=openpyxl.load_workbook(filename=file, data_only=True)
    sheet = workbook['OVERALL Results']
    row = 5
    students={}
    matric = sheet.cell(row=row, column=1).value
    lastname = sheet.cell(row=row, column=2).value
    firstname = sheet.cell(row=row, column=3).value
    route = sheet.cell(row=row, column=4).value
    while matric:
        students[matric]={"firstname":firstname, "lastname":lastname, "route":route}
        row +=1
        matric = sheet.cell(row=row, column=1).value
        lastname = sheet.cell(row=row, column=2).value
        firstname = sheet.cell(row=row, column=3).value
        route = sheet.cell(row=row, column=4).value
    return students