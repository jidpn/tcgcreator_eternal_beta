$(document).ready(function(){
		$("#id_pac_cost").after("<input type=\"button\" onclick=\"getCostSpecify('id_pac_cost')\" value=\"絞り込み\"><input type=\"text\" id=\"id_pac_cost_specify\">");
		$.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_effect_kind/",
   'data': "",
'success': function(data){
		$("#id_pac_next_kind").html(data);
		}});
});
