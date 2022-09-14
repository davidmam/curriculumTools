var loadactivities = function (data) {
    $('#activities_table').html("<tr class='actentry'><th>Seq</th><th>Activity Title</th><th>Level</th><th>Block</th><th>Versions</th><th></tr></tr>" +
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
var loadprogrammeILOs = function (data) {};
var loadmoduleILOs = function (data) {};
var loadactivityILOs = function (data) {};
