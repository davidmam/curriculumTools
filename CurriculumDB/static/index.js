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
        versions = versions + " <span id='prog_"+vprog['id']+"'><a href='/Programme/"+vprog['id']+"' >("+vprog['P_version'];
        if (vprog['status'] == "CURRENT"){
            versions = versions+" - CURRENT";
        }
        versions=versions+")</a></span>";
    }
    content = "<tr class='progentry'><td>"+prog['P_code']+"</td><td><span id='prog_"+prog['id']+"'>"+title+"</span></td><td>"+versions+"</td></tr>"
    $('#programmes_table tr.progentry').after(content);
    
   
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
                     content = "<tr class='progentry'><td>"+prog['P_code']+"</td><td><span id='prog_"+prog['id']+"'>"+title+"</span></td><td>"+versions+"</td><td></td></tr>"
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

var getcalendarblocks = function () { 
// retrieves a dictionary of calendar blocks
    blocks= [
    {ID:1, code:'A', description:'Semester 1 weeks 1-5'},
    {ID:2, code:'B', description:'Semester 1 weeks 7-11'},
    {ID:3, code:'AB', description:'Semester 1 weeks 1-11'},
    {ID:4, code:'C', description:'Semester 2 weeks 1-5'},
    {ID:5, code:'CD', description:'Semester 2 weeks 1-11'},
    {(ID:6, code:'D', description:'Semester 2 weeks 7-11');
    {ID:7, code:'Other', description:'Outwith semester'}];
    
    return blocks
}
var getschools = function () {
// retrieve a list of schools
}

var loadmodules = function (data) {

    var blocks = getcalendarblocks()
    blockselect = ""
    for b in blocks {
        blockselect = blockselect+"<option value='"+blocks[b]['id']+"' title='"+blocks[b]['description']+"' >"+blocks[b]['code']+"</option>"
    }
    $('#modules_table').html("<tr class='modentry'><th>Module Code</th><th>Module Title</th><th>Level</th><th>Block</th><th>Versions</th><th></tr></tr>" +
    "<tr><td><input name='newmodcode' id='newmodcode' type=text /> </td><td><input name='newmodtitle' id='newmodtitle' type=text /> </td><td><select id='newmodlevel' name='newmodlevel'><option value='1'>1</option><option value='2'>2</option><option value='3'>3</option><option value='4'>4</option><option value='5'>5</option></select></td><td><select id='newmodblock' name='newmodblock'>"+blockselect+"</select></td><td><input name='newmodversion' id='newmodversion' type=text /> </td><td><form id='newmod'><button type='submit' class='form-add-button' name='newmodsubmit' id='newmodsubmit'><i title='Add new module' class='fas fa-plus'></i></button></form></td></tr>");
    
    
    for m in data['heads'] {
        mod = data['modules'][data['heads'][p]]
        code = mod['code']
        title = "<a href='/Module/"+mod['id']+"' > "+mod['name']+" ("+mod['version']+" - "+mod['status']+")</a>";
        versions = ""
        for v in data['versions'][mod['id']]{
            vmod = data['modules'][data['versions'][mod['id']][v]]
            versions = versions + " <span id='mod_"+vmod['id']+"'><a href='/Module/"+vmod['id']+"' >("+vmod['version'];
            if (vmod['status'] == "CURRENT"){
                versions = versions+" - CURRENT";
            }
            versions=versions+")</a></span>";
        }
        content = "<tr class='modentry'><td>"+mod['code']+"</td><td><span id='mod_"+mod['id']+"'>"+title+"</span></td><td>"+mod['level']+"</td><td>"+mod['block']+"</td><td>"+versions+"</td></tr>"
        $('#modules_table tr.modentry').after(content);
        
    }
     $('#newmod').submit( function (event) {

         var postdata = { 'name': $('#newmodname').val(),
         'code': $('#newmodcode').val(),
         'block':$('#newmodblock').val(),
         'TMlevel': parseInt($('#newmodlevel').val()),
         'version': $('#newmodversion').val()
                 };
         
         //alert(postdata);
         try {
             $.ajax({ url: "/ajax/module/add",
                 method: 'POST',
                 data: postdata,
             }).done( function (respdata){
                 if('error' in respdata){
                     $('#qb_ajax_messages').html(respdata['error']);
                     alert(respdata['user'] + respdata['error']);
                 }else{
                     
                     // TODO
                     var mod=respdata['module'];
                      code = mod['code']
                      title = "<a href='/Module/"+mod['id']+"' > "+mod['name']+" ("+mod['version']+" - "+mod['status']+")</a>";
                      versions = ""
                     content = "<tr class='modentry'><td>"+mod['code']+"</td><td><span id='mod_"+mod['id']+"'>"+title+"</span></td><td>"+versions+"</td><td>"+mod['block']+"</td><td>"+mod['level']+"</td><td></td></tr>"
                     //var content = '<tr class="progentry"><td><span id="qbname_'+qb.qbid+'">'+qb.name+'</span></td><td>'+qb.description+'</td><td>'+qb.qcount+'</td><td>'+qb.access+'</td><td><form id="qbform_'+qb.qbid+'" action="/questionbank" method="POST"><input type="hidden" name="qbname" value="'+qb.name+'" /><button type="submit"  class="form-edit-button" name="qbsubmit"><i title="Edit content bank" class="fas fa-edit"></i></button></form></td></tr>';
                     $('#modules_table tr.modentry:last').after(content);
                     
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


$(document).ready(function () {

getallprogrammes(loadprogrammes);
getallmodules(loadmodules);

});