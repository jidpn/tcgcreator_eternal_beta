	var trigger_kind_id = [];
	var condition_i = 0;
	var trigger_flag = 1;
	var global_trigger_val=1;
	$(document).ready(function(){
	    var path_name = location.pathname;
	    path_name = path_name.substring(0,path_name.length-7)
        $("input[name=\"_save\"]").before("<input type=\"button\" value=\"insert\" onclick=\"location.href='"+path_name+"tag_monster'\">");
        $("input[name=\"_save\"]").before("<input type=\"button\" value=\"diagram\" onclick=\"location.href='"+path_name+"diagram'\">");
        $("input[name=\"_save\"]").before("<input type=\"button\" value=\"cost_diagram\" onclick=\"location.href='"+path_name+"cost_diagram'\">");
		$("#id_trigger_timing").after("<input type=\"button\" onclick=\"getTriggerTiming()\" value=\"追加\">");
		$("#id_trigger_condition").after("<input type=\"button\" onclick=\"getConditionKind('trigger_condition',1,100,0)\" value=\"追加\">");
		$("#id_next_effect").after("<input type=\"button\" onclick=\"getMonsterEffectNextSpecify('id_next_effect')\" value=\"絞り込み\"><input type=\"text\" id=\"id_next_effect_name_specify\"><select id=\"id_next_effect_effect_kind\"></select>");
		$("#id_trigger_cost").after("<input type=\"button\" onclick=\"getCostNextSpecify('id_trigger_cost')\" value=\"絞り込み\"><input type=\"text\" id=\"id_trigger_cost_name_specify\"><select id=\"id_trigger_cost_effect_kind\"></select>");
		$("#id_next_effect").after("<input type=\"button\" onclick=\"getLastMonsterEffectNextSpecify('id_next_effect')\" value=\"最新\">");
		$("#id_trigger_cost").after("<input type=\"button\" onclick=\"getLastCostNextSpecify('id_trigger_cost')\" value=\"最新\">");
		$("#id_trigger_cost_pac").after("<input type=\"button\" onclick=\"getPacCostNextSpecify('id_trigger_cost_pac')\" value=\"絞り込み\"><input type=\"text\" id=\"id_trigger_cost_pac_name_specify\"><select id=\"id_trigger_cost_pac_effect_kind\"></select>");
		$("#id_trigger_cost_pac").after("<input type=\"button\" onclick=\"getLastPacCostNextSpecify('id_trigger_cost_pac')\" value=\"最新\">");
		$("#id_pac").after("<input type=\"button\" onclick=\"getPacNextSpecify('id_pac')\" value=\"絞り込み\"><input type=\"text\" id=\"id_pac_name_specify\"><select id=\"id_pac_effect_kind\"></select>");
		$("#id_pac").after("<input type=\"button\" onclick=\"getLastPacNextSpecify('id_pac')\" value=\"最新\">");
		// $("#id_trigger_cost").after("<input type=\"button\" onclick=\"getTriggerCost()\" value=\"追加\">");
		$("#id_trigger_monster").after("<input type=\"button\" onclick=\"getConditionKind('trigger_monster',0,100,0)\" value=\"追加\">");
		$("#id_fusion_monster").after("<input type=\"button\" onclick=\"getConditionKind('fusion_monster',0,100,0)\" value=\"追加\">");
		$("#id_instead_condition").after("<input type=\"button\" onclick=\"getConditionKind('instead_condition',0,100,0)\" value=\"追加\">");
		$("#id_fusion1").after("<input type=\"button\" onclick=\"getConditionKind('fusion1',0,100,0)\" value=\"追加\">");
		$("#id_fusion2").after("<input type=\"button\" onclick=\"getConditionKind('fusion2',0,100,0)\" value=\"追加\">");
		$("#id_fusion3").after("<input type=\"button\" onclick=\"getConditionKind('fusion3',0,100,0)\" value=\"追加\">");
		$("#id_instead1").after("<input type=\"button\" onclick=\"getConditionKind('instead1',0,100,0)\" value=\"追加\">");
		$("#id_instead2").after("<input type=\"button\" onclick=\"getConditionKind('instead2',0,100,0)\" value=\"追加\">");
		$("#id_instead3").after("<input type=\"button\" onclick=\"getConditionKind('instead3',0,100,0)\" value=\"追加\">");
		$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_effect_kind/",
   'data': "",
'success': function(data){
		$("#id_next_effect_effect_kind").html(data);
		$("#id_pac_kind").html(data);
		$("#id_trigger_cost_effect_kind").html(data);
		$("#id_trigger_cost_pac_effect_kind").html(data);
    }
	});
	$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_monster_kind/",
   'data': "delete_flag=0&num=0&id=trigger_kind&id2=trigger_kind",
'success': function(data){
		$("#id_trigger_kind").after("<input type=\"button\" onclick=\"changeMonsterKindNum('id_trigger_kind','trigger_kind',1)\" value=\"追加\"><br>");
			$("#id_trigger_kind").after(data);
        }
	})
	});
		
	function getTriggerCondition(){
		$("#monster_condition").show();
		$("#monster_condition").draggable();
		getTriggerConditionKind(-1);
	}
	
	function changeConditionNum(){
		var tmp_str = "";
		for(var i=0;i<condition_i;i++){
			tmp_str+=$("#monster_kind-"+(i)).val()+"_";;
		}
		tmp_str = tmp_str.substr(0,tmp_str.length-1);
		$("#id_trigger_effect_kind").val(tmp_str);

	}
	var monter_kind_i = 0;
	var chain_kind_i = 0;

	function getChainChangeBefore(){
		getChainKindChange(chain_kind_i)
	}
	function getTriggerCost(){
		$("#monster_cost").show();
		$("#monster_cost").draggable();
		getTriggerCostKind(-1);
	}
	
	function changeCostNum(){
		var tmp_str = "";
		for(var i=0;i<cost_i;i++){
			tmp_str+=$("#monster_kind-"+(i)).val()+"_";
		}
		tmp_str = tmp_str.substr(0,tmp_str.length-1);
		$("#id_trigger_effect_kind").val(tmp_str);

	}
	function getTriggerCostKind(cost_kind){
		if(cost_kind == "0" || cost_kind == "1"){
			$("#monster_cost_place_tab").show();
		}else{
			$("#monster_cost_place_hide").show();
		}
		if(cost_kind == "0"){
			$("#monster_cost_place_to_wrapper").show();
		}else{
			$("#monster_cost_place_to_wrapper").hide();
		}
		$("#monster_cost").show();
		$("#monster_cost").offset({top:0,left:200});
	$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_place_kind/",
   'data': "",
'success': function(data){
		$(".monster_cost_place").show();
		$("#monster_cost_place_1").html(data);
		$("#monster_cost_place_to").html(data);
		$.ajax({
			   'type': "POST",
			   'url': "/tcgcreator/get_monster/",
			   'data': "",
			'success': function(data){
					$("#monster_cost_monster").show();
					$("#monster_cost_monster").html(data);
					$.ajax({
			  			 'type': "POST",
			  			 'url': "/tcgcreator/get_equation/",
			  			 'data': "",
						'success': function(data){
							$("#monster_cost_equation").show();
							$("#monster_cost_equation").html(data);
			      		 } 
					})
			        } 
				})
        } 
	})
	}	
	function addTriggerCostPlace(i){
		var html = $("#monster_cost_place_1").html();
		and_or = "または";
		var html = and_or+'<select id="monster_cost_place_'+(i+1)+'" class="monster_cost_place" >'+html+'</select>';
		html+='<select id="monster_cost_place_add_'+(i+1)+'" onchange="addTriggerCostPlace('+(i+1)+')" class="monster_cost_place" ><option value=""></option><option value="and">かつ</option><option value="or">または</option></select>';
		$("#monster_cost_place_add_"+i).after(html);
		$("#monster_cost_place_add_"+(i)).remove();;
	}
	function putTriggerCost(){
		var val= $("#id_trigger_cost").val();
		var tmp = $("#monster_cost_place_1").val();
		var place = "(";
		var place_to;
		var tmp2 =$("#monster_cost_kind").val();
		if(tmp2 == "0"){
			place_to = $("#monster_cost_place_to").val();
			place_to = "(place_to = "+place_to+")";
		}else if(tmp2=="1"){
			place_to = "(place_designation)";
		}
		
		if(tmp != "0"){
			place += "place = "+tmp;
			for(var i=2;$("#monster_cost_place_add_"+(i-1)).val();i++){
				var tmp = $("#monster_cost_place_"+i).val();
				var operator = $("#monster_cost_place_add_"+(i-1)).val();
				if(tmp != "0"){
					place += " "+operator+" "+tmp;
				}
			}
			place+=")";
		}
		var monster_cost = "";
		var j=0;
		for(var i=1;$("#get_monster_variable_"+i).length != 0;i++){
			if($("#get_monster_variable_equal_"+i).length != 0){
				num = $("#get_monster_variable_"+i).val();
				operator = $("#get_monster_variable_equal_"+i).val();
				if(operator == ""){
					continue;
				}
				monster_cost += '(id='+i+'&num='+num+'&operator='+operator+')';
				j++;
			}else{
				num = $("#get_monster_variable_"+i).val();
				if(num == "0" || num == ""){
					continue;
				}
				monster_cost += "(id="+i+"&num="+num+"&operator=)";
				j++;
			}
			
		}
		equation = "(equation = '"+$("#get_equation_det").val()+"')";
		equation_kind = "(equation_kind = "+$("#get_equation_kind").val()+")";
		equation_number = "(equation_number = "+$("#get_equation_number").val()+")";
		if($("#get_monster_name_equal").val() == ""){
			monster_name_kind = "";
		}else if($("#get_monster_name_equal").val() == "="){
			monster_name_kind = '(monster_name_kind = "+$("#monster_name").val()+")';
		}else{
			monster_name_kind = '(monster_name_kind like "+$("#monster_name").val()+")';
		}
		val += "{"+place+place_to+monster_name_kind+monster_cost+equation+equation_kind+equation_number+"}";
		$("#id_trigger_cost").val(val);
		$("#monster_cost").hide();
		$("#monster_monster").hide();
		$("#monster_equation").hide();
		$("#monster_cost_place_to_wrapper").hide();
		$(".monster_cost_place").hide();
		for(var i=2;$("#monster_cost_place_"+(i)).length;i++){
			$("#monster_cost_place_"+i).remove();
			$("#monster_cost_place_add"+i).remove();
			
		}
		
		
	}
	function getTriggerMonster(){
		$("#trigger_monster").show();
		$("#trigger_monster").draggable();
		getTriggerMonsterKind();
	}
	
	function changeTriggerMonsterNum(){
		var tmp_str = "";
		for(var i=0;i<cost_i;i++){
			tmp_str+=$("#monster_kind-"+(i)).val()+"_";;
		}
		tmp_str = tmp_str.substr(0,tmp_str.length-1);
		$("#id_trigger_effect_kind").val(tmp_str);

	}
	function getTriggerMonsterKind(){
			$("#monster_monster_place_tab").show();
		$("#trigger_monster").show();
		$("#trigger_monster").offset({top:0,left:200});
	$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_place_kind/",
   'data': "",
'success': function(data){
		$(".monster_monster_place").show();
		$("#monster_monster_place_1").html(data);
		$("#monster_monster_place_to").html(data);
		$("#monster_condition_place_1").html("");
		$.ajax({
			   'type': "POST",
			   'url': "/tcgcreator/get_monster/",
			   'data': "",
			'success': function(data){
					$("#monster_monster_monster").show();
					$("#monster_monster_monster").html(data);
					$("#monster_monster").html("");
			        } 
				})
        } 
	})
	}	
	function addTriggerMonsterPlace(i){
		var html = $("#monster_monster_place_1").html();
		and_or = "または";
		var html = and_or+'<select id="monster_monster_place_'+(i+1)+'" class="monster_monster_place" >'+html+'</select>';
		html+='<select id="monster_monster_place_add_'+(i+1)+'" onchange="addTriggerCostPlace('+(i+1)+')" class="monster_monster_place" ><option value=""></option><option value="and">かつ</option><option value="or">または</option></select>';
		$("#monster_monster_place_add_"+i).after(html);
		$("#monster_monster_place_add_"+(i)).remove();;
	}
	function putTriggerMonster(){
		var val= $("#id_trigger_monster").val();
		var tmp = $("#monster_monster_place_1").val();
		var place = "(";
		var place_to;
		var tmp2 =$("#monster_monster_kind").val();
		var json={};
		if(val == ""){
			val2=[];
		}else{
			val2= JSON.parse(val);
		}
		json["place"]  = [];
		if(tmp != "0"){
			json["place"][0] = tmp;
			var place_counter=1;
			for(var i=2;$("#monster_monster_place_add_"+(i-1)).val();i++){
				var tmp = $("#monster_monster_place_"+i).val();
				if(tmp != "0"){
					json["place"][place_counter] =tmp;
					place_counter++;
				}
			}
		}
		json["monster_monster"] = [];
		var j=0;
		for(var i=1;$("#get_monster_variable_"+i).length != 0;i++){
			json["monster_monster"][i-1] = {};
			if($("#get_monster_variable_equal_"+i).length != 0){
				num = $("#get_monster_variable_"+i).val();
				operator = $("#get_monster_variable_equal_"+i).val();
				if(operator == ""){
					continue;
				}
				json["monster_monster"][i-1]["num"]= num
				json["monster_monster"][i-1]["operator"]= operator;
			}else{
				num = $("#get_monster_variable_"+i).val();
				if(num == "0" || num == ""){
					continue;
				}
				json["monster_monster"][i-1]["num"]= num
				json["monster_monster"][i-1]["operator"]= "=";
			}
			
		}
		if($("#get_monster_name_equal").val() == ""){
			json["monster_name_kind"] = "";
		}else if($("#get_monster_name_equal").val() == "="){
			json["monster_name_kind"] = {};
			json["monster_name_kind"]["operator"] = "=";
			json["monster_name_kind"]["monster_name"] =$("#monster_name").val();
		}else{
			json["monster_name_kind"] = {};
			json["monster_name_kind"]["operator"] = "like";
			json["monster_name_kind"]["monster_name"] =$("#monster_name").val();
		}
		json["as_trigger_monster"] = $("#as_monster_monster").val()
		val2.push(json)
		val = JSON.stringify(val2);
		$("#id_trigger_monster").val(val);
		$("#trigger_monster").hide();
		$("#trigger_monster").hide();
		$("#monster_equation").hide();
		$(".monster_monster_place").hide();
		for(var i=2;$("#monster_monster_place_"+(i)).length;i++){
			$("#monster_monster_place_"+i).remove();
			$("#monster_monster_place_add"+i).remove();
			
		}
		
		
	}
	function getTriggerTiming(){
		$.ajax({
			   'type': "POST",
			   'url': "/tcgcreator/get_timing/",
			   'data': "",
			'success': function(data){
					$("#timing").show();
					$("#timing").draggable();
					$("#timing").offset({top:0,left:200});
					$("#timing_phase").html(data);
			        } 
				})
        } 
	function putTiming(){
		var phase = $("#timing_phase").val();
		
		$("#id_trigger_timing").val(phase);	
	}
	function getMonsterEffectNextSpecify(id){
	        name=$("#"+id+"_name_specify").val();
	        monster_effect_val=$("#"+id+"_effect_kind").val();
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_monster_effect_wrapper_specify/",
		   'data': "name="+name+"&monster_effect_val="+monster_effect_val,
			'success': function(data){
				$("#"+id).html(data);
			}
	    });
	}
