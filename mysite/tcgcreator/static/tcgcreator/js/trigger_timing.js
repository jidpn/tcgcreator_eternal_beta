monster_kind_i = 0;
	$(document).ready(function(){
		$("#id_trigger").after("<input type=\"button\" onclick=\"getTriggerSpecify('id_trigger')\" value=\"絞り込み\"><input type=\"text\" id=\"id_trigger_specify\"><select id=\"id_trigger_kind\"></select>");
		$("#id_trigger").after("<input type=\"button\" onclick=\"getLastTriggerSpecify('id_trigger')\" value=\"最新\">");
		$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_effect_kind/",
   'data': "",
'success': function(data){
		$("#id_trigger_kind").html(data);
		}});
	$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_monster_kind/",
   'data': "delete_flag=0&num=0&id=kinds&id2=kinds",
'success': function(data){
		$("#id_kinds").after("<input type=\"button\" onclick=\"changeMonsterKindNum('id_kinds','kinds',1)\" value=\"追加\"><br>");
			$("#id_kinds").after(data);
        }
	})
	$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_monster_kind/",
   'data': "delete_flag=0&num=0&id=exist_kinds&id2=exist_kinds",
'success': function(data){
		$("#id_exist_kinds").after("<input type=\"button\" onclick=\"changeMonsterKindNum('id_exist_kinds','exist_kinds',1)\" value=\"追加\"><br>");
			$("#id_exist_kinds").after(data);
        }
	});
	$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_monster_kind/",
   'data': "delete_flag=0&num=0&id=relation_kind&id2=relation_kind",
'success': function(data){
		$("#id_relation_kind").after("<input type=\"button\" onclick=\"changeMonsterKindNum('id_relation_kind','relation_kind',1)\" value=\"追加\"><br>");
			$("#id_relation_kind").after(data);
        }
	});
	});
	function getTriggerTimingKindChangeBefore(){
		getTriggerTimingKindChange(monster_kind_i)
	}
	function changeMonsterKindNum(){
		var tmp_str = "";
		for(var i=0;i<monster_kind_i;i++){
			tmp_str+=$("#monster_kind-"+(i)).val()+"_";;
		}
		tmp_str = tmp_str.substr(0,tmp_str.length-1);
		$("#id_kinds").val(tmp_str);

	}
	function getLastTriggerSpecify(id){
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_last_trigger_specify/",
		   'data': "",
			'success': function(data){
				$("#"+id).html(data);
			}
	    });
	}
	function getTriggerSpecify(id){
	        name=$("#"+id+"_specify").val();
	        trigger_val=$("#"+id+"_kind").val();
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_trigger_specify/",
		   'data': "name="+name+"&trigger_val="+trigger_val,
			'success': function(data){
				$("#"+id).html(data);
			}
	    });
	}
