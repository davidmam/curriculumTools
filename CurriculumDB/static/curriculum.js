
var getallprogrammes = function (callback){
    $.ajax({ url: "/ajax/programmes",
            method: 'GET',}).done( function (respdata){
            if('error' in respdata){
                $('#messages').html(respdata['error']);
                alert(respdata['user'] + respdata['error']);
            }
            callback(respdata['programmes'])
            // callback the function that will then add this on the relevant page.
    };

var  getallmodules = function (callback){
    //TODO
     $.ajax({ url: "/ajax/modules",
             method: 'GET',}).done( function (respdata){
             if('error' in respdata){
                 $('#messages').html(respdata['error']);
                 alert(respdata['user'] + respdata['error']);
             }
             callback(respdata['modules'])
             // callback the function that will then add this on the relevant page.
    };
    
var getallactivities= function (callback){
    $.ajax({ url: "/ajax/activities",
         method: 'GET',}).done( function (respdata){
         if('error' in respdata){
             $('#messages').html(respdata['error']);
             alert(respdata['user'] + respdata['error']);
         }
         callback(respdata['activities'])
         // callback the function that will then add this on the relevant page.
};

var getallprogrammeILOs = function (callback){
    $.ajax({ url: "/ajax/programmeILOs",
             method: 'GET',}).done( function (respdata){
             if('error' in respdata){
                 $('#messages').html(respdata['error']);
                 alert(respdata['user'] + respdata['error']);
             }
             callback(respdata['programmeILOs'])
             // callback the function that will then add this on the relevant page.    
    };

var  getallmoduleILOs = function (callback){
    $.ajax({ url: "/ajax/moduleILOs",
             method: 'GET',}).done( function (respdata){
             if('error' in respdata){
                 $('#messages').html(respdata['error']);
                 alert(respdata['user'] + respdata['error']);
             }
             callback(respdata['moduleILOs'])
             // callback the function that will then add this on the relevant page.    
    //TODO
    };
    
var getallactivityILOs= function (callback){
    $.ajax({ url: "/ajax/activityILOs",
             method: 'GET',}).done( function (respdata){
             if('error' in respdata){
                 $('#messages').html(respdata['error']);
                 alert(respdata['user'] + respdata['error']);
             }
             callback(respdata['activityILOs'])
             // callback the function that will then add this on the relevant page.    
//TODO
};

var addActivity = function (data, callback){
    $.ajax({ url: "/ajax/activity/add",
             method: 'POST', data: data}).done( function (respdata){
             if('error' in respdata){
                 $('#messages').html(respdata['error']);
                 alert(respdata['user'] + respdata['error']);
             }
             callback(respdata['activity'])
             // callback the function that will then add this on the relevant page.    
};
var addProgramme = function (data, callback){
    $.ajax({ url: "/ajax/programme/add",
             method: 'POST', data: data}).done( function (respdata){
             if('error' in respdata){
                 $('#messages').html(respdata['error']);
                 alert(respdata['user'] + respdata['error']);
             }
             callback(respdata['programme'])
             // callback the function that will then add this on the relevant page.    
};
var addModule = function (data, callback){
    $.ajax({ url: "/ajax/module/add",
             method: 'POST', data: data}).done( function (respdata){
             if('error' in respdata){
                 $('#messages').html(respdata['error']);
                 alert(respdata['user'] + respdata['error']);
             }
             callback(respdata['module'])
             // callback the function that will then add this on the relevant page.    
};
var addActivityILO = function (data, callback){
    $.ajax({ url: "/ajax/activityILO/add",
             method: 'POST', data: data}).done( function (respdata){
             if('error' in respdata){
                 $('#messages').html(respdata['error']);
                 alert(respdata['user'] + respdata['error']);
             }
             callback(respdata['activityILO'])
             // callback the function that will then add this on the relevant page.    
};
var addProgrammeILO = function (data, callback){
    $.ajax({ url: "/ajax/programmeILO/add",
             method: 'POST', data: data}).done( function (respdata){
             if('error' in respdata){
                 $('#messages').html(respdata['error']);
                 alert(respdata['user'] + respdata['error']);
             }
             callback(respdata['programmeILO'])
             // callback the function that will then add this on the relevant page.    
};
var addModuleILO = function (data, callback){
    $.ajax({ url: "/ajax/moduleILO/add",
             method: 'POST', data: data}).done( function (respdata){
             if('error' in respdata){
                 $('#messages').html(respdata['error']);
                 alert(respdata['user'] + respdata['error']);
             }
             callback(respdata['moduleILO'])
             // callback the function that will then add this on the relevant page.    
};
