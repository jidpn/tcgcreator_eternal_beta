	var prev;
	var monster_kind_id = [];
	var cost_kind_i = 0;
	$(document).ready(function(){
	
	$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_monster_kind/",
   'data': "delete_flag=0&num=0&id=monster_kind_rel&id2=monster_kind_rel",
'success': function(data){
		$("#id_cost_kind_rel").after("<input type=\"button\" onclick=\"changeCostKindNumRel()\" value=\"追加\"><br>");
			$("#id_cost_kind_rel").after(data);
        }
	})
	$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_monster_kind/",
   'data': "delete_flag=0&num=0",
'success': function(data){
		$("#id_cost_kind").after("<input type=\"button\" onclick=\"changeCostKindNum()\" value=\"追加\"><br>");
			$("#id_cost_kind").after(data);
        } 
	})
	});
	function deleteMonsterChangeKind(){
		$("#id_cost_kind").val("");
	}
	function changeCostKindNum(){
		var tmp_str,tmp;
		tmp = $("#id_cost_kind").val();
		tmp_str=$("#monster_kind-0").val();
		if(tmp == ""){
			tmp = tmp_str;
		}else{
			tmp += "_"+tmp_str;
		}
		$("#id_cost_kind").val(tmp);

	}
	function changeCostKindNumRel(){
		var tmp_str,tmp;
		tmp = $("#id_cost_kind_rel").val();
		tmp_str=$("#monster_kind_rel-0").val();
		if(tmp == ""){
			tmp = tmp_str;
		}else{
			tmp += "_"+tmp_str;
		}
		$("#id_cost_kind_rel").val(tmp);

	}

		
