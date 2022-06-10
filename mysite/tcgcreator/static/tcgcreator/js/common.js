    var initEquation = false;
   var global_custom_variable = 0;
   var mouse_x;
   var mouse_y;
   $(document).mousemove(function(event) {
        mouse_x = event.pageX;
        mouse_y = event.pageY;
    });
      var copy_kind_i = 0;
	function getCopyKindChangeBefore(){
		getCopyKindChange(copy_kind_i)
	}
	function deleteCopyKindChange(){
		for(var i=0;i<copy_kind_i;i++){
			$("#copy_kind-"+i).remove()
		}
		$("#id_copy_kind").val("");
		getCopyKindChange(0);
		copy_kind_i=0;
	}
	function getCopyKindChange(num){

	$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_monster_kind/",
   'data': "delete_flag=0&id=copy_kind&id2=copy_kind&num="+num,
'success': function(data){
		if(num==0 ){
			$("#copy_kind").after(data);
			copy_kind_i++;
		}else{
			$("#copy_kind-"+(num-1)).after(data);
			copy_kind_i++;
		}
        }
	})
	}
	$(document).ready(function(){
		$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_monster/",
		   'data': "",
		'success': function(data){
			$("#rel_monster_editor").html("<option value=\"\"></option>"+data);
			$("#monster_editor").html("<option value=\"\"></option>"+data);
			$("#monster_editor_sum").html("<option value=\"\"></option>"+data);
		}});
		$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_effect_kind/",
		   'data': "",
		'success': function(data){
			$("#rel_kind_editor").html(data);
			$("#monster_effect_kind_common").html(data);
			$("#monster_effect_kind_select").html(data);
		}});

		$("#copy_kind").after("<input type=\"button\" onclick=\"getCopyKindChangeBefore()\" value=\"追加\"><input type=\"button\" onclick=\"deleteCopyKindChange(0)\" value=\"削除\"><br>");
		getSelectTrigger(0);
		$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_phase_and_turn/",
		   'data': "",
		'success': function(data){
			$("#monster_variable_change_life_0").html(data);
			$("#copy_monster_variable_change_life").html(data);
		}});
		$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_effect_kind/",
   'data': "",
'success': function(data){
		$("#monster_variable_change_effect_kind_0").html(data);
		}});
        });
	function showUnderNameEqual(id){
		ids = id.split("_");
		if(ids.length == 3){
			if($("#get_under_name_equal_"+ids[0]+"_"+ids[1]+"_"+ids[2]).val() == ""){
				$("#get_under_name_equal_"+ids[0]+"_"+ids[1]+"_"+ids[2]).val("=") ;

			}
		}else if(ids.length == 2){
			if($("#get_under_name_equal_"+ids[0]+"_"+ids[1]).val() == ""){
				$("#get_under_name_equal_"+ids[0]+"_"+ids[1]).val("=") ;

			}
		}else if(ids.length == 1){
			if($("#get_under_name_equal_"+ids[0]).val() == ""){
				$("#get_under_name_equal_"+ids[0]).val("=") ;

			}
		}
	}
	function showMonsterNameEqual(id){
		ids = id.split("_");
		if(ids.length == 3){
			if($("#get_monster_name_equal_"+ids[0]+"_"+ids[1]+"_"+ids[2]).val() == ""){
				$("#get_monster_name_equal_"+ids[0]+"_"+ids[1]+"_"+ids[2]).val("=") ;
			
			}
		}else if(ids.length == 2){
			if($("#get_monster_name_equal_"+ids[0]+"_"+ids[1]).val() == ""){
				$("#get_monster_name_equal_"+ids[0]+"_"+ids[1]).val("=") ;
			
			}
		}else if(ids.length == 1){
			if($("#get_monster_name_equal_"+ids[0]).val() == ""){
				$("#get_monster_name_equal_"+ids[0]).val("=") ;
			
			}
		}
	}
	function showUnderEquation(id){
		monster_or_global = id;
		ids = id.split("_");
		if(ids.lenght == 7){
			if($("#get_under_variable_equal_"+ids[3]+"_"+ids[4]+"_"+ids[5]+"_"+ids[6]).val() == ""){

				$("#get_under_variable_equal_"+ids[3]+"_"+ids[4]+"_"+ids[5]+"_"+ids[6]).val("=") ;

			}
		}else if(ids.length== 6){
			if($("#get_under_variable_equal_"+ids[3]+"_"+ids[4]+"_"+ids[5]).val() == ""){

				$("#get_under_variable_equal_"+ids[3]+"_"+ids[4]+"_"+ids[5]).val("=") ;

			}
		}else if(ids.length == 5){
			if($("#get_under_variable_equal_"+ids[3]+"_"+ids[4]).val() == ""){

				$("#get_under_variable_equal_"+ids[3]+"_"+ids[4]).val("=") ;

			}
		}
		showEquationDet();
	}
	function deleteMonsterVariable(id){
		ids = id.split("_");
		if($("#get_monster_variable_equal_"+ids[3]+"_"+ids[4]+"_"+ids[5]+"_"+ids[6]).val() == "" ){
			$("#"+id).val("");
			
		}
	}
	function changeToEqual(id){
		ids = id.split("_");
			if($("#get_monster_variable_equal_"+ids[3]+"_"+ids[4]+"_"+ids[5]+"_"+ids[6]).val() == "" ){

			$("#get_monster_variable_equal_"+ids[3]+"_"+ids[4]+"_"+ids[5]+"_"+ids[6]).val('='); 
			
		}
	}
	function showMonsterEquation(id){
		monster_or_global = id;
		ids = id.split("_");
		if(ids.lenght == 7){
			if($("#get_monster_variable_equal_"+ids[3]+"_"+ids[4]+"_"+ids[5]+"_"+ids[6]).val() == ""){
				
				$("#get_monster_variable_equal_"+ids[3]+"_"+ids[4]+"_"+ids[5]+"_"+ids[6]).val("=") ;
				
			}
		}else if(ids.length== 6){
			if($("#get_monster_variable_equal_"+ids[3]+"_"+ids[4]+"_"+ids[5]).val() == ""){
				
				$("#get_monster_variable_equal_"+ids[3]+"_"+ids[4]+"_"+ids[5]).val("=") ;
				
			}
		}else if(ids.length == 5){
			if($("#get_monster_variable_equal_"+ids[3]+"_"+ids[4]).val() == ""){
				
				$("#get_monster_variable_equal_"+ids[3]+"_"+ids[4]).val("=") ;
				
			}
		}
		showEquationDet();
	}
	function addMonsterVariableChange(i){
		i++;
		$(".add_button_monster_variable_change").hide();
		var result = '<table><tr><td>変数変更名</td><td><input type="text" id="monster_variable_change_name_'+i+'"></td></tr><tr><td>寿命</td><td><select id="monster_variable_change_life_'+i+'"></select><input type="text" id="monster_variable_change_life_length_'+i+'"></td></tr><tr><td>種別</td><td><select id="monster_variable_change_effect_kind_'+i+'"></select></td></tr><tr><td>元々の値</td><td><select id="monster_variable_change_initial_'+i+'"><option value="1">元々の値</option><option value="0">値</option></select><select id="monster_variable_change_add_'+i+'"><option value="0">加える</option><option value="1">にする</option></select>persist<input type="checkbox" id="persist_'+i+'"><input type="text" id="monster_variable_change_val_'+i+'" onfocus="showMonsterVariableEquation('+i+')"></td></tr><tr><td>minus<input type="checkbox" id="monster_variable_change_minus_'+i+'"</td></tr><tr><input type="button" onclick="addMonsterVariableChange('+i+')" class="add_button_monster_variable_change" value="追加" id="add_button_monster_variable_change_'+i+'"></td></tr>';
		$("#monster_variable_change").append(result);
		$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_phase_and_turn/",
		   'data': "",
		'success': function(data){
			$("#monster_variable_change_life_"+i).html(data);
		}});
		$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_effect_kind/",
   'data': "",
'success': function(data){
		$("#monster_variable_change_effect_kind_"+i).html(data);
		}});
	}
	function addPutRelation(i){
		i++;
		$(".add_button_put_relation").hide();
		var result = 'リレーション名<input type="text" id="relation_name_'+String(i)+'">';
        result+= 'リレーション<input type="text" id="relation_monster_'+String(i)+'">';
        result+= 'リレーションタイプ<input type="text" id="put_relation_kind_'+String(i)+'">';
        result+= '<input type="button" onclick="addPutRelation('+String(i)+')" class="add_button_put_relation" value="追加" id="add_relation_'+String(i)+'" class="add_relation">';
        result+=' <select id="put_relation_to_'+i+'"> <option value="0">リレーション受ける</option> <option value="1">リレーションする</option></select>';
		$("#put_relation").append(result);
		addKindType("put_relation_kind_"+i,'put_relation_kind');
	}
	function putGlobalVariableToEquation(){
		var editor =$("#equation_editor_det").val();
	    var val = $("#equation_editor_global_val").val();
	    val = val.split("_");
	    val = "^"+val[1]+":"+val[2]+"^";
	    editor+=val;
		$("#equation_editor_det").val(editor);
	}
	function putDesignatedToEquation(){
		var editor =$("#equation_editor_det").val();
	    var tmp = "{";
        tmp+=$("#name_editor").val()+":";
        tmp+=$("#val_name_editor").val()+":";
        tmp+=$("#flag_editor").val()+":";
        tmp+=$("#rel_name_editor").val()+":";
        if($("#rel_kind_editor").val() == "0"){
            tmp+=":";
        }else{
            tmp+=$("#rel_kind_editor").val()+":";
        }
        tmp+=$("#rel_to_editor").val()+":";
        tmp+=$("#rel_monster_editor").val()+":";
        tmp+=$("#equation_under").prop("checked")?"1"+":":"0"+":";
        tmp+=$("#monster_editor").val()+":";
        tmp+=$("#monster_effect_kind_get_val").val()+":";
            if($("#i_val2").prop("checked") == true){
                tmp+="1";
            }else{
                tmp+="0";
            }
        tmp+="}";
		editor += tmp;
		$("#equation_editor_det").val(editor);

	}

	function putPlaceToEquation(){
		var editor =$("#equation_editor_det").val();
		var place = $("#equation_editor_place").val();
		if(place == ""){
		    return;
		}
		var tmp = "";
		var cond_html,i;
		place = place.split("_");

		if(place[0] == "field"){
			tmp += "|";
			tmp += place[1]+":";
			tmp += place[2]+":";
			tmp += $("#val_name_for_editor").val()+":";
			tmp += $("#flag_for_editor").val()+":";
			tmp += $("#eternal_flag_for_editor").val()+":";
			tmp += $("#method_for_editor").val()+":";
			cond_html= "";
			for(i=0;$("#cond_for_editor"+String(i)).length && $("#cond_for_editor"+String(i)).val()!="";i++){
			    cond_html+=$("#cond_for_editor"+i).val()+"@"+$("#value_for_editor"+i).val()+"@"+$("#cond_equation_for_editor"+i).val()+"@"+$("#cond_and_or"+i).val()+"^";
			}
			if(cond_html != ""){
			    cond_html = cond_html.substr(0,cond_html.length-1);
			}
			tmp += cond_html+":";
			tmp+= $("#equation_editor_x").val()+":";
			tmp+= $("#equation_editor_y").val();
            tmp+=$("#rel_name_editor").val()+":";
            if($("#rel_kind_editor").val() == "0"){
                tmp+=":";
            }else{
                tmp+=$("#rel_kind_editor").val()+":";
            }
            tmp+=$("#rel_to_editor").val()+":";
            tmp+=$("#rel_monster_editor").val()+":";
			tmp += $("#monster_editor_sum").val()+":";
     if($("#i_val1").prop("checked")== true){
		         tmp += ":1";
     }else {
		         tmp += ":0";
     }
			tmp += "|";
		}else{
			tmp+="&";
			tmp+=place[0]+":";
			tmp+=place[1]+":";
			tmp+=place[2]+":";
			tmp += $("#val_name_for_editor").val()+":";
			cond_html= "";
			for(i=0;$("#cond_for_editor"+String(i)).length && $("#cond_for_editor"+String(i)).val()!="";i++){
			    cond_html+=$("#cond_for_editor"+i).val()+"@"+$("#value_for_editor"+i).val()+"@"+$("#cond_equation_for_editor"+i).val()+"@"+$("#cond_and_or"+i).val()+"^";
			}
			if(cond_html != ""){
			    cond_html = cond_html.substr(0,cond_html.length-1);
			}
			tmp += cond_html+":";
			tmp += $("#method_for_editor").val()+":";
			tmp += $("#flag_for_editor").val()+":";
			tmp += $("#eternal_flag_for_editor").val()+":";
			tmp += $("#monster_editor_sum").val()+":";
     if($("#i_val1").prop("checked")== true){
		         tmp += ":1";
     }else {
		         tmp += ":0";
     }
			tmp += "&";
		}
		editor += tmp;
		$("#equation_editor_det").val(editor);
	}
	function getPlaceForEquation(){
		$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_place_kind/",
		   'data': "",
		'success': function(data){
			$("#equation_editor_place").html(data);
		}});
	}
	function getGlobalValForEquation(){
		$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_variable_kind/",
		   'data': "",
		'success': function(data){
			$("#equation_editor_global_val").html(data);
		}});
	}
	function showEach(){
		$("#monster_effect_each").show();
		$("#monster_effect_each").draggable();
    		$("#monster_effect_each").offset({top:mouse_y,left:mouse_x});
	}

	function showCheckForce(){
		$("#check_force").show();
		$("#check_force").draggable();
		getCheckForceDeckId();
		getCheckForceTiming();
	}
	function getCheckForceTiming(){
	$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_tcg_timing/",
   'data': "",
'success': function(data){
            $("#check_force_ignore_timing").html(data);
	}
	})
	}
	function getCheckForceDeckId(){
	$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_hand_id/",
   'data': "",
'success': function(data){
            $("#check_force_deck_id").html(data);
	}
	})
	}
	function showEquationDet(){
	    if($("#equation_editor").css("display") == "none"){
		    $("#equation_editor").show();
    		$("#equation_editor").draggable();
    		$("#equation_editor").offset({top:mouse_y,left:mouse_x});
    	}
		getGlobalValForEquation();
		getEternalKindForEquation();
		getPlaceForEquation();
	}
	function getMultipleChoice(id){
	    $("#multiple_choice").show();
		$("#multiple_choice").draggable();
		$("#multiple_choice").offset({top:0,left:200});
	    initMultipleChoice();
	}
	function putMultipleChoice(){
	    id = "monster_effect";
	    var json = {};
	    json["monster_effect_wrapper"] =[];
	    json["sentence"] =[];
	    var i;
	    var result_json;
	    for(i=1;$("#multiple_choice_"+i).length != 0;i++){
	        json["monster_effect_wrapper"].push($("#multiple_choice_"+i).val());
	        json["sentence"].push($("#multiple_choice_text_"+i).val());
	    }
	    result_json = JSON.stringify(json);
	    $("#id_"+id).val(result_json);
	}
	function addRelation(id,relation_id){
		id = id.split("_");
		var org = parseInt(id[id.length-1]);
		var result="";
		result="リレーション名<input type=\"text\" id=\"relation_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+id[3]+"\">";
		result+="リレーションモンスター<select id=\"relation_id_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+id[3]+"\"></select>";
		result+="リレーションタイプ<input type=\"text\" id=\"relation_kind_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+id[3]+"\">";
		result+="リレーションvalid<input type=\"text\" id=\"relation_valid_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+id[3]+"\">";
        result+="<select id=\"relation_to_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+id[3]+"\"><option value=\"0\">リレーション受ける</option><option value=\"1\">リレーションする</option></select>"
		result+="<input value=\"追加\" type=\"button\" id=\"add_relation_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+String(parseInt(id[3]+1))+"\" onclick=\"addRelation('"+id[0]+"_"+id[1]+"_"+id[2]+"_"+String(parseInt(id[3]+1))+"')\">";
		if(org == 0){
		    $("#relation_add_"+id[0]+"_"+id[1]+"_"+id[2]+"_0").hide();
		    $("#relation_add_"+id[0]+"_"+id[1]+"_"+id[2]+"_0").after(result);
		}else{
			$("#add_relation_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+String(parseInt(id[3]))).after(result);
		}
		addKindType("relation_kind_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+id[3],'relation_kind');
		addKindType("relation_valid_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+id[3],'relation_valid');
		addMonster("relation_id_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+id[3],relation_id);
	}
	function narrowDown(i){
	    var narrow_down = $("#multiple_choice_narrow_down_"+i).val();
	    $.ajax({
        'type': "POST",
   'url': "/tcgcreator/get_monster_effect_wrapper_specify/",
   'data': "monster_effect_val=0&name="+narrow_down,
        'success': function(data){
            $('#multiple_choice_'+(i)).html(data);
        }

        });
	}
	function initMultipleChoice(){
	    var narrow_down = "";
	    $.ajax({
        'type': "POST",
   'url': "/tcgcreator/get_monster_effect_wrapper_specify/",
   'data': "monster_effect_val=0&name="+narrow_down,
        'success': function(data){
            $('#multiple_choice_'+(1)).html(data);
        }

        });
	}
	function addMultipleChoice(){
	    for(var i=1;$("#multiple_choice_"+i).length != 0;i++){
	    }
	    var narrow_down = "";
	    $.ajax({
        'type': "POST",
   'url': "/tcgcreator/get_monster_effect_wrapper_specify/",
   'data': "monster_effect_val=0&name="+narrow_down,
        'success': function(data){
            var html = '<div id="multiple_choice_div_'+i+'"><select id="multiple_choice_'+i+'">'+data+'</select><br>sentence<input type="text" id="multiple_choice_text_'+i+'"><br><input type="button" value="絞り込み" onclick="narrowDown(\''+i+'\')"><input id="multiple_choice_narrow_down_'+i+'" type="text" value=""></div>';
            $('#multiple_choice_div_'+(i-1)).after(html);
        }

        });
	}
	function addMonster(id,id2){
	$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_monster/",
   'data': "delete_flag=0&num=0",
'success': function(data){
			$("#"+id).html(data);
			if(id2 != undefined){
			    $("#"+id).val(id2);
			}
	}
	})
        }
	function addKindType(id,id2){
	$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_monster_kind/",
   'data': "delete_flag=0&num=0&id="+id+"&id2="+id2,
'success': function(data){
			$("#"+id).after(data);
	}
	})

	}
	function addCustomMonsterCondition(id){
		id = id.split("_");
		var org = id[id.length-1];
		var result="";
		if(org == 0){
		result="カスタム変数名<input type=\"text\" id=\"custom_monster_variable_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+id[3]+"\">";
		}
		result+="値<input type=\"text\" onfocus=\"showMonsterEquation('custom_get_monster_variable_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+id[3]+"')\" id=\"custom_get_monster_variable_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+id[3]+"\">";
		result+='<select id="custom_get_monster_variable_equal_'+id[0]+'_'+id[1]+'_'+id[2]+'_'+id[3]+'"><option value="">全て</option><option value="=" selected>=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select>';
		result+='<select id="custom_monster_variable_and_or_'+id[0]+"_"+id[1]+"_"+id[2]+'_'+id[3]+'" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select>';
		if(org == 0){
			result+='<input type="button" value="カスタム追加" id="custom_add_'+id[0]+"_"+id[1]+'_'+String(parseInt(id[2])+1)+'_0" class="custom_add" onclick="addCustomMonsterCondition(\''+id[0]+"_"+id[1]+'_'+String(parseInt(id[2])+1)+'_0\')">';
			$("#custom_add_"+id[0]+"_"+id[1]+"_"+id[2]+"_0").after(result);
			$("#custom_add_"+id[0]+"_"+id[1]+"_"+id[2]+"_0").remove();
		}else{
			$("#custom_monster_variable_and_or_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+String(parseInt(id[3])-1)).after(result);
		}
	}
	function addRelationCondition(id){
		i++;
		$(".add_button_relation_condition").hide();
		var result = 'リレーション名<input type="text" id="relation_name_'+String(i)+'">';
        result+= 'リレーション<input type="text" id="relation_monster_'+String(i)+'">';
        result+= 'リレーションタイプ<input type="text" id="relation_condition_kind_'+String(i)+'">';
        result+= '<input type="button" onclick="addRelationCondition('+String(i)+')" class="add_button_relation_condition" value="追加" id="add_relation_condition_'+String(i)+'" class="add_relation">';
        result+=' <select id="relation_condition_to_'+i+'"> <option value="0">リレーション受ける</option> <option value="1">リレーションする</option><option value="-1">両方</select>';
		$("#relation_condition").append(result);
		addKindType("relation_condition_kind_"+i,'relation_kind');
	}
	function addMonsterEffectKindEquation(){
        if($("#monster_effect_kind_get_val").val() == ""){
            $("#monster_effect_kind_get_val").val($("#monster_effect_kind_select").val());
        }else{
            $("#monster_effect_kind_get_val").val($("#monster_effect_kind_get_val").val()+"_"+$("#monster_effect_kind_select").val());
        }
	}
	/*
	function addMonsterEquation2(id,variable_id)
		var id = id.split("_");
		var org = id[id.length-1];
		id[id.length-1] = String(parseInt(id[id.length-1])+1);
		result = "";
        result+='<select id="monster_variable_init'+id[0]+"_"+id[1]+'_0" > <option value="0">現在の値</option><option value="1">元々の値</option> <option value="2">元々の元々の値</option> </select><input id="monster_variable_add_'+str(monster_variable.id)+'_0" type="button" value="追加"  onclick="addMonsterEquation(\''+str(i)+'_'+str(monster_variable.id)+'_0\')"><br>'

        kinds = monster_variable.monster_variable_kind_id.monster_variable_sentence
        kinds_org = kinds
        kinds = kinds.split("|")
        k=1
        for kind in kinds:
            result+="<option value=\""+str(k)+"\">"+kind+"</option>"
            k+=1
        result+="</select>"
        result+='<select id="monster_variable_and_or_'+str(monster_variable.id)+'_0" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="monster_variable_add'+"_"+str(monster_variable.id)+'_0" type="button" value="追加"  onclick="addMonsterEquation2(\''+str(i)+'_'+str(monster_variable.id)+'_0\',\''+kinds_org+'\')"><br>'
        */
	function addUnderEquation(id){
		var id = id.split("_");
		var org = id[id.length-1];
		id[id.length-1] = String(parseInt(id[id.length-1])+1);
		var result="";
		if(id.length==4){
		result+="<br><input type=\"text\" onfocus=\"showMonsterEquation('get_under_variable_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+id[3]+"')\" id=\"get_under_variable_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+id[3]+"\">"
		result+='<select id="get_under_variable_equal_'+id[0]+'_'+id[1]+'_'+id[2]+"_"+id[3]+'"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select>'
		result+='<select id="under_variable_and_or_'+id[0]+"_"+id[1]+"_"+id[2]+"_"+id[3]+'" onchange="addMonsterEquation(\''+id[0]+'_'+id[1]+'_'+id[2]+"_"+id[3]+'\')"> <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="under_variable_add_'+id[0]+"_"+id[1]+'_'+id[2]+'_'+id[3]+'" type="button" value="追加" onclick="addMonsterEquation(\''+id[0]+'_'+id[1]+'_'+id[2]+'_'+id[3]+'\')">'

		$("#under_variable_add_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+org).after(result);
		$("#under_variable_add_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+org).hide();
		}else if (id.length==3){
		result+="<br><input type=\"text\" onfocus=\"showMonsterEquation('get_under_variable_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+"')\" id=\"get_under_variable_"+id[0]+"_"+id[1]+"_"+id[2]+"\">"
		result+='<select id="get_under_variable_equal_'+id[0]+'_'+id[1]+'_'+id[2]+'"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select>'
		result+='<select id="under_variable_and_or_'+id[0]+"_"+id[1]+"_"+id[2]+'" onchange="addMonsterEquation(\''+id[0]+'_'+id[1]+'_'+id[2]+'\')"> <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="under_variable_add_'+id[0]+"_"+id[1]+'_'+id[2]+'" type="button" value="追加" onclick="addMonsterEquation(\''+id[0]+'_'+id[1]+'_'+id[2]+'\')">'

		$("#under_variable_add_"+id[0]+"_"+id[1]+"_"+org).after(result);
		$("#under_variable_add_"+id[0]+"_"+id[1]+"_"+org).hide();
		}else if (id.length==2){
		result+="<br><input type=\"text\" onfocus=\"showMonsterEquation('get_under_variable_"+id[0]+"_"+id[1]+"')\" id=\"get_under_variable_"+id[0]+"_"+id[1]+"\">"
		result+='<select id="get_under_variable_equal_'+id[0]+'_'+id[1]+'"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select>'
		result+='<select id="under_variable_and_or_'+id[0]+"_"+id[1]+'" onchange="addMonsterEquation(\''+id[0]+'_'+id[1]+'\')"> <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="under_variable_add_'+id[0]+"_"+id[1]+'" type="button" value="追加" onclick="addMonsterEquation(\''+id[0]+'_'+id[1]+'\')">'

		$("#under_variable_add_"+id[0]+"_"+org).after(result);
		$("#under_variable_add_"+id[0]+"_"+org).hide();
		}
	}
	function addUnderEquation(id){
		var id = id.split("_");
		var org = id[id.length-1];
		id[id.length-1] = String(parseInt(id[id.length-1])+1);
		var result="";
		if(id.length==4){
		result+="<br><input type=\"text\" onfocus=\"showMonsterEquation('get_under_variable_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+id[3]+"')\" id=\"get_under_variable_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+id[3]+"\">"
		result+='<select id="get_under_variable_equal_'+id[0]+'_'+id[1]+'_'+id[2]+"_"+id[3]+'"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select>'
		result+='<select id="under_variable_and_or_'+id[0]+"_"+id[1]+"_"+id[2]+"_"+id[3]+'" onchange="addMonsterEquation(\''+id[0]+'_'+id[1]+'_'+id[2]+"_"+id[3]+'\')"> <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="under_variable_add_'+id[0]+"_"+id[1]+'_'+id[2]+'_'+id[3]+'" type="button" value="追加" onclick="addMonsterEquation(\''+id[0]+'_'+id[1]+'_'+id[2]+'_'+id[3]+'\')">'

		$("#under_variable_add_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+org).after(result);
		$("#under_variable_add_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+org).hide();
		}else if (id.length==3){
		result+="<br><input type=\"text\" onfocus=\"showMonsterEquation('get_under_variable_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+"')\" id=\"get_under_variable_"+id[0]+"_"+id[1]+"_"+id[2]+"\">"
		result+='<select id="get_under_variable_equal_'+id[0]+'_'+id[1]+'_'+id[2]+'"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select>'
		result+='<select id="under_variable_and_or_'+id[0]+"_"+id[1]+"_"+id[2]+'" onchange="addMonsterEquation(\''+id[0]+'_'+id[1]+'_'+id[2]+'\')"> <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="under_variable_add_'+id[0]+"_"+id[1]+'_'+id[2]+'" type="button" value="追加" onclick="addMonsterEquation(\''+id[0]+'_'+id[1]+'_'+id[2]+'\')">'

		$("#under_variable_add_"+id[0]+"_"+id[1]+"_"+org).after(result);
		$("#under_variable_add_"+id[0]+"_"+id[1]+"_"+org).hide();
		}else if (id.length==2){
		result+="<br><input type=\"text\" onfocus=\"showMonsterEquation('get_under_variable_"+id[0]+"_"+id[1]+"')\" id=\"get_under_variable_"+id[0]+"_"+id[1]+"\">"
		result+='<select id="get_under_variable_equal_'+id[0]+'_'+id[1]+'"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select>'
		result+='<select id="under_variable_and_or_'+id[0]+"_"+id[1]+'" onchange="addMonsterEquation(\''+id[0]+'_'+id[1]+'\')"> <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="under_variable_add_'+id[0]+"_"+id[1]+'" type="button" value="追加" onclick="addMonsterEquation(\''+id[0]+'_'+id[1]+'\')">'

		$("#under_variable_add_"+id[0]+"_"+org).after(result);
		$("#under_variable_add_"+id[0]+"_"+org).hide();
		}
	}
	function addMonsterEquation(id){
		var id = id.split("_");
		var org = id[id.length-1];
		id[id.length-1] = String(parseInt(id[id.length-1])+1);
		var result="";
		if(id.length==4){
		result+="<br><input type=\"text\" onfocus=\"showMonsterEquation('get_monster_variable_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+id[3]+"')\" id=\"get_monster_variable_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+id[3]+"\">"
		result+='<select id="get_monster_variable_equal_'+id[0]+'_'+id[1]+'_'+id[2]+"_"+id[3]+'"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select>'
		result+='<select id="monster_variable_and_or_'+id[0]+"_"+id[1]+"_"+id[2]+"_"+id[3]+'" onchange="addMonsterEquation(\''+id[0]+'_'+id[1]+'_'+id[2]+"_"+id[3]+'\')"> <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="monster_variable_add_'+id[0]+"_"+id[1]+'_'+id[2]+'_'+id[3]+'" type="button" value="追加" onclick="addMonsterEquation(\''+id[0]+'_'+id[1]+'_'+id[2]+'_'+id[3]+'\')">'
		
		$("#monster_variable_add_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+org).after(result);
		$("#monster_variable_add_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+org).hide();
		}else if (id.length==3){
		result+="<br><input type=\"text\" onfocus=\"showMonsterEquation('get_monster_variable_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+"')\" id=\"get_monster_variable_"+id[0]+"_"+id[1]+"_"+id[2]+"\">"
		result+='<select id="get_monster_variable_equal_'+id[0]+'_'+id[1]+'_'+id[2]+'"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select>'
		result+='<select id="monster_variable_and_or_'+id[0]+"_"+id[1]+"_"+id[2]+'" onchange="addMonsterEquation(\''+id[0]+'_'+id[1]+'_'+id[2]+'\')"> <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="monster_variable_add_'+id[0]+"_"+id[1]+'_'+id[2]+'" type="button" value="追加" onclick="addMonsterEquation(\''+id[0]+'_'+id[1]+'_'+id[2]+'\')">'
		
		$("#monster_variable_add_"+id[0]+"_"+id[1]+"_"+org).after(result);
		$("#monster_variable_add_"+id[0]+"_"+id[1]+"_"+org).hide();
		}else if (id.length==2){
		result+="<br><input type=\"text\" onfocus=\"showMonsterEquation('get_monster_variable_"+id[0]+"_"+id[1]+"')\" id=\"get_monster_variable_"+id[0]+"_"+id[1]+"\">"
		result+='<select id="get_monster_variable_equal_'+id[0]+'_'+id[1]+'"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select>'
		result+='<select id="monster_variable_and_or_'+id[0]+"_"+id[1]+'" onchange="addMonsterEquation(\''+id[0]+'_'+id[1]+'\')"> <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="monster_variable_add_'+id[0]+"_"+id[1]+'" type="button" value="追加" onclick="addMonsterEquation(\''+id[0]+'_'+id[1]+'\')">'
		
		$("#monster_variable_add_"+id[0]+"_"+org).after(result);
		$("#monster_variable_add_"+id[0]+"_"+org).hide();
		}
	}
	function addUnderEquation2(id,kinds_org){
		kinds = kinds_org.split("|")
		id = id.split("_");
		org = id[id.length-1];
		id[id.length-1] = String(parseInt(id[id.length-1])+1);
		if(id.length == 4){
			var result="";
			result+="<select id=\"get_under_variable_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+id[3]+"\">";
			result+="<option value=\"0\">全て</option>"
			for(var i=1;i<=kinds.length;i++){
					result+="<option value=\""+i+"\">"+kinds[i-1]+"</option>"
			}
			result+="</select>";
			result+='<input id="under_variable_add_'+id[0]+"_"+id[1]+'_'+id[2]+'_'+id[3]+'" value="追加" type="button" onclick="addUnderEquation2(\''+id[0]+'_'+id[1]+'_'+id[2]+'_'+id[3]+'\',\''+kinds_org+'\')"><br>'
            result+='<select id="under_variable_and_or_'+id[0]+"_"+id[1]+"_"+id[2]+'_'+id[3]+'" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select>'
            result+='<select id="under_variable_init'+id[0]+id[1]+"_"+id[2]+'_'+id[3]+'" > <option value="0">現在の値</option><option value="1">元々の値</option> <option value="2">元々の元々の値</option> </select>'
			$("#under_variable_add_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+org).after(result);
			$("#under_variable_add_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+org).hide();
		}else if(id.length == 3){
			var result="";
			result+="<select id=\"get_under_variable"+id[0]+"_"+id[1]+"_"+id[2]+"\">";
			result+="<option value=\"0\">全て</option>"
			for(var i=1;i<=kinds.length;i++){
					result+="<option value=\""+i+"\">"+kinds[i-1]+"</option>"
			}
			result+="</select>";
			result+='<input id="under_variable_add_'+id[0]+"_"+id[1]+'_'+id[2]+'" value="追加" type="button" onclick="addUnderEquation2(\''+id[0]+'_'+id[1]+'_'+id[2]+'\',\''+kinds_org+'\')"><br>'
            result+='<select id="under_variable_init'+id[0]+id[1]+"_"+id[2]+'" > <option value="0">現在の値</option><option value="1">元々の値</option> <option value="2">元々の元々の値</option> </select>'
			$("#under_variable_add_"+id[0]+"_"+id[1]+"_"+org).hide();
		}else if(id.length == 2){
			var result="";
			result+="<select id=\"get_under_variable"+id[0]+"_"+id[1]+"\">";
			result+="<option value=\"0\">全て</option>"
			for(var i=1;i<=kinds.length;i++){
					result+="<option value=\""+i+"\">"+kinds[i-1]+"</option>"
			}
			result+="</select>";
			result+='<input id="under_variable_add_'+id[0]+'_'+id[1]+'" value="追加" type="button" onclick="addUnderEquation2(\''+id[0]+'_'+id[2]+'\',\''+kinds_org+'\')"><br>'
            result+='<select id="under_variable_init'+id[0]+id[1]+'" > <option value="0">現在の値</option><option value="1">元々の値</option> <option value="2">元々の元々の値</option> </select>'
			$("#under_variable_add_"+id[0]+"_"+org).after(result);
			$("#under_variable_add_"+id[0]+"_"+org).hide();
		}
	}
	function addMonsterEquation2(id,kinds_org){
		kinds = kinds_org.split("|")
		id = id.split("_");
		org = id[id.length-1];
		id[id.length-1] = String(parseInt(id[id.length-1])+1);
		if(id.length == 4){
			var result="";
			result+="<select id=\"get_monster_variable_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+id[3]+"\">";
			result+="<option value=\"0\">全て</option>"
			for(var i=1;i<=kinds.length;i++){
					result+="<option value=\""+i+"\">"+kinds[i-1]+"</option>"
			}
			result+="</select>";
			result+='<input id="monster_variable_add_'+id[0]+"_"+id[1]+'_'+id[2]+'_'+id[3]+'" value="追加" type="button" onclick="addMonsterEquation2(\''+id[0]+'_'+id[1]+'_'+id[2]+'_'+id[3]+'\',\''+kinds_org+'\')"><br>'
            result+='<select id="monster_variable_and_or_'+id[0]+"_"+id[1]+"_"+id[2]+'_'+id[3]+'" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select>'
            result+='<select id="monster_variable_init'+id[0]+id[1]+"_"+id[2]+'_'+id[3]+'" > <option value="0">現在の値</option><option value="1">元々の値</option> <option value="2">元々の元々の値</option> </select>'
			$("#monster_variable_add_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+org).after(result);
			$("#monster_variable_add_"+id[0]+"_"+id[1]+"_"+id[2]+"_"+org).hide();
		}else if(id.length == 3){
			var result="";
			result+="<select id=\"get_monster_variable"+id[0]+"_"+id[1]+"_"+id[2]+"\">";
			result+="<option value=\"0\">全て</option>"
			for(var i=1;i<=kinds.length;i++){
					result+="<option value=\""+i+"\">"+kinds[i-1]+"</option>"
			}
			result+="</select>";
			result+='<input id="monster_variable_add_'+id[0]+"_"+id[1]+'_'+id[2]+'" value="追加" type="button" onclick="addMonsterEquation2(\''+id[0]+'_'+id[1]+'_'+id[2]+'\',\''+kinds_org+'\')"><br>'
            result+='<select id="monster_variable_init'+id[0]+id[1]+"_"+id[2]+'" > <option value="0">現在の値</option><option value="1">元々の値</option> <option value="2">元々の元々の値</option> </select>'
			$("#monster_variable_add_"+id[0]+"_"+id[1]+"_"+org).after(result);
			$("#monster_variable_add_"+id[0]+"_"+id[1]+"_"+org).hide();
		}else if(id.length == 2){
			var result="";
			result+="<select id=\"get_monster_variable"+id[0]+"_"+id[1]+"\">";
			result+="<option value=\"0\">全て</option>"
			for(var i=1;i<=kinds.length;i++){
					result+="<option value=\""+i+"\">"+kinds[i-1]+"</option>"
			}
			result+="</select>";
			result+='<input id="monster_variable_add_'+id[0]+'_'+id[1]+'" value="追加" type="button" onclick="addMonsterEquation2(\''+id[0]+'_'+id[2]+'\',\''+kinds_org+'\')"><br>'
            result+='<select id="monster_variable_init'+id[0]+id[1]+'" > <option value="0">現在の値</option><option value="1">元々の値</option> <option value="2">元々の元々の値</option> </select>'
			$("#monster_variable_add_"+id[0]+"_"+org).after(result);
			$("#monster_variable_add_"+id[0]+"_"+org).hide();
		}
	}
	function addUnderName(id){
		id = id.split("_");
		org = id[id.length-1];
		id[id.length-1] = String(parseInt(id[id.length-1])+1);
		var result="";
		if(id.length==3){
	result+="<input type=\"text\" onfocus=\"showUnderNameEqual('"+id[0]+"_"+id[1]+"_"+id[2]+"')\" id=\"under_name_"+id[0]+'_'+id[1]+"_"+id[2]+"\">";
	result+='<select id="get_under_name_equal_'+id[0]+'_'+id[1]+'_'+id[2]+'"><option value="">全て</option><option value="=">=</option><option value="like">含む</option></select><select id="under_name_and_or_'+id[0]+'_'+id[1]+'_'+id[2]+'" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="under_name_add_'+id[0]+'_'+id[1]+'_'+id[2]+'" type="button" value="追加"  onclick="addUnderName(\''+id[0]+"_"+id[1]+'_'+id[2]+'\')"><br>';

		$("#under_name_add_"+id[0]+"_"+id[1]+"_"+org).after(result);
		$("#under_name_add_"+id[0]+"_"+id[1]+"_"+org).hide();
		}else if(id.length==2){
	result+="<input type=\"text\" onfocus=\"showUnderNameEqual('"+id[0]+"_"+id[1]+"')\" id=\"under_name_"+id[0]+'_'+id[1]+"\">";
	result+='<select id="get_under_name_equal_'+id[0]+'_'+id[1]+'"><option value="">全て</option><option value="=">=</option><option value="like">含む</option></select><select id="under_name_and_or_'+id[0]+'_'+id[1]+'" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="under_name_add_'+id[0]+'_'+id[1]+'" type="button" value="追加"  onclick="addUnderName(\''+id[0]+"_"+id[1]+'\')"><br>';

		$("#under_name_add_"+id[0]+"_"+org).after(result);
		$("#under_name_add_"+id[0]+"_"+org).hide();
		}else if(id.length==1){
	result+="<input type=\"text\" onfocus=\"showUnderNameEqual('"+id[0]+"')\" id=\"under_name_"+id[0]+"\">";
	result+='<select id="get_under_name_equal_'+id[0]+'"><option value="">全て</option><option value="=">=</option><option value="like">含む</option></select><select id="under_name_and_or_'+id[0]+'" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="under_name_add_'+id[0]+'" type="button" value="追加"  onclick="addUnderName(\''+id[0]+'\')"><br>';

		$("#under_name_add_"+org).after(result);
		$("#under_name_add_"+org).hide();
		}
	}
	function addMonsterName(id){
		id = id.split("_");
		org = id[id.length-1];
		id[id.length-1] = String(parseInt(id[id.length-1])+1);
		var result="";
		if(id.length==3){
	result+="<input type=\"text\" onfocus=\"showMonsterNameEqual('"+id[0]+"_"+id[1]+"_"+id[2]+"')\" id=\"monster_name_"+id[0]+'_'+id[1]+"_"+id[2]+"\">";
	result+='<select id="get_monster_name_equal_'+id[0]+'_'+id[1]+'_'+id[2]+'"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value="like">含む</option>></select><select id="monster_name_and_or_'+id[0]+'_'+id[1]+'_'+id[2]+'" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="monster_name_add_'+id[0]+'_'+id[1]+'_'+id[2]+'" type="button" value="追加"  onclick="addMonsterName(\''+id[0]+"_"+id[1]+'_'+id[2]+'\')"><br>';
		
		$("#monster_name_add_"+id[0]+"_"+id[1]+"_"+org).after(result);
		$("#monster_name_add_"+id[0]+"_"+id[1]+"_"+org).hide();
		}else if(id.length==2){
	result+="<input type=\"text\" onfocus=\"showMonsterNameEqual('"+id[0]+"_"+id[1]+"')\" id=\"monster_name_"+id[0]+'_'+id[1]+"\">";
	result+='<select id="get_monster_name_equal_'+id[0]+'_'+id[1]+'"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value="like">含む</option></select><select id="monster_name_and_or_'+id[0]+'_'+id[1]+'" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="monster_name_add_'+id[0]+'_'+id[1]+'" type="button" value="追加"  onclick="addMonsterName(\''+id[0]+"_"+id[1]+'\')"><br>';
		
		$("#monster_name_add_"+id[0]+"_"+org).after(result);
		$("#monster_name_add_"+id[0]+"_"+org).hide();
		}else if(id.length==1){
	result+="<input type=\"text\" onfocus=\"showMonsterNameEqual('"+id[0]+"')\" id=\"monster_name_"+id[0]+"\">";
	result+='<select id="get_monster_name_equal_'+id[0]+'"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value="like">含む</option></select><select id="monster_name_and_or_'+id[0]+'" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="monster_name_add_'+id[0]+'" type="button" value="追加"  onclick="addMonsterName(\''+id[0]+'\')"><br>';
		
		$("#monster_name_add_"+org).after(result);
		$("#monster_name_add_"+org).hide();
		}
	}
	function showChainMaxEquation(){
		monster_or_global = "chain_variable_max";
		showEquationDet();
	}
	function showChainMinEquation(){
		monster_or_global = "chain_variable_min";
		showEquationDet();
	}
	function showMaxEquationTo(){
		monster_or_global = "max_equation_number_to";
		showEquationDet();
	}
	function showMinEquationTo(){
		monster_or_global = "min_equation_number_to";
		showEquationDet();
	}
	function showMaxEquation(num){
		monster_or_global = "max_equation_number_"+num;
		showEquationDet();
	}
	function showMinEquation(num){
		monster_or_global = "min_equation_number_"+num;
		showEquationDet();
	}
	function showUnderMinEquation(num){
		monster_or_global = "under_min_equation_number_"+num;
		showEquationDet();
	}
	function showUnderMaxEquation(num){
		monster_or_global = "under_max_equation_number_"+num;
		showEquationDet();
	}
	function showVariableEquation(){
		monster_or_global = "variable_change_val";
		showEquationDet();
	}
	function showMonsterVariableEquation(i){
		monster_or_global = "monster_variable_change_val"+i;
		showEquationDet();
	}
	function showFlagEquation(){
		monster_or_global = "flag_change_val";
		showEquationDet();
	}
	function putEquation(){

	var equation = $("#equation_editor_det").val();
	equation = equation.split("");
	
	var i;
	var j;
	var c;
	var index;
	var stack = [];
	var result = [];
	var workstack = [];
        for(i = 0;i<equation.length;i++){
		token = equation[i];
           	 switch (token) {
               	 case '+':
               	 case '-':
                 	while (stack.length!=0) {
                        	c = stack[stack.length-1];
	                        if (c == '*' || c == '/') {
	                            result.push(stack.pop());
	                        } else {
	                            break;
	                        }
	                 }
                   	 stack.push(token);
                   	 break;
              	 case '*':
               	 case '/':
               	 case '(':
                    stack.push(token);
                    break;
                case ')':
                    index = stack.indexOf('(');

			workstack = [];
                    for (j = 0; j <= index; i++) {
                         c = stack.pop();
                        if (c != '(') {
                            workStack.push(c);
                        }
                    }

                    while (workStack.length != 0) {
                        result.push(workStack.pop());
                    }
                    break;
		case '{':
			variable = "";
			for(;equation[i]!="}";i++){
				variable += equation[i];
			}
			variable+="}";
			result.push(variable);
			break;
		case '^':
			variable = "^";
			i++;
			for(;equation[i]!="^";i++){
				variable += equation[i];
			}
			variable+="^";
			result.push(variable);
			break;
		case '[':
			variable = "";
			for(;equation[i]!="]";i++){
				variable += equation[i];
			}
			variable+="]";
			result.push(variable);
			break;
		case '|':
			variable = "|";
			i++;
			for(;equation[i]!="|";i++){
				variable += equation[i];
			}
			variable+="|";
			console.log(variable);
			result.push(variable);
			break;
		case '&':
			variable = "&";
			i++;
			for(;equation[i]!="&";i++){
				variable += equation[i];
			}
			variable+="&";
			result.push(variable);
			break;
		case 't':
			variable = "t";
			i++;
			for(;equation[i]!="t";i++){
				variable += equation[i];
			}
			variable+="t";
			result.push(variable);
			break;
                default:
                    // 数値の場合
                    result.push(token);
                    break;
            }
        }

        while (stack.length != 0) {
            result.push(stack.pop());
        }
	$("#"+monster_or_global).val(result.join("$"));
    }
	function showIfEditorPlaceIsField(){
		var tmp = $("#equation_editor_place").val();
		tmp = tmp.split("_");
		if(tmp[0] == "field"){
			$("#editor_place_is_designated").show();
		}else{
			$("#editor_place_is_designated").hide();
		}
	}
	function showXandYForEditorPlace(){
		var tmp = $("#editor_place_is_designated").val();
		if(tmp == "1"){
			$("#equation_editor_x").show();
			$("#equation_editor_y").show();
		}else{
			$("#equation_editor_x").hide();
			$("#equation_editor_y").hide();
		}
	}
	function getShuffle(id){
            global_id2 = id;
		$("#shuffle").show();
		$("#shuffle").draggable();
		$("#shuffle").offset({top:0,left:200});
		$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_place_kind/",
		   'data': "",
			'success': function(data){
				$("#monster_effect_shuffle_place").html(data);
			}
		});
	}
	function putShuffle(){
            id = global_id2;
		var val= $("#"+id).val();
		var tmp = $("#monster_effect_shuffle_place").val();
		var val2;
		if(val == ""){
			val2=[];
		}else{
			val2= JSON.parse(val);
		}
		json={};
		json["place"] = {};
		json["place"][0] = tmp;
		val2.push(json);
		val = JSON.stringify(val2);
		$("#"+id).val(val);
	}
    function CopyEffect(){
		$("#copy_effect").show();
		$("#copy_effect").draggable();
		$("#copy_effect").offset({top:0,left:200});
    }
    function getSelectTrigger(num,data2){
		$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_trigger_with_monster/",
		   'data': "",
			'success': function(data){
				$("#triggers_"+num).html(data);
                                if(data2 != undefined){
                                $("#triggers_"+num).val(data2["trigger"]);
                                }
			}
		});
		$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_monster_effect_wrapper/",
		   'data': "",
			'success': function(data){
				$("#next_effect_"+num).html(data);
                                if(data2 != undefined){
                        $("#next_effect_"+num).val(data2["next_effect"]);
                                }
			}
		});
		$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_pac_wrapper/",
		   'data': "",
			'success': function(data){
				$("#next_pac_"+num).html(data);
                                if(data2 != undefined){
                                $("#next_pac_"+num).val(data2["next_pac"]);
                                }
			}
		});
    }
	function getRaiseTrigger(){
		$("#raise_trigger").show();
		$("#raise_trigger").draggable();
		$("#raise_trigger").offset({top:0,left:200});
		$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_trigger/",
		   'data': "",
			'success': function(data){
				$("#monster_effect_raise_trigger").html(data);
			}
		});
	}
	function putCopyEffect(id){
	    json={};
	    json["copy_monster"] =$("#copy_effect_card").val();
	    json["copy_effect_cost"] =$("#copy_effect_cost").prop("checked")? 2 : 1;
	    json["copy_kind"] =$("#copy_kind").val();
	    json["copy2"] =($("#copy2").prop("checked") == true);
	    json["force"] =($("#force_effect").prop("checked") == true);
		val = JSON.stringify(json);
		$("#id_"+id).val(val);
	}
	function putEach(id){
	    var json;
		json={};
		json["each"] = $("#each").val();
		json["val"] = $("#each_val").val();
		json["max"] = $("#each_max").val();
		json["del"] = $("#each_del").val();
		val = JSON.stringify(json);
		$("#id_"+id).val(val);
	}
	function putRaiseTrigger(id){
		var val= $("#"+id).val();
		var tmp = $("#monster_effect_raise_trigger").val();
		var val2;
		if(val == ""){
			val2=[];
		}else{
			val2= JSON.parse(val);
		}
		json={};
		json["trigger"] = {};
		json["trigger"][0] = tmp;
		val2.push(json);
		val = JSON.stringify(val2);
		$("#"+id).val(val);
	}
    function showMonsterVariable(id){
        $(".show_monster_variable_"+id).hide();
        $(".hide_monster_variable_"+id).show();
        $(".monster_variable_box"+id).show();
        }
    function hideMonsterVariable(id){
        $(".show_monster_variable_"+id).show();
        $(".hide_monster_variable_"+id).hide();
        $(".monster_variable_box"+id).hide();
        }
    function showUnderVariable(id){
        $(".show_under_variable_"+id).hide();
        $(".hide_under_variable_"+id).show();
        $(".under_variable_box"+id).show();
        }
    function hideUnderVariable(id){
        $(".show_under_variable_"+id).show();
        $(".hide_under_variable_"+id).hide();
        $(".under_variable_box"+id).hide();
        }
    function showCardExist(){
        $(".show_card_exist").hide();
        $(".hide_card_exist").show();
        $(".card_exist_box").show();
        }
    function hideCardExist(){
        $(".show_card_exist").show();
        $(".hide_card_exist").hide();
        $(".card_exist_box").hide();
        }
    function showMultipleTimes(){
        $(".show_multiple_times").hide();
        $(".hide_multiple_times").show();
        $(".multiple_times_box").show();
        }
    function hideMultipleTimes(){
        $(".show_multiple_times").show();
        $(".hide_multiple_times").hide();
        $(".multiple_times_box").hide();
        }
    function showMultipleEffectKind(){
        $(".show_multiple_effect_kind").hide();
        $(".hide_multiple_effect_kind").show();
        $(".multiple_effect_kind_box").show();
        }

    function hideMultipleEffectKind(){
        $(".show_multiple_effect_kind").show();
        $(".hide_multiple_effect_kind").hide();
        $(".multiple_effect_kind_box").hide();
        }
    function showFieldXandY(){
        $(".show_field_x_and_y").hide();
        $(".hide_field_x_and_y").show();
        $(".field_x_and_y").show();
        }
    function hideFieldXandY(){
        $(".show_field_x_and_y").show();
        $(".hide_field_x_and_y").hide();
        $(".field_x_and_y").hide();
        }
    function showTo(){
        $(".show_to").hide();
        $(".hide_to").show();
        $(".to").show();
        }
    function hidePutFlag(){
        $(".show_to").show();
        $(".hide_to").hide();
        $(".to").hide();
        }
    function showCopyMonster(){
        $(".show_copy_monster_flag").hide();
        $(".hide_copy_monster_flag").show();
        $("#copy_monster").show();
        }
    function hideCopyMonster(){
        $(".show_copy_monster_flag").show();
        $(".hide_copy_monster_flag").hide();
        $("#copy_monster").hide();
        }
    function showPutFlag(){
        $(".show_put_flag").hide();
        $(".hide_put_flag").show();
        $("#monster_variable_change").show();
        }
    function hidePutFlag(){
        $(".show_put_flag").show();
        $(".hide_put_flag").hide();
        $("#monster_variable_change").hide();
        }
    function showAsMonster(){
        $(".show_as_monster").hide();
        $(".hide_as_monster").show();
        $(".as_monster").show();
        }
    function hideAsMonster(){
        $(".show_as_monster").show();
        $(".hide_as_monster").hide();
        $(".as_monster").hide();
        }
    function showUnderEquation(){
        $(".show_under_equation").hide();
        $(".hide_under_equation").show();
        $(".under_equation").show();
        }
    function hideUnderEquation(){
        $(".show_under_equation").show();
        $(".hide_under_equation").hide();
        $(".under_equation").hide();
        }
    function showEquation(){
        $(".show_equation").hide();
        $(".hide_equation").show();
        $(".monster_equation").show();
        }
    function hideEquation(){
        $(".show_equation").show();
        $(".hide_equation").hide();
        $(".monster_equation").hide();
        }
    function showExclude(){
        $(".show_exclude").hide();
        $(".hide_exclude").show();
        $(".exclude").show();
        }
    function hideExclude(){
        $(".show_exclude").show();
        $(".hide_exclude").hide();
        $(".exclude").hide();
        }
    var put_relation_flag = false;
    function showPutRelation(){
        $(".show_put_relation").hide();
        $(".hide_put_relation").show();
        $(".put_relation").show();
        if(put_relation_flag== false){
		    addKindType("put_relation_kind_"+0,'put_relation_kind');
		    put_relation_flag = true;
        }
    }
    function hidePutRelation(){
        $(".show_put_relation").show();
        $(".hide_put_relation").hide();
        $(".put_relation").hide();
    }
    function showRelation(){
        $(".show_relation").hide();
        $(".hide_relation").show();
        $(".relation_box").show();
    }
    function hideRelation(){
        $(".show_relation").show();
        $(".hide_relation").hide();
        $(".relation_box").hide();
    }
    function showCustomMonsterCondition(){
        $(".show_custom_monster_condition").hide();
        $(".hide_custom_monster_condition").show();
        $(".custom_monster_condition_box").show();
        }
    function hideCustomMonsterCondition(){
        $(".show_custom_monster_condition").show();
        $(".hide_custom_monster_condition").hide();
        $(".custom_monster_condition_box").hide();
        }
    function showMonsterCondition(){
        $(".show_monster_condition").hide();
        $(".hide_monster_condition").show();
        $(".monster_condition_box").show();
        }
    function hideMonsterCondition(){
        $(".show_monster_condition").show();
        $(".hide_monster_condition").hide();
        $(".monster_condition_box").hide();
        }
    function showMonster(){
        $(".show_monster").hide();
        $(".hide_monster").show();
        $(".monster_box").show();
        }
    function hideMonster(){
        $(".show_monster").show();
        $(".hide_monster").hide();
        $(".monster_box").hide();
        }
    function showMonsterFrom(){
        $(".show_monster_from").hide();
        $(".hide_monster_from").show();
        $(".monster_from_box").show();
        }
    function hideMonsterFrom(){
        $(".show_monster_from").show();
        $(".hide_monster_from").hide();
        $(".monster_from_box").hide();
        }
    function showMonsterTurnCount(){
        $(".show_monster_turn_count").hide();
        $(".hide_monster_turn_count").show();
        $(".monster_turn_count_box").show();
        }
    function hideMonsterTurnCount(){
        $(".show_monster_turn_count").show();
        $(".hide_monster_turn_count").hide();
        $(".monster_turn_count_box").hide();
        }
    function showMonsterId(){
        $(".show_monster_id").hide();
        $(".hide_monster_id").show();
        $(".monster_id_box").show();
        }
    function hideMonsterId(){
        $(".show_monster_id").show();
        $(".hide_monster_id").hide();
        $(".monster_id_box").hide();
        }
    function showUnderMonster(){
        $(".show_under_monster").hide();
        $(".hide_under_monster").show();
        $(".under_monster_box").show();
        }
    function hideUnderMonster(){
        $(".show_under_monster").show();
        $(".hide_under_monster").hide();
        $(".under_monster_box").hide();
        }
    function showUnderCondition(){
        $(".show_under_condition").hide();
        $(".hide_under_condition").show();
        $(".under_condition_box").show();
        }
    function hideUnderCondition(){
        $(".show_under_condition").show();
        $(".hide_under_condition").hide();
        $(".under_condition_box").hide();
        }
    function showUnderId(){
        $(".show_under_id").hide();
        $(".hide_under_id").show();
        $(".under_id_box").show();
        }
    function hideUnderId(){
        $(".show_under_id").show();
        $(".hide_under_id").hide();
        $(".under_id_box").hide();
        }
    function showUnderName(){
        $(".show_under_name").hide();
        $(".hide_under_name").show();
        $(".under_name_box").show();
        }
    function hideUnderName(){
        $(".show_under_name").show();
        $(".hide_under_name").hide();
        $(".under_name_box").hide();
        }
    function showMonsterName(){
        $(".show_monster_name").hide();
        $(".hide_monster_name").show();
        $(".monster_name_box").show();
        }
    function hideMonsterName(){
        $(".show_monster_name").show();
        $(".hide_monster_name").hide();
        $(".monster_name_box").hide();
        }
    function showUnder(){
        $(".show_under").hide();
        $(".hide_under").show();
        $(".under").show();
        }
    function hideUnder(){
        $(".show_under").show();
        $(".hide_under").hide();
        $(".under").hide();
        }
    function showUnderFlag(){
        $(".show_under_flag").hide();
        $(".hide_under_flag").show();
        $(".flag_under_box").show();
        }
    function hideUnderFlag(){
        $(".show_under_flag").show();
        $(".hide_under_flag").hide();
        $(".flag_under_box").hide();
        }
    function showFlag(){
        $(".show_flag").hide();
        $(".hide_flag").show();
        $(".flag_box").show();
        }
    function hideFlag(){
        $(".show_flag").show();
        $(".hide_flag").hide();
        $(".flag_box").hide();
        }
    function showPlace(){
        $(".show_place").hide();
        $(".hide_place").show();
        $(".trigger_condition_place_box").show();
        }
    function hidePlace(){
        $(".show_place").show();
        $(".hide_place").hide();
        $(".trigger_condition_place_box").hide();
        }
	function addPlaceAll(place,i,j,json=null,k=-1,tmp=0){
	if(tmp<l){
	$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_place_kind/",
   'data': "",
'success': function(data){
        if(k != -1){
			if( $("#"+place+"_"+i+"_"+tmp+"_"+k).length == 0){
			$("#"+place+"_add_"+i+"_"+tmp+"_"+(k-1)).after('<select id="'+place+'_'+i+'_'+j+'_'+k+'" class="monster_condition_place" style=""> </select> <select id="'+place+'_add_'+i+"_"+j+"_"+k+'" onchange="addPlace(\''+place+'\','+i+','+(j+1)+',null,'+(k+1)+')" class="monster_condition_place" style=""> <option value=""></option><option value="and"> <option value="or">または</option> </select>');
			 $("#"+place+"_"+i+"_"+tmp+"_"+k).html(data);
			}
		    if(json != null){
		        putPlaceFrom(place,i,tmp,k,json)
		    }
		    return;
        }else{
		if(tmp!=undefined){
			if( $("#"+place+"_"+i+"_"+tmp).length == 0){
			$("#"+place+"_add_"+i+"_"+(tmp-1)).after('<select id="'+place+'_'+i+'_'+tmp+'" class="monster_condition_place" style=""> </select> <select id="'+place+'_add_'+i+"_"+tmp+'" onchange="addPlace(\''+place+'\','+i+','+(tmp+1)+')" class="monster_condition_place" style=""> <option value=""></option><option value="and"> <option value="or">または</option> </select>');
			 $("#"+place+"_"+i+"_"+tmp).html(data);
			}
		}else{
			if( $("#"+place+"_"+i).length == 0){
			$("#"+place+"_add_"+i).after('<select id="'+place+'_'+i+'" class="monster_condition_place" style=""> </select> <select id="'+place+'_add_'+i+'" onchange="addPlace(\''+place+'\','+(i+1)+','+')" class="monster_condition_place" style=""> <option value=""></option><option value="and"> <option value="or">または</option> </select>');
			 $("#"+place+"_"+i).html(data);
			}
		}
		}
		if(json != null){
		    putPlace(place,i,tmp,json)
		}
	addPlaceAll(place,i,j,json,k,tmp+1);
	}
	});
	}
	}
	function getConditionVariables(id){
		$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_variable_kind/",
		   'data': "",
		'success': function(data){
			$("."+id+"_variable_condition_").show();
			$("#"+id+"_variable_condition_1").html(data);
		}
		});
	}
	function addFieldX(i,next,id){
		result='<input id="'+id+'_field_x_'+i+'_'+next+'" style=""><input type="button" value="追加" id="add_field_x_'+i+'_'+next+'" onclick="addFieldX('+i+','+(next+1)+',\''+id+'\')">'
		result+='演算子<select id="get_field_x_det_'+i+'_'+next+'"><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select><br>';
		result+='<select id="get_field_x_and_or_'+i+'_'+next+'" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><br>';
		$("#add_field_x_"+i+"_"+(next-1)).after(result);
	}
	function addFieldY(i,next,id){
		result='<input id="'+id+'_field_y_'+i+'_'+next+'" style="">';
		result+='演算子<select id="get_field_y_det_'+i+'_'+next+'"><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select><br>';
		result+='<select id="get_field_y_and_or_'+i+'_'+next+'" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select>';
		result+='<input type="button" value="追加" id="add_field_y_'+i+'_'+next+'" onclick="addFieldX('+i+','+(next+1)+',\''+id+'\')"><br>'
		$("#add_field_y_"+i+"_"+(next-1)).after(result);
	}
	function changeMonsterKindNum(id2,id,mode){
		var tmp_str = "";
		if(mode == 0){
		        id = 'monster_kind';
		        id2 = 'id_trigger_kind';
		}
		tmp_str = $("#"+id2).val();
		if (tmp_str !=""){
		    tmp_str+="_";

		}
		tmp_str+=$("#"+id+"-"+(0)).val();
		$("#"+id2).val(tmp_str);

	}
        function showMonsterVariableForCopy(id){
                $(".show_"+id).show();
                $(".hide_"+id).hide();
                $(".variable_box_"+id).show();
        }
        function hideMonsterVariableForCopy(id){
                $(".show_"+id).hide();
                $(".hide_"+id).show();
                $(".variable_box_"+id).hide();
        }
        function showMonsterVariableDet(id){
                $(".show_"+id).show();
                $(".hide_"+id).hide();
                $(".variable_box_"+id).show();
        }
        function hideMonsterVariableDet(id){
                $(".show_"+id).hide();
                $(".hide_"+id).show();
                $(".variable_box_"+id).hide();
        }
        function addCustomVariable(id){
                var html="";

                html="<input type=\"text\" id=\""+id+"_custom_variable_name_"+global_custom_variable+"\">";
                global_custom_variable++;
                $("#"+id+"_custom_add").after(html);
        }
	    function getTurnEnd(){
		$("#turn_end").show();
		$("#turn_end").draggable();
		$("#turn_end").offset({top:0,left:200});
	    }
	    function getMonsterEffectCheckTimingAndPhase(i){
		$("#monster_effect_check_timing_and_phase").show();
		$("#monster_effect_check_timing_and_phase").draggable();
		$("#monster_effect_check_timing_and_phase").offset({top:0,left:200});
		    getMonsterEffectTimingAndPhase();
	    }

	function getMonsterEffectTimingAndPhase(){
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_phase/",
		   'data': "",
			'success': function(data){
				$("#monster_check_phase").html(data);
			}
		});
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_tcg_timing/",
		   'data': "",
			'success': function(data){
				$("#monster_check_timing").html(data);
			}
		});
	}
	function putCheckTimingAndPhase(id){
	    json={};
	    if($("#check_phase_flag").prop("checked") == true){
	        json["check_phase"] = parseInt($("#monster_check_phase").val());
	    }
	    if($("#check_timing_flag").prop("checked") == true){
	        json["check_timing"] = parseInt($("#monster_check_timing").val());
	    }
		val = JSON.stringify(json);
		$("#id_"+id).val(val);
	}
	function getMonsterEffectGetSelectTrigger(id){
		$("#get_triggers").show();
		$("#get_triggers").draggable();
		$("#get_triggers").offset({top:0,left:200});
                json = $("#id_"+id).val();
                if(json==""){
                        return;
                }
                data = JSON.parse(json);
                for(var i=0;i<data.length;i++){
                        if($("#triggers_"+String(i)).length == 0){
                                addSelectTrigger(i-1,data[i]);
                        }else{
                        $("#triggers_"+String(i)).val(data[i]["trigger"]);
                        $("#next_effect_"+String(i)).val(data[i]["next_effect"]);
                        $("#next_pac_"+String(i)).val(data[i]["next_pac"]);
                        }
                }
	}
	function addSelectTrigger(num,data){
    var add_num = String(num+1);
    var add_html = '<select id="triggers_'+add_num+'"> </select> <select id="next_effect_'+add_num+'"> </select> <select id="next_pac_'+add_num+'"></select><input type="button" id="add_select_trigger_'+add_num+'" value="追加" onclick="addSelectTrigger('+add_num+')">';
    getSelectTrigger(add_num,data);
    $("#add_select_trigger_"+num).after(add_html);
    $("#add_select_trigger_"+num).hide();
    }
    function putSelectTrigger(id){
        var json = [];
        for(var i=0;$("#triggers_"+String(i)).length != 0;i++){
            json[i]= {};
            json[i]["trigger"]= parseInt($("#triggers_"+String(i)).val());
            json[i]["next_effect"]= parseInt($("#next_effect_"+String(i)).val());
            json[i]["next_pac"]= parseInt($("#next_pac_"+String(i)).val());
        }
        var result = JSON.stringify(json);
        $("#"+id).val(result);
    }
    function addCond(num){
        $("#cond_editor_add"+num).hide();

        num++;
        add_html = '変数名<input type="text" id="cond_for_editor'+num+'"> 値<input type="text" id="value_for_editor'+num+'"><select id="cond_equation_for_editor'+num+'" style=""> <option value="=">=</option> <option value="<=">&lt;=</option> <option value=">=">&gt;=</option> <option value="!=">!=</option> </select> <select id="cond_and_or'+num+'"><option value="or">or</option><option value="and">and</option></select><input type="button" value="条件追加" id="cond_editor_add'+num+'" onclick="addCond('+num+')">';
        $("#cond_editor_add"+(num-1)).after(add_html);
         }
    var unicodeUnescape = function(str) {
    var result = '', strs = str.match(/\\u.{4}/ig);
    if (!strs) return '';
    for (var i = 0, len = strs.length; i < len; i++) {
        result += String.fromCharCode(strs[i].replace('\\u', '0x'));
    }
    return result;
};

function unescapeUnicode(string) {
    return string.replace(/\\u([a-fA-F0-9]{4})/g, function(matchedString, group1) {
        return String.fromCharCode(parseInt(group1, 16));
    });
}
function changeMonsterEffectValidKind(j,i){
    var tmp,tmp2;
    tmp = $('#monster_effect_kind_'+j+'_'+i).val();
    if (tmp != ""){
            tmp = tmp + "_";
    }
    tmp2 = $('#monster_effect_kind_choose_'+j+'_'+i).val();
    $('#monster_effect_kind_'+j+'_'+i).val(tmp+tmp2);
}

	function getEternalKindForEquation(){
		$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_effect_kind/",
   'data': "",
'success': function(data){
		$("#eternal_kind_choose_for_editor").html(data);
		}});
	}
	function addEternalKindForEquation(){
	    tmp = $("#eternal_flag_for_editor").val();
	    tmp2 = $("#eternal_kind_choose_for_editor").val();
	    if (tmp == ""){
	        $("#eternal_flag_for_editor").val(tmp2);
	    }else{
	        $("#eternal_flag_for_editor").val(tmp+"_"+tmp2);
	    }
	}
	function putGetMonster(j,i){
	    var initial_val = $("#get_monster_"+j+"_"+i).val();
	    var new_val = $("#get_monster_select_"+j+"_"+i).val();
	    if (initial_val == ""){
	        $("#get_monster_"+j+"_"+i).val(new_val);
	    }else{
	        $("#get_monster_"+j+"_"+i).val(initial_val+"_"+new_val);
	    }
	}
	function getMonsterSpecify(id){
	        name=$("#"+id+"_specify").val();
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_monster_specify/",
		   'data': "name="+name,
			'success': function(data){
				$("#"+id).html(data);
			}
	    });
	}
	function addPlace(place,i,j,json=null,k=-1,deferred=null){
	$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_place_kind/",
   'data': "",
'success': function(data){
        if(k != -1){
			if( $("#"+place+"_"+i+"_"+j+"_"+k).length == 0){
			$("#"+place+"_add_"+i+"_"+j+"_"+(k-1)).after('<select id="'+place+'_'+i+'_'+j+'_'+k+'" class="monster_condition_place" style=""> </select> <select id="'+place+'_add_'+i+"_"+j+"_"+k+'" onchange="addPlace(\''+place+'\','+i+','+(j+1)+',null,'+(k+1)+')" class="monster_condition_place" style=""> <option value=""></option><option value="and"> <option value="or">または</option> </select>');
			 $("#"+place+"_"+i+"_"+j+"_"+k).html(data);
			}
		    if(json != null){
		        putPlaceFrom(place,i,j,k,json)
		    }
		    return;
        }else{
		if(j!=undefined){
			if( $("#"+place+"_"+i+"_"+j).length == 0){
			$("#"+place+"_add_"+i+"_"+(j-1)).after('<select id="'+place+'_'+i+'_'+j+'" class="monster_condition_place" style=""> </select> <select id="'+place+'_add_'+i+"_"+j+'" onchange="addPlace(\''+place+'\','+i+','+(j+1)+')" class="monster_condition_place" style=""> <option value=""></option><option value="and"> <option value="or">または</option> </select>');
			 $("#"+place+"_"+i+"_"+j).html(data);
			}
		}else{
			if( $("#"+place+"_"+i).length == 0){
			$("#"+place+"_add_"+i).after('<select id="'+place+'_'+i+'" class="monster_condition_place" style=""> </select> <select id="'+place+'_add_'+i+'" onchange="addPlace(\''+place+'\','+(i+1)+','+')" class="monster_condition_place" style=""> <option value=""></option><option value="and"> <option value="or">または</option> </select>');
			 $("#"+place+"_"+i).html(data);
			}
		}
		}
		if(json != null){
		    putPlace(place,i,j,json)
		}
	}
	});
	}
	function getConditionVariables(id){
		$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_variable_kind/",
		   'data': "",
		'success': function(data){
			$("."+id+"_variable_condition_").show();
			$("#"+id+"_variable_condition_1").html(data);
		}
		});
	}
	function addFieldX(i,next,id){
		result='<input id="'+id+'_field_x_'+i+'_'+next+'" style=""><input type="button" value="追加" id="add_field_x_'+i+'_'+next+'" onclick="addFieldX('+i+','+(next+1)+',\''+id+'\')">'
		result+='演算子<select id="get_field_x_det_'+i+'_'+next+'"><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select><br>';
		result+='<select id="get_field_x_and_or_'+i+'_'+next+'" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><br>';
		$("#add_field_x_"+i+"_"+(next-1)).after(result);
	}
	function addFieldY(i,next,id){
		result='<input id="'+id+'_field_y_'+i+'_'+next+'" style="">';
		result+='演算子<select id="get_field_y_det_'+i+'_'+next+'"><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select><br>';
		result+='<select id="get_field_y_and_or_'+i+'_'+next+'" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select>';
		result+='<input type="button" value="追加" id="add_field_y_'+i+'_'+next+'" onclick="addFieldX('+i+','+(next+1)+',\''+id+'\')"><br>'
		$("#add_field_y_"+i+"_"+(next-1)).after(result);
	}
	function changeMonsterKindNum(id2,id,mode){
		var tmp_str = "";
		if(mode == 0){
		        id = 'monster_kind';
		        id2 = 'id_trigger_kind';
		}
		tmp_str = $("#"+id2).val();
		if (tmp_str !=""){
		    tmp_str+="_";

		}
		tmp_str+=$("#"+id+"-"+(0)).val();
		$("#"+id2).val(tmp_str);

	}
        function showMonsterVariableForCopy(id){
                $(".show_"+id).show();
                $(".hide_"+id).hide();
                $(".variable_box_"+id).show();
        }
        function hideMonsterVariableForCopy(id){
                $(".show_"+id).hide();
                $(".hide_"+id).show();
                $(".variable_box_"+id).hide();
        }
        function showMonsterVariableDet(id){
                $(".show_"+id).show();
                $(".hide_"+id).hide();
                $(".variable_box_"+id).show();
        }
        function hideMonsterVariableDet(id){
                $(".show_"+id).hide();
                $(".hide_"+id).show();
                $(".variable_box_"+id).hide();
        }      
        function addCustomVariable(id){
                var html="";
                
                html="<input type=\"text\" id=\""+id+"_custom_variable_name_"+global_custom_variable+"\">";
                global_custom_variable++;
                $("#"+id+"_custom_add").after(html);
        }
	    function getTurnEnd(){
		$("#turn_end").show();
		$("#turn_end").draggable();
		$("#turn_end").offset({top:0,left:200});
	    }
	    function getMonsterEffectCheckTimingAndPhase(i){
		$("#monster_effect_check_timing_and_phase").show();
		$("#monster_effect_check_timing_and_phase").draggable();
		$("#monster_effect_check_timing_and_phase").offset({top:0,left:200});
		    getMonsterEffectTimingAndPhase();
	    }

	function getMonsterEffectTimingAndPhase(){
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_phase/",
		   'data': "",
			'success': function(data){
				$("#monster_check_phase").html(data);
			}
		});
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_tcg_timing/",
		   'data': "",
			'success': function(data){
				$("#monster_check_timing").html(data);
			}
		});
	}
	function putCheckTimingAndPhase(id){
	    json={};
	    if($("#check_phase_flag").prop("checked") == true){
	        json["check_phase"] = parseInt($("#monster_check_phase").val());
	    }
	    if($("#check_timing_flag").prop("checked") == true){
	        json["check_timing"] = parseInt($("#monster_check_timing").val());
	    }
		val = JSON.stringify(json);
		$("#id_"+id).val(val);
	}
	function getMonsterEffectGetSelectTrigger(id){
		$("#get_triggers").show();
		$("#get_triggers").draggable();
		$("#get_triggers").offset({top:0,left:200});
                json = $("#id_"+id).val();
                if(json==""){
                        return;
                }
                data = JSON.parse(json);
                for(var i=0;i<data.length;i++){
                        if($("#triggers_"+String(i)).length == 0){
                                addSelectTrigger(i-1,data[i]);
                        }else{
                        $("#triggers_"+String(i)).val(data[i]["trigger"]);
                        $("#next_effect_"+String(i)).val(data[i]["next_effect"]);
                        $("#next_pac_"+String(i)).val(data[i]["next_pac"]);
                        }
                }
	}
	function addSelectTrigger(num,data){
    var add_num = String(num+1);
    var add_html = '<select id="triggers_'+add_num+'"> </select> <select id="next_effect_'+add_num+'"> </select> <select id="next_pac_'+add_num+'"></select><input type="button" id="add_select_trigger_'+add_num+'" value="追加" onclick="addSelectTrigger('+add_num+')">';
    getSelectTrigger(add_num,data);
    $("#add_select_trigger_"+num).after(add_html);
    $("#add_select_trigger_"+num).hide();
    }
    function putSelectTrigger(id){
        var json = [];
        for(var i=0;$("#triggers_"+String(i)).length != 0;i++){
            json[i]= {};
            json[i]["trigger"]= parseInt($("#triggers_"+String(i)).val());
            json[i]["next_effect"]= parseInt($("#next_effect_"+String(i)).val());
            json[i]["next_pac"]= parseInt($("#next_pac_"+String(i)).val());
        }
        var result = JSON.stringify(json);
        $("#"+id).val(result);
    }
    function addCond(num){
        $("#cond_editor_add"+num).hide();

        num++;
        add_html = '変数名<input type="text" id="cond_for_editor'+num+'"> 値<input type="text" id="value_for_editor'+num+'"><select id="cond_equation_for_editor'+num+'" style=""> <option value="=">=</option> <option value="<=">&lt;=</option> <option value=">=">&gt;=</option> <option value="!=">!=</option> </select> <select id="cond_and_or'+num+'"><option value="or">or</option><option value="and">and</option></select><input type="button" value="条件追加" id="cond_editor_add'+num+'" onclick="addCond('+num+')">';
        $("#cond_editor_add"+(num-1)).after(add_html);
         }
    var unicodeUnescape = function(str) {
    var result = '', strs = str.match(/\\u.{4}/ig);
    if (!strs) return '';
    for (var i = 0, len = strs.length; i < len; i++) {
        result += String.fromCharCode(strs[i].replace('\\u', '0x'));
    }
    return result;
};

function unescapeUnicode(string) {
    return string.replace(/\\u([a-fA-F0-9]{4})/g, function(matchedString, group1) {
        return String.fromCharCode(parseInt(group1, 16));
    });
}
function changeMonsterEffectValidKind(j,i){
    var tmp,tmp2;
    tmp = $('#monster_effect_kind_'+j+'_'+i).val();
    if (tmp != ""){
            tmp = tmp + "_";
    }
    tmp2 = $('#monster_effect_kind_choose_'+j+'_'+i).val();
    $('#monster_effect_kind_'+j+'_'+i).val(tmp+tmp2);
}

	function getEternalKindForEquation(){
		$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_effect_kind/",
   'data': "",
'success': function(data){
		$("#eternal_kind_choose_for_editor").html(data);
		}});
	}
	function addEternalKindForEquation(){
	    tmp = $("#eternal_flag_for_editor").val();
	    tmp2 = $("#eternal_kind_choose_for_editor").val();
	    if (tmp == ""){
	        $("#eternal_flag_for_editor").val(tmp2);
	    }else{
	        $("#eternal_flag_for_editor").val(tmp+"_"+tmp2);
	    }
	}
	function getMonsterSpecify(id){
	        name=$("#"+id+"_specify").val();
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_monster_specify/",
		   'data': "name="+name,
			'success': function(data){
				$("#"+id).html(data);
			}
	    });
	}
