
var getallprogrammes = function (callback){
    $.ajax({ url: "/ajax/programmes",
            method: 'GET',}).done( function (respdata){
            if('error' in respdata){
                $('#messages').html(respdata['error']);
                alert(respdata['user'] + respdata['error']);
            }
            $('#programmes_table').html('<tr><th>Programme Title</th><th>Versions</th></tr>')
            // need to build a list of all programmes.
            for prog in respdata['programmes']{
                $('#programmes_table').append('<tr><td>'+prog['name'])
            }
    };

var  getallmodules = function (callback){
    //TODO
    };
    
var getallactivities= function (callback){
//TODO
};

var getallprogrammeILOs = function (callback){
//TODO    
    };

var  getallmoduleILOs = function (callback){
    //TODO
    };
    
var getallactivityILOs= function (callback){
//TODO
};

var addActivity = function (data, callback){};
var addProgramme = function (data, callback){};
var addModule = function (data, callback){};
var addActivityILO = function (data, callback){};
var addModuleILO = function (data, callback){};
var addProgrammeILO = function (data, callback){};

