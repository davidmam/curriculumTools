# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 20:34:24 2022

@author: DMAMartin
"""

from functools import lru_cache
import re
import neo4j
# Neo4J database wrappers.



class InsufficientParameterSpecException(Exception):
    pass
class BadParameterException(Exception):
    pass

class NotFoundException(Exception):
    pass
class UnparseableYearException(Exception):
    pass

class AcademicYear():
    '''Class to represent an academic year'''
    
    def __init__(self, year):
        '''
        Class representing an academic year to allow standardised comparison and representation

        Parameters
        ----------
        year : Text description of the academic year or Academic year object
            Can be 2425 24/25 2024/5

        Returns
        -------
        Academic Year object

        '''
        patterns = [r'^(\d{2})$',
                    r'^(\d{2})(\d{2})$',
                    r'^(\d{2})/\d{2}$',
                    r'^\d{2}(\d{2})/\d{1,2}$']
        
        if hasattr(year,'yearvalue'):
            self.yearvalue=year.yearvalue
        else:
            yearval=''
            for pat in patterns:
                match= re.match(pat,year)
                if match:
                    if len(match.groups())>1:
                        if int(match.group(1))==int(match.group(2))-1:
                            yearval = int(match.group(1))
                            break
                    yearval=int(match.group(1))
                    break
            if yearval:
                self.yearvalue=yearval
            else:
                raise UnparseableYearException(f'Cannot understand Academic Year {year}')
        
    def __eq__(self, o):
        return self.yearvalue == o.yearvalue
    def __gt__(self,o):
        print(self.yearvalue, o.yearvalue)
        return self.yearvalue > o.yearvalue
    def __lt__(self,o):
        return self.yearvalue < o.yearvalue
    def __ge__(self,o):
        return self.yearvalue >= o.yearvalue
    def __le__(self,o):
        return self.yearvalue <= o.yearvalue
                        
    def __str__(self):
        return f'Academic Year 20{self.yearvalue}/{self.yearvalue+1}'
    def __repr__(self):
        return str(self)
        
class Node():
    '''Represents a Node in a Neo4j database. 
    Contains methods for accessing links, ensuring that on creation the 
    correct parameters are given etc.'''

    ntype='Node'
    
    requiredParams = {
        }
    optionalParams= {}
    
    def __init__(self, factory=None,  **kwparams):
        '''Initialiser. Checks required parameters are present'''
        if factory is None:
            raise Exception('Curriculum factory must be given as factory')
        self.factory = factory
        self.ntype=self.__class__.__name__.split('.')[-1]
        self.paramChecks={'default': self._checkDefault}
        self.params={}
        self.edges=[]
        self._get_labels()
        for par in self.requiredParams:
            if not kwparams.get(par):
                print(par, kwparams)
                raise InsufficientParameterSpecException(f'Missing parameter <{par}> of type <{self.requiredParams[par]}>')
            if not self.paramChecks.get(par,self._checkDefault)(kwparams[par]):
                raise BadParameterException(f'Parameter <{par}> should be of type <{self.requiredParams[par]}>')
            self.params[par]=kwparams[par]
        for par in self.optionalParams:
            if par not in kwparams:
                continue
            if not self.paramChecks.get(par,self._checkDefault)(kwparams[par]):
                raise BadParameterException(f'Parameter <{par}> should be of type <{self.requiredParams[par]}>')
            self.params[par]=kwparams[par]
        if 'elementID' not in kwparams:
            self._create_node()
        else:
            self.element_id=kwparams['elementID']
            self.edges =self.getEdges()
    def __str__(self):
        '''Returns a string represntation of the node'''
        params = ", ".join([f'{k}: {self.params[k]}' for k in self.requiredParams])
        return f'{self.ntype}: [{params}] ID: {self.element_id}'
    
    def __repr__(self):
        return self.__str__()
                            
    def _create_node(self):
        '''Internal method that creates a new instance of the node, if it does not exist'''
        paramlist = ", ".join([f'{k}: ${k}' for k in self.params])
        paramlist = "{"+paramlist+"}"
        nodelabels = ':'.join(self.labels)
        query= f"MERGE (a:{nodelabels} {paramlist}) RETURN a"
        records,summary, keys = self.factory.db.execute_query(query, self.params, database_=self.factory.dbname)   
        self.element_id = records[0].items()[0][1].element_id
            
    def _checkDefault(self, value):
        '''default placeholder for parameter value checks. Returns True'''
        return True
    
    def _checkAY(self, value):
        '''Checks for a correctly formatted Academic year as:
            2425
            24/25
            2024/5'''
        #TODO 
        return True
    def getparam(self, prop, default=None):
        '''
        Returns a parameter value (default if not found)

        Parameters
        ----------
        prop : property name
            
        default : TYPE, optional
             The default is None.

        Returns
        -------
        Property value
            
        '''
        return self.params.get(prop,default)
    
    def setparam(self, key, value):
        '''
        Sets the parameter key to value. No type checking.

        Parameters
        ----------
        key : legal value for a dictionary key
            
        value : Value to store.
        
        Returns
        -------
        None.

        '''
        self.params[key]=value
        self.update()
    
    def getEdges(self,relation=None,**kwargs):
        '''retrieves edges connected to or from the Node.
        Relation is the type of relation to retrieve (default is all)
        other arguments are applied as matching parameters'''
        edges=[]
        filterstring=''
        filterparams={}
        for kw in kwargs:
            if kw != 'id':
                filterstring += f"'{kw}': ${kw},"
                filterparams[kw] = kwargs[kw]
        rel=''
        if relation:
            rel=f":{relation}"
        filterparams['id'] = self.element_id
        if filterstring:
            filterstring = "{"+filterstring+"}"
        records, summary, keys = self.factory.db.execute_query(
        f"MATCH (p: {self.ntype} {{id: $id }}) -[e{rel} {filterstring}]-(q) RETURN e,q",
        filterparams,
        routing_=neo4j.RoutingControl.READ,  # or just "r"
        database_=self.factory.dbname)
        for edge in records:
            relation = edge.items[0][1]
            target = edge.items[1][1]
            edges.append({'source': self,'edge': relation, 'target': target})
        return edges
    def isCurrent(self, year):
        '''
        If the edge has a start/end year, check if the given year is the period in which the relation is valid

        Returns
        -------
        Boolean: True if the eyar is between start and end (inclusive), after start if no end, or True if no start

        '''
        
        if self.params.get('startyear'):
            if AcademicYear(year)< AcademicYear(self.params.get('startyear')):
                return False
            if self.params.get('endyear'):
                if AcademicYear(year)> AcademicYear(self.params.get('endyear')):
                    return False
        return True
    
    
    def toDict(self):
        retp ={'element_id': self.element_id}
        for p in self.params:
            retp[p]=self.params[p]
        return retp
    
    def update(self, **kwargs):
        '''
        Update named parameters for a Node

        Parameters
        ----------
        **kwargs : key,value parameter set
            any key,value parameters. Existing values will be overwritten.
            No type checking

        Returns
        -------
        None.

        '''
        paramlist =[]
        if not kwargs:
            return
        for k in kwargs:
            if k !='id':
                paramlist.append( f'a.{k}= ${k}')
                self.params[k]=kwargs[k]
        kwargs['id'] = self.element_id    
        paramlist = "{"+paramlist+"}"
        query= f"MERGE (a:{self.ntype}) WHERE elementID(a) = $id SET {', '.join(paramlist)}"
        records,summary, keys = self.factory.db.execute_query(query,kwargs, database_=self.factory.dbname)   
        
    def _get_labels(self):
        self.labels = [x.__name__ for x in globals()[self.__class__.__name__].__mro__]
        self.labels.remove('object')
        self.labels.remove('Node')
        
    
    
class Edge():
    '''Represents an edge in a Neo4J database'''
    requiredParameters={
        'relation': 'relationship type',
        'source': 'Node ',
        'target': 'Node '}
    optionalParams={
        'startyear': 'Academic year start',
        'endyear': 'Academic year to'
        }
    def __init__(self, factory, **kwargs):
        '''Edge between two nodes. Must specify source, target and relationship type.'''
        for kw in self.requiredParameters:
            if kw not in kwargs:
                raise InsufficientParameterSpecException(f"{kw} not specified in Edge constructor")
            self.params[kw]=kwargs[kw]
    def set_expiry(self, expirydate):
        '''
        Sets the 'to' parameter with an academic year for when this relation was withdrawn. 
        The date specified will be the last academic year for which it was valid.

        Parameters
        ----------
        expirydate : Academic year
            Academic year is an academic year object or text description of it.

        Returns
        -------
        None.

        '''
        self.params['to'] =AcademicYear(expirydate)
    
    def isCurrent(self, year):
        '''
        If the edge has a start/end year, check if the given year is the period in which the relation is valid

        Returns
        -------
        Boolean: True if the eyar is between start and end (inclusive), after start if no end, or True if no start

        '''
        
        if self.params.get('startyear'):
            if AcademicYear(year)< AcademicYear(self.params.get('startyear')):
                return False
            if self.params.get('endyear'):
                if AcademicYear(year)> AcademicYear(self.params.get('endyear')):
                    return False
        return True
    def getSource(self):
        '''
        Returns a Python object representing the source node

        Returns
        -------
        None.

        '''
        
class CurriculumFactory():
    
    def __init__(self, db, dbname='curriculum'):
        self.db = db
        self.dbname = dbname
        self.programmecache = {}
        self.modulecache = {}
        self.activitycache = {}
        self.personcache = {}
        
    def get_connection(self):
        return self.db
    
    @lru_cache    
    def get_element_by_ID(self, elementID):
        '''
        Retrieves an element by ID and creates the appropriate node for it, if it is a node.
        
        Parameters
        ----------
        elementID : Internal neo4j element ID
            text string uniquely identifying the object in the database.

        Returns
        -------
        Object of correct class, if available or None if not found.

        '''
        erecords, _, _ = self.db.execute_query(
            "MATCH (a ) where elementId(a)=$id"
            "RETURN a", id=elementID,
             database_=self.dbname,
        )
        if not erecords :
            return
        nodeclass = list(erecords[0].items()[0][1].labels())[0]
        params = dict(erecords[0].items()[0][1])
        params['elementID']=elementID
        if nodeclass in globals():
            return globals()[nodeclass](**params)
        
      
    def get_or_create_Element(self, ElementName,**kwargs):
        '''
        Generic get and create method. This requires all elements to have a unique id under the property code

        Parameters
        ----------
        ElementName : Name of element to create, eg Programme
            This will directly map to the class name.
        **kwargs : Parameters to use. These will be checked against every class.
            

        Returns
        -------
        Element of type ElementName on success

        '''
        
        elem= None
        
        if ElementName not in globals():
            return
        ElementClass=globals()[ElementName]
        if kwargs.get('elementID',None):
            elem = self.get_element_by_id(kwargs['elementID'])
            return elem
        if kwargs.get('code'):
            try:
                result,_,_=self.db.execute_query(f'MATCH (p:{ElementName} {{code: $name}} ) return p', name=kwargs['code'], database_=self.dbname)
                if result:
                    params=dict(result[0].items()[0][1])
                    params['elementID']=result[0]['p'].element_id
                    elem = ElementClass(self, **params)
                    return elem
            except Exception as e:
                e.add_note(str(params))
                raise e
                
        for p in ElementClass.requiredParams:
            if p not in kwargs:
                raise InsufficientParameterSpecException(f'Not enough parameters specified for {ElementName}: missing{p}')
        
        elem = ElementClass(self, **kwargs)
        return elem


    def get_all_elements(self, ElementName, **params):
        '''
        Returns all elements of type ElementName

        Parameters
        ----------
        ElementName : name of an element
            This can be any element type for which a model exists.
        **params : Keyword parameters to use in the search
            Exact matches only at present.

        Returns
        -------
        List of elements

        '''
        
        elements = []
        if ElementName not in globals():
            return elements
        paramdetails =[]
        paramtext=''
        for p in params:
            paramdetails.append(f'{p}: ${p}')
        if paramdetails:
            paramtext= f'{ {",".join(paramdetails)} }'
        erecords, _, _ = self.db.execute_query(
            f"MATCH (a :{ElementName} {paramtext}) RETURN a",
            params,
             database_=self.dbname,
        )
        try:
            if not erecords :
                return elements
            for item in erecords:
                elem=item.items()[0][1]
                nodeclass = list(elem.labels)[0]
                params = dict(elem)
                params['elementID']=elem.element_id
                if nodeclass in globals():
                    elements.append( globals()[nodeclass](self, **params))
            return elements  
        except Exception as e:
            print(e)
            return erecords
    def getElementsForElement(self, element, target, max_steps=2,relation=None):
        '''
        Retreive all elements of type Target linked to element,optionally by relation (or all relations) 
        at a maximum distance of max_steps (default 2)
        
        Parameters
        ----------
        element : TYPE
            DESCRIPTION.
        target : TYPE
            DESCRIPTION.
        max_steps: integer
            Maximum link number to explore (default 2)
        relation: text
            Limit relations to those of type relation
        Returns
        -------
        List of Node type objects.
        '''
        if target not in globals():
            return []
        cypher = f"MATCH (e) --{{1,{max_steps}}} (thing:$target) where elementID(e)=$id RETURN DISTINCT thing"
        result,_,_=self.db.execute_query(cypher, target=target, id=element.element_id,database_=self.dbname)
        elems = []
        if result:
            for elem in result:
                item = elem.items()[0][1]
                params =dict(item)
                params['elementID'] = item.element_id
                elems.append(globals()[target](self, **params))
        return elems
         
class Programme(Node):
    
    DRAFT = 0
    CURRENT = 1
    ARCHIVED = 2
    WITHDRAWN =3
    ntype='Programme'
    requiredParams = {
        'code': 'Programme code',
        'name': 'Programme name'
        }
    optionalParams= {
        'startyear':'First academic year',
        'endyear': 'Last academic year',
        'school':'School which manages the Programme'}
    def __init__(self, factory, **params ):
        '''
        Create a Programme instance.

        Parameters
        ----------
        factory - database connection and cache for Programme
        **params : 
            Create or replace table Programme (
        '''
        super().__init__(factory,**params)
        
        self.modules = {}
        self.ILO = []
        if self.element_id:
            self.loadmodules()
            self.loadILO()
        

    
    
    
    def loadmodules(self):
        '''
        Loads module links from the database to the modules list. Does not create now entries in the database.

        Returns
        -------
        None.

        '''
        self.modules={}
        cypher = "MATCH (p:Programme ) -[a]-(b:Module) WHERE elementID(p) = $id RETURN a,b"
        records,_,_ =self.factory.db.execute_query(cypher, id=self.element_id, database_=self.factory.dbname)
        for t in records:
            relation = t.items()[0][1]
            target = dict(t.items()[1][1])
            target['element_id'] = t.items()[1][1].element_id
            if target['code'] not in self.modules:
                self.modules[target['code']]=[]
            self.modules[target['code']].append({'relation': {'type': relation.type, 'params':dict(relation)}, 
                                                        'target':{ 'moduleID': target['element_id'],'params':target}})
            
        

        
    def loadILO(self):
        '''
        Loads ILO links from the database. Does not create new links or ILOs.

        Returns
        -------
        None.

        '''
        self.ILO = {}
        cypher = "MATCH (p:Programme ) -[a]-(b:ProgrammeILO) WHERE elementID(p) = $id RETURN a,b"
        records,_,_ =self.factory.db.execute_query(cypher, id=self.element_id, database_=self.factory.dbname)
        for t in records:
            relation, target = t.items()[0:2]
            
            self.ILO[target.element_id]= (dict(target), dict(relation))
        
 
        
    def withdraw(self, year):
        '''
        Set the Programme to WITHDRAWN. Only possible if there are no future versions.

        Returns
        -------
        None.

        '''
        if AcademicYear(year) and AcademicYear(year) > AcademicYear(self.params['startyear']):
            self.params['endyear']=year
            cypher = 'MATCH (p:Programme) where elementID(p)=$id SET p.endyear=$year'
            records,_,_ =self.factory.db.execute_query(cypher, id=self.element_id,year=year, database_=self.factory.dbname)
        

    def map_module(self, module, optional=0, year=None, remove=False):
        '''
        Add a module to the Programme, updating if exisitng  already appended.

        Parameters
        ----------
        module : Module object
            DESCRIPTION.
        optional: Boolean
        remove: Academic Year for last instance
        Returns
        -------
        None.

        '''
        relations=('IS_CORE','IS_ELECTIVE')
        relation= relations[int(bool(optional))]
        cypher1 = 'MATCH (p:Programme) where elementID(p)=$pid \n MATCH (m:Module) where elementID(m)=$mid \n merge (p) <-[b:{relation}]-(m)  return p,b,m'
        
        if module.params['code'] in self.modules:
            if remove:
                
                records,_,_ =self.factory.db.execute_query(cypher1.format(relation=relation), 
                                                           pid=self.element_id,year=year, 
                                                           mid=module.element_id,
                                                           database_=self.factory.dbname)
                for r in self.modules[module.params['code']]:
                    if r['relation']['type']==relation:
                        r['relation']['params']['endyear']=year
            else:
                for r in self.modules[module.params['code']]:
                    if r['relation']['type']!=relation:
                        r['relation']['params']['endyear']=year
                        records,_,_ =self.factory.db.execute_query(cypher1.format(relation=relations[(int(bool(optional))+1)%2]), 
                                                                   pid=self.element_id,year=year, 
                                                                   mid=module.element_id,
                                                                   database_=self.factory.dbname)
         
        if not remove:
            if module.params['code'] not in self.modules:
                 self.modules[module.params['code']]=[]
            cypher2 =f'MATCH (p:Programme) where elementID(p)=$pid MATCH (m:Module)  where elementID(m)=$mid MERGE (p)<-[:{relation} {{startyear:$year }}] - (m) return m,p'
            records,_,_ =self.factory.db.execute_query(cypher2, 
                                                        pid=self.element_id,year=year, 
                                                        mid=module.element_id,
                                                        database_=self.factory.dbname)
        self.loadmodules()
           
                                           
               
           
           
    def map_ilo(self, ilo, year, remove=False):
        '''
        Associates or updates a Programme ILO mapping to a Programme.

        Parameters
        ----------
        ilo : ProgrammeILO 
            Programme ILO object
        year : text describing the academic year
            Must be either the start year, or for removing an ILO the last year for which it will be relevant.
        remove : Boolean, optional
            Flag to say whether the ILO should be dissociated from teh Programme. The default is False.

        Returns
        -------
        None.

        '''
        
        if not AcademicYear(year):
            raise UnparseableYearException(f'Cannot parse year value {year}')
        if ilo.element_id in self.ILO:
            if remove:
                self.ILO[ilo.element_id]['endyear']=year
                cypher="MATCH (p: Programme) -[b]- (i:ProgrammeILO) WHERE elementID(p) =$pid AND elementID(i) =$iid SET b.endyear=$year"
                records,_,_ = self.factory.db.execute_query(cypher,pid=self.element_id, iid=ilo.element_id, year=year, database_=self.factory.dbname)
            return
        if remove:
            return
        cypher = "MERGE (p:Programme) -[b:HAS_ILO {startyear:$year}]->(i:ProgrammeILO) where elementID(p)=$pid AND elementID(i) = $iid RETURN b"
        records,_,_ = self.factory.db.execute_query(cypher,pid=self.element_id, iid=ilo.element_id, year=year, database_=self.factory.dbname)
        if records:
            relation=records[0].items()[0][1]
            self.ILO[ilo.element_id]=(dict(ilo),dict(relation))

    
class Module(Node):
    
    DRAFT = 0
    CURRENT = 1
    ARCHIVED = 2
    WITHDRAWN = 3
    PREREQUISITE = 1
    COREQUISITE = 0
    ANTIREQUISITE = 2
    ntype='Module'
    requiredParams = {
        'code': 'Module code',
        'name': 'Module name',
        'credits': 'Credit weight',
        'scqflevel': 'SCQF level',
        'shelevel': 'SHE level',
        'semester': '1, 2 or both'
        }
    optionalParams= {
        'block': 'Teaching block: C or D',
        'startyear':'First academic year',
        'endyear': 'Last academic year'
        }
    
    def __init__(self, factory,  **params ):
        '''
        Create a Programme instance.

        Parameters
        ----------
        factory - database connection and cache for Module
        **params : 
                    '''
        super().__init__(factory,**params)
        
        self.ILO={}
        self.Activities={}
        self.Assessments = {}
        if self.element_id:
            self.loadILO()
            self.loadConstraints()
            self.loadActivities()
            self.loadAssessments()
            
    def loadActivities(self):
        '''
        Loads module links from the database to the modules list. Does not create now entries in the database.

        Returns
        -------
        None.

        '''
        self.Activities=[]
        cypher = "MATCH (m:Module ) -[a]-(b:TeachingActivity) WHERE elementID(m) = $id RETURN a,b"
        records,_,_ =self.factory.db.execute_query(cypher, id=self.element_id, database_=self.factory.dbname)
        for t in records:
            relation = t.items()[0][1]
            target = t.items()[1][1]
            self.Activities.append({'relation': {'type': relation.type, 'params':dict(relation)}, 
                                                        'target':{ 'TeachingActivityID': target.element_id,'params':dict(target)}})
            
        
        
        
    def loadILO(self):
        '''
        Loads ILO links from the database. Does not create new links or ILOs.

        Returns
        -------
        None.

        '''
        self.ILO = {}
        cypher = "MATCH (m:Module ) -[a]-(b:ModuleILO) WHERE elementID(m) = $id RETURN a,b"
        records,_,_ =self.factory.db.execute_query(cypher, id=self.element_id, database_=self.factory.dbname)
        for t in records:
            relation, target = t.items()[0:2]
            self.ILO[target.element_id]= (dict(target),dict(relation))
        

    def loadConstraints(self):
        '''
        Loads in but does not create constraint

        Returns
        -------
        None.

        ''' 
        self.requisites = {}
        cypher = "MATCH (m:Module ) <-[a]- (b:Module) WHERE elementID(m) = $id RETURN a,b"
        records,_,_ =self.factory.db.execute_query(cypher, id=self.element_id, database_=self.factory.dbname)
        for t in records:
            relation, target = t.items()[0:2]
            relationdata = dict(relation)
            relationdata['element_id']=relation.element_id
            relationdata['type']=relation.type
            targetdata = dict(target)
            targetdata['element_id']=target.element_id
            self.requisites.append({'constraint':relationdata, 'module': targetdata})
    def loadAssessments(self):
        '''Retrieve any linked assessments from the database
        # TODO
        '''
        #TODO
        
    def setConstraint(self, constraint, module, year, remove=False):
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
        #TODO
            
        
        
        
    def map_ilo(self, ilo, year, remove=False):
        '''
        Associates or updates a Module ILO mapping to a Module.
    
        Parameters
        ----------
        ilo : ModuleILO 
            Module ILO object
        year : text describing the academic year
            Must be either the start year, or for removing an ILO the last year for which it will be relevant.
        remove : Boolean, optional
            Flag to say whether the ILO should be dissociated from the Module. The default is False.
    
        Returns
        -------
        None.
    
        '''
        
        if not AcademicYear(year):
            raise UnparseableYearException(f'Cannot parse year value {year}')
        if ilo.element_id in self.ILO:
            if remove:
                self.ILO[ilo.element_id]['endyear']=year
                cypher="MATCH (m: Module) -[b]- (i:ModuleILO) WHERE elementID(m) =$mid AND elementID(i) =$iid SET b.endyear=$year"
                records,_,_ = self.factory.db.execute_query(cypher,mid=self.element_id, iid=ilo.element_id, year=year, database_=self.factory.dbname)
            return
        if remove:
            return
        cypher = "MERGE (m:Module) -[b:HAS_ILO {startyear:$year}]->(i:ModuleILO) where elementID(m)=$mid AND elementID(i) = $iid RETURN b"
        records,_,_ = self.factory.db.execute_query(cypher,mid=self.element_id, iid=ilo.element_id, year=year, database_=self.factory.dbname)
        if records:
            relation=records[0].items()[0][1]
            self.ILO[ilo.element_id]=(dict(ilo),dict(relation))
    
    def map_activity( self, activity, relationtype='HAS_ACTIVITY'):
        '''
        Adds an activity to a module

        Parameters
        ----------
        activity : TeachingActivity

        Returns
        -------
        None.

        '''
        if activity.element_id not in [x['target']['TeachingActivityID'] for x in self.Activities]:
            cypher = f"MERGE (m:Module ) -[a:{relationtype}]-(b:TeachingActivity) WHERE elementID(m) = $id AND elementID(b)=$tid RETURN a,b"
            records,_,_ =self.factory.db.execute_query(cypher, id=self.element_id, tid=activity.element_id, database_=self.factory.dbname)
            for t in records:
                relation = t.items()[0][1]
                target = t.items()[1][1]
                self.Activities.append({'relation': {'type': relation.type, 'params':dict(relation)}, 
                                                            'target':{ 'TeachingActivityID': target.element_id,'params':dict(target)}})
        

        
# class TeachingActivityType(Node): 
    
#     ntype='TeachingActivityType'
#     requiredParams = {
#         'code': 'Module code',
#         'name': 'Module name',
#         'credits': 'Credit weight',
#         'level': 'SCQF level'
#         }
#     optionalParams= {
#         'startyear':'First academic year',
#         'endyear': 'Last academic year',
#         'school':'School which manages the Programme'}

    
#     def __init__(self, factory, **kwargs):
#         self.factory=factory
#         self.name = kwargs.get("name")
#         self.definition = kwargs.get("definition")
#         self.id = kwargs.get("id")
#         if self.id is None:
#             self.create()
            
        
#     def create(self):
#         '''
#         Creates a new database entry for the TeachingActivityType entity

#         Returns
#         -------
#         None.

#         '''
#         insertsql = "Insert into TeachingActivityType (name, definition) VALUES (%s,%s)"
#         cursor = self.factory.db.cursor()
#         cursor.excecute(insertsql, (self.name, self.definition))
#         self.id = cursor.lastrowid



class TeachingActivity (Node):
    ntype='TeachingActivity'
    requiredParams = {
        'year': 'AcademicYear',
        'type': 'Activity type'
        }
    optionalParams= {
        'duration':'length of activity'
        }

    def __init__(self, factory, **kwargs):
        #description, duration, TAtype, version,previous_TA, moduleID, sequence
        super().__init__(factory, **kwargs)
        self.loadILO()
        
    def loadILO(self):
        '''
        Loads ILO links from the database. Does not create new links or ILOs.

        Returns
        -------
        None.

        '''
        self.ILO = {}
        cypher = "MATCH (t:TeachingActivity ) -[a]-(b:ActivityILO) WHERE elementID(t) = $id RETURN a,b"
        records,_,_ =self.factory.db.execute_query(cypher, id=self.element_id, database_=self.factory.dbname)
        for t in records:
            relation, target = t.items()[0:2]
            self.ILO[target.element_id]= (dict(target),dict(relation))
    def map_ilo(self, ilo):
        '''
        Associates or updates a Module ILO mapping to a Module.
    
        Parameters
        ----------
        ilo : ModuleILO 
            Module ILO object
        year : text describing the academic year
            Must be either the start year, or for removing an ILO the last year for which it will be relevant.
        remove : Boolean, optional
            Flag to say whether the ILO should be dissociated from the Module. The default is False.
    
        Returns
        -------
        None.
    
        '''
        
        if ilo.element_id in self.ILO:
            return
        cypher = "MERGE (t:TeachingActivity) -[b:HAS_ILO ]->(i:ActivityILO) where elementID(t)=$tid AND elementID(i) = $iid RETURN b"
        records,_,_ = self.factory.db.execute_query(cypher,tid=self.element_id, iid=ilo.element_id, database_=self.factory.dbname)
        if records:
            relation=records[0].items()[0][1]
            self.ILO[ilo.element_id]=(dict(ilo),dict(relation))
            

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
        module.map_activity(self)
        self.module=module
        

        
        
        
class ILO(Node):
    ntype='ILO'
    ILO_KNOWLEDGE = 1
    ILO_UNDERSTANDING=2
    ILO_SKILL=3
    ILO_ATTITUDE=4
    requiredParams = {
        }
    optionalParams= {
        'SOLO': 'Solo level of the ILO'
        }
    def __init__(self, factory,**kwparams):
        super().__init__(factory,**kwparams)
    
    

class ActivityILO(ILO):

    bloomterms = ('None','Remember',	'Understand',	'Apply',	'Analyze',	'Evaluate',	'Create')
    bloommap ={
        }
    categories = ('Knowledge','Understanding', 'Skill', 'Attitude')

    def __init__(self, factory, **kwargs):
        super().__init__(factory, **kwargs)
        self.milo=None
        self._get_milo()
      
    def _get_milo(self):
        '''
        Retrieves and assigns any mapped MILO to this AILO. 
        Raises an exception if more than one MILO is mapped in the DB

        Returns
        -------
        relation object between AILO and AILO

        '''
       
        cypher = "MATCH (a:ActivityILO) -[b:MAPS_TO] - (m:ModuleILO) WHERE elementID(a)=$id RETURN a,b,m"
        records,_,_ = self.factory.db.execute_query(cypher,id=self.element_id, 
                                                    database_=self.factory.dbname)
        if records:
            if len(records)>1:
                raise Exception('Maps to multiple Module ILOs')
            
            target=records[0].items()[2][1]
            self.milo = target    
    
    def getActivitiesForILO(self):
        '''
        Retrieve all Activities with this ILO

        Returns
        -------
        List of TeachingActivity

        '''
        activities = self.factory.getElementsForElement(self,'TeachingActivity',max_steps=1)
        return activities

    def supports(self, milo=None):
        '''
        Maps (if milo given) and returns the moduleILO, if present,
        to which this activity ILO maps
        
        
        Parameters
        ----------
        milo : ModuleILO, optional
            ModuleILO object which should be mapped to this activity ILO. 
            The default is None.
        
        Returns
        -------
        ModuleILO if assigned, None if not assigned
        
        '''
        if self.milo and milo:
            if milo != self.milo:
                #delete existing relation and replace.
                cypherd = "MATCH (a:ActivityILO) -[b:MAPS_TO] - (m:ModuleILO) WHERE elementID(a)=$id DELETE b"
                records,_,_ = self.factory.db.execute_query(cypherd,id=self.element_id, 
                                                            database_=self.factory.dbname)
            else:
                return self.milo
        if milo:
            cyphera = "MERGE (a:ActivityILO) -[MAPS_TO]-> (m:ModuleILO) WHERE elementID(a)=$id AND elementID(m) =$mid"
            records,_,_ = self.factory.db.execute_query(cyphera,
                                                        id=self.element_id, mid=milo.element_id,
                                                        database_=self.factory.dbname)
            self.milo=milo
        return self.milo

    
class ModuleILO(ILO):
     
    def __init__(self, factory, **kwargs):
        super().__init__(factory, **kwargs)
        self.pilo=None
        self._get_pilo()

    def _get_pilo(self):
        '''
        Retrieves and assigns any mapped PILO to this MILO. 
        Raises an exception if more than one PILO is mapped in the DB

        Returns
        -------
        relation object between MILO and PILO

        '''
        
        cypher = "MATCH (m:ModuleILO) -[a:MAPS_TO] - (p:ProgrammeILO) WHERE elementID(m)=$id RETURN m,a,p"
        records,_,_ = self.factory.db.execute_query(cypher,id=self.element_id, 
                                                    database_=self.factory.dbname)
        if records:
            if len(records)>1:
                raise Exception('Maps to multiple Programme ILOs')
            
            target=records[0].items()[2][1]
            self.pilo = target

    def getModulesForILO(self):
        '''
        Retrieve all Activities with this ILO
         
        Returns
        -------
        List of Modules
         
        '''
        modules = self.factory.getElementsForElement(self,'Module',max_steps=1)
        return modules
            
    def supports(self, pilo=None):
        '''
        Maps (if pilo given) and returns the progammeILO, if present to which this module ILO maps
        
        
        Parameters
        ----------
        pilo : ProgrammeILO, optional
            ProgrammeILO object which should be mapped to this module ILO. 
            The default is None.
        
        Returns
        -------
        ProgrammeILO if assigned, None if not assigned
        
        '''
        if self.pilo and pilo:
            if pilo != self.pilo:
                #delete existing relation and replace.
                cypherd = "MATCH (m:ModuleILO) -[a:MAPS_TO] - (p:ProgrammeILO) WHERE elementID(m)=$id DELETE a"
                records,_,_ = self.factory.db.execute_query(cypherd,id=self.element_id, 
                                                            database_=self.factory.dbname)
            else:
                return self.pilo
        if pilo:
            cyphera = "MERGE (m:ModuleILO) -[MAPS_TO]-> (p:ProgrammeILO) WHERE elementID(m)=$id AND elementID(p) =$pid"
            records,_,_ = self.factory.db.execute_query(cyphera,
                                                        id=self.element_id, pid=pilo.element_id,
                                                        database_=self.factory.dbname)
            self.pilo=pilo
        return self.pilo

    
class ProgrammeILO(ILO):
   
     
    def __init__(self, factory, **kwargs):
        super().__init__(factory, **kwargs)
        self.pilo=None

    def getProgrammesForILO(self):
        '''
        Retrieve all Activities with this ILO
         
        Returns
        -------
        List of Modules
         
        '''
        programmes = self.factory.getElementsForElement(self,'Programme',max_steps=1)
        return programmes
            
     
    
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

class Assessment(TeachingActivity):
    ntype='Assessment'
    requiredParams = {
        'year': 'AcademicYear',
        'type': 'Activity type',
        'weighting': 'percentage weighting',
        'code': 'SEQ number'
        }
    optionalParams= {
        }

    def __init__(self, factory,**kwargs):
        super().__init__(factory, **kwargs)
        

   

