var trigger_flag = 0;	
$(document).ready(function(){
		$("#id_fusion1").after("<input type=\"button\" onclick=\"getConditionKind('fusion1',0,100,0)\" value=\"追加\">");
		$("#id_fusion2").after("<input type=\"button\" onclick=\"getConditionKind('fusion2',0,100,0)\" value=\"追加\">");
		$("#id_fusion3").after("<input type=\"button\" onclick=\"getConditionKind('fusion3',0,100,0)\" value=\"追加\">");
		$("#id_unique_effect").after("<input type=\"button\" onclick=\"getMonsterEffectNextSpecify('id_unique_effect')\" value=\"絞り込み\"><input type=\"text\" id=\"id_unique_effect_name_specify\"><select id=\"id_unique_effect_effect_kind\"></select>");
		$("#id_unique_effect").after("<input type=\"button\" onclick=\"getLastMonsterEffectNextSpecify('id_unique_effect')\" value=\"最新\">");
	});
