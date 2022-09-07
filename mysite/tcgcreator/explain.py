from .models import (
    Monster,Config
)
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render
from pprint import pprint


def explain(request):
    config = Config.objects.first()
    if "id" not in request.GET:
        HttpResponse("error")
    monster_id = request.GET["id"]
    monster = Monster.objects.get(id=monster_id)
    img_url = monster.img
    if config.show_img == 1:
        return render(request, "tcgcreator/explain.html", {"img_url": img_url,"config":config})
    else:
        monsteritems = (
            MonsterItem.objects.all()
            .filter(monster_id__id=monster_id)
            .order_by("-monster_variables_id__priority")
            .select_related("monster_variables_id")
            .select_related("monster_variables_id__monster_variable_kind_id")
        )
        return_value  = {}
        return_value["name"] = Monster.monster_name
        return_value["monster_sentence"] = Monster.monster_sentence
        tmp6 = []
        for monsteritem in monsteritems:
            tmp5 = {}
            monster_variable = monsteritem.monster_variables_id
            tmp5["name"] = monster_variable.monster_variable_name
            tmp5["minus"] = monster_variable.monster_variable_minus
            tmp5["value"] = monsteritem.monster_item_text
            tmp5["i_val"] = monsteritem.monster_item_text
            tmp5["i_i_val"] = monsteritem.monster_item_text
            tmp5["show"] = monster_variable.monster_variable_show_battle
            tmp5["kind"] = monster_variable.monster_variable_kind_id.monster_variable_sentence 
            tmp5["kind_id"] = monster_variable.monster_variable_kind_id.id
            tmp2 = monsteritem.monster_item_text.split("_")
            if monster_variable.monster_variable_kind_id.monster_variable_name == "数値":
                tmp5["str"] = tmp5["value"]
            else:
                tmp5["str"] = ""
                for tmp3 in tmp2:
                    tmp4 = monster_variable.monster_variable_kind_id.monster_variable_sentence.split(
                        "|"
                    )
                tmp5["str"] += tmp4[int(tmp5["value"]) - 1]
            tmp6.append(tmp5)  
        return_value["variable"] = tmp6
        return render(request, "tcgcreator/explain_no_img.html", json.dumps(tmp5))
