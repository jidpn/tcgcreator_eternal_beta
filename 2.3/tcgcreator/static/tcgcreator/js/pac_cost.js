
$(document).ready(function(){
		$("#id_pac_cost_next").after("<input type=\"button\" onclick=\"getCostNextSpecify('id_pac_cost_next')\" value=\"絞り込み\"><input type=\"text\" id=\"id_pac_cost_next_name_specify\"><select id=\"id_pac_cost_next_effect_kind\"></select>");
		$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_effect_kind/",
   'data': "",
'success': function(data){
		$("#id_pac_cost_next_effect_kind").html(data);
		}});
});
