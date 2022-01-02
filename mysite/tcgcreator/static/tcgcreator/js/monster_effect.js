	var prev;
	var monster_kind_id = [];
	var effect_move_i = 0;
	var global_monster_move_val = 1;
	var global_monster_condition_val = 1;
	var monster_or_global;	
 	function displayMonsterMove(i){
		var j;
		for(j=1;$("#monster_move_"+j).length != 0;j++){
			$("#monster_move_"+j).hide();
		}
		$("#monster_move_"+i).show();
	}
	$(document).ready(function(){
	
		hideAllWindow();
		$("#id_monster_condition").after("<input type=\"button\" onclick=\"getConditionKind('monster_condition',1)\" value=\"追加\">");
		switch($("#id_monster_effect_val").val()){

            case "62":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"showEach()\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break
            case "59":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"showCheckForce()\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
		        break;
		    case "18":
		    case "51":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectTimingVariable()\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
		        break;
			case "66":
			case "67":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMultipleChoice('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");

                            break;
		    case "57":
		    case "65":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectAs('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");

                            break;
		    case "25":
			case "70":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectRelation('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
		        break;

			case "12":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getRaiseTrigger(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break;
			case "11":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getClear(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break;
			case "33":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getClearRelation(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break;
			case "34":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getChangeValByMonster(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break;
			case "35":
			case "71":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getCopyMonster(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break;
			case "36":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getUnderMonster(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break;
			case "50":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getOverMonster(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break;
			case "38":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getUndoRelateMonster(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break;
			case "37":
			case "48":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"CopyEffect()\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				$("#put_copy_effect_cost").hide();
				break;
			case "10":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getShuffle('id_monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break;
			case "5":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterChooseBoth('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				$("#monster_who").show();
				break;
				case "30":
				case "31":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterMultiple('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				$("#monster_who").show();
				break;
			case "1":
			case "72":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectMovePlace('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
			break;
			case "73":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectMovePlace2('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
			break;
			case "40":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectMovePlace('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
			break;
			case "43":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectGetSelectTrigger('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
			break;
			case '3':
			case "4":
			case "44":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectMove('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				$("#monster_who").hide();
				break;
			case "16":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectYesOrNo('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
			break;
			case "7":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectMovePhase(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
			break;
			case "14":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectChangeTiming(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
			break;
			case "41":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectCheckTimingAndPhase(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
			break;
			case "8":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectChangeTurn(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
			break;
			case "2":
			case "49":
			case "53":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getVariableChange(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteVariableChange(0)\" value=\"削除\"><br>");
				break;
			case "29":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getVariableChangeMultiple(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteVariableChange(0)\" value=\"削除\"><br>");
				break;
			case "9":
			case "32":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterVariableChange('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteVariableChange(0)\" value=\"削除\"><br>");
				break;
			case "27":
			case "28":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getChainVariableChange('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break;
			case "63":
			case "64":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getGlobalVariableChange('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break;
			}
		
		$("#id_monster_effect_val").change(function(){
		hideAllWindow();
			switch($("#id_monster_effect_val").val()){
            case "62":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"showEach()\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break
            case "59":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"showPutForce()\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
		        break;
			case "43":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectGetSelectTrigger('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
			break;
                    case "18":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectTimingVariable()\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
                            break;


			case "1":
			case "72":
			case "40":
		    case "17":
		    case "51":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectMovePlace('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				$("#monster_who").hide();
				break;
			case "73":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectMovePlace2('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
			break;
		    case "25":
			case "70":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectRelation('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
		        break;
			case "12":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getRaiseTrigger(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break;
			case "11":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getClear(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break;
			case "33":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getClearRelation(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break;
			case "34":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getChangeValByMonster(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break;
				case "10":
				    $("#id_monster_effect").after("<input type=\"button\" onclick=\"getShuffle('id_monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break;
			case "35":
			case "71":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getCopyMonster(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break;
			case "36":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getUnderMonster(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break;
			case "50":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getOverMonster(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break;
			case "38":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getUndoRelateMonster(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break;
			case "37":
			case "48":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"CopyEffect()\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				$("#put_copy_effect_cost").hide();
				break;
			case "16":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectYesOrNo('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
			break;
			case "66":
			case "67":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMultipleChoice('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");

                            break;
		    case "57":
		    case "65":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectAs('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");

                            break;
				case "3":
				case "4":
				case "44":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectMove('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				$("#monster_who").hide();
				break;
				case "5":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterChooseBoth('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				$("#monster_who").show();
				break;
				case "30":
				case "31":
				$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterMultiple('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				$("#monster_who").show();
				break;
			case "7":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectMovePhase(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
			break;
			case "8":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectChangeTurn(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
			break;
			case "53":
			case "49":
			case "2":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getVariableChange(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteVariableChange(0)\" value=\"削除\"><br>");
				break;
			case "29":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getVariableChangeMultiple(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteVariableChange(0)\" value=\"削除\"><br>");
				break;
			case "9":
			case "32":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterVariableChange('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteVariableChange(0)\" value=\"削除\"><br>");
				break;
			case "14":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectChangeTiming(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
			break;
			case "41":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getMonsterEffectCheckTimingAndPhase(0)\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
			break;
			case "27":
			case "28":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getChainVariableChange('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break;
			case "63":
			case "64":
			$("#id_monster_effect").after("<input type=\"button\" onclick=\"getGlobalVariableChange('monster_effect')\" value=\"追加\"><input type=\"button\" onclick=\"deleteMonsterEffect(0)\" value=\"削除\"><br>");
				break;
				}
		});
	});

    function putClearRelation(){
		var tmp = $("#clear_place_relation").val();
		var relation_name = $("#clear_relation_name").val();
		var relation_kind = $("#clear_relation_kind").val();
		var relation_to = $("#clear_relation_to").val();
		json = {};
		json["place"] = {};
		json["place"][0] =  tmp;
		json["relation"] = {};
		json["relation"]["relation_name"]= relation_name
		json["relation"]["relation_kind"]= relation_kind
		json["relation"]["relation_to"]= relation_to
		val2 = [];
		val2.push(json)
		val = JSON.stringify(val2);
		$("#id_monster_effect").val(val);
    }
	function putClear(){
		var tmp = $("#clear_place").val();
		json = {};
		json["place"] = {};
		json["place"][0] =  tmp;
		val2 = [];
		val2.push(json)
		val = JSON.stringify(val2);
		$("#id_monster_effect").val(val);
		
	}
	function putVariableChange(){
		var val =  {};
		val["variable_name"] = $("#variable_name").val();
		val["variable_who"] = parseInt($("#variable_who").val());
		val["variable_change_how"] = parseInt($("#variable_change_how").val());
		val["variable_change_val"] = $("#variable_change_val").val();
		$("#id_monster_effect").val(JSON.stringify(val));
		$("#variable_change").hide();
		
	}
	function putVariableChangeMultiple(){
		var val =  {};
		if($("#id_monster_effect").val() == ""){
		       json = []
		}else{
		    json = JSON.parse($("#id_monster_effect").val())
		}
		val["variable_name"] = $("#variable_name").val();
		val["variable_who"] = parseInt($("#variable_who").val());
		val["variable_change_how"] = parseInt($("#variable_change_how").val());
		val["variable_change_val"] = $("#variable_change_val").val();
		json.push(val);
		$("#id_monster_effect").val(JSON.stringify(json));
		$("#variable_change").hide();

	}
	function getGlobalVariableChange(i){

		$("#monster_effect_global_variable").show();
		$("#monster_effect_global_variable").draggable();
		$("#monster_effect_global_variable").offset({top:0,left:200});
    getGlobalVariableForInut(); ;
	}
	function putGlobalVariableChange(){
	    val = {};
		val["min_equation_number"] = $("#global_variable_min").val();
		val["max_equation_number"] = $("#global_variable_max").val();
		val["chain_variable"] = $("#global_variable").val();
		$("#id_monster_effect").val(JSON.stringify(val));
		$("#monster_effect_globaln_variable").hide();

	}
	function getChainVariableChange(i){

		$("#monster_effect_chain_variable").show();
		$("#monster_effect_chain_variable").draggable();
		$("#monster_effect_chain_variable").offset({top:0,left:200});
	}
	function getMonsterEffectYesOrNo(i){
		$("#monster_effect_yes_or_no").show();
		$("#monster_effect_yes_or_no").draggable();
		$("#monster_effect_yes_or_no").offset({top:0,left:200});
	}
	function getUnderMonster(){
		getConditionKind("monster_effect",36,100,0);
	}
	function getOverMonster(){
		getConditionKind("monster_effect",50,100,0);
	}
	function getUndoRelateMonster(){
		getConditionKind("monster_effect",38,100,0);
	}
	function getCopyMonster(){
		getConditionKind("monster_effect",35,100,0);
		$("#trigger_condition_copy_monster").show();
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_variables_condition_for_copy/",
		   'data': "id=copy_monster",
			'success': function(data){
				$("#copy_monster_change_val").html(data);
			}
		});
	}
	function getChangeValByMonster(){
		getConditionKind("monster_effect",0,100,0);
        var val = $("#id_monster_effect").val();
        if( val != ""){
            val = JSON.parse(val);
        }
		$("#variable_change_by_monster").show();
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_variable_kind/",
		   'data': "",
			'success': function(data){
				$("#variable_name_by_monster").html(data);
				if(val != ""){
                    $("#variable_name_by_monster").val(val["variable_name"]);
                    $("#variable_who_by_monster").val(String(val["variable_who"]) );
		            $("#variable_change_how_by_monster").val(String(val["variable_change_how"]));
		            $("#variable_change_val_by_monster").val(val["variable_change_val"]);
		        }

		    }
        });
	}
	function getMonsterEffectMovePhase(i){
		$("#monster_effect_phase_move").show();
		$("#monster_effect_phase_move").draggable();
		$("#monster_effect_phase_move").offset({top:0,left:200});
		getMonsterEffectPhase(i);
	}
	function getMonsterEffectTimingVariable(){
		$("#monster_effect_timing_variable").show();
		$("#monster_effect_timing_variable").draggable();
		$("#monster_effect_timing_variable").offset({top:0,left:200});
        $("#timing_variable_org_monster").val("");
        $("#timing_variable_monster").val("");
	}
	function getMonsterEffectChangeTiming(i){
		$("#monster_effect_change_timing").show();
		$("#monster_effect_change_timing").draggable();
		$("#monster_effect_change_timing").offset({top:0,left:200});
		getMonsterEffectChangeTimingDet(i);
	}
	function getClearRelation(i){
		$("#clear_relation").show();
		$("#clear_relation").draggable();
		$("#clear_relation").offset({top:0,left:200});
		$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_place_kind/",
   'data': "",
'success': function(data){
		$("#clear_place_relation").html(data);
		$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_effect_kind/",
   'data': "",
'success': function(data){
		$("#clear_relation_kind").html(data);
		}});
		}});
	}
	function getClear(i){
		$("#clear").show();
		$("#clear").draggable();
		$("#clear").offset({top:0,left:200});
		$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_place_kind/",
   'data': "",
'success': function(data){
		$("#clear_place").html(data);
		}});
	}
	function getMonsterEffectChangeTurn(i){
		$("#monster_effect_change_turn").show();
		$("#monster_effect_change_turn").draggable();
		$("#monster_effect_change_turn").offset({top:0,left:200});
	}
	function getVariableChange(i){
		$("#variable_change").show();
		$("#variable_change").draggable();
		$("#variable_change").offset({top:0,left:200});
		$("#variable_change_multiple").hide()
		$("#variable_change_single").show()
		getMonsterEffectVariable(i);
	}
	function getVariableChangeMultiple(i){
		$("#variable_change").show();
		$("#variable_change").draggable();
		$("#variable_change").offset({top:0,left:200});
		$("#variable_change_multiple").show()
		$("#variable_change_single").hide()
		getMonsterEffectVariable(i);
	}
	function deleteVariableChange(){
		$("#id_monster_effect").val("");
	}
	
	function deleteMonsterEffect(i){
		$("#id_monster_effect").val("");
	}
	function deleteMonsterChange(i){
		for(var i=0;i<current_i;i++){
			$("#monster_kind-"+i).remove()
		}
		$("#id_monster_effect_move_kinds").val("");
		current_i=0;
	}
	function changeEffectMoveNum(){
		var tmp_str = "";
		for(var i=0;i<current_i;i++){
			tmp_str+=$("#monster_kind-"+(i)).val()+"_";;
		}
		tmp_str = tmp_str.substr(0,tmp_str.length-1);
		$("#id_monster_effect_move_kinds").val(tmp_str);

	}
	function getMonsterEffectMoveKindPlace(num){
		$("#monster_effect_move").show();
		$("#monster_effect_move").offset({top:0,left:200});
		$("#monster_monster_effect_move").hide();
		$("#monster_monster_effect_move_how_main").hide();
		$("#monster_equation").hide();
		$("#monster_monster_effect_move_to").hide();
		$("#monster_monster_effect_move_how_main_to").hide();
		$("#monster_equation_to").hide();
	}
	function getMonsterEffectMoveKind(num){
		$("#monster_effect_move").show();
		$("#monster_effect_move").offset({top:0,left:200});
		$("#monster_monster_effect_move").hide();
		$("#monster_monster_effect_move_how_main").hide();
		$("#monster_equation").hide();
	}
	function getMonsterEffectVariable(){
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_variable_kind/",
		   'data': "",
			'success': function(data){
				$("#variable_name").html(data);
			}
		});
	}
	function getMonsterEffectChangeTimingDet(){
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_tcg_timing/",
		   'data': "",
			'success': function(data){
				$("#monster_change_timing").html(data);
			}
		});
	}
	function getMonsterEffectPhase(){
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_phase/",
		   'data': "",
			'success': function(data){
				$("#monster_change_phase").html(data);
			}
		});
	}
	function getWhetherIsFieldTo(val){
		var tmp = val.split("_");
		if(tmp[0] == "field"){
			$("#field_to").show();
			$("#field_x_to").show();
			$("#field_y_to").show();
		}else{
			$("#field_to").hide();
			$("#field_x_to").hide();
			$("#field_y_to").hide();
		}
	}
	function getWhetherIsField(val){
		var tmp = val.split("_");
		if(tmp[0] == "field"){
			$("#field_whether_monster_exists").show();
			$("#field_x").show();
			$("#field_y").show();
		}else{
			$("#field_x").hide();
			$("#field_y").hide();
			$("#field_whether_monster_exists").hide();
		}
	}
	function getMonsterEffectMoveKind2(num){
	if($("#id_monster_effect").val() == ""){
			$("#as_monster_to").show();
		$("#as_monster_from").show();
	$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_place_kind/",
   'data': "i=1",
'success': function(data){
		$(".monster_effect_move_place").show();
		$("#monster_effect_move_place_1_0").html(data);
		$.ajax({
			   'type': "POST",
			   'url': "/tcgcreator/get_monster/",
			   'data': "i=1",
			'success': function(data){
						$("#monster_monster_effect_move_1").show();
						$("#monster_monster_effect_how_main").show();
						$("#monster_monster_effect_move_1").html(data);
					$.ajax({
			  			 'type': "POST",
			  			 'url': "/tcgcreator/get_equation/",
			  			 'data': "num=1",
						'success': function(data){
									$("#monster_equation").show();
									$("#monster_equation").html(data);
			      		 } 
					})
			        } 
				})
		}
	})
	}else{
		getMonsterEffectMoveKindWithData();
	}	
	}
	function getMonsterEffectMoveKindWithData(){
		val = $("#id_monster_effect").val();
		val = JSON.parse(val);
		equ = val["equation"];
		val2 = val;
		val = val["monster"];
	for(i=1;i<=val.length;i++){
		$("#change_button_move_"+(i-1)).after('<input type="button" value="移動元'+i+'" onclick="displayMove('+i+')" id="change_button_move_'+i+'">');
              (function(i){
	$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_place_kind/",
   'data': "i="+i,
'success': function(data){
		$(".monster_effect_move_place").show();
		for(l=0;l<val[i-1]["place"].length;l++){
		$("#monster_effect_move_place_"+i+"_"+l).html(data);
		if($("#monster_effect_move_place_"+i+"_"+l).length==0){
			addPlace("monster_effect_move_place",i,l);
		}
		$("#monster_effect_move_place_"+i+"_"+l).val( val[i-1]["place"][l]["det"]);
		$("#monster_effect_move_place_add_"+i+"_"+l).val(val[i-1]["place"][l]["and_or"]);
		}
              (function(i){
		$.ajax({
			   'type': "POST",
			   'url': "/tcgcreator/get_monster/",
   				'data': "i="+i,
			'success': function(data){
					$("#monster_monster_effect_move_"+i).show();
					$("#monster_monster_effect_move_"+i).html(data);
					$("#flag_equal_"+i).val(val[i-1]["flag"]["operator"]);
					$("#get_monster_name_equal_"+i).val(val[i-1]["monster_name_kind"]["operator"]);
					$("#get_monster_name_"+i).val(val[i-1]["monster_name_kind"]["monster_name"]);
					for(j=1;j<=val[i-1]["monster_condition"].length;j++){
						for(var k=0;k<=val[i-1]["monster_condition"][j-1].length;k++){
							if(val[i-1]["monster_condition"][j-1][k] == undefined){
								continue;
							}
							if(k!=0){
								addMonsterEquation(i+"_"+j+"_"+(k-1));
							}
							$("#get_monster_variable_equal_"+i+"_"+j+"_"+k).val(val[i-1]["monster_condition"][j-1][k]["operator"]);
							$("#get_monster_variable_"+i+"_"+j+"_"+k).val(val[i-1]["monster_condition"][j-1][k]["num"]);
							$("#monster_variable_and_or_"+i+"_"+j+"_"+k).val(val[i-1]["monster_condition"][j-1][k]["and_or"]);
						}
					}
						$("#field_x").val(val[i-1]["field_x"]);
						$("#field_y").val(val[i-1]["field_y"]);
						if(val[i-1]["whether_monster"]){
						    $("monster_exist").prop("checked",true);
						}

					
					if(i==1){
					$.ajax({
			  			 'type': "POST",
			  			 'url': "/tcgcreator/get_equation/",
			  			 'data': "num=1",
						'success': function(data){
							$(".monster_equation").show();
							$("#monster_equation").html(data);
							$("#as_monster_effect_from").val(val2["as_monster_effect_from"]);
							$("#as_monster_effect_to").val(val2["as_monster_effect_to"]);
							$("#min_equation_number").val(val2["min_equation_number"]);
							$("#max_equation_number").val(val2["max_equation_number"]);
						$("#field_x_to").val(val2["field_x_to"]);
						$("#field_y_to").val(val2["field_y_to"]);
			      		 } 
					})
					}
			        } 
				})
				})(i)
		}
	})
	})(i)
	}
	}
	function addMonsterEffectName(i){
		var html = '<input type="text" id="monster_name_det_'+(i+1)+'">';
		html+='<select id="monster_name_add_'+(i+1)+'" onchange="addMonsterEffectName('+(i+1)+')" class="monster_effect_move_place" style="display:none"><option value=""></option><option value="and">かつ</option><option value="or">または</option></select>';
		$("#monster_name_add_"+i).after(html);
	}
	function addMonsterEffectMovePlace(){
	global_monster_move_val++;
	i = global_monster_move_val;
	
	$("#change_button_monster_move_"+(i-1)).after('<input type="button" value="条件'+i+'" onclick="displayMonsterMove('+i+')" id="change_button_monster_move_'+i+'">');
		$.ajax({
			   'type': "POST",
			   'url': "/tcgcreator/get_monster/",
			   'data': "i="+i,
			'success': function(data){
		$("#monster_move_"+(i-1)).after('<div id="monster_move_'+i+'"><div id="monster_monster_effect_move_'+i+'" style=""></div> </div> <div id="monster_equation_'+i+'" class="monster_equation" style=""></div> </div> </div>');
					$("#monster_monster_effect_move_"+i).show();
					$("#monster_monster_effect_move_"+i).html(data);
 					displayMonsterMove(i);
			        } 
		})
		}
	function addMonsterEffectMovePlaceTo(i){
		var html= $("#monster_effect_move_place_1_to").html();
		var html = '<select id="monster_effect_move_place_'+(i+1)+'_to" class="monster_effect_move_place" >'+html+'</select>';
		html+='<select id="monster_effect_move_place_add_1_to" onchange="addMonsterEffectMovePlaceTo('+(i+1)+')" class="monster_effect_move_place" style="display:none"><option value=""></option><option value="and">かつ</option><option value="or">または</option></select>';
		$("#monster_effect_move_place_add_"+i+"_to").after(html);
	}
	function putChainVariableChange(){
	    val = {};
		val["min_equation_number"] = $("#chain_variable_min").val();
		val["max_equation_number"] = $("#chain_variable_max").val();
		val["chain_variable"] = $("#chain_variable").val();
		$("#id_monster_effect").val(JSON.stringify(val));
		$("#monster_effect_chain_variable").hide();

	}
	function putMonsterEffectYesOrNo(){
	    val = {};
		val["mine_or_other"] = $("#yes_or_no").val();
		$("#id_monster_effect").val(JSON.stringify(val));
		$("#monster_effect_yes_or_no").hide();

	}
	function putMonsterEffectTimingToVariable(){
		var val =  {};
		val["org_val"] = $("#timing_variable_org_monster").val();
		val["val"] = $("#timing_variable_monster").val();
		$("#id_monster_effect").val(JSON.stringify(val));
		$("#monster_effect_timing_variable").hide();

	}
	function putMonsterEffectChangeTurn(){
		var val =  {};
		val["change_turn"] = 1;
		if($("#turn_end_change_turn_flag").prop("checked") == false){
		       val["turn_count_change"] = false;
		}else{
		       val["turn_count_change"] = true;
		}
		$("#id_monster_effect").val(JSON.stringify(val));
		$("#monster_effect_change_turn").hide();
		
	}
	function putMonsterEffectMovePhase(){
		var val =  {};
		val["move_to_phase"] = parseInt($("#monster_change_phase").val());
		$("#id_monster_effect").val(JSON.stringify(val));
		$("#monster_effect_phase_move").hide();
		
	}
	function putMonsterEffectChangeTiming(){
		var val =  {};
		val["move_to_timing"] = parseInt($("#monster_change_timing").val());
		val["t_num"] = parseInt($("#t_num").val());
		val["timing_fresh"] = false;
		$("#id_monster_effect").val(JSON.stringify(val));
		$("#monster_effect_change_timing").hide();
		
	}
	function putMonsterEffectMove(){
		if($("#min_equation_number").val() == "" || $("#max_equation_number").val() == "" ){
			alert("input min and max");
			return;
		}
		var val;
		var k;
		var place;
		val = {};
		val["monster"] = []
		
		var json={};
		json = {};
		place = [];
		for(l=0;$("#monster_effect_move_place_"+1+"_"+l).val();l++){
		place[l] = {};
		var and_or = $("#monster_effect_move_place_add_"+1+"_"+l).val();
		place[l]["and_or"] = and_or;
			var tmp = $("#monster_effect_move_place_"+1+"_"+l).val();
			if(tmp != "0"){
				place[l]["det"] =  tmp;
			}
		}
		for(var i=1;$("#get_monster_name_equal_"+i).length;i++){
			json = {};
			json["place"] = place;
		var j=0;
		if($("#get_monster_name_equal_"+i).val() == ""){
			json["monster_name_kind"] = "";
		}else if($("#get_monster_name_equal_"+i).val() == "="){
			json["monster_name_kind"] = {};
			json["monster_name_kind"]["operator"] = "=";
			json["monster_name_kind"]["monster_name"] =$("#monster_name_"+i).val();
		}else{
			json["monster_name_kind"] = {};
			json["monster_name_kind"]["operator"] = "like";
			json["monster_name_kind"]["monster_name"] =$("#monster_name_"+i).val();
		}
		if($("#flag_equal_"+i).val() == ""){
			json["flag"] = "";
		}else{
			json["flag"] = {};
			json["flag"]["operator"] = "=";
			json["flag"]["flag_det"] =$("#flag_"+i).val();
		}
		json["monster_condition"] = [];
		for(var j=1;$("#get_monster_variable_"+i+"_"+j+"_0").length != 0;j++){
			json["monster_condition"][j-1] = [];
			for(k=0;$("#get_monster_variable_"+i+"_"+j+"_"+k).length != 0;k++){
			json["monster_condition"][j-1][k] = {};
			if($("#get_monster_variable_equal_"+i+"_"+j+"_"+k).length != 0){
				num = $("#get_monster_variable_"+i+"_"+j+"_"+k).val();
				operator = $("#get_monster_variable_equal_"+i+"_"+j+"_"+k).val();
				and_or = $("#monster_variable_and_or_"+i+"_"+j+"_"+k).val();
				if(operator == ""){
					continue;
				}
				json["monster_condition"][j-1][k]["num"] = num;
				json["monster_condition"][j-1][k]["operator"] = operator;
				json["monster_condition"][j-1][k]["and_or"] = and_or;
					
			}else{
				num = $("#get_monster_variable_"+i+"_"+j+"_"+k).val();
				and_or = $("#monster_variable_and_or_"+i+"_"+j+"_"+k).val();
				if(num == "" || num==0){
					continue;
				}
				json["monster_condition"][j-1][k]["num"] = num;
				json["monster_condition"][j-1][k]["operator"] = "";
				json["monster_condition"][j-1][k]["and_or"] = and_or;
			}
			}
			
		}
		if($("#field_x").val() != ""){
			json["field_x"] = $("#field_x").val();
		}
		if($("#field_y").val() != ""){
			json["field_y"] = $("#field_y").val();
		}
		val["monster"].push(json);
		}
		val["sentence"] = $("#monster_sentence").val();
		val["move_how"] = $("#monster_effect_move_how_"+i).val();
		if( $("#min_equation_number").val()){
			val["min_equation_number"] = $("#min_equation_number").val();
		}else{
			val["min_equation_number"] = 1;
		}
		if( $("#max_equation_number").val()){
			val["max_equation_number"] = $("#max_equation_number").val();
		}else{
			val["max_equation_number"] = 1;
		}
		val["as_monster_effect_from"] = $("#as_monster_effect_from").val();
		val["exclude"] = $("#exclude_monster_variable_change").val();
		if($("#field_x_to").val() != ""){
			val["field_x_to"] = $("#field_x_to").val();
		}
		if($("#field_y_to").val() != ""){
			val["field_y_to"] = $("#field_y_to").val();
		}
		if($("#flag_add_det").prop("checked") == true){
			val["flag_add"] = true;
		}else{
			val["flag_add"] = false;
		}
		val = JSON.stringify(val);
		$("#id_monster_effect").val(val);
		$("#monster_effect_move").hide();
		$("#monster_monster_effect_move_1").hide();
		$("#monster_equation").hide();
		$(".monster_effect_move_place").hide();
		for(var i=1;$("#monster_effect_move_place_"+(i)+"_0").length;i++){
			for(var j=0;$("#monster_effect_move_place_"+i+"_"+j).length;j++){
				if(i==1 && j==0){
					continue;
				}
				$("#monster_effect_move_place_"+i+"_"+j).remove();
			}
			if(i!=1){
			$("#monster_monster_effect_move_"+i).remove();
			}
			
		}
		
		
	}
	function  hideAllWindow(){
		$("#monster_effect_phase_move").hide();
		$("#monster_effect_change_turn").hide();
		$("#variable_change").hide();
		$("#monster_variable_change").hide();
		$("#monster_effect_move").hide();
		$("#variable_change_by_monster").hide();
	}
	function getMonsterConditionVariables(){
		$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_variable_kind/",
		   'data': "",
		'success': function(data){
			$(".variable_condition").show();
			$("#variable_condition_1").html(data);
		}
		});
	}
	function putMonsterCondition(){
		if($("#min_equation_number").val() == "" || $("#max_equation_number").val() == "" ){
			alert("input min and max");
			return;
		}
		var k=0;
		var l=0;
			val = {};
			val["monster"] = []
			val["variable"] = []
			
		var tmp2 = $("#variable_condition_1").val();
		var json = {};
		
		if(tmp2 != "0" && tmp2!="" && tmp2!=null){
			json = {};
			for(var i=1;$("#variable_condition_add_"+(i-1)).val();i++){
				tmp_json={}
				var tmp = $("#variable_condition_"+i).val();
				var operator = $("#variable_condition_equation_"+(i-1)).val();
				var variable_val = $("#variable_equation_val_"+(i-1)).val();;
				var and_or = $("#variable_condition_add_"+(i-1)).val()
				if(tmp != "0"){
					tmp_json["variable"] =  tmp;
					tmp_json["varaiable_equation"] =  operator;
					val["variable"].push(tmp_json)
				}
			}
		}
		json["place"] = [];
		for(l=0;$("#monster_condition_place_"+1+"_"+l).val();l++){
		json["place"][l] = {};
		var and_or = $("#monster_condition_place_add_"+1+"_"+l).val();
		json["place"][l]["and_or"] = and_or;
			var tmp = $("#monster_condition_place_"+1+"_"+l).val();
			if(tmp != "0"){
				json["place"][l]["det"] =  tmp;
			}
		}
		for(var i=1;$("#get_monster_name_equal_"+i).length;i++){
		if($("#get_monster_name_equal_"+i).val() == ""){
			json["monster_name_kind"] = "";
		}else if($("#get_monster_name_equal").val() == "="){
			json["monster_name_kind"] = {};
			json["monster_name_kind"]["operator"] = "=";
			json["monster_name_kind"]["monster_name"] =$("#monster_name_"+i).val();
		}else{
			json["monster_name_kind"] = {};
			json["monster_name_kind"]["operator"] = "like";
			json["monster_name_kind"]["monster_name"] =$("#monster_name_"+i).val();
		}
		if($("#flag_equal_"+i).val() == ""){
			json["flag"] = "";
		}else{
			json["flag"] = {};
			json["flag"]["operator"] = "=";
			json["flag"]["flag_det"] =$("#flag_"+i).val();
		}
		json["monster_condition"] = [];
		for(var j=1;$("#get_monster_variable_"+i+"_"+j+"_0").length != 0;j++){
			json["monster_condition"][j-1] = [];
			for(k=0;$("#get_monster_variable_"+i+"_"+j+"_"+k).length != 0;k++){
			json["monster_condition"][j-1][k] = {};
			if($("#get_monster_variable_equal_"+i+"_"+j+"_"+k).length != 0){
				num = $("#get_monster_variable_"+i+"_"+j+"_"+k).val();
				operator = $("#get_monster_variable_equal_"+i+"_"+j+"_"+k).val();
				and_or = $("#monster_variable_and_or_"+i+"_"+j+"_"+k).val();
				if(operator == ""){
					continue;
				}
				json["monster_condition"][j-1][k]["num"] = num;
				json["monster_condition"][j-1][k]["operator"] = operator;
				json["monster_condition"][j-1][k]["and_or"] = and_or;
					
			}else{
				num = $("#get_monster_variable_"+i+"_"+j+"_"+k).val();
				and_or = $("#monster_variable_and_or_"+i+"_"+j+"_"+k).val();
				if(num == "" || num==0){
					continue;
				}
				json["monster_condition"][j-1][k]["num"] = num;
				json["monster_condition"][j-1][k]["operator"] = "";
				json["monster_condition"][j-1][k]["and_or"] = and_or;
			}
			}
			
		}
		val["monster"].push(json);
		}
		if($("#as_monster_effect_condition").val() != ""){
			val["as_monster_condition"] = $("#as_monster_effect_condition").val();
		}
		if($("#as_cost_monster_effect_condition").val() != ""){
			val["as_cost_monster_condition"] = $("#as_cost_monster_effect_condition").val();
		}
		val["min_equation_number"] = $("#min_equation_number").val();
		val["max_equation_number"] = $("#max_equation_number").val();
		val["equation"] = {};
		val["equation"]["equation"] = $("#get_equation_det_"+i).val();
		val["equation"]["equation_kind"] = $("#get_equation_kind"+i).val();
		val["equation"]["equation_number"] = $("#get_equation_number"+i).val();
		var j=0;
		val =  JSON.stringify(val);
		$("#id_monster_condition").val(val);
		$(".monster_condition_place").hide();
		$("#monster_condition").hide();
		$("#monster_condition_1").hide();
		$("#monster_condition_place_tab").hide();
		for(var i=2;$("#monster_condition_place_"+i).length;i++){
			$("#monster_condition_place_"+i).remove();
			$("#monster_condition_place_add"+i).remove();
			$("#monster_condition_"+i).remove();
			$("#change_button_"+i).remove();
			
		}
		
		
	}
	function putCheckForce(){
	   var data = {};
	   data["deck_id"] = parseInt($("#check_force_deck_id").val());
	   data["ignore_timing"] = [];
	   var tmp = $("#check_force_ignore_timing").val();
	   var i;
	   for(i=0;i<tmp.length;i++){
	        data["ignore_timing"].push(parseInt(tmp[i]));
	   }
	    $("#id_monster_effect").val(JSON.stringify(data));
	    $("#check_force").hide();
	}
