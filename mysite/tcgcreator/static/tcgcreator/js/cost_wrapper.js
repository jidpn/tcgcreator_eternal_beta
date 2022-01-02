	$(document).ready(function(){
		$("#id_cost").after("<input type=\"button\" onclick=\"getCostSpecify('id_cost')\" value=\"絞り込み\"><input type=\"text\" id=\"id_cost_specify\">");
		$("#id_cost").after("<input type=\"button\" onclick=\"getLastCostSpecify('id_cost')\" value=\"最新\"><input type=\"text\" id=\"id_cost_specify\">");
		$("#id_cost_next").after("<input type=\"button\" onclick=\"getCostNextSpecify('id_cost_next')\" value=\"絞り込み\"><input type=\"text\" id=\"id_cost_next_name_specify\"><select id=\"id_cost_next_effect_kind\"></select>");
		$("#id_cost_next").after("<input type=\"button\" onclick=\"getLastCostNextSpecify('id_cost_next')\" value=\"最新\"><input type=\"text\" id=\"id_cost_next_name_specify\"><select id=\"id_cost_next_effect_kind\"></select>");
		$("#id_cost_next2").after("<input type=\"button\" onclick=\"getCostNextSpecify('id_cost_next2')\" value=\"絞り込み\"><input type=\"text\" id=\"id_cost_next2_name_specify\"><select id=\"id_cost_next2_effect_kind\"></select>");
		$("#id_cost_next2").after("<input type=\"button\" onclick=\"getLastCostNextSpecify('id_cost_next2')\" value=\"最新\"><input type=\"text\" id=\"id_cost_next2_name_specify\"><select id=\"id_cost_next2_effect_kind\"></select>");
		if(trigger_flag != 1){
		$("#id_pac").after("<input type=\"button\" onclick=\"getPacCostNextSpecify('id_pac')\" value=\"絞り込み\"><input type=\"text\" id=\"id_pac_name_specify\"><select id=\"id_pac_effect_kind\"></select>");
		$("#id_pac").after("<input type=\"button\" onclick=\"getLastPacCostNextSpecify('id_pac')\" value=\"最新\"><input type=\"text\" id=\"id_pac_name_specify\"><select id=\"id_pac_effect_kind\"></select>");
		 }
		$("#id_pac2").after("<input type=\"button\" onclick=\"getPacCostNextSpecify('id_pac2')\" value=\"絞り込み\"><input type=\"text\" id=\"id_pac2_name_specify\"><select id=\"id_pac2_effect_kind\"></select>");
		$("#id_pac2").after("<input type=\"button\" onclick=\"getLastPacCostNextSpecify('id_pac2')\" value=\"最新\"><input type=\"text\" id=\"id_pac2_name_specify\"><select id=\"id_pac2_effect_kind\"></select>");
		$("#id_pac_next").after("<input type=\"button\" onclick=\"getPacCostNextSpecify('id_pac_next')\" value=\"絞り込み\"><input type=\"text\" id=\"id_pac_next_name_specify\"><select id=\"id_pac_next_effect_kind\"></select>");
		$("#id_pac_next").after("<input type=\"button\" onclick=\"getLastPacCostNextSpecify('id_pac_next')\" value=\"最新\"><input type=\"text\" id=\"id_pac_next_name_specify\"><select id=\"id_pac_next_effect_kind\"></select>");
		$("#id_pac_next2").after("<input type=\"button\" onclick=\"getPacCostNextSpecify('id_pac_next2')\" value=\"絞り込み\"><input type=\"text\" id=\"id_pac_next2_name_specify\"><select id=\"id_pac_next2_effect_kind\"></select>");
		$("#id_pac_next2").after("<input type=\"button\" onclick=\"getLastPacCostNextSpecify('id_pac_next2')\" value=\"最新\"><input type=\"text\" id=\"id_pac_next2_name_specify\"><select id=\"id_pac_next2_effect_kind\"></select>");
		$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_effect_kind/",
   'data': "",
'success': function(data){
		$("#id_cost_next_effect_kind").html(data);
		$("#id_cost_next2_effect_kind").html(data);
		$("#id_pac_effect_kind").html(data);
		$("#id_pac2_effect_kind").html(data);
		$("#id_pac_next_effect_kind").html(data);
		$("#id_pac_next2_effect_kind").html(data);
		}});
		});
	function getCostSpecify(id){
	        name=$("#"+id+"_specify").val();
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_cost/",
		   'data': "name="+name,
			'success': function(data){
				$("#"+id).html(data);
			}
	    });
	}
	function getLastCostSpecify(id){
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_last_cost/",
			'success': function(data){
				$("#"+id).html(data);
			}
	    });
	}
	function getCostNextSpecify(id){
	        name=$("#"+id+"_name_specify").val();
	        cost_val=$("#"+id+"_effect_kind").val();
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_cost_wrapper_specify/",
		   'data': "name="+name+"&cost_val="+cost_val,
			'success': function(data){
				$("#"+id).html(data);
			}
	    });
	}
	function getLastCostNextSpecify(id){
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_last_cost_wrapper_specify/",
		   'data': "",
			'success': function(data){
				$("#"+id).html(data);
			}
	    });
	}
	function getPacCostNextSpecify(id){
	        name=$("#"+id+"_name_specify").val();
	        pac_val=$("#"+id+"_effect_kind").val();
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_pac_cost_wrapper_specify/",
		   'data': "name="+name+"&cost_val="+pac_val,
			'success': function(data){
				$("#"+id).html(data);
			}
	    });
	}
	function getLastPacCostNextSpecify(id){
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_last_pac_cost_wrapper_specify/",
			'success': function(data){
				$("#"+id).html(data);
			}
	    });
	}
