-- # -*- coding: utf-8 -*-
-- """
-- Created on Wed Jun 15 14:19:16 2022
-- 
-- @author: DMAMartin
-- """

Create or replace Table ApprovalEvents (
ID integer not null primary key auto_increment,
Event_name text not null,
Event_date text not null
);

Create or replace table Programme (
    ID integer primary key not null auto_increment, 
-- Unique identifier
    P_name text not null, 
    P_code text not null,
    P_version text not null,
    Previous_P integer,
    foreign key Previous_P references Programme (ID),
    change text not null, 
    Future_P integer,
    foreign key (Future_P) references Programme(ID),
    approvalEvent integer,
    foreign key (approvalEvent) references ApprovalEvents(ID),
    status ENUM('DRAFT', 'CURRENT', 'ARCHIVED', 'WITHDRAWN') not null default 'DRAFT'
);
    
CREATE or REPLACE Table ProgrammeElement (
    ID integer not null primary key auto_increment,
    Ecode text not null,
-- Text holding section number in spec form
    Etext text not null default "n/a",
-- Boilerplate text for program spec form        
);

CREATE or REPLACE Table ProgrammeElementMAP (
    ID integer primary key not null auto_increment,
    ProgrammeID integer not null,
    foreign key (ProgrammeID) references Programme (ID),
    ElementID integer not null,
    foreign key (ElementID) references ProgrammeElement (ID) 
);



CREATE or REPLACE Table School (
ID integer primary key auto_increment,
name text not null,
abbrev text not null);

CREATE or REPLACE Table Person (
ID integer primary key auto_increment,
firstname text not null,
lastname text not null,
email text not null,
affiliation integer,
foreign key (affiliation) references School (ID) 
);

CREATE or REPLACE TABLE CalendarBlock (
ID integer not null primary key auto_increment,
block text not null,
description text
);

CREATE or REPLACE Table TModule (
ID integer primary key auto_increment,
code text not null,
name text not null,
TMlevel integer not null,
altlevel integer,
version text not null,
previous_M integer,
future_M integer,
credits integer not null default 20,
block integer not null,
change text not null,
foreign key (block) references CalendarBlock(ID),
foreign key (previous_M) references TModule(ID),
foreign key (future_M) references TModule(ID),
 approvalEvent integer,
    foreign key (approvalEvent) references ApprovalEvents(ID),
    status ENUM('DRAFT', 'CURRENT', 'ARCHIVED', 'WITHDRAWN') not null default 'DRAFT',
    sqcflevel integer not null
);

CREATE or REPLACE TABLE ModuleConstraint (
ID integer not null primary key auto_increment,
moduleID integer not null,
foreign key (moduleID) references TModule (ID),
constraintType ENUM('co-requisite','pre-requisite','anti-requisite') not null,
constraintModuleID integer not null,
foreign key (constraintModuleID) references TModule (ID)
);

CREATE or REPLACE TABLE ModuleProgrammeMAP (
ID integer not null primary key auto_increment,
moduleID integer not null,
programmeID integer not null,
optional ENUM ('optional', 'core') not null,
optionset integer,
foreign key (moduleID) references TModule (ID),
foreign key (programmeID) references Programme (ID)
);

CREATE or REPLACE Table  ProgrammeLead (
ID integer primary key auto_increment,
programmeID integer not null,
foreign key (programmeID) references Programme (ID),
personID integer not null,
foreign key (personID) references Person (ID),

);

CREATE or REPLACE Table  ModuleManager (
ID integer primary key auto_increment,
moduleID integer not null,
foreign key (moduleID) references TModule (ID),
personID integer not null,
foreign key (personID) references Person (ID),

);

CREATE or REPLACE Table ModuleElement (
ID integer primary key auto_increment,
    Ecode text not null,
-- Text holding section number in spec form
    Etext text not null default "n/a",
-- Boilerplate text for module spec form   
);

CREATE or REPLACE Table ModuleElementMAP (
ID integer primary key auto_increment,
moduleID integer not null,
FOREIGN KEY (moduleID) references TModule (ID),
elementID integer not null,
FOREIGN KEY (elementID) references ModuleElement(ID)  
);

CREATE or REPLACE Table TeachingActivityType (
ID integer primary key auto_increment,
name text unique not null,
definition text not null
);

CREATE or REPLACE Table TeachingActivity (
ID integer not null primary key auto_increment,
name text not null,
description text not null,
duration integer not null,
TAtype integer not null,
version text,
previous_TA integer,
moduleID integer not null,
seq integer not null,
weighting integer not null,
foreign key (moduleID) references TModule (ID),
foreign key (previous_TA) references TeachingActivity (ID),
foreign key (TAtype) references TeachingActvityType (ID)
);

CREATE or REPLACE Table TeachingActivityStaff (
ID integer primary key auto_increment,
personID integer not null,
activityID integer not null,
foreign key (personID) references Person (ID),
foreign key (activityID) references TeachingActivity (ID)
);

Create or Replace Table TeachingActivityDocument (
ID integer not null primary key auto_increment,
description text not null,
documentpath text not null,
activityID integer not null,
foreign key (activityID) references TeachingActivity (ID)
);



CREATE or REPLACE Table ProgrammeILO (
ID integer not null auto_increment primary key,
ILOtext text not null,
category ENUM('Knowledge','Understanding', 'Skill', 'Attitude') not null
);

CREATE or REPLACE Table ProgrammeILOMAP (
ID integer not null auto_increment primary key,
programmeID integer not null,
piloID integer not null,
foreign key (programmeID) references Programme(ID),
foreign key (piloID) references ProgrammeILO (ID)
);



CREATE or REPLACE Table ModuleILO (
ID integer not null auto_increment primary key,
ILOtext text not null,
category int not null
);

CREATE or REPLACE Table ModuleILOMAP (
ID integer not null auto_increment primary key,
moduleID integer not null,
miloID integer not null,
foreign key (moduleID) references TModule(ID),
foreign key (miloID) references ModuleILO (ID)
);


CREATE or REPLACE Table ActivityILO (
ID integer not null auto_increment primary key,
ILOtext text not null,
category integer not null,
moduleILO integer,
bloom ENUM('None','Remember',	'Understand',	'Apply',	'Analyze',	'Evaluate',	'Create') Not null,
Foreign Key (moduleILO) REFERENCES ModuleILO (ID)
);

CREATE or REPLACE Table ActivityILOMAP (
ID integer not null auto_increment primary key,
activityID integer not null,
ailoID integer not null,
foreign key (activityID) references TeachingActivity(ID),
foreign key (ailoID) references ActivityILO (ID)
);


CREATE or REPLACE TABLE AssessmentType (
ID integer not null primary key auto_increment,
name text not null,
definition text not null
);

CREATE or REPLACE TABLE Assessment (
ID integer not null primary key auto_increment,
name text not null,
description text not null,
type integer not null,
foreign key (type) references AssessmentType (ID),
file text
);

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

CREATE or REPLACE TABLE AssessmentMarker (
ID integer not null primary key auto_increment,
personID integer not null,
assessmentinstanceID integer not null,
foreign key (personID) references Person (ID),
foreign key (assessmentinstanceID) references AssessmentInstance (ID)
);

CREATE or REPLACE AssessmentActivityILOMAP (
ID integer not null primary key auto_increment,
assessmentID integer not null,
activityiloID integer not null,
foreign key (assessmentID) references Assessment (ID),
foreign key (activityiloID) references ActivityILO (ID);
);

CREATE or REPLACE TABLE Benchmark (
ID integer not null primary key auto_increment,
statement text not null,
statementref text not null,
statementurl text,
statementorg text not null
);

Create or replace table BenchmarkSpecMAP (
ID integer not null primary key auto_increment,
benchmarkID integer not null,
elementID integer not null,
foreign key (benchmarkID) references Benchmark (ID),
foreign key (elementID) references ModuleElement (ID)
);

CREATE or REPLACE TABLE QAorg (
ID integer not null primary key auto_increment,
name text not null,
description text not null,
url text not null);

CREATE or REPLACE TABLE QADescriptor (
ID integer not null primary key auto_increment,
orgID integer not null,
foreign key (orgID) references QAorg (ID),
orgref text not null,
orgsubject text not null,
descriptor text not null
);

CREATE or REPLACE TABLE DescriptorActivityILOMAP (
ID integer not null primary key auto_increment,
ailoID integer not null,
descriptorID integer not null,
foreign key (ailoID) references ActivityILO (ID),
foreign key (descriptorID) references QADescriptor (ID) 
);

CREATE or REPLACE TABLE RSBCriterion (
ID integer not null primary key auto_increment,
description text not null,
category text not null,
clevel text not null,
sublevel text not null,
version text not null,
prev_version integer,
foreign key (prev_version) references RSBCriterion (ID)
);

CREATE or REPLACE TABLE RSBCriterionMAP (
ID integer nto null primary key auto_increment,
rsbcritID integer not null,
ailoID integer not null,
foreign key (rsbcritID) references RSBCriterion (ID),
foreign key (ailoID) references ActivityILO (ID)
);