// Javascript file for curriculum database

var loadprogrammes = function (data) {
$('#programmes_table').html("<tr class='progentry'><th>Programme Code</th><th>Programme Title</th><th>Versions</th><th></th></tr>" +
"<tr><td><input name='newprogcode' id='newprogcode' type=text> </td><td><input name='newprogtitle' id='newprogtitle' type=text> </td><td><input name='newprogversion' id='newprogversion' type=text> </td><td><form id='newprog'><button type='submit' class='form-add-button' name='newprogsubmit' id='newprogsubmit'><i title='Add new programme' class='fas fa-plus'></i></button></form></td></tr>");

for p in data['heads'] {
    prog = data['programmes'][data['heads'][p]]
    code = prog['P_code']
    title = "<a href='/Programme/"+prog['id']+"' > "+prog['P_name']+" ("+prog['P_version']+" - "+prog['status']+")</a>";
    versions = ""
    for v in data['versions'][prog['id']]{
        vprog = data['programmes'][data['versions'][prog['id']][v]]
        versions = versions + " <span id='prog_"+vprog['id']+"'>(<a href='/Programme/"+vprog['id']+"' />"+vprog['P_version'];
        if (vprog['status'] == "CURRENT"){
            versions = versions+" - CURRENT";
        }
        versions=versions+"</a>)</span>";
    }
    content = "<tr class='progentry'><td>"+prog['P_code']+"</td><td><span id='prog_"+prog['id']+"'>"+title+"</span></td><td>"+versions+"</td></tr>"
    $('#programmes_table tr.progentry').after(content);
    $('#prog_'+prog['id']).on('click', function () {viewprogramme(prog['id'])});
    for v in data['versions'][prog['id']]{
        $('#prog_'+data['versions'][prog['id']][v]).on('click', function () {viewprogramme(data['versions'][prog['id']][v])});
    }
     $('#newprog').submit( function (event) {

         var postdata = { 'P_name': $('#newprogname').val(),
         'P_code': $('#newprogcode').val(),
         'P_version': $('#newprogversion').val()
                 };
         
         //alert(postdata);
         try {
             $.ajax({ url: "/ajax/programme/add",
                 method: 'POST',
                 data: postdata,
             }).done( function (respdata){
                 if('error' in respdata){
                     $('#qb_ajax_messages').html(respdata['error']);
                     alert(respdata['user'] + respdata['error']);
                 }else{
                     
                     // TODO
                     var prog=respdata['programme'];
                      code = prog['P_code']
                      title = "<a href='/Programme/"+prog['id']+"' > "+prog['P_name']+" ("+prog['P_version']+" - "+prog['status']+")</a>";
                      versions = ""
                     content = "<tr class='progentry'><td>"+prog['P_code']+"</td><td><span id='prog_"+prog['id']+"'>"+title+"</span></td><td>"+versions+"</td></tr>"
                     //var content = '<tr class="progentry"><td><span id="qbname_'+qb.qbid+'">'+qb.name+'</span></td><td>'+qb.description+'</td><td>'+qb.qcount+'</td><td>'+qb.access+'</td><td><form id="qbform_'+qb.qbid+'" action="/questionbank" method="POST"><input type="hidden" name="qbname" value="'+qb.name+'" /><button type="submit"  class="form-edit-button" name="qbsubmit"><i title="Edit content bank" class="fas fa-edit"></i></button></form></td></tr>';
                     $('#programmes_table tr.progentry:last').after(content);
                     
                     //$('#qbname_'+qb.qbid).click({qbid:qb.qbid},function (e) {$('#qbform_'+e.data.qbid).submit();});
                     //get_qb_for_user();
                 }
             });
         } catch (err){
             alert(err);
         }
         event.preventDefault();
         return false;
     });

};

var viewprogramme = function (progid ){ };

};


var loadmodules = function (data) {};
var loadactivities = function (data) {};
var loadprogrammeILOs = function (data) {};
var loadmoduleILOs = function (data) {};
var loadactivityILOs = function (data) {};


$(document).ready(function () {

getallprogrammes(loadprogrammes);
getallmodules(loadmodules);
getallactivities(loadactivities);


});