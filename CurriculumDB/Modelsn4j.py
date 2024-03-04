# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 20:34:24 2022

@author: DMAMartin
"""

from functools import lru_cache

# Neo4J database wrappers.

#TODO

class CurriculumFactory():
    
    def __init__(self, db):
        self.db = db
        self.programmecache = {}
        self.modulecache = {}
        self.activitycache = {}
        self.personcache = {}
        
    def get_connection(self):
        return self.db
        
    def get_or_create_programme(self, **kwargs):
        '''
        Create a new Programme object, retrieving from the database as necessary,or from the cache
        

        Parameters
        ----------
        **kwargs : either id or P_name and P_code must be present. 

        Returns
        -------
        Programme object

        '''
        prog = None
        if kwargs.get('id',None):
            prog = self.get_programme_by_id(kwargs['id'])
        else:
            prog = Programme(self, P_name = kwargs.get('P_name'), P_code= kwargs.get('P_code'), P_version = kwargs.get('P_version','UNK'), P_previous=kwargs.get('P_previous'))
            prog = self.get_programme_by_id(prog.id)
            
        return prog
        
    @lru_cache
    def get_programme_by_id(self, id):
        '''
        retreives the given id numebr program from the database and caches the object.        

        Parameters
        ----------
        id : integer
            unique identifier for a Programme

        Returns
        -------
        Programme

        '''
        query = "SELECT P_name, P_code, P_version,Previous_P, Future_P, approvalEvent, status, change from Programme where ID = %s "
        cursor = self.db.cursor()
        cursor.execute(query, (id)) 
        (P_name, P_code, P_version,Previous_P, Future_P, approvalEvent,status,change) = cursor.fetchone()
        args = {"id":id, "P_name":P_name, "P_code":P_code, "P_version":P_version, "Previous_P":Previous_P, "Future_P":Future_P, "approvalEvent":approvalEvent, "status":status, "change": change}
        prog = Programme(self, **args)
        return prog
    
    @lru_cache
    def get_module_by_id(self, id):
        '''
        retreives the given id number Module from the database and caches the object.        

        Parameters
        ----------
        id : integer
            unique identifier for a Module

        Returns
        -------
        Module

        '''
        query = "SELECT name, code, TMlevel, altlevel, version, credits, block, change, Previous_M, Future_P, approvalEvent, status, sqcflevel from TModule where ID = %s "
        cursor = self.db.cursor()
        cursor.execute(query, (id))
        (name, code, TMlevel, altlevel, version, credits, block, change, Previous_M, Future_M, approvalEvent,status, sqcflevel) = cursor.fetchone()
        args = {"id":id, "name":name, "code":code, "level":TMlevel, "altlevel":altlevel,  "version":version,"credits": credits, "block": block, 
                "change": change, "Previous_M":Previous_M, "Future_M":Future_M, "approvalEvent":approvalEvent, "status":status, 'sqcflevel':sqcflevel}
        prog = Module(self, **args)
        return prog

    def get_or_create_Module(self, **kwargs):
        '''
        Create a new Module object, retrieving from the database as necessary,or from the cache
        

        Parameters
        ----------
        **kwargs : either id or name and code must be present. 

        Returns
        -------
        Module object

        '''
        mod = None
        if kwargs.get('id',None):
            mod = self.get_module_by_id(kwargs['id'])
        else:
            mod = Module(self, name = kwargs.get('name'), code= kwargs.get('code'), version = kwargs.get('version',None),credits=kwargs.get("credits"), block=kwargs.get('block') )
            mod = self.get_module_by_id(mod.id)
           
        return mod
    
    @lru_cache
    def get_TeachingActivityType_by_id(self, id):
        '''
        retreives the given id number TeachingActivityType from the database and caches the object.        

        Parameters
        ----------
        id : integer
            unique identifier for a TeachingActivityType

        Returns
        -------
        Module

        '''
        query = "SELECT name, definition from TeachingActivityType where ID = %s "
        cursor = self.db.cursor()
        cursor.execute(query, (id))
        (name, definition) = cursor.fetchone()
        args = {"id":id, "name":name, "definition": definition}
        prog = TeachingActivityType(self, **args)
        return prog

    def get_or_create_TeachingActivityType(self, **kwargs):
        '''
        Create a new TeachingActivityType object, retrieving from the database as necessary,or from the cache
        

        Parameters
        ----------
        **kwargs : either id or name and definition must be present. 

        Returns
        -------
        TeachingActivityType object

        '''
        mod = None
        if kwargs.get('id',None):
            mod = self.get_TeachingActivityType_by_id(kwargs['id'])
        else:
            mod = TeachingActivityType(self, **kwargs)
            mod = self.get_TeachingActivityType_by_id(mod.id)
        return mod
        

    @lru_cache
    def get_TeachingActivity_by_id(self, id):
        '''
        retreives the given id number TeachingActivity from the database and caches the object.        

        Parameters
        ----------
        id : integer
            unique identifier for a TeachingActivity

        Returns
        -------
        TeachingActivity
        
        CREATE or REPLACE Table TeachingActivity (
        ID integer not null primary key auto_increment,
        name text not null,
        description text not null,
        duration integer not null,
        TAtype integer not null,
        version text,
        previous_TA integer,
        moduleID integer not null,
        sequence integer not null,
        foreign key (moduleID) references TModule (ID),
        foreign key (previous_TA) references TeachingActivity (ID),
        foreign key (TAtype) references TeachingActvityType (ID)
        );


        '''
        query = "SELECT name, description, duration, TAtype, version,previous_TA, moduleID, sequence from TeachingActivity where ID = %s "
        cursor = self.db.cursor()
        cursor.execute(query, (id))
        (name, description, duration, TAtype, version,previous_TA, moduleID, sequence, weighting) = cursor.fetchone()
        args = {"id":id, "name":name,  "description":description, "duration":duration, "TAtype":TAtype, "version":version, "previous_TA":previous_TA, "moduleID":moduleID, "sequence":sequence, "weighting":weighting}
        prog = TeachingActivity(self, **args)
        return prog

    def get_or_create_TeachingActivity(self, **kwargs):
        '''
        Create a new TeachingActivity object, retrieving from the database as necessary,or from the cache
        

        Parameters
        ----------
        **kwargs : either id or name and definition must be present. 

        Returns
        -------
        TeachingActivityType object

        '''
        mod = None
        if kwargs.get('id',None):
            mod = self.get_TeachingActivity_by_id(kwargs['id'])
        else:
            mod = TeachingActivity(self, **kwargs)
            mod = self.get_TeachingActivity_by_id(mod.id)
            
        return mod
        
    @lru_cache
    def get_ProgrammeILO_by_id(self, id):
        '''
        retreives the given id number TeachingActivity from the database and caches the object.        

        Parameters
        ----------
        id : integer
            unique identifier for a TeachingActivity

        Returns
        -------
        ProgrammeILO
        
CREATE or REPLACE Table ProgrammeILO (
ID integer not null auto_increment primary key,
ILOtext text not null,
category ENUM('Knowledge','Understanding', 'Skill', 'Attitude') not null
);


        '''
        query = "SELECT ILOtext, category from ProgrammeILO where ID = %s "
        cursor = self.db.cursor()
        cursor.execute(query, (id))
        (ILOtext, category ) = cursor.fetchone()
        args = {"id":id, "ILOtext":ILOtext, "category":category}
        prog = ProgrammeILO(self, **args)
        return prog


    def get_or_create_ProgrammeILO(self, **kwargs):
        '''
        Create a new TeachingActivity object, retrieving from the database as necessary,or from the cache
        

        Parameters
        ----------
        **kwargs : either id or name and definition must be present. 

        Returns
        -------
        ProgrammeILO object

        '''
        mod = None
        if kwargs.get('id',None):
            mod = self.get_ProgrammeILO_by_id(kwargs['id'])
        else:
            mod = ProgrammeILO(self, **kwargs)
            mod = self.get_ProgrammeILO_by_id(mod.id)
            
        return mod
        
    @lru_cache
    def get_ModuleILO_by_id(self, id):
        '''
        retreives the given id number TeachingActivity from the database and caches the object.        

        Parameters
        ----------
        id : integer
            unique identifier for a TeachingActivity

        Returns
        -------
        ModuleILO
        
        CREATE or REPLACE Table ModuleILO (
        ID integer not null auto_increment primary key,
        ILOtext text not null,
        category ENUM('Knowledge','Understanding', 'Skill', 'Attitude') not null,
        programmeILO integer not null,
        foreign key (programmeILO) references ProgrammeILO (ID)
        );



        '''
        query = "SELECT ILOtext, category, programmeILO, bloom from ModuleILO where ID = %s "
        cursor = self.db.cursor()
        cursor.execute(query, (id))
        (ILOtext, category, programmeILO ) = cursor.fetchone()
        args = {"id":id, "ILOtext":ILOtext, "category":category, "programmeILO":programmeILO}
        prog = ModuleILO(self, **args)
        return prog


    def get_or_create_ModuleILO(self, **kwargs):
        '''
        Create a new TeachingActivity object, retrieving from the database as necessary,or from the cache
        

        Parameters
        ----------
        **kwargs : either id or name and definition must be present. 

        Returns
        -------
        TeachingActivityType object

        '''
        mod = None
        if kwargs.get('id',None):
            mod = self.get_ModuleILO_by_id(kwargs['id'])
        else:
            mod = ModuleILO(self, **kwargs)
            mod = self.get_ModuleILO_by_id(mod.id)
            
        return mod
        
    @lru_cache
    def get_ActivityILO_by_id(self, id):
        '''
        retreives the given id number TeachingActivity from the database and caches the object.        

        Parameters
        ----------
        id : integer
            unique identifier for a TeachingActivity

        Returns
        -------
        ActivityILO
       CREATE or REPLACE Table ActivityILO (
       ID integer not null auto_increment primary key,
       ILOtext text not null,
       category ENUM('Knowledge','Understanding', 'Skill', 'Attitude') not null,
       moduleILO integer,
       bloom ENUM('None','Remember',	'Understand',	'Apply',	'Analyze',	'Evaluate',	'Create') Not null,
       Foreign Key (moduleILO) REFERENCES ModuleILO (ID)
       );


        '''
        query = "SELECT ILOtext, category, moduleILO, bloom from ActivityILO where ID = %s "
        cursor = self.db.cursor()
        cursor.execute(query, (id))
        (ILOtext, category, moduleILO, bloom ) = cursor.fetchone()
        args = {"id":id, "ILOtext":ILOtext, "category":category, "moduleILO":moduleILO, "bloom":bloom}
        prog = ActivityILO(self, **args)
        return prog

    def get_or_create_ActivityILO(self, **kwargs):
        '''
        Create a new ActivityILO object, retrieving from the database as necessary,or from the cache
        

        Parameters
        ----------
        **kwargs : either id or name and definition must be present. 

        Returns
        -------
        ActivityILO object

        '''
        mod = None
        if kwargs.get('id',None):
            mod = self.get_ActivityILO_by_id(kwargs['id'])
        else:
            mod = ActivityILO(self, **kwargs)
            mod = self.get_ActivityILO_by_id(mod.id)
            
        return mod
        
    @lru_cache
    def get_AssessmentType_by_id(self, id):
        '''
        retreives the given id number AssessmentType from the database and caches the object.        

        Parameters
        ----------
        id : integer
            unique identifier for a TeachingActivity

        Returns
        -------
        AssessmentType
       
CREATE or REPLACE TABLE AssessmentType (
ID integer not null primary key auto_increment,
name text not null,
definition text not null
);


        '''
        query = "SELECT name, definition from AssessmentType where ID = %s "
        cursor = self.db.cursor()
        cursor.execute(query, (id))
        (name,definition ) = cursor.fetchone()
        args = {"id":id, "name":name, "definition":definition}
        prog = AssessmentType(self, **args)
        return prog

    def get_or_create_AssessmentType(self, **kwargs):
        '''
        Create a new ActivityILO object, retrieving from the database as necessary,or from the cache
        

        Parameters
        ----------
        **kwargs : either id or name and definition must be present. 

        Returns
        -------
        ActivityILO object

        '''
        mod = None
        if kwargs.get('id',None):
            mod = self.get_AssessmentType_by_id(kwargs['id'])
        else:
            mod = AssessmentType(self, **kwargs)
            mod = self.get_AssessmentType_by_id(mod.id)
            
        return mod
    
    @lru_cache
    def get_Assessment_by_id(self, id):
        '''
        retreives the given id number Assessment from the database and caches the object.        

        Parameters
        ----------
        id : integer
            unique identifier for an Assessment

        Returns
        -------
        Assessment

CREATE or REPLACE TABLE Assessment (
ID integer not null primary key auto_increment,
name text not null,
description text not null,
atype integer not null,
foreign key (type) references AssessmentType (ID)
);


        '''
        query = "SELECT name, description, type from Assessment where ID = %s "
        cursor = self.db.cursor()
        cursor.execute(query, (id))
        (name, description, atype) = cursor.fetchone()
        args = {"id":id, "name":name, "description":description, "type":atype}
        prog = Assessment(self, **args)
        return prog

    def get_or_create_Assessment(self, **kwargs):
        '''
        Create a new Assessment object, retrieving from the database as necessary,or from the cache
        

        Parameters
        ----------
        **kwargs : either id or name and definition must be present. 

        Returns
        -------
        Assessment object

        '''
        mod = None
        if kwargs.get('id',None):
            mod = self.get_Assessment_by_id(kwargs['id'])
        else:
            mod = Assessment(self, **kwargs)
            mod = self.get_Assessment_by_id(mod.id)
            
        return mod

    @lru_cache
    def get_AssessmentInstance_by_id(self, id):
        '''
        retreives the given id number AssessmentInstance from the database and caches the object.        

        Parameters
        ----------
        id : integer
            unique identifier for an AssessmentInstance

        Returns
        -------
        AssessmentInstance
        
CREATE or REPLACE TABLE AssessmentInstance (
ID integer not null primary key auto_increment,
moduleID integer not null,
weightpercent integer not null,
weekstart integer not null,
weekend integer not null,
assessmentID integer not null,
seq integer not null,
foreign key (moduleID) references TModule (ID),
foreign key (assessmentID) references Assessment (ID),
duration text not null
);


        '''
        query = "SELECT moduleID,weightpercent,weekstart,weekend,assessmentID,seq,duration from AssessmentInstance where ID = %s "
        cursor = self.db.cursor()
        cursor.execute(query, (id))
        (moduleID,weightpercent,weekstart,weekend,assessmentID,seq,duration ) = cursor.fetchone()
        args = {"id":id, "moduleID":moduleID,"weightpercent":weightpercent,"weekstart":weekstart,"weekend":weekend,"assessmentID":assessmentID,"seq":seq,"duration":duration }
        prog = AssessmentInstance(self, **args)
        return prog

    def get_or_create_AssessmentInstance(self, **kwargs):
        '''
        Create a new AAssessmentInstance object, retrieving from the database as necessary,or from the cache
        

        Parameters
        ----------
        **kwargs : either id or name and definition must be present. 

        Returns
        -------
        AssessmentInstance object

        '''
        mod = None
        if kwargs.get('id',None):
            mod = self.get_AssessmentInstance_by_id(kwargs['id'])
        else:
            mod = AssessmentInstance(self, **kwargs)
            mod = self.get_AssessmentInstance_by_id(mod.id)
            
        return mod

    def get_all_programmes(self, filterfunc=None):
        '''
        Retreive all programmes

        Parameters
        ----------
        filterfunc : TYPE
            DESCRIPTION.

        Returns
        -------
        list of Programmes

        '''
        sql="SELECT ID from Programme where Future_P is NULL"
        result = {}
        heads = []
        cursor=self.db.cursor()
        cursor.execute(sql,())
        for p in cursor.fetchall():
            result[p[0]] = self.get_programme_by_id(p[0])
            if result[p[0]].future is None:
                heads.append(p[0])
                
        versions = {}
        for p in heads:
            versions[p.id]=[]
            prev = p.previous
            while prev:
                versions[p.id].append(prev)
                prev=result[prev].previous
                
        return {'heads': heads, 'versions': versions, 'programmes': result}
    
    def get_all_modules(self, filterfunc=None):
        '''
        Retreive all modules

        Parameters
        ----------
        filterfunc : TYPE
            DESCRIPTION.

        Returns
        -------
        list of TModules

        '''
        sql="SELECT ID from TModule"
        result = []
        cursor=self.db.cursor()
        cursor.execute(sql,())
        for p in cursor.fetchall():
            result.append(self.get_module_by_id(p[0]))
        return result
    
    def get_all_activities(self, filterfunc=None):
        '''
        Retreive all Activities

        Parameters
        ----------
        filterfunc : TYPE
            DESCRIPTION.

        Returns
        -------
        list of Programmes

        '''
        sql="SELECT ID from TeachingActivity"
        result = []
        cursor=self.db.cursor()
        cursor.execute(sql,())
        for p in cursor.fetchall():
            result.append(self.get_TeachingActivityType_by_id(p[0]))
        return result
    
    def get_all_programmeILOs(self, filterfunc=None):
        '''
        Retreive all programme ILOs

        Parameters
        ----------
        filterfunc : TYPE
            DESCRIPTION.

        Returns
        -------
        list of Programme ILOs

        '''
        sql="SELECT ID from ProgrammeILO"
        result = []
        cursor=self.db.cursor()
        cursor.execute(sql,())
        for p in cursor.fetchall():
            result.append(self.get_ProgrammeILO_by_id(p[0]))
        return result
    
    def get_all_moduleILOs(self, filterfunc=None):
        '''
        Retreive all module ILOs

        Parameters
        ----------
        filterfunc : TYPE
            DESCRIPTION.

        Returns
        -------
        list of ModuleILOs

        '''
        sql="SELECT ID from ModuleILO"
        result = []
        cursor=self.db.cursor()
        cursor.execute(sql,())
        for p in cursor.fetchall():
            result.append(self.get_ModuleILO_by_id(p[0]))
        return result
    
    def get_all_activityILOs(self, filterfunc=None):
        '''
        Retreive all Activity ILOs

        Parameters
        ----------
        filterfunc : TYPE
            DESCRIPTION.

        Returns
        -------
        list of ActivityILOs

        '''
        sql="SELECT ID from ActivityILO"
        result = []
        cursor=self.db.cursor()
        cursor.execute(sql,())
        for p in cursor.fetchall():
            result.append(self.get_programme_by_id(p[0]))
        return result
            
    

class Programme():
    
    DRAFT = 0
    CURRENT = 1
    ARCHIVED = 2
    WITHDRAWN =3
    
    def __init__(self, factory,  **params ):
        '''
        Create a Programme instance.

        Parameters
        ----------
        factory - database connection and cache for Programme
        **params : 
            Create or replace table Programme (
    ID integer primary key not null auto_increment, 
-- Unique identifier
    P_name text not null, 
    P_code text not null,
    P_version text not null,
    Previous_P integer,
    foreign key Previous_P references Programme (ID),
    approvalEvent integer,
    foreign key (approvalEvent) references ApprovalEvents(ID)
);
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        self.factory = factory
        self.status = Programme.DRAFT
        self.id = params.get('id', None)
        self.name = params.get('P_name', 'Unknown programme')
        self.code = params.get('P_code', 'UNK')
        self.version = params.get("P_version", "UNK")
        self.previous =params.get("Previous_P", None)
        self.future = params.get("Future_P", None)
        self.change = params.get("change","")
        self.approval = params.get( "approvalEvent",None)
        self.status = params.get("status", 0)
        
        self.modules = {}
        self.ILO = []
        if self.id:
            self.loadmodules()
            self.loadILO()
        else:
            self.create()
        self.elements={}
        self.loadelements()
    
    def toDict(self):
        return {
            'status': ('DRAFT', 'CURRENT','ARCHIVED','WITHDRAWN')[self.status],
            'id':self.id ,
            'P_name':self.name ,
            'P_code':self.code ,
            'P_version':self.version,
            'Previous_P': self.previous,
            'Future_P': self.future, 
            'change':self.change, 
            'approval':self.approval 
            }
    
    def loadelements(self):
        '''
        Loads elements from the database. Where a directly assigned element is available, it is linked. 
        Where it is not available, the most recent element is added.

        Returns
        -------
        None.

        '''
        self.elements = {}
        sql1 = "SELECT e.ID, e.Ecode, e.Etext, m.ID as mapID from ProgrammeElement e inner join ProgrammeElementMAP m on e.ID = m.ElementID where m.ProgrammeID = %s "
        sql2 = "SELECT max(ID) as latest, Ecode, Etext from ProgrammeElement GROUP BY Ecode"
        cursor = self.factory.db.cursor()
        cursor.execute(sql2)
        for x in cursor.fetchall():
            self.elements[x[1]] = {'id':x[0], 'text':x[2], 'mapID': x[3]}
        cursor.execute(sql1, (self.id))
        for x in cursor.fetchall():
            self.elements[x[1]] = {'id':x[0], 'text':x[2]}
            
    
    def loadmodules(self):
        '''
        Loads module links from the database to the modules list. Does not create now entries in the database.

        Returns
        -------
        None.

        '''
        self.modules=[]
        sql = "SELECT moduleID, optional,TMlevel, code, name, credits, block, m.ID as mapID from ModuleProgrammeMAP m inner join TModule t on m.moduleID = t.ID where programmeID = %s"
        cursor = self.factory.db.cursor()
        cursor.execute(sql, (self.id))
        modules=cursor.fetchall()
        for m in modules:
            self.modules.append(dict(zip(("moduleID", "optional","TMlevel", "code", "name", "credits", "block", "mapID"),m)))
            

        
    def loadILO(self):
        '''
        Loads ILO links from the database. Does not create new links or ILOs.

        Returns
        -------
        None.

        '''
        self.ILO = []
        sql = "SELECT i.ID, i.ILOtext, i.category, m.mapID from ProgrammeILO  i inner join ProgrammeILOMAP m on m.piloID = i.ID where m.programmeID = %s"
        cursor = self.factory.db.cursor()
        cursor.execute(sql, (self.id))
        for ilo in cursor.fetchall():
            self.ILO.append(ilo)
        
        
        
    def create(self, changemessage='first creation'):
        '''
        Creates a new database entry for the Programme entity

        Returns
        -------
        None.

        '''
        insertsql = "Insert into Programme (P_name, P_code, P_version,Previous_P,change ) values (%s,%s,%s,%s,%s)"
        cursor = self.factory.db.excecute(insertsql, (self.name, self.code, self.version,self.previous, changemessage))
        self.id = cursor.lastrowid
        
    def update(self, **kwargs):
        '''
        Update a limited set of fields

        Parameters
        ----------
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        keylist = list (kwargs.keys())
        sql = "UPDATE Programme SET {} WHERE ID = %s"
        
        values= [kwargs[k] for k in keylist]
        values.append(self.id)
        query = ",".join(["{} = %s ".format(k) for k in keylist])
        cursor = self.factory.db.cursor()
        cursor.excecute(sql.format(query), values)
        
    def withdraw(self):
        '''
        Set the Programme to WITHDRAWN. Only possible if there are no future versions.

        Returns
        -------
        None.

        '''
        if not self.future:
            self.status = Programme.WITHDRAWN
            self.update(status='WITHDRAWN')
        
    def archive(self):
        '''
    Set a Programme to archived. Can only be done if there is a future version

        Returns
        -------
        None.

        '''
        if self.future:
            self.status = Programme.ARCHIVED
            self.update(status="ARCHIVED")
 
    def approve(self, approvalevent):
        '''
        Adds an approval event to a Programme

        Parameters
        ----------
        approvalevent : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        if not self.approval:
            self.approval = approvalevent.id
            self.status = Programme.CURRENT
            if self.previous:
                #retrieve previous and set to archived.
                self.factory.get_Programme_by_id(self.previous).archive()
            self.update(approvalEvent=self.approval,status=self.status)
            
    def add_element(self, element):
        '''
        Add an element to the Programme, updating if exisitng category already appended.

        Parameters
        ----------
        element : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        sqli = "INSERT INTO ProgrammeElementMAP (ProgrammeID,ElementID) VALUES(%s,%s)"
        sqlu = "UPDATE ProgrammeElementMAP SET ElementID = %s where ID=%s"
        cursor = self.factory.db.cursor()
        if element.ecode in self.elements:
            if self.elements[element.ecode]['id'] != element.id:
                if 'mapID' in self.elements[element.ecode]:
                    cursor.execute(sqlu,(element.id, self.elements[element.ecode]['mapID'] ))
                else : #replace generic with specific element
                    cursor.execute(sqli, (self.id, element.id))
                    
        else:
            cursor.execute(sqli, (self.id, element.id))
        self.loadelements()

    def map_module(self, module, optional=0, remove=False):
           '''
           Add a module to the Programme, updating if exisitng  already appended.

           Parameters
           ----------
           element : TYPE
               DESCRIPTION.

           Returns
           -------
           None.

           '''
           sqli = "INSERT INTO ModuleProgrammeMAP (moduleID,programmeID, optional) VALUES (%s, %s, %s)"
           sqlu = "UPDATE ModuleProgrammeMAP SET optional = %s WHERE ID = %s"
           sqld = "DELETE FROM ModuleProgrammeMAP where ID = %s"
           modlist = [m for m in self.modules if m['moduleID']==module.id]
           if modlist:
               thismod = modlist[0]
               if remove:
                   cursor = self.factory.db.cursor()
                   cursor.execute(sqld, ( thismod['mapID']))
                   
               elif optional != thismod['optional']:
                   cursor = self.factory.db.cursor()
                   cursor.execute(sqlu, (('optional','core')[optional], thismod['mapID']))
                   thismod['optional']=optional
                   
           else:
               cursor = self.factory.db.cursor()
               cursor.execute(sqli, (module.id,self.id,optional))
               self.loadmodules()    
           
           
    def map_ilo(self, ilo, remove=False):
        '''
        Adds ILO to the Programme, if it is not already assosciated

        Parameters
        ----------
        ilo : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        sqli = "INSERT INTO ProgrammeILOMAP (programmeID, piloID) VALUES (%s , %s)"
        sqld = "DELETE FROM ProgrammeILOMAP where programmeID = %s and piloID = %s"
        ilos= [x for x in self.ILO if x[0]==ilo.id]
        cursor = self.factory.db.cursor()
        if ilos and remove:
            cursor.execute(sqld, (self.id, ilo.id))
        elif ilos or remove:
            pass
        else:
            cursor.execute(sqli,(self.id, ilo.id))
        self.loadILO()
        
        
    
class Module():
    
    DRAFT = 0
    CURRENT = 1
    ARCHIVED = 2
    WITHDRAWN = 3
    PREREQUISITE = 1
    COREQUISITE = 0
    ANTIREQUISITE = 2
    
    def __init__(self, factory, **params):
        self.factory = factory
        self.id = params.get('ID',None)
        self.code = params.get('code', 'UNK')
        self.name = params.get('name', 'UNK')
        self.level = params.get('TMlevel',0)
        self.altlevel =params.get('altlevel')
        self.version = params.get('version','UNK')
        self.previous = params.get('previous_M', None)
        self.future = params.get('future_M',None)
        self.credits = params.get('credits', 20)
        self.block = params.get('block', None)
        self.approval = params.get('approvalEvent', None)
        self.status = params.get('status', 0)
        if self.id is None:
            self.create()
        self.ILO =[]
        self.loadILOs()
        self.elements={}
        self.loadElements()
        self.requisites = {}
        self.loadConstraints()
        self.activities=[]
        self.loadActivities()
     
    def loadILO(self):
        '''
        Loads ILO links from the database. Does not create new links or ILOs.

        Returns
        -------
        None.

        '''
        self.ILO=[]
        sql = "SELECT i.ID, i.ILOtext, i.category from ModuleILO  i inner join ModuleILOMAP m on m.miloID = i.ID where m.moduleID = %s"
        cursor = self.factory.db.cursor()
        cursor.execute(sql, (self.id))
        for ilo in cursor.fetchall():
            self.ILO.append(ilo)
        
    def loadelements(self):
        '''
        Loads elements from the database. Where a directly assigned element is available, it is linked. 
        Where it is not available, the most recent element is added.

        Returns
        -------
        None.

        '''
        sql1 = "SELECT e.ID, e.Ecode, e.Etext, m.ID as mapID from ModuleElement e inner join ModuleElementMAP m on e.ID = m.ElementID where m.ModuleID = %s "
        sql2 = "SELECT max(ID) as latest, Ecode, Etext from ModuleElement GROUP BY Ecode"
        cursor = self.factory.db.cursor()
        cursor.execute(sql2)
        for x in cursor.fetchall():
            self.elements[x[1]] = {'id':x[0], 'text':x[2]}
        cursor.execute(sql1, (self.id))
        for x in cursor.fetchall():
            self.elements[x[1]] = {'id':x[0], 'text':x[2], 'mapID':x[3]}

    def loadConstraints(self):
        '''
        Loads in but does not create constraint

        Returns
        -------
        None.

        ''' 
        self.requisites = {}
        constrainttypes = ('co-requisite', 'pre-requisite', 'anti-requisite')
        sql = "Select m.ID,m.code,m.name , c.constraintType, c.ID as conID from ModuleConstraint c inner join TModule m on m.ID = c.constraintModuleID  where c.moduleID = %s"
        cursor = self.factory.db.cursor()
        cursor.execute(sql, (self.id))
        for con in cursor.fetchall():
            (id, code, name, type)=con
            if constrainttypes[con[3]] not in self.requisites:
                self.requisites[ constrainttypes[con[3]]] =[]
            self.requisites[ constrainttypes[con[3]]].append(con)
            
    def setConstraints(self, constraint, module,  remove=False):
        '''
        Constraint is an integer corresponding to the constraint type. 
        module is teh module acting as a constraint.
        remove is boolean actig as to whether a constraint is added/updated (false) or removed (true)

        Parameters
        ----------
        constraintlist : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        constrainttypes = ('co-requisite', 'pre-requisite', 'anti-requisite')
        sqli = "Insert into ModuleConstraint (moduleID, constraintModuleID, constraintType) VALUES (%s, %s, %s)"
        sqld = "Delete from ModuleConstraint WHERE moduleID = %s and constraintModuleID = %s"
        cursor =  self.factory.db.cursor()
        cursor.execute(sqld,(self.id, module.id))
        if not remove:
            cursor.execute(sqli, (self.id, module.id, constrainttypes[constraint]))
        self.loadConstraints()
            
        
        
    def loadActivities(self):
        '''
        Loads but does not create activities associated with the module.

        Returns
        -------
        None.

        '''
        self.activities = []
        sql = "Select ActivityID from ActivityModuleMAP where ModuleID = %s"
        cursor = self.factory.db.cursor()
        cursor.execute(sql, (self.id))
        for con in cursor.fetchall():
            self.activities.append(con)
            
    def get_activities (self):
        '''
        Returns a list of TeachingActivity objects which are delivered in this TModule 

        Returns
        -------
        List of TeachingActivity

        '''
        actlist = []
        for x in self.activities:
            actlist.append(self.factory.get_TeachingActivity_by_id(x))
        return actlist
    
        
        
        
    def create(self, changemessage='first creation'):
        '''
        Creates a new database entry for the Programme entity

        Returns
        -------
        None.

        '''
        insertsql = "Insert into TModule (name, code, TMlevel, altlevel, version, previous_M, future_M, credits, block, change ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor = self.factory.db.excecute(insertsql, (self.name, self.code, self.level, self.altlevel, self.version,self.previous, self.credits, self.block, changemessage))
        self.id = cursor.lastrowid
        
    def update(self, **kwargs):
        '''
        Update a limited set of fields

        Parameters
        ----------
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        keylist = list (kwargs.keys())
        sql = "UPDATE TModule SET {} WHERE ID = %s"
        
        values= [kwargs[k] for k in keylist]
        values.append(self.id)
        query = ",".join(["{} = %s ".format(k) for k in keylist])
        cursor = self.factory.db.cursor()
        cursor.excecute(sql.format(query), values)
        
    def withdraw(self):
        '''
        Set the Modulee to WITHDRAWN. Only possible if there are no future versions.
        
        Returns
        -------
        None.
        
        '''
        if not self.future:
            self.status = Module.WITHDRAWN
            self.update(status='WITHDRAWN')

    def archive(self):
        '''
    Set a Module to archived. Can only be done if there is a future version

        Returns
        -------
        None.

        '''
        if self.future:
            self.status = Module.ARCHIVED
            self.update(status="ARCHIVED")
 
    def approve(self, approvalevent):
        '''
        Adds an approval event to a Module

        Parameters
        ----------
        approvalevent : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        if not self.approval:
            self.approval = approvalevent.id
            self.status = Module.CURRENT
            if self.previous:
                #retrieve previous and set to archived.
                self.factory.get_Module_by_id(self.previous).archive()
            self.update(approvalEvent=self.approval,status=self.status)

    def map_ilo(self, ilo, remove=False):
        '''
        Adds ILO to the Programme, if it is not already assosciated

        Parameters
        ----------
        ilo : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        sqli = "INSERT INTO ModuleILOMAP (moduleID, miloID) VALUES (%s , %s)"
        sqld = "DELETE FROM ModuleILOMAP where moduleID = %s and miloID = %s"
        ilos= [x for x in self.ILO if x[0]==ilo.id]
        cursor = self.factory.db.cursor()
        if ilos and remove:
            cursor.execute(sqld, (self.id, ilo.id))
        elif ilos or remove:
            pass
        else:
            cursor.execute(sqli,(self.id, ilo.id))
        self.loadILO()


        
class TeachingActivityType():
    
    def __init__(self, factory, **kwargs):
        self.factory=factory
        self.name = kwargs.get("name")
        self.definition = kwargs.get("definition")
        self.id = kwargs.get("id")
        if self.id is None:
            self.create()
            
        
    def create(self):
        '''
        Creates a new database entry for the TeachingActivityType entity

        Returns
        -------
        None.

        '''
        insertsql = "Insert into TeachingActivityType (name, definition) VALUES (%s,%s)"
        cursor = self.factory.db.cursor()
        cursor.excecute(insertsql, (self.name, self.definition))
        self.id = cursor.lastrowid
    
class TeachingActivity ():

    def __init__(self, factory, **kwargs):
        #description, duration, TAtype, version,previous_TA, moduleID, sequence
        self.factory = factory
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.duration = kwargs.get("duration")
        self.type=kwargs.get("TAtype")
        self.version= kwargs.get("version")
        self.previous=kwargs.get("previous_TA")
        self.modules=[]
        self.sequence=kwargs.get("sequence")
        self.weighting = kwargs.get("weighting")
        if kwargs.get("id") is None:
            self.create()
        self.loadILO()
        self.load_modules()
        
    def create(self):
        cursor = self.factory.db.cursor()
        sql = "Insert into TeachingActivity (description, duration, TAtype, version,previous_TA,  sequence, weighting) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (self.name,self.description, self.duration, self.type, self.version, self.previous,  self.sequence, self.weighting))
        self.id = cursor.lastrowid
        
    def update(self, **kwargs):
        '''
        Update a limited set of fields

        Parameters
        ----------
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        keylist = list (kwargs.keys())
        sql = "UPDATE TeachingActivity SET {} WHERE ID = %s"
        
        values= [kwargs[k] for k in keylist]
        values.append(self.id)
        query = ",".join(["{} = %s ".format(k) for k in keylist])
        cursor = self.factory.db.cursor()
        cursor.excecute(sql.format(query), values)
        
    def loadILO(self):
        '''
        Loads ILO links from the database. Does not create new links or ILOs.

        Returns
        -------
        None.

        '''
        self.ILO=[]
        sql = "SELECT i.ID, i.ILOtext, i.category from ActivityILO  i inner join ActivityILOMAP m on m.ailoID = i.ID where m.activityID = %s"
        cursor = self.factory.db.cursor()
        cursor.execute(sql, (self.id))
        for ilo in cursor.fetchall():
            self.ILO.append(ilo)
            
    def map_ilo(self,  ilo, remove=False):
        '''
        Adds ILO to the Activity, if it is not already assosciated

        Parameters
        ----------
        ilo : ActivityILO
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        sqli = "INSERT INTO ActivityILOMAP (activityID, ailoID) VALUES (%s , %s)"
        sqld = "DELETE FROM ActivityILOMAP where activityID = %s and ailoID = %s"
        ilos= [x for x in self.ILO if x[0]==ilo.id]
        cursor = self.factory.db.cursor()
        if ilos and remove:
            cursor.execute(sqld, (self.id, ilo.id))
        elif ilos or remove:
            pass
        else:
            cursor.execute(sqli,(self.id, ilo.id))
        self.loadILO()
        
    def load_modules (self):
        '''
        Append assigned modules to the teaching activity.

        Returns
        -------
        None.

        '''
        sql = " SELECT ModuleID from ActivityModuleMAP where Activity ID = %s"
        self.modules = []
        cursor = self.factory.db.cursor()
        cursor.execute(sql, (self.id))
        for mod in cursor.fetchall():
            self.modules.append(mod)
    def assign_to_module(self, module):
        '''
        Add an activity to a module

        Parameters
        ----------
        module : A TModule object to attach the activity to.
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        self.load_modules()
        if module.id in self.modules:
            return
        sql = "Insert into ActivityModuleMAP (ModuleID, ActivityID) VALUES (%s,%s);"
        cursor = self.factory.db.cursor()
        cursor.execute(sql,(module.id, self.id))
        self.modules.append(module.id)
    
    def get_modules(self):
        '''
        Returns a list of TModule objects with which the activity is associated.

        Returns
        -------
        list of TModule

        '''
        modules = []
        for x in self.modules:
            modules.append(self.factory.get_module_by_id(x))
        
        return modules


class ActivityILO():
    '''
    CREATE or REPLACE Table ActivityILO (
    ID integer not null auto_increment primary key,
    ILOtext text not null,
    category ENUM('Knowledge','Understanding', 'Skill', 'Attitude') not null,
    moduleILO integer,
    bloom ENUM('None','Remember',	'Understand',	'Apply',	'Analyze',	'Evaluate',	'Create') Not null,
    Foreign Key (moduleILO) REFERENCES ModuleILO (ID)
    );
    '''
    bloomterms = ('None','Remember',	'Understand',	'Apply',	'Analyze',	'Evaluate',	'Create')
    bloommap ={
        }
    categories = ('Knowledge','Understanding', 'Skill', 'Attitude')
    def __init__(self, factory, **kwargs):
        self.factory = factory
        self.ILOtext = kwargs.get("ILOtext")
        self.category = kwargs.get("category")
        self.bloom = kwargs.get('bloom')
        self.moduleILO = kwargs.get('moduleILO')
        self.id = kwargs.get("id")
        if self.id is None:
            self.create()
            
        
    def create(self):
        '''
        Creates a new database entry for the TeachingActivityType entity

        Returns
        -------
        None.

        '''
        insertsql = "Insert into ActivityILO (ILOtext,category,bloom,moduleILO) VALUES (%s,%s,%s,%s)"
        cursor = self.factory.db.cursor()
        cursor.excecute(insertsql, (self.ILOtext,self.category,self.bloom,self.moduleILO))
        self.id = cursor.lastrowid   
    
    def getActivitiesForILO(self):
        '''
        Retrieve all Activities with this ILO

        Returns
        -------
        List of TeachingActivity

        '''
        cursor = self.factory.db.cursor()
        sql = "Select ActivityID from ActivityILOMAP where ailoID = %s"
        cursor.execute(sql, (self.id))
        activities=[]
        for a in cursor.fetchall():
            activities.append(self.factory.get_TeachingActivity_by_id(a[0]))
        return activities
    
class ModuleILO():
    '''
    CREATE or REPLACE Table ModuleILO (
    ID integer not null auto_increment primary key,
    ILOtext text not null,
    category ENUM('Knowledge','Understanding', 'Skill', 'Attitude') not null,
    programmeILO integer not null,
    foreign key (programmeILO) references ProgrammeILO (ID)
    );
    '''
    categories = ('Knowledge','Understanding', 'Skill', 'Attitude')
    def __init__(self, factory, **kwargs):
        self.factory = factory
        self.ILOtext = kwargs.get("ILOtext")
        self.category = kwargs.get("category")
        self.programmeILO = kwargs.get('programmeILO')
        self.id = kwargs.get("id")
        if self.id is None:
            self.create()
            
        
    def create(self):
        '''
        Creates a new database entry for the TeachingActivityType entity

        Returns
        -------
        None.

        '''
        insertsql = "Insert into ModuleILO (ILOtext,category,programmeILO) VALUES (%s,%s,%s)"
        cursor = self.factory.db.cursor()
        cursor.excecute(insertsql, (self.ILOtext,self.category,self.programmeILO))
        self.id = cursor.lastrowid   
    
    def getModulesForILO(self):
        '''
        Retrieve all Modules with this ILO

        Returns
        -------
        List of TModule

        '''
        cursor = self.factory.db.cursor()
        sql = "Select ModuleID from ModuleILOMAP where miloID = %s"
        cursor.execute(sql, (self.id))
        activities=[]
        for a in cursor.fetchall():
            activities.append(self.factory.get_TModule_by_id(a[0]))
        return activities
        
class ProgrammeILO():
    '''
    CREATE or REPLACE Table ProgrammeILO (
    ID integer not null auto_increment primary key,
    ILOtext text not null,
    category ENUM('Knowledge','Understanding', 'Skill', 'Attitude') not null
    );

    '''
    
    categories = ('Knowledge','Understanding', 'Skill', 'Attitude')
    def __init__(self, factory, **kwargs):
        self.factory = factory
        self.ILOtext = kwargs.get("ILOtext")
        self.category = kwargs.get("category")
        self.id = kwargs.get("id")
        if self.id is None:
            self.create()
            
        
    def create(self):
        '''
        Creates a new database entry for the TeachingActivityType entity

        Returns
        -------
        None.

        '''
        insertsql = "Insert into ProgrammeILO (ILOtext,category) VALUES (%s,%s)"
        cursor = self.factory.db.cursor()
        cursor.excecute(insertsql, (self.ILOtext,self.category))
        self.id = cursor.lastrowid   
    
    def getProgrammesForILO(self):
        '''
        Retrieve all Activities with this ILO

        Returns
        -------
        List of TeachingActivity

        '''
        cursor = self.factory.db.cursor()
        sql = "Select ProgrammeID from ProgrammeILOMAP where piloID = %s"
        cursor.execute(sql, (self.id))
        activities=[]
        for a in cursor.fetchall():
            activities.append(self.factory.get_Programme_by_id(a[0]))
        return activities
    
class AssessmentType():
    '''
    CREATE or REPLACE TABLE AssessmentType (
    ID integer not null primary key auto_increment,
    name text not null,
    definition text not null
    );
    '''

    def __init__(self, factory, **kwargs):
        self.factory = factory
        self.name = kwargs.get("name")
        self.definition = kwargs.get("definition")
        self.id = kwargs.get("id")
        if self.id is None:
            self.create()
            
        
    def create(self):
        '''
        Creates a new database entry for the AssessmentType entity

        Returns
        -------
        None.

        '''
        insertsql = "Insert into AssessmentType (name, definition) VALUES (%s,%s)"
        cursor = self.factory.db.cursor()
        cursor.excecute(insertsql, (self.name,self.definition))
        self.id = cursor.lastrowid   

class Assessment():
    
    '''
    CREATE or REPLACE TABLE Assessment (
    ID integer not null primary key auto_increment,
    name text not null,
    description text not null,
    atype integer not null,
    foreign key (atype) references AssessmentType (ID)
    );
    '''

    def __init__(self, factory, **kwargs):
        self.factory = factory
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.atype = kwargs.get('atype')
        self.id = kwargs.get("id")
        if self.id is None:
            self.create()
        self.ILO =[]
        self.loadILO()
        
    def create(self):
        '''
        Creates a new database entry for the Assessment entity

        Returns
        -------
        None.

        '''
        insertsql = "Insert into Assessment (name, description, atype) VALUES (%s,%s,%s)"
        cursor = self.factory.db.cursor()
        cursor.excecute(insertsql, (self.name,self.description, self.atype))
        self.id = cursor.lastrowid   

    def loadILO(self):
        '''
        Loads ILO links from the database. Does not create new links or ILOs.

        Returns
        -------
        None.

        '''
        self.ILO=[]
        sql = "SELECT i.ID, i.ILOtext, i.category from ActivityILO  i inner join AssessmentActivityILOMAP m on m.activityiloID = i.ID where m.assessmentID = %s"
        cursor = self.factory.db.cursor()
        cursor.execute(sql, (self.id))
        for ilo in cursor.fetchall():
            self.ILO.append(ilo)
            
    def map_ilo(self,  ilo, remove=False):
        '''
        Adds ILO to the Activity, if it is not already assosciated

        Parameters
        ----------
        ilo : ActivityILO
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        sqli = "INSERT INTO AssessmentActivityILOMAP (assessmentID, activityiloID) VALUES (%s , %s)"
        sqld = "DELETE FROM ActivityILOMAP where assessmentID = %s and activityID = %s"
        ilos= [x for x in self.ILO if x[0]==ilo.id]
        cursor = self.factory.db.cursor()
        if ilos and remove:
            cursor.execute(sqld, (self.id, ilo.id))
        elif ilos or remove:
            pass
        else:
            cursor.execute(sqli,(self.id, ilo.id))
        self.loadILO()
    
class AssessmentInstance():
    '''
    CREATE or REPLACE TABLE AssessmentInstance (
    ID integer not null primary key auto_increment,
    moduleID integer not null,
    weightpercent integer not null,
    weekstart integer not null,
    weekend integer not null,
    assessmentID integer not null,
    seq integer not null,
    foreign key (moduleID) references TModule (ID),
    foreign key (assessmentID) references Assessment (ID),
    duration text not null
    );
    '''
    
    def __init__(self, factory, **kwargs):
        self.factory = factory
        self.moduleIO = kwargs.get("moduleID")
        self.weightpercent = kwargs.get("weightpercent")
        self.weekstart = kwargs.get("weekstart")
        self.weekend = kwargs.get("weekend")
        self.assessmentID = kwargs.get("assessmentID")
        self.seq = kwargs.get("seq")
        self.duration = kwargs.get("duration")
        self.id = kwargs.get("id")
        if self.id is None:
            self.create()
            
        
    def create(self):
        '''
        Creates a new database entry for the TeachingActivityType entity

        Returns
        -------
        None.

        '''
        insertsql = "Insert into AssessmentInstance (moduleID,weightpercent,weekstart,weekend,assessmentID,seq,duration) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor = self.factory.db.cursor()
        cursor.excecute(insertsql, (self.moduleID,self.weightpercent,self.weekstart,self.weekend,self.assessmentID,self.seq,self.duration))
        self.id = cursor.lastrowid   
