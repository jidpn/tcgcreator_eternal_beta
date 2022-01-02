    $(document).ready(function(){
		$("#id_monster_effect_next").after("<input type=\"button\" onclick=\"getMonsterEffectNextSpecify('id_monster_effect_next')\" value=\"絞り込み\"><input type=\"text\" id=\"id_monster_effect_next_name_specify\"><select id=\"id_monster_effect_next_effect_kind\"></select>");
		$("#id_monster_effect_next").after("<input type=\"button\" onclick=\"getLastMonsterEffectNextSpecify('id_monster_effect_next')\" value=\"最新\">");
		$("#id_monster_effect_next2").after("<input type=\"button\" onclick=\"getMonsterEffectNextSpecify('id_monster_effect_next2')\" value=\"絞り込み\"><input type=\"text\" id=\"id_monster_effect_next2_name_specify\"><select id=\"id_monster_effect_next2_effect_kind\"></select>");
		$("#id_monster_effect_next2").after("<input type=\"button\" onclick=\"getLastMonsterEffectNextSpecify('id_monster_effect_next2')\" value=\"最新\">");
		$("#id_pac_next").after("<input type=\"button\" onclick=\"getPacNextSpecify('id_pac_next')\" value=\"絞り込み\"><input type=\"text\" id=\"id_pac_next_name_specify\"><select id=\"id_pac_next_kind\"></select>");
		$("#id_pac_next").after("<input type=\"button\" onclick=\"getLastPacNextSpecify('id_pac_next')\" value=\"最新\">");
		$("#id_pac_next2").after("<input type=\"button\" onclick=\"getPacNextSpecify('id_pac_next2')\" value=\"絞り込み\"><input type=\"text\" id=\"id_pac_next2_name_specify\"><select id=\"id_pac_next2_kind\"></select>");
		$("#id_pac_next2").after("<input type=\"button\" onclick=\"getLastPacNextSpecify('id_pac_next2')\" value=\"最新\">");
		$("#id_pac").after("<input type=\"button\" onclick=\"getPacSpecify('id_pac')\" value=\"絞り込み\"><input type=\"text\" id=\"id_pac_name_specify\">");
		$("#id_pac").after("<input type=\"button\" onclick=\"getLastPacSpecify('id_pac')\" value=\"最新\">");
		$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_effect_kind/",
   'data': "",
'success': function(data){
		$("#id_pac_next_kind").html(data);
		$("#id_pac_next2_kind").html(data);
		}});
});
	function getPacSpecify(id){
	        name=$("#"+id+"_name_specify").val();
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_pac_specify/",
		   'data': "name="+name,
			'success': function(data){
				$("#"+id).html(data);
			}
	    });
	}
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
	function getLastPacNextSpecify(id){
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_last_pac_wrapper_specify/",
			'success': function(data){
				$("#"+id).html(data);
			}
	    });
	}
	function getLastPacSpecify(id){
			$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_last_pac_specify/",
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
