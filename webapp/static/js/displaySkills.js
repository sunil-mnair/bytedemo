function displaySkills(data){
    var skill_data = '';
    $.each(data,function(key,value){
                       
        for (i=0; i < value.length; i++){

            skill_data += '<tr>';
            skill_data += '<td>'+value[i].skill+'</td>';
            skill_data += '<td>'+'<input type="checkbox" id="skills" name="'+value[i].id+'" max="30" class="form-control" '+value[i].checked+'>'+'</td>';
            skill_data += '</tr>';
        }  
                    
    });
                    
    $('#skill-tbody').html(skill_data);
}