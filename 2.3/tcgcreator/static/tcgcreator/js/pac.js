$(document).ready(function(){
    var path_name = location.pathname;
    path_name = path_name.substring(0,path_name.length-7)
       $("input[name=\"_saveasnew\"]").before("<input type=\"button\" value=\"diagram\" onclick=\"location.href='"+path_name+"diagram'\">");
		$("#id_pac_next").after("<input type=\"button\" onclick=\"getPacNextSpecify('id_pac_next')\" value=\"絞り込み\"><input type=\"text\" id=\"id_pac_next_name_specify\"><select id=\"id_pac_next_kind\"></select>");
		$("#id_pac_next").after("<input type=\"button\" onclick=\"getLastMonsterEffectNextSpecify('id_pac_next')\" value=\"最新\">");
		$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_effect_kind/",
   'data': "",
'success': function(data){
		$("#id_pac_next_kind").html(data);
		}});
});
	function getPacNextSpecify(id){
	        name=$("#"+id+"_name_specify").val();
	        monster_effect_val=$("#"+id+"_kind").val();
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_pac_wrapper_specify/",
		   'data': "name="+name+"&pac_val="+monster_effect_val,
			'success': function(data){
				$("#"+id).html(data);
			}
	    });
	}
	function getLastMonsterEffectNextSpecify(id){
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_last_monster_effect_wrapper_specify/",
			'success': function(data){
				$("#"+id).html(data);
			}
	    });
	}
