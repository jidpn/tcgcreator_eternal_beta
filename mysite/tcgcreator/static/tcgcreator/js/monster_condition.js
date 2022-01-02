    //var global_id2 = "";
    function displayCondition(id,i,j){
        var k;
        for(k=1;$("#"+id+"_"+i+"_"+k).length != 0;k++){
            $("#"+id+"_"+i+"_"+k).hide();
            $("#"+id+"_button_"+i+"_"+k).removeClass("active");
        }
            $("#"+id+"_button_"+i+"_"+j).addClass("active");
        $("#"+id+"_"+i+"_"+j).show();
    }
    function displayConditionAll(id,i){
        var k;
        var j;
        for(k=0;$("#choose_"+id+"_"+k).length != 0;k++){
            $("#as_"+id+"_wrapper_"+k).hide();
            for(j=1;$("#"+id+"_"+k+"_"+j).length;j++){
                $("#"+id+"_"+k+"_"+j).hide();
            }
            $("#"+id+"_wrapper_"+k).hide();
            $("."+id+"_equation").hide();
            $("#choose_"+id+"_"+k).hide();
            $("#choose_"+id+"_"+k).removeClass("active");
        }
        $("#choose_"+id+"_"+i).addClass("active");
        $("#choose_"+id+"_"+i).show();
        $("#"+id+"_"+i+"_"+1).show();
        $("#"+id+"_equation_"+i).show();
        $("#as_"+id+"_wrapper_"+i).show();
    }
    function addConditionPlace(id,i,j){
        if(!(i==0 && j==1)){
            $("#"+id+"_add_button_"+i+"_"+j).remove();
        }else{
            $("#"+id+"_add_button_"+i+"_"+j).hide();
        }
    j++;

    $("#"+id+"_button_"+i+"_"+(j-1)).after('<input type="button" value="条件'+j+'" onclick="displayCondition(\''+id+'\','+i+','+j+')" id="'+id+'_button_'+i+'_'+j+'"><input type="button" value="追加" id="'+id+'_add_button_'+i+'_'+j+'" onclick="addConditionPlace(\''+id+'\','+i+','+j+')">');
        $.ajax({
               'type': "POST",
               'url': "/tcgcreator/get_monster_condition/",
               'data': "i="+i+"&j="+j,
            'success': function(data){
        $("#"+id+"_"+i+"_"+(j-1)).after('<div id="'+id+'_'+i+'_'+j+'"><div id="monster_monster_'+i+'_'+j+'" style=""></div> </div> <div id="monster_equation_'+i+'_'+j+'" class="monster_equation" style=""></div> </div> </div>');
                    $("#monster_monster_"+i+"_"+j).show();
                    $("#monster_monster_"+i+"_"+j).html(data);
                    displayCondition(id,i,j);
                    }
        })
        }
    function ChooseBothWithData(data){
        val = JSON.parse(data);
    $.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_place_kind/",
   'data': "i=1",
'success': function(data){
        $("."+id+"_place").show();
        $("#"+id+"_place_0_0").html(data);
        $.ajax({
               'type': "POST",
               'url': "/tcgcreator/get_monster_condition/",
               'data': "i=1&j=0",
            'success': function(data){
                    $("#"+id+"_0_1").html("<div id=\"monster_monster_0_1\"></div>");

                    $("#monster_monster_0_1").html(data);
                    $.ajax({
                         'type': "POST",
                         'url': "/tcgcreator/get_equation/",
                         'data': "c=0",
                        'success': function(data){
                            $("."+id+"_equation").show();
                            $("#"+id+"_equation_0").html(data);
                         }
                    })
                    $.ajax({
                         'type': "POST",
                         'url': "/tcgcreator/get_field_x_and_y/",
                         'data': "id="+id+"&c=0",
                        'success': function(data){
                            $("."+id+"_field_x_and_y_0").show();
                            $("#"+id+"_field_x_and_y_0").html(data);
                         }
                    })
                    }
                })
        }
    })
    var i=0;
    var j=1;
    $("#choose_"+id+"_"+i).after('<div id="choose_'+id+'_'+j+'"> <input type="button" class="active" value="条件1" onclick="displayCondition(\''+id+'\','+j+',1)" id="'+id+'_button_'+j+'_1"><input type="button" value="追加" id="'+id+'_add_button_'+j+'_1" onclick="addConditionPlace(\''+id+'\','+j+',1)"><br><select id="'+id+'_place_'+j+'_0" class="'+id+'_place" style=""> </select> <select id="'+id+'_place_add_'+j+'_0" onchange="addPlace(\''+id+'_place\','+j+',1)" class="'+id+'_place" style=""> <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select> <div id="'+id+'_'+j+'_1"> </div> <div id="'+id+"_field_x_and_y_"+j+'"></div><div id="'+id+'_equation_'+j+'" class="'+id+'_equation" style=""></div> </div> </div>as<a class="show_as_monster" href="javascript:showAsMonster()">+</a><a style="display:none" class="hide_as_monster" href="javascript:hideAsMonster()">-</a><div "display:none" class="as_monster" id="as_'+id+'_wrapper_'+j+'">as <input type="text" id="as_'+id+'_'+j+'"></div> </div > </div></div>');
    $.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_place_kind/",
   'data': "i="+j,
'success': function(data){
        $("."+id+"_place").show();
        $("#"+id+"_place_"+j+"_0").html(data);
        $.ajax({
               'type': "POST",
               'url': "/tcgcreator/get_monster_condition/",
               'data': "i=1&j="+j,
            'success': function(data){
                    $("#"+id+"_"+j+"_1").html("<div id=\"monster_monster_"+j+"_1\"></div>");

                    $("#monster_monster_"+j+"_1").html(data);
                    $.ajax({
                         'type': "POST",
                         'url': "/tcgcreator/get_equation/",
                         'data': "c="+j,
                        'success': function(data){
                            $("."+id+"_equation").show();
                            $("#"+id+"_equation_"+j).html(data);
                            displayConditionAll(id,0);
                            $.ajax({
                                 'type': "POST",
                                 'url': "/tcgcreator/get_field_x_and_y/",
                                 'data': "id="+id+"&c="+j,
                                'success': function(data){
                                    $("."+id+"_field_x_and_y").show();
                                    $("#"+id+"_field_x_and_y_"+j).html(data);
                                    putConditionVal(0,val);
                                    putConditionVal(1,val);
                         }
                    })
                         }
                    })
                    }
        })
    }});
    }
    function ChooseBoth(){
        if($("#id_"+global_id2).val() != ""){
            ChooseBothWithData($("#id_"+global_id2).val());
            return;
        }
    $.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_place_kind/",
   'data': "i=1",
'success': function(data){
        $("."+id+"_place").show();
        $("#"+id+"_place_0_0").html(data);
        $.ajax({
               'type': "POST",
               'url': "/tcgcreator/get_monster_condition/",
               'data': "i=1&j=0",
            'success': function(data){
                    $("#"+id+"_0_1").html("<div id=\"monster_monster_0_1\"></div>");

                    $("#monster_monster_0_1").html(data);
                    $.ajax({
                         'type': "POST",
                         'url': "/tcgcreator/get_equation/",
                         'data': "c=0",
                        'success': function(data){
                            $("."+id+"_equation").show();
                            $("#"+id+"_equation_0").html(data);
                         }
                    })
                    $.ajax({
                         'type': "POST",
                         'url': "/tcgcreator/get_field_x_and_y/",
                         'data': "id="+id+"&c=0",
                        'success': function(data){
                            $("."+id+"_field_x_and_y_0").show();
                            $("#"+id+"_field_x_and_y_0").html(data);
                         }
                    })
                    }
                })
        }
    })
    var i=0;
    var j=1;
    $("#choose_"+id+"_"+i).after('<div id="choose_'+id+'_'+j+'"> <input type="button" class="active" value="条件1" onclick="displayCondition(\''+id+'\','+j+',1)" id="'+id+'_button_'+j+'_1"><input type="button" value="追加" id="'+id+'_add_button_'+j+'_1" onclick="addConditionPlace(\''+id+'\','+j+',1)"><br><select id="'+id+'_place_'+j+'_0" class="'+id+'_place" style=""> </select> <select id="'+id+'_place_add_'+j+'_0" onchange="addPlace(\''+id+'_place\','+j+',1)" class="'+id+'_place" style=""> <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select> <div id="'+id+'_'+j+'_1"> </div> <div id="'+id+"_field_x_and_y_"+j+'"></div><div id="'+id+'_equation_'+j+'" class="'+id+'_equation" style=""></div> </div> </div>as<a class="show_as_monster" href="javascript:showAsMonster()">+</a><a style="display:none" class="hide_as_monster" href="javascript:hideAsMonster()">-</a><div "display:none" class="as_monster" id="as_'+id+'_wrapper_'+j+'">as <input type="text" id="as_'+id+'_'+j+'"></div> </div > </div></div>');
    $.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_place_kind/",
   'data': "i="+j,
'success': function(data){
        $("."+id+"_place").show();
        $("#"+id+"_place_"+j+"_0").html(data);
        $.ajax({
               'type': "POST",
               'url': "/tcgcreator/get_monster_condition/",
               'data': "i=1&j="+j,
            'success': function(data){
                    $("#"+id+"_"+j+"_1").html("<div id=\"monster_monster_"+j+"_1\"></div>");

                    $("#monster_monster_"+j+"_1").html(data);
                    $.ajax({
                         'type': "POST",
                         'url': "/tcgcreator/get_equation/",
                         'data': "c="+j,
                        'success': function(data){
                            $("."+id+"_equation").show();
                            $("#"+id+"_equation_"+j).html(data);
                            displayConditionAll(id,0);
                         }
                    })
                    $.ajax({
                         'type': "POST",
                         'url': "/tcgcreator/get_field_x_and_y/",
                         'data': "id="+id+"&c="+j,
                        'success': function(data){
                            $("."+id+"_field_x_and_y").show();
                            $("#"+id+"_field_x_and_y_"+j).html(data);
                         }
                    })
                    }
        })
    }});
    }

    function getConditionKind(id_det,kind,y,x){
		$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_variable_kind/",
		   'data': "",
		'success': function(data){
			$("#monster_variable_player_id").html(data);
		}
		});
        global_id2 = id_det;
        global_mode = kind;
        if(kind == undefined){
            kind =-1;
        }
        id="trigger_condition";
        $("#"+id).show();
        $("#"+id).draggable();
        $("#"+id).offset({top:mouse_y,left:mouse_x});
        $("#"+id+"_0_1").show();
            $("#as_"+id+"_"+0).val();
        deleteConditionPlace(id);
        deleteConditionPlaceAll(id);
        if(kind == 3 || kind == 57 || kind == 4 || kind == 1 || kind== 36 || kind == 50 || kind == 51 || kind == 70){
            $("#monster_effect_place_to").show();
            $.ajax({
           'type': "POST",
   'url': "/tcgcreator/get_place_kind_to/",
   'data': "i=1",
'success': function(data){
        $("#monster_effect_place_1_to").html(data);
        }
        });
        }else{
            $("#monster_effect_place_to").hide();
        }
        if(kind == 4 || kind == 1 || kind == 36 || kind == 50 || kind == 51 || kind == 57 || kind == 70) {
            $("#monster_effect_move_to").show();
            $("#trigger_condition_all_add_button_0").hide();
            $("#monster_effect_move_how").show();
        }else{
            $("#monster_effect_move_to").hide();
            $("#trigger_condition_all_add_button_0").show();
            $("#monster_effect_move_how").show();
        }
        if(kind == 57 || kind == 0 || kind == 1 || kind==2 || kind==3 || kind == 4 || kind == 5  || kind==6 || kind == 73|| kind == 30 || kind == 31|| kind==35 || kind==36 || kind == 50 || kind == 25 || kind == 38 || kind == 51 || kind == 70 || kind == 71){
            $("#"+id+"_place_tab").show();
        }else{
            $("#"+id+"_place_tab").hide();
        }
        if(kind == 2){
            $("#"+id+"_variable_condition_tab").show();
            $("#monster_effect_move_how").hide();
        }else{
        }
        if(kind == 6 ){
            $("#"+id+"_who_choose").show();
            $("#"+id+"_multiple_choose").hide();
            $("#"+id+"_all_button_0").hide();
            $("#"+id+"_all_add_button_0").hide();
            ChooseBoth();
            return;
        }else if(kind == 30 || kind == 31){
            $("#"+id+"_who_choose").hide();
            $("#"+id+"_multiple_choose").show();
            $("#"+id+"_all_button_0").hide();
            $("#"+id+"_all_add_button_0").hide();
            $(".show_multiple_effect_kind").show();
            ChooseBoth();
    $.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_effect_kind/",
   'data': "i=1",
    'success': function(data){
        $("#multiple_effect_kind").html(data);
    }

    });
            return;
        }else{
            $("#"+id+"_who_choose").hide();
            $("#"+id+"_multiple_choose").hide();
            $("#"+id+"_all_button_0").show();
            $("#"+id+"_all_add_button_0").show();
        }
    if($("#id_"+global_id2).val() == ""){
        getConditionVariables(id);
    $.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_place_kind/",
   'data': "i=1",
'success': function(data){
        $("."+id+"_place").show();
        $("#"+id+"_place_0_0").html(data);
        $.ajax({
               'type': "POST",
               'url': "/tcgcreator/get_monster_condition/",
               'data': "i=1&j=0",
            'success': function(data){
                    $("#"+id+"_0_1").html("<div id=\"monster_monster_0_1\"></div>");

                    $("#monster_monster_0_1").html(data);
                    $.ajax({
                         'type': "POST",
                         'url': "/tcgcreator/get_equation/",
                         'data': "c=0",
                        'success': function(data){
                            $("."+id+"_equation").show();
                            $("#"+id+"_equation_0").html(data);
                         }
                    })
                    $.ajax({
                         'type': "POST",
                         'url': "/tcgcreator/get_field_x_and_y/",
                         'data': "id="+id+"&c=0",
                        'success': function(data){
                            $("."+id+"_field_x_and_y_0").show();
                            $("#"+id+"_field_x_and_y_0").html(data);
                         }
                    })
                    }
                })
        }
    })
    }else{
        getConditionKindWithData(id_det,kind,y,x);
    }
    }
    function getConditionKindWithData(id_det,kind,y,x){
        global_id2 = id_det;
        global_mode = kind;
        if(kind == undefined){
            kind =-1;
        }
        id="trigger_condition";
        var val = $("#id_"+id_det).val();
        val = JSON.parse(val);
        getConditionVariablesWithData(id_det,val["variable"]);
        $("#"+id).show();
        $("#"+id).draggable();
        $("#"+id).offset({top:x,left:y});
        $("#"+id+"_0_1").show();
    $.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_place_kind/",
   'data': "i=1",
'success': function(data){
        $("."+id+"_place").show();
        $("#"+id+"_place_0_0").html(data);
        $.ajax({
               'type': "POST",
               'url': "/tcgcreator/get_monster_condition/",
               'data': "i=1&j=0",
            'success': function(data){
                    $("#"+id+"_0_1").html("<div id=\"monster_monster_0_1\"></div>");

                    $("#monster_monster_0_1").html(data);
                    $.ajax({
                         'type': "POST",
                         'url': "/tcgcreator/get_equation/",
                         'data': "c=0",
                        'success': function(data){
                            $("."+id+"_equation").show();
                            $("#"+id+"_equation_0").html(data);
            putConditionVal(0,val);
            for(k=1;val["monster"][k] != undefined;k++){
                addConditionPlaceAll(id,k-1,val);
            }
                         }
                    })
                    $.ajax({
                         'type': "POST",
                         'url': "/tcgcreator/get_field_x_and_y/",
                         'data': "id="+id+"&c=0",
                        'success': function(data){
                            $("."+id+"_field_x_and_y_0").show();
                            $("#"+id+"_field_x_and_y_0").html(data);
        if(kind == 57 || kind == 3 || kind == 4 || kind == 1 || kind == 0 || kind == 70){
            if($.inArray("exclude",val)){
                $("#exclude_change_variable").val(val["exclude"]);
            }
            if($.inArray("flag_change_how",val)){
                $("#flag_change_how").val(val["flag_change_how"]);
            }
            if($.inArray("flag_change_val",val)){
                $("#flag_change_val").val(val["flag_change_val"]);
            }
            $("#monster_effect_place_to").show();
            $.ajax({
           'type': "POST",
        'url': "/tcgcreator/get_place_kind_to/",
   'data': "i=1",
'success': function(data){
        $("#monster_effect_place_1_to").html(data);
        if(val["place_to"] != undefined){
            $("#monster_effect_place_1_to").val(val["place_to"][0]);
        }
		$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_variable_kind/",
		   'data': "",
		'success': function(data){
			$("#monster_variable_player_id").html(data);
            $("#monster_variable_val_player").val(val["monster_variable_val_player"]);
            $("#monster_variable_player_id").val(val["monster_variable_player_id"]) ;
            $("#monster_variable_player_how").val(val["monster_variable_player_how"]) ;
		}
		});
        if(val["monster_variable_change_name"] != undefined){
            $("#monster_variable_change_name_"+0).val(val["monster_variable_change_name"][0]) ;
            $("#monster_variable_change_life_"+0).val(val["monster_variable_change_life"][0]);
            if(val["persist"] != undefined){
                $("#persist_"+0).prop("checked",true);
            }
            $("#monster_variable_change_life_length_"+0).val(val["monster_variable_change_life_length"][0]);
            $("#monster_variable_change_val_"+0).val(val["monster_variable_change_val"][0]);
            if(val["minus"]!= undefined  && val["minus"][0]){
                $("#monster_variable_change_minus_"+0).prop("checked",true);
            }
            $("#monster_variable_change_initial_"+0).val(val["monster_variable_change_initial"][0]);
            $("#monster_variable_change_effect_kind_"+0).val(val["monster_variable_change_effect_kind"][0]);
            for(k=1;val["monster_variable_change_name"][k]!= undefined;k++){
	            addMonsterVariableChange(k-1);
                $("#monster_variable_change_name_"+k).val( val["monster_variable_change_name"][k] );
                if(val["persist"][k]){
                    $("#persist_"+k).prop("checked",true);
                }
                $("#monster_variable_change_life_"+k).val(val["monster_variable_change_life"][k]);
                $("#monster_variable_change_life_length_"+k).val(val["monster_variable_change_life_length"][k]);
                if(val["minus"] != undefined && val["minus"][k] ){
                    $("#monster_variable_change_minus_"+k).prop("checked",true);
                }
                $("#monster_variable_change_initial_"+k).val(val["monster_variable_change_initial"][k]);
                $("#monster_variable_change_effect_kind_"+k).val(val["monster_variable_change_effect_kind"][k]);
                $("#monster_variable_change_val_"+k).val(val["monster_variable_change_val"][k]);
            }
        }
        if(val["relation_name"] != undefined && val["relation_name"][0] != undefined){
            $("#relation_name_"+0).val(val["relation_name"][0]) ;
            $("#relation_monster_"+0).val(val["relation_monster"][0]) ;
            $("#put_relation_kind_"+0).val(val["relation_kind"][0]) ;
            $("#put_relation_to_"+0).val(val["relation_to"][0]) ;
            for(k=1;val["relation_name"][k]!= undefined;k++){
	            addPutRelation(k-1);
                $("#relation_name_"+k).val(val["relation_name"][k]) ;
                $("#relation_monster_"+k).val(val["relation_monster"][k]) ;
                $("#put_relation_kind_"+k).val(val["relation_kind"][k]) ;
                $("#put_relation_to_"+k).val(val["relation_to"][k]) ;
            }
        }
        }
        });
        }else{
            $("#monster_effect_place_to").hide();
        }
        if(kind == 30 || kind == 31){
            $("#attack_monster").show();
            $("#defendent_monster").show();
        }else{
            $("#attack_monster").hide();
            $("#defendent_monster").hide();
        }
            $("#monster_effect_move_how").val(val["move_how"] );
        if(kind == 57 ||  kind == 4 || kind == 1 || kind == 17 || kind == 36 || kind == 50 || kind == 51 || kind == 70){
            $("#monster_effect_move_to").show();
            $("#monster_effect_move_how_to").val(val["move_how_to"] );
            if(val["place_to"]!= undefined){
            $("#monster_effect_place_1_to").val(val["place_to"][0]);
            }

            $("#as_monster_effect_to").val(val["as_monster_condition_to"]);
            if(val["field_x_to"] != undefined){
                $("#monster_effect_field_x_to").val(val["field_x_to"]);
            }
            if(val["field_y_to"] != undefined){
                $("#monster_effect_field_y_to").val(val["field_y_to"]);
            }
            $("#trigger_condition_all_add_button_0").show();
        }else{
            $("#monster_effect_move_to").hide();
            $("#trigger_condition_all_add_button_0").show();
        }
        }
                    })
                    }
                })
        }
    })
    }
    /*
    function getConditionKindWithData(){
        var id="trigger_condition";
        var id_det=global_id2;
        var val = $("#id_"+id_det).val();
        val = JSON.parse(val);
        var k;
        $("#monster_effect_place_to").hide();
        if(global_mode==3 || global_mode == 4 || global_mode ==1 ){

        $("#exclude_change_variable").val(val["exclude"]);
        $("#flag_change_how").val(val["flag_change_how"]);
        $("#flag_change_val").val(val["flag_change_val"]);
        for(k=0;k<val["monster_variable_name"].length;k++){
            if($("#monster_variable_name_"+k).length == 0){
                addMonsterVariableChange(k-1);
            }
        $("#monster_variable_name_"+k).val(val["monster_variable_name"][k]);
        $("#monster_variable_who_"+k).val(val["monster_variable_who"][k]);
        $("#monster_variable_change_how_"+k).val(val["monster_variable_change_how"][k]);
        $("#monster_variable_change_val_"+k).val(val["monster_variable_change_val"][k] );
        $("#monster_variable_change_name_"+k).val(val["monster_variable_change_name"][k]);
        }
            }
        $("#as_monster_variable_from").val(val["monster_variable_as"]  );
        }

        kind = global_mode;
        for(var c = 0;c<val.length;c++){
        equ = val[c]["equation"];
        field_x_and_y = val[c]["field_x_and_y"];
        val2 = val[c];
        monster = val[c]["monster"];
    for(i=1;i<=monster.length;i++){
               (function(i,c){
    $.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_place_kind/",
   'data': "i="+i,
'success': function(data){
        var l;
        $(".monster_condition_place").show();
        for(l=0;l<monster[i-1]["place"].length;l++){
        $("#monster_condition_place_"+i+"_"+l).html(data);
        if($("#monster_condition_place_"+i+"_"+l).length==0){
            addPlace("monster_condition_place",i,l);
        }
        $("#monster_condition_place_"+i+"_"+l).monster( val[i-1]["place"][l]["det"]);
        $("#monster_condition_place_add_"+i+"_"+l).monster(val[i-1]["place"][l]["and_or"]);
        }
               (function(i,c){
        $.ajax({
               'type': "POST",
               'url': "/tcgcreator/get_monster_condition/",
                'data': "i="+i+"&j="+c,
            'success': function(data){
                    $("#monster_monster_"+i).show();
                    $("#monster_monster_"+i).html(data);
                    $("#flag_equal_"+i).val(monster[i-1]["flag"]["operator"]);
                    $("#get_monster_name_equal_"+i).val(monster[i-1]["monster_name_kind"]["operator"]);
                    $("#get_monster_place_id_"+i).val(monster[i-1]["monster_place_id"]);
                    $("#get_monster_unique_id_"+i).val(monster[i-1]["monster_unique_id"]);
                    $("#get_monster_name_"+i).val(monster[i-1]["monster_name_kind"]["monster_name"]);
                    for(j=1;j<=monster[i-1]["monster_condition"].length;j++){
                        for(var k=0;k<=monster[i-1]["monster_condition"][j-1].length;k++){
                            if(monster[i-1]["monster_condition"][j-1][k] == undefined){
                                continue;
                            }
                            if(k!=0){
                                addMonsterEquation(i+"_"+j+"_"+(k-1));
                            }
                            $("#get_monster_variable_equal_"+i+"_"+j+"_"+k).val(monster[i-1]["monster_condition"][j-1][k]["operator"]);
                            $("#get_monster_variable_"+i+"_"+j+"_"+k).val(monster[i-1]["monster_condition"][j-1][k]["num"]);
                            $("#monster_variable_and_or_"+i+"_"+j+"_"+k).val(monster[i-1]["monster_condition"][j-1][k]["and_or"]);
                        }
                    }

                    if(i==1){
                    if(kind != 3){
                                (function(i,c){
                        $.ajax({
                         'type': "POST",
                         'url': "/tcgcreator/get_equation/",
                         'data': "c="+c,
                        'success': function(data){
                            $("."+id+"_equation").show();
                            $("#"+id+"_equation_"+c).html(data);
                            $("#get_equation_det_"+c).val(equ["equation"]);
                            $("#get_equation_number_"+c).val(equ["equation_number"]);
                            $("#get_equation_kind_"+c).val(equ["equation_kind"]);
        $("#min_equation_number_"+c).val(equ["min_equation_number"]);
        $("#max_equation_number_"+c).val(equ["max_equation_number"]);
                            }
                        })
                         })(i,c);
                    }
                        (function(i,c){
                        $.ajax({
                         'type': "POST",
                         'url': "/tcgcreator/get_field_x_and_y/",
                         'data': "id="+id+"&c="+c,
                        'success': function(data){
                            var j;
                            $("#"+id+"_field_x_and_y_"+c).html(data);
                            for(j=0;j<field_x_and_y["x"].length;j++){
                                $("#field_x_"+c+"_"+j).val(field_x_and_y["x"][j]);
                            }
                            for(j=0;j<field_x_and_y["y"].length;j++){
                                $("#field_y_"+c+"_"+j).val(field_x_and_y["y"][j]);
                            }

                            }
                        })
                        })(i,c);
                    }
                }
                })
                })(i,c)
        }
    })
    })(i,c)
    }
    }
    }
    */
    function putPlace(place,m,l,json){
        place = json["place"][l];
        $("#"+id+"_place_add_"+m+"_"+l).val(place["and_or"]);
        $("#"+id+"_place_"+m+"_"+l).val(place["det"]);
    }
    function putPlaceFrom(place,m,l,k,json){
        place_from = json["place_from"][k];
        $("#"+place+"_add_"+m+"_"+l+"_"+k).val(place_from["and_or"]);
        $("#"+place+"_"+m+"_"+l+"_"+k).val(place_from["place"]);
    }
    function putConditionVal(m,val){
        json = {};
        var tmp = {};
        place = [];
        json = val["monster"][m]["monster"];
        $("#as_monster_to").val(val["as_monster_to"]);
        $("#choose").val(val["choose"]);
        if(val["different_flag"] == 1){
            $("#different_flag").prop("checked",true);
        }
        if(val["all_flag"] == 1){
            $("#all_flag").prop("checked",true);
        }
        if(val["auto_select"] != undefined){
            $("#auto_select").val(val["auto_select"]);
        }
        if(val["from_left"] != undefined && val["from_left"] == true){
            $("#from_left").prop("checked",true);
        }else{
            $("#from_left").prop("checked",false);
        }
        for(l=0;json["place"][l]!= undefined;l++){
        }
        addPlaceAll("trigger_condition_place",m,l-1,json,-1,0);
        if(json["monster_turn_count"]!= undefined){
            $("#monster_turn_count_"+m+"_1").val(json["turn_count"]);
        }
        if(json["place_from"] != undefined){
            for(var place_from_i=0;place_from_i<json["place_from"].length;place_from_i++){
                if(place_from_i!= 0){
        			addPlace("monster_from",m,1,json,place_from_i);
                }
                $("#monster_from_"+m+"_1_"+place_from_i).val(json["place_from"][place_from_i]["place"]);
                $("#monster_from_add_"+m+"_1_"+place_from_i).val(json["place_from"][place_from_i]["and_or"]);
            }
        }
        $("#monster_place_id_"+m+"_1").val(json["place_id"]);
        $("#monster_unique_id_"+m+"_1").val(json["unique_id"]);
        for(var j=0;json["monster_name_kind"][j] != undefined;j++){
                $("#get_monster_name_equal_"+m+"_1_"+j).val(json["monster_name_kind"][j]["operator"]) ;
                $("#monster_name_"+m+"_1_"+j).val(json["monster_name_kind"][j]["monster_name"]);
                $("#monster_name_and_or_"+m+"_1_"+j).val(json["monster_name_kind"][j]["and_or"]);
        }
        if(json["under"] != undefined){
            under = json["under"];
        if(under["flag"]["operator"]!= undefined){
           $("#under_flag_equal_"+m+"_1").val(under["flag"]["operator"]);
            $("#under_flag_"+m+"_1").val(under["flag"]["flag_det"] );
        }
        for(j=1;under["monster_condition"][j-1] != undefined;j++){
            for(p=1;$("#get_under_variable_"+m+"_1_"+p+"_0").length != 0;p++){
                if(under["monster_condition"][j-1][0]["name"] == $("#get_under_variable_name_"+m+"_1_"+p).val()){
                    break;
                }
            }
            $("#under_variable_init_"+m+"_1_"+p+"_"+0).val(under["monster_condition"][j-1][0]["init"]);
            for(k=0;under["monster_condition"][j-1][k] != undefined;k++){

                if(k!=0){
                   addMonsterEquation(m+"_1_"+p+"_"+(k-1));
                }
                $("#get_under_variable_"+m+"_1_"+p+"_"+k).val(under["monster_condition"][j-1][k]["num"]);
                $("#get_under_variable_equal_"+m+"_1_"+p+"_"+k).val(under["monster_condition"][j-1][k]["operator"]);
                $("#under_variable_and_or_"+m+"_1_"+p+"_"+k).val(under["monster_condition"][j-1][k]["and_or"]);
            }
         }
            $("#under_min_equation_number_"+String(m)).val(under["min_equation_number"]);
            $("#under_max_equation_number_"+String(m)).val(under["max_equation_number"]);
            $("#get_under_equation_det_"+m).val(under["equation"]["equation"]);
            $("#get_under_equation_kind_"+m).val(under["equation"]["equation_kind"]);
        }
        if(json["flag"]["operator"]!= undefined){
           $("#flag_equal_"+m+"_1").val(json["flag"]["operator"]);
            $("#flag_"+m+"_1").val(json["flag"]["flag_det"] );
        }
        for(j=1;json["monster_condition"][j-1] != undefined;j++){
            for(p=1;$("#get_monster_variable_"+m+"_1_"+p+"_0").length != 0;p++){
                if(json["monster_condition"][j-1][0]["name"] == $("#get_monster_variable_name_"+m+"_1_"+p).val()){
                    break;
                }
            }
            $("#monster_variable_init_"+m+"_1_"+p+"_"+0).val(json["monster_condition"][j-1][0]["init"]);
            for(k=0;json["monster_condition"][j-1][k] != undefined;k++){

                if(k!=0){
                   addMonsterEquation(m+"_1_"+p+"_"+(k-1));
                }
                $("#get_monster_variable_"+m+"_1_"+p+"_"+k).val(json["monster_condition"][j-1][k]["num"]);
                $("#get_monster_variable_equal_"+m+"_1_"+p+"_"+k).val(json["monster_condition"][j-1][k]["operator"]);
                $("#monster_variable_and_or_"+m+"_1_"+p+"_"+k).val(json["monster_condition"][j-1][k]["and_or"]);
            }
         }
        for(j=0;json["custom_monster_condition"][j] != undefined;j++){
            for(k=0;json["custom_monster_condition"][j][k] != undefined;k++){
                if(k==0){
                    addCustomMonsterCondition(m+'_1_'+(j)+'_'+k);
                }
                $("#custom_monster_variable_"+m+"_1_"+j+"_"+k).val(json["custom_monster_condition"][j][k]["name"]);
                $("#custom_get_monster_variable_"+m+"_1_"+j+"_"+k).val(json["custom_monster_condition"][j][k]["num"]);
                $("#custom_get_monster_variable_equal_"+m+"_1_"+j+"_"+k).val(json["custom_monster_condition"][j][k]["operator"]);
                $("#custom_monster_variable_and_or_"+m+"_1_"+j+"_"+k).val();
            }
         }
        if(json["relation"]!= undefined){
        for(j=0;json["relation"][j] != undefined;j++){
                addRelation(m+'_1_'+j+'_'+0,json["relation_id"]);
                $("#relation_"+m+"_1_"+j+"_"+0).val(json["relation"][j]);
                if(json["relation_valid"] != undefined){
                    $("#relation_valid_"+m+"_1_"+j+"_"+0).val(json["relation_valid"][j]);
                }
                $("#relation_kind_"+m+"_1_"+j+"_"+0).val(json["relation_kind"][j]);
                $("#relation_to_"+m+"_1_"+j+"_"+0).val(json["relation_to"][j]);
         }
       }
        $("#monster_effect_kind_"+m+"_"+1).val(val["monster"][m]["monster"]["effect_valid"]);
        $("#get_monster_"+m+"_"+1).val(val["monster"][m]["monster"]["monster_effect"]);
        $("#as_"+id+"_"+m).val(val["monster"][m]["as_monster_condition"]);
        $("#min_equation_number_"+String(m)).val(val["monster"][m]["min_equation_number"]);
        $("#max_equation_number_"+String(m)).val(val["monster"][m]["max_equation_number"]);
        tmp["equation"] = {};
        $("#get_equation_det_"+m).val(val["monster"][m]["equation"]["equation"]);
        $("#get_equation_kind_"+m).val(val["monster"][m]["equation"]["equation_kind"]);
        //$("#get_equation_number_"+m).val(val["monster"][m]["equation"]["equation_number"]);
        $("#"+id+"_and_or_"+m).val(val["monster"][m]["and_or"]);
        $("#exclude_"+0).val(val["exclude"]);
        for(var field_x =0;val["field_x"][field_x] != undefined;field_x++){
            $("#"+id+"_field_x_"+m+"_"+field_x).val(val["field_x"][field_x]);
            $("#get_field_x_det_"+m+"_"+field_x).val(val["field_x_operator"][field_x]);
            $("#get_field_x_and_or_"+m+"_"+field_x).val(val["field_x_and_or"][field_x]);
        }
        for(var field_y =0;val["field_y"][field_y] != undefined;field_y++){
            $("#"+id+"_field_y_"+m+"_"+field_y).val(val["field_y"][field_y]);
            $("#get_field_y_det_"+m+"_"+field_y).val(val["field_y_operator"][field_y]);
            $("#get_field_y_and_or_"+m+"_"+field_y).val(val["field_y_and_or"][field_y]);
        }
        $("#sentence").val(val["sentence"]);
        if( val["whether_monster"]){
            $("#monster_exist").prop("checked",true);
        }
    }
    function putCondition(){
        var id = "trigger_condition";
        var id_det = global_id2;
        var j;
        mode = global_mode;
            val = {};
            val["monster"] = []
        var k=0;

        var tmp = [];
        var json = {};

        var place;
        val["variable"] = [];
        val["all_flag"] = $("#all_flag").prop("checked");
        val["auto_select"] = $("#auto_select").val();
        if($("#from_left").prop("checked") == true){
            val["from_left"]= true;
        }else{
            val["from_left"]= false;
        }
        val["different_flag"] = $("#different_flag").prop("checked");
		for(var i=1;$("#"+id+"variable_condition_add_"+(i-1)).val();i++){
			tmp_json={}
			var tmp = $("#"+id+"variable_condition_"+i).val();
			var operator = $("#"+id+"variable_condition_equation_"+(i-1)).val();
			var variable_val = $("#"+id+"variable_equation_val_"+(i-1)).val();;
			if(tmp != "0"){
				tmp_json["variable"] =  tmp;
				tmp_json["varaiable_equation"] =  operator;
				val["variable"].push(tmp_json)
			}
		}
        if(mode == 30 || mode == 31){
            val["multiple_effect_kind"] = $("#multiple_effect_kind").val();
            val["double"] = $("#multiples_times").prop("checked");
        }
        if(mode == 57 || mode == 3 || mode==4 || mode ==1 || mode == 9 || mode == 30 || mode == 31 || mode == 35 || mode == 36 || mode == 50 || mode == 25 ||mode==38 || mode == 51 || mode == 0 || mode == 71){
        val["flag_change_how"]=$("#flag_change_how").val();
        val["flag_change_val"]=$("#flag_change_val").val();
        val["monster_variable_change_name"]=[];
        val["monster_variable_change_val"]=[];
        val["minus"]=[];
        val["monster_variable_change_life"]=[];
        val["persist"]=[];
        val["monster_variable_change_initial"]=[];
        val["monster_variable_change_effect_kind"]=[];
        val["monster_variable_change_life_length"]=[];
        val["relation_name"]=[];
        val["relation_monster"]=[];
        val["put_relation_kind"]=[];
        val["put_relation_to"]=[];
        val["monster_variable_val_player"] = $("#monster_variable_val_player").val();
        val["monster_variable_player_id"] = $("#monster_variable_player_id").val() ;
        val["monster_variable_player_how"] = $("#monster_variable_player_how").val() ;

        for(k=0;$("#monster_variable_change_name_"+k).val();k++){
        val["monster_variable_change_name"][k] = $("#monster_variable_change_name_"+k).val();
        val["persist"][k] = $("#persist_"+k).prop("checked");
        val["monster_variable_change_val"][k] = $("#monster_variable_change_val_"+k).val();
        val["minus"][k] = $("#monster_variable_change_minus_"+k).prop("checked");
        val["monster_variable_change_life"][k] = $("#monster_variable_change_life_"+k).val();
        if($("#monster_variable_change_life_length_"+k).val()){
            val["monster_variable_change_life_length"][k] = parseInt($("#monster_variable_change_life_length_"+k).val());
        }else{
            val["monster_variable_change_life_length"][k] = 1;
        }
        val["monster_variable_change_initial"][k] = parseInt($("#monster_variable_change_initial_"+k).val());
        val["monster_variable_change_effect_kind"][k] = $("#monster_variable_change_effect_kind_"+k).val();
        }
        for(k=0;$("#relation_name_"+k).val();k++){
        val["relation_name"][k]=$("#relation_name_"+k).val();
        val["relation_monster"][k]=$("#relation_monster_"+k).val();
        val["put_relation_kind"][k]=$("#put_relation_kind_"+k).val();
        val["put_relation_to"][k]=parseInt($("#put_relation_to_"+k).val());
        }
        }
        k=0;
        if(mode == 1 || mode == 2 || mode == 40 || mode == 73 ){
            val["variable"] = []
        var tmp2 = $("#"+id+"_variable_condition_1").val();
        if(tmp2!="" && tmp2!=null){
            json = {};
            for(var i=1;$("#"+id+"_variable_condition_"+(i)).val();i++){
                tmp_json={}
                var tmp = $("#"+id+"_variable_condition_"+i).val();
                var operator = $("#"+id+"_variable_condition_equation_"+(i)).val();
                var variable_val = $("#"+id+"_variable_equation_val_"+(i)).val();;
                var and_or = $("#"+id+"_variable_condition_add_"+(i)).val();;
                if(tmp != "0"){
                    tmp_json["variable"] =  tmp;
                    tmp_json["variable_equation"] =  operator;
                    tmp_json["variable_val"] =  variable_val;
                    tmp_json["and_or"] =  and_or;
                    val["variable"].push(tmp_json)
                }
            }
        }
        }
        var l;
        json = {};
        for(m=0;$("#"+id+"_place_"+m+"_"+0).length;m++ ){
        var tmp = {};
        place = [];
        for(l=0;$("#"+id+"_place_"+m+"_"+l).val();l++){
        place[l] = {};
        var and_or = $("#"+id+"_place_add_"+m+"_"+l).val();
        place[l]["and_or"] = and_or;
            var tmp_place = $("#"+id+"_place_"+m+"_"+l).val();
            if(tmp_place != "0"){
                place[l]["det"] =  tmp_place;
            }
        }
        json = {};
        for(var i=1;$("#get_monster_name_equal_"+m+"_"+i+"_0").length;i++){
            json["place_from"]= [];
            for(var k=0;$("#monster_from_"+m+"_"+i+"_"+k).length;k++){
                json["place_from"][k]= {};
                json["place_from"][k]["place"] = $("#monster_from_"+m+"_"+i+"_"+k).val();
                json["place_from"][k]["and_or"] = $("#monster_from_add_"+m+"_"+i+"_"+k).val();
            }
            json["turn_count"] = $("#monster_turn_count_"+m+"_"+i).val();
            json["place_id"] = $("#monster_place_id_"+m+"_"+i).val();
            json["unique_id"] = $("#monster_unique_id_"+m+"_"+i).val();
            json["place"] = place;
            json["monster_name_kind"] = [];
            for(var j=0;$("#get_monster_name_equal_"+m+"_"+i+"_"+j).length;j++){
            if($("#get_monster_name_equal_"+m+"_"+i+"_"+j).val() == ""){
                json["monster_name_kind"][j] = {};
                json["monster_name_kind"][j]["operator"] = "";
                json["monster_name_kind"][j]["monster_name"] ="";
                json["monster_name_kind"][j]["and_or"] = "";
            }else if($("#get_monster_name_equal_"+m+"_"+i+"_"+j).val() == "="){
                json["monster_name_kind"][j] = {};
                json["monster_name_kind"][j]["operator"] = "=";
                json["monster_name_kind"][j]["monster_name"] =$("#monster_name_"+m+"_"+i+"_"+j).val();
                json["monster_name_kind"][j]["and_or"] =$("#monster_name_and_or_"+m+"_"+i+"_"+j).val();
            }else{
                json["monster_name_kind"][j] = {};
                json["monster_name_kind"][j]["operator"] = "like";
                json["monster_name_kind"][j]["and_or"] =$("#monster_name_and_or_"+m+"_"+i+"_"+j).val();
                json["monster_name_kind"][j]["monster_name"] =$("#monster_name_"+m+"_"+i+"_"+j).val();
            }
        }
        if($("#under_min_equation_number_"+m).val() != "" || $("#under_max_equation_number_"+m).val() != "" ){
            under = {}
            under["min_equation_number"] = $("#under_min_equation_number_"+m).val();
            under["max_equation_number"] = $("#under_max_equation_number_"+m).val();
            under["equation"] = {};
            under["equation"]["equation"] = $("#get_under_equation_det_"+m).val();
            under["equation"]["equation_kind"] = $("#get_under_equation_kind_"+m).val();
            under["monster_effect"] = $("#get_under_"+m+"_"+i).val();
            under["monster_name_kind"] = [];
            for(var j=0;$("#get_under_name_equal_"+m+"_"+i+"_"+j).length;j++){
            if($("#get_under_name_equal_"+m+"_"+i+"_"+j).val() == ""){
                under["monster_name_kind"][j] = {};
                under["monster_name_kind"][j]["operator"] = "";
                under["monster_name_kind"][j]["monster_name"] ="";
                under["monster_name_kind"][j]["and_or"] = "";
            }else if($("#get_under_name_equal_"+m+"_"+i+"_"+j).val() == "="){
                under["monster_name_kind"][j] = {};
                under["monster_name_kind"][j]["operator"] = "=";
                under["monster_name_kind"][j]["monster_name"] =$("#under_name_"+m+"_"+i+"_"+j).val();
                under["monster_name_kind"][j]["and_or"] =$("#under_name_and_or_"+m+"_"+i+"_"+j).val();
            }else{
                under["monster_name_kind"][j] = {};
                under["monster_name_kind"][j]["operator"] = "like";
                under["monster_name_kind"][j]["and_or"] =$("#under_name_and_or_"+m+"_"+i+"_"+j).val();
                under["monster_name_kind"][j]["monster_name"] =$("#under_name_"+m+"_"+i+"_"+j).val();
            }
            }
        if($("#under_flag_"+m+"_"+i).val() == ""){
            under["flag"] = "";
        }else{
            under["flag"] = {};
            under["flag"]["operator"] = $("#under_flag_equal_"+m+"_"+i).val();
            under["flag"]["flag_det"] =$("#under_flag_"+m+"_"+i).val();
        }
        under["monster_condition"] = [];
        index2 = 0;
        index_flag = false;
        for(j=1;$("#get_under_variable_"+m+"_"+i+"_"+j+"_0").length != 0;j++){
            name = $("#get_under_variable_name_"+m+"_"+i+"_"+j).val();
            init= $("#under_variable_init_"+m+"_"+i+"_"+j+"_"+0).val();
            init = parseInt(init);
            index = 0;
                if(index_flag == true){
                    index2++;
                }
                index_flag = false;
            for(k=0;$("#get_under_variable_"+m+"_"+i+"_"+j+"_"+k).length != 0;k++){
            if($("#get_under_variable_equal_"+m+"_"+i+"_"+j+"_"+k).length != 0){
                num = $("#get_under_variable_"+m+"_"+i+"_"+j+"_"+k).val();
                operator = $("#get_under_variable_equal_"+m+"_"+i+"_"+j+"_"+k).val();
                and_or = $("#under_variable_and_or_"+m+"_"+i+"_"+j+"_"+k).val();
                if(operator == ""){
                    continue;
                }
                if( under["monster_condition"][index2] == undefined){
                    under["monster_condition"][index2] = [];
                    index_flag = true;
                }
                if( under["monster_condition"][index2][index] == undefined){
                    under["monster_condition"][index2][index] = {};
                }
                under["monster_condition"][index2][index]["init"] = init;
                under["monster_condition"][index2][index]["name"] = name;
                under["monster_condition"][index2][index]["num"] = num;
                under["monster_condition"][index2][index]["operator"] = operator;
                under["monster_condition"][index2][index]["and_or"] = and_or;
                index++;

            }else{
                num = $("#get_under_variable_"+m+"_"+i+"_"+j+"_"+k).val();
                and_or = $("#under_variable_and_or_"+m+"_"+i+"_"+j+"_"+k).val();
                if(num == "" || num==0){
                    continue;
                }
                if( under["monster_condition"][index2] == undefined){
                    under["monster_condition"][index2] = [];
                    index_flag = true;
                }
                if( under["monster_condition"][index2][index] == undefined){
                    under["monster_condition"][index2][index] = {};
                }
                under["monster_condition"][index2][index]["init"] = init;
                under["monster_condition"][index2][index]["name"] = name;
                under["monster_condition"][index2][index]["num"] = num;
                under["monster_condition"][index2][index]["operator"] = "";
                under["monster_condition"][index2][index]["and_or"] = and_or;
                index++;
            }
            }

        }
        json["under"] = under;
        }
        if($("#flag_"+m+"_"+i).val() == ""){
            json["flag"] = "";
        }else{
            json["flag"] = {};
            json["flag"]["operator"] = $("#flag_equal_"+m+"_"+i).val();
            json["flag"]["flag_det"] =$("#flag_"+m+"_"+i).val();
        }
        json["monster_condition"] = [];
        index2 = 0;
        index_flag = false;
        for(j=1;$("#get_monster_variable_"+m+"_"+i+"_"+j+"_0").length != 0;j++){
            name = $("#get_monster_variable_name_"+m+"_"+i+"_"+j).val();
            init= $("#monster_variable_init_"+m+"_"+i+"_"+j+"_"+0).val();
            init = parseInt(init);
            index = 0;
                if(index_flag == true){
                    index2++;
                }
                index_flag = false;
            for(k=0;$("#get_monster_variable_"+m+"_"+i+"_"+j+"_"+k).length != 0;k++){
            if($("#get_monster_variable_equal_"+m+"_"+i+"_"+j+"_"+k).length != 0){
                num = $("#get_monster_variable_"+m+"_"+i+"_"+j+"_"+k).val();
                operator = $("#get_monster_variable_equal_"+m+"_"+i+"_"+j+"_"+k).val();
                and_or = $("#monster_variable_and_or_"+m+"_"+i+"_"+j+"_"+k).val();
                if(operator == ""){
                    continue;
                }
                if( json["monster_condition"][index2] == undefined){
                    json["monster_condition"][index2] = [];
                    index_flag = true;
                }
                if( json["monster_condition"][index2][index] == undefined){
                    json["monster_condition"][index2][index] = {};
                }
                json["monster_condition"][index2][index]["init"] = init;
                json["monster_condition"][index2][index]["name"] = name;
                json["monster_condition"][index2][index]["num"] = num;
                json["monster_condition"][index2][index]["operator"] = operator;
                json["monster_condition"][index2][index]["and_or"] = and_or;
                index++;

            }else{
                num = $("#get_monster_variable_"+m+"_"+i+"_"+j+"_"+k).val();
                and_or = $("#monster_variable_and_or_"+m+"_"+i+"_"+j+"_"+k).val();
                if(num == "" || num==0){
                    continue;
                }
                if( json["monster_condition"][index2] == undefined){
                    json["monster_condition"][index2] = [];
                    index_flag = true;
                }
                if( json["monster_condition"][index2][index] == undefined){
                    json["monster_condition"][index2][index] = {};
                }
                json["monster_condition"][index2][index]["init"] = init;
                json["monster_condition"][index2][index]["name"] = name;
                json["monster_condition"][index2][index]["num"] = num;
                json["monster_condition"][index2][index]["operator"] = "";
                json["monster_condition"][index2][index]["and_or"] = and_or;
                index++;
            }
            }

        }
        json["custom_monster_condition"] = [];
        for(j=0;$("#custom_monster_variable_"+m+"_"+i+"_"+j+"_0").val();j++){
            json["custom_monster_condition"][j] = [];
            for(k=0;$("#custom_get_monster_variable_"+m+"_"+i+"_"+j+"_"+k).length != 0;k++){
            json["custom_monster_condition"][j][k] = {};
            if($("#custom_get_monster_variable_equal_"+m+"_"+i+"_"+j+"_"+k).length != 0){
                num = $("#custom_get_monster_variable_"+m+"_"+i+"_"+j+"_"+k).val();
                operator = $("#custom_get_monster_variable_equal_"+m+"_"+i+"_"+j+"_"+k).val();
                and_or = $("#custom_monster_variable_and_or_"+m+"_"+i+"_"+j+"_"+k).val();
                if(operator == ""){
                    continue;
                }
                json["custom_monster_condition"][j][k]["name"] = $("#custom_monster_variable_"+m+"_"+i+"_"+j+"_0").val();
                json["custom_monster_condition"][j][k]["num"] = num;
                json["custom_monster_condition"][j][k]["operator"] = operator;
                json["custom_monster_condition"][j][k]["and_or"] = and_or;

            }
            }

        }
            json["relation"] = [];
            json["relation_id"] = [];
            json["relation_valid"] = [];
            json["relation_kind"] = [];
            json["relation_to"] = [];
            for(k=0;$("#relation_"+m+"_"+i+"_0_"+k).length != 0;k++){
            if($("#relation_"+m+"_"+i+"_0_"+k).length != 0){
                json["relation"][k] = $("#relation_"+m+"_"+i+"_0_"+k).val();
                json["relation_id"][k] = $("#relation_id_"+m+"_"+i+"_0_"+k).val();
                json["relation_valid"][k] = $("#relation_valid_"+m+"_"+i+"_0_"+k).val();
                json["relation_kind"][k] = $("#relation_kind_"+m+"_"+i+"_0_"+k).val();
                json["relation_to"][k] = $("#relation_to_"+m+"_"+i+"_0_"+k).val();
            }
            }
            json["effect_valid"] = parseInt($("#monster_effect_kind_"+m+"_"+i).val());
            json["monster_effect"] = $("#get_monster_"+m+"_"+i).val();

        tmp["monster"]=json;
        }

            tmp["as_monster_condition"] = $("#as_"+id+"_"+m).val();
                if((mode == 57 || mode == 5) && !tmp["as_monster_condition"]){
                        alert("asを入れてください");
                        return;
                }
        tmp["min_equation_number"] = $("#min_equation_number_"+m).val();
        tmp["max_equation_number"] = $("#max_equation_number_"+m).val();
        tmp["equation"] = {};
        tmp["equation"]["equation"] = $("#get_equation_det_"+m).val();
        tmp["equation"]["equation_kind"] = $("#get_equation_kind_"+m).val();
       // tmp["equation"]["equation_number"] = $("#get_equation_number_"+m).val();
        var and_or = $("#"+id+"_and_or_"+m).val();
        if( and_or ==  undefined){
            and_or = "and"
        }
        tmp["and_or"] = and_or;
        val["exclude"] = $("#exclude_0").val();
        val["field_x"] = [];
        val["field_x_operator"] = [];
        val["field_x_and_or"] = [];
        for(var field_x=0;$("#"+id+"_field_x_"+m+"_"+field_x).val() != undefined && $("#"+id+"_field_x_"+m+"_"+field_x).val() != "";field_x++){
            val["field_x"][field_x] = $("#"+id+"_field_x_"+m+"_"+field_x).val();
            val["field_x_operator"][field_x] = $("#get_field_x_det_"+m+"_"+field_x).val();
            val["field_x_and_or"][field_x] = $("#get_field_x_and_or_"+m+"_"+field_x).val();
        }
        val["field_y"] = [];
        val["field_y_operator"] = [];
        val["field_y_and_or"] = [];
        for(var field_y=0;$("#"+id+"_field_y_"+m+"_"+field_y).val() != undefined && $("#"+id+"_field_y_"+m+"_"+field_y).val() != "";field_y++){
            val["field_y"][field_y] = $("#"+id+"_field_y_"+m+"_"+field_y).val();
            val["field_y_operator"][field_y] = $("#get_field_y_det_"+m+"_"+field_y).val();
            val["field_y_and_or"][field_y] = $("#get_field_y_and_or_"+m+"_"+field_y).val();
        }
        val["monster"].push(tmp);
        }
        val["sentence"] = $("#sentence").val();
        val["whether_monster"] = $("#monster_exist").prop("checked")?1:0;
        if(mode==2){
            val["move_how"] = parseInt($("#"+id+"_move_how").val());;
        }
        if(mode == 4 || mode == 3 || mode == 40 || mode ==1 || mode == 17 || mode == 36 || mode == 50 || mode == 51 || mode == 57 || mode == 70){
            val["move_how"] = parseInt($("#monster_effect_move_how").val());
            val["move_how_to"] = parseInt($("#monster_effect_move_how_to").val());
            var tmp = $("#monster_effect_place_1_to").val();
            val["place_to"] = {};
            val["place_to"][0] =  tmp;
            val["as_monster_condition_to"] = $("#as_monster_effect_to").val();
            if((mode == 4) && !tmp && ! val["as_monster_condition_to"]){
                    alert("移動先を入力してください");
                    return;
            }
            val["as_monster_to"] = $("#as_monster_to").val();
            if($("#monster_effect_field_x_to").val() != ""){
                val["field_x_to"] = $("#monster_effect_field_x_to").val();
            }
            if($("#monster_effect_field_y_to").val() != ""){
                val["field_y_to"] = $("#monster_effect_field_y_to").val();
            }
        }
        if($("#variable_name_by_monster").val()){
                val["variable_name"] = $("#variable_name_by_monster").val();
                val["variable_who"] = parseInt($("#variable_who_by_monster").val());
		        val["variable_change_how"] = parseInt($("#variable_change_how_by_monster").val());
		        val["variable_change_val"] = $("#variable_change_val_by_monster").val();
        }
        var j=0;
        if(mode == 35 || mode == 71){
                val["copy_monster_variables"] = [];
                val["copy_monster_variables_from_initial"] = [];
                val["copy_monster_variables_to_initial"] = [];
                for(var k=0;$("#monster_variable_name_copy_monster_"+String(k)).length != 0;k++){
                        if($("#copy_monster_"+String(k)).prop("checked") == true){
                                val["copy_monster_variables"].push($("#copy_monster_"+String(k)).val());
                            if($("#copy_monster_"+String(k)+"_init_from").prop("checked") == true){
                                val["copy_monster_variables_from_initial"].push(true);
                            }else{
                                val["copy_monster_variables_from_initial"].push(false);
                            }
                            if($("#copy_monster_"+String(k)+"_init_to").prop("checked") == true){
                                val["copy_monster_variables_to_initial"].push(true);
                            }else{
                                val["copy_monster_variables_to_initial"].push(false);
                            }
                        }
                }
                for(var k=0;$("#copy_monster_custom_variable_name_"+String(k)).length != 0;k++){
                        val["copy_monster_variables"].push($("#copy_monster_custom_variable_name_"+String(k)).val());
                }
                val["copy_monster"]= $("#copy_monster_det").val();
                if($("#copy_id").prop("checked") ==true){
                        val["copy_id"] = true;
                }else{
                        val["copy_id"] = false;
                }
                if($("#copy_monster_name").prop("checked") ==true){
                        val["copy_monster_name"] = true;
                }else{
                        val["copy_monster_name"] = false;
                }
                val["monster_variable_change_life"]= $("#copy_monster_variable_change_life").val();
                val["monster_variable_change_life_length"]= $("#copy_monster_variable_change_life_length").val();

        }
        val["choose"] = $("#choose").val();
        val =  JSON.stringify(val);
        $("#id_"+id_det).val(val);
        $("#"+id).hide();
        for(var i=2;$("#"+id+"_place_"+(i)).length;i++){
            $("#"+id+"_place_"+i).remove();
            $("#"+id+"_place_add"+i).remove();

        }
        $("#"+id+"_equation_0").html("");
        for(var i=1;$("#"+id+"_equation_"+(i)).length;i++){
            $("#"+id+"_equation_"+i).remove();

        }


    }
    function deleteConditionPlace(id){
        var i;
        for(i = 2;$("#"+id+"_add_button_"+0+"_"+i).length != 0;i++){
            $("#"+id+"_add_button_"+0+"_"+i).remove();
            $('#'+id+'_button_'+0+'_'+i).remove();
            $("#"+id+"_"+0+"_"+i).remove();
        }
        $("#"+id+"_add_button_"+0+"_"+1).show();
        $('#'+id+'_button_'+0+'_'+1).show();
    }
    function deleteConditionPlaceAll(id){
        var i;
        for(i = 1;$("#choose_"+id+"_"+i).length != 0;i++){
            $("#choose_"+id+"_"+i).remove();
            $("#"+id+"_all_button_"+i).remove();
            $("#"+id+"_all_add_button_"+i).remove();
            $("#"+id+'_and_or_'+i).remove();
        }
        $("#"+id+"_all_add_button_"+0).show();
    }

    function addConditionPlaceAll(id,i,json=null){
        if(i!=0 ){
            $("#"+id+"_all_add_button_"+i).remove();
        }else{
            $("#"+id+"_all_add_button_"+i).hide();
        }
    var j=i+1;
    $("#choose_"+id+"_"+i).after('<div id="choose_'+id+'_'+j+'"> <input type="button" class="active" value="条件1" onclick="displayCondition(\''+id+'\','+j+',1)" id="'+id+'_button_'+j+'_1"><input type="button" value="追加" id="'+id+'_add_button_'+j+'_1" onclick="addConditionPlace(\''+id+'\','+j+',1)"><br> 場所 <a class="show_place" href="javascript:showPlace()">+</a><a style="display:none" class="hide_place" href="javascript:hidePlace()">-</a> <div class="trigger_condition_place_box" style="display:none"> <select id="'+id+'_place_'+j+'_0" class="'+id+'_place" style=""> </select> <select id="'+id+'_place_add_'+j+'_0" onchange="addPlace(\''+id+'_place\','+j+',1)" class="'+id+'_place" style=""> <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select></div> <div id="'+id+'_'+j+'_1"> </div>カード有無 <a class="show_card_exist" href="javascript:showCardExist()">+</a><a style="display:none" class="hide_card_exist" href="javascript:hideCardExist()">-</a> <div class="card_exist_box" style="display:none"> <input type="checkbox" id="monster_exist" value="1" checked> </div><br> フィールド位置  <a class="show_field_x_and_y" href="javascript:showFieldXandY()">+</a><a style="display:none" class="hide_field_x_and_y" href="javascript:hideFieldXandY()">-</a> <div style="display:none" class="field_x_and_y" id="trigger_condition_field_x_and_y_'+j+'"> </div><div id="'+id+'_equation_'+j+'" class="'+id+'_equation" style=""></div> </div> </div><div id="as_'+id+'_wrapper_'+j+'">as <input type="text" id="as_'+id+'_'+j+'"></div> </div > </div></div>')
    $("#"+id+"_all_button_"+i).after('<select id="'+id+'_and_or_'+j+'"><option value=""></option><option value="and">かつ</option><option value="or">または</option></select><input type="button" value="'+(j+1)+'" onclick="displayConditionAll(\''+id+'\','+j+')" id="'+id+'_all_button_'+j+'"><input id="trigger_condition_all_add_button_'+j+'" type="button" value="追加" onclick="addConditionPlaceAll(\''+id+'\','+j+')">');
    $.ajax({
   'type': "POST",
   'url': "/tcgcreator/get_place_kind/",
   'data': "i="+j,
'success': function(data){
        $("."+id+"_place").show();
        $("#"+id+"_place_"+j+"_0").html(data);
        $.ajax({
               'type': "POST",
               'url': "/tcgcreator/get_monster_condition/",
               'data': "i=1&j="+j,
            'success': function(data){
                    $("#"+id+"_"+j+"_1").html("<div id=\"monster_monster_"+j+"_1\"></div>");

                    $("#monster_monster_"+j+"_1").html(data);
                    $.ajax({
                         'type': "POST",
                         'url': "/tcgcreator/get_equation/",
                         'data': "c="+j,
                        'success': function(data){
                            $("."+id+"_equation").show();
                            $("#"+id+"_equation_"+j).html(data);
                            displayConditionAll(id,j);
                               $.ajax({
                         'type': "POST",
                         'url': "/tcgcreator/get_field_x_and_y/",
                         'data': "id="+id+"&c="+j,
                        'success': function(data){
                            $("."+id+"_field_x_and_y").show();
                            $("#"+id+"_field_x_and_y_"+j).html(data);
                            if(json!= null){
                                putConditionVal(i+1,json);
                            }
                         }
                    })
                         }
                    })
                    }
        })
    }});

    }
    function addVariableCondition(id,num){
    $("#"+id+"_variable_"+num).after('<div id="'+id+'_variable_'+(num+1)+'"><select id="'+id+'_variable_condition_'+(num+1)+'" class="variable_condition" style=""></select> <select id="'+id+'_variable_condition_equation_'+(num+1)+'" class="variable_condition" style=""> <option value="=">=</option> <option value="<=">&lt;=</option> <option value=">=">&gt;=</option> <option value="!=">!=</option> </select> <select id="'+id+'_variable_condition_add_'+(num+1)+'" onchange="addVariable('+id+','+(num+1)+')" class="variable_condition" style=""> <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select> <input type="text" id="'+id+'_variable_equation_val_'+(num+1)+'" onfocus="showMonsterEquation(\''+id+'_variable_equation_val_'+(num+1)+'\')"> <input type="button" value="追加" onclick="addVariableCondition(\''+id+'\','+(num+1)+')"></div>');
		$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_variable_kind/",
		   'data': "",
		'success': function(data){
			$("."+id+"_variable_condition_").show();
			$("#"+id+"_variable_condition_"+(num+1)).html(data);
		}
		});
    }
	function getMonsterMultiple(id){
		getConditionKind(id,30,100,0);
	}
	function getMonsterMultipleOther(id){
		getConditionKind(id,31,100,0);
	}
	function getConditionVariables(id){
		$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_variable_kind/",
		   'data': "",
		'success': function(data){
			$("."+id+"_variable_condition_").show();
			$("#"+id+"_variable_condition_1").html(data);
		} }); }
	function getConditionVariablesWithData(id_det,data){
	    var i;
	    id_det ="trigger_condition"
	    if(data.length){
	    for(i=1;i<=data.length;i++){
	        if(i!=1){
                addVariableConditionWithData(id_det,i-1,data[i-1]);
	        }else{
	            addVariableConditionData1(id_det,1,data[0]);
	        }

	    }
	    }else{
	        getConditionVariables(id_det);
	    }

	}
function getGlobalVariableForInut(){
		$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_variable_kind/",
		   'data': "",
		'success': function(data2){
			$("#global_variable").html(data2);
    }});
}
    function addVariableConditionWithData(id,num,data){
    $("#"+id+"_variable_"+num).after('<div id="'+id+'_variable_'+(num+1)+'"><select id="'+id+'_variable_condition_'+(num+1)+'" class="variable_condition" style=""></select> <select id="'+id+'_variable_condition_equation_'+(num+1)+'" class="variable_condition" style=""> <option value="=">=</option> <option value="<=">&lt;=</option> <option value=">=">&gt;=</option> <option value="!=">!=</option> </select> <select id="'+id+'_variable_condition_add_'+(num+1)+'" onchange="addVariable('+id+','+(num+1)+')" class="variable_condition" style=""> <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select> <input type="text" id="'+id+'_variable_equation_val_'+(num+1)+'" onfocus="showMonsterEquation(\''+id+'_variable_equation_val_'+(num+1)+'\')"> <input type="button" value="追加" onclick="addVariableCondition(\''+id+'\','+(num+1)+')"></div>');
		$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_variable_kind/",
		   'data': "",
		'success': function(data2){
			$("."+id+"_variable_condition_").show();
			$("#"+id+"_variable_condition_"+(num+1)).html(data2);
			addVariableConditionData(id,num+1,data);

		}
		});
    }
    function addVariableConditionData(id,num,data){
        $("#"+id+"_variable_condition_"+num).val(data["variable"]);
        $("#"+id+"_variable_condition_equation_"+num).val(data["variable_equation"]);
        $("#"+id+"_variable_equation_val_"+num).val(data["variable_val"]);
        $("#"+id+"_variable_condition_add_"+num).val(data["and_or"]);
    }
    function addVariableConditionData1(id,num,data){
		$.ajax({
		   'type': "POST",
		   'url': "/tcgcreator/get_variable_kind/",
		   'data': "",
		'success': function(data2){
			$("."+id+"_variable_condition_").show();
			$("#"+id+"_variable_condition_1").html(data2);
        $("#"+id+"_variable_condition_"+num).val(data["variable"]);
        $("#"+id+"_variable_condition_equation_"+num).val(data["variable_equation"]);
        $("#"+id+"_variable_equation_val_"+num).val(data["variable_val"]);
        $("#"+id+"_variable_condition_add_"+num).val(data["and_or"]);
		}
		});
    }
