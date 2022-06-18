from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template.response import TemplateResponse
from django.db.models.functions import Cast
from django.db.models import IntegerField
from django.utils.html import format_html
from django.views.generic import View
import html
import os
import uuid
from tcgcreator.models import (
    Background,
    UserPoint,
    MonsterVariables,
    MonsterVariablesKind,
    MonsterItem,
    Monster,
    FieldKind,
    MonsterEffectKind,
    FieldSize,
    Field,
    Deck,
    Grave,
    Hand,
    FieldKind,
    Phase,
    UserDeck,
    UserDeckGroup,
    Duel,
    UserDeckChoice,
    GlobalVariable,
    DuelDeck,
    DuelGrave,
    DuelHand,
    EnemyDeckGroup,
    EnemyDeckChoice,
    EnemyDeck,
    DefaultDeckGroup,
    DefaultDeckChoice,
    DefaultDeck,
    Trigger,
    Timing,
    Pac,
    Config,
    MonsterEffectWrapper,
    PacWrapper,
    MonsterEffect,
    Cost,
    CostWrapper,
    PacCost,
    PacCostWrapper
)
from .duel import DuelObj
from .forms import (
    EditMonsterVariablesForm,
    EditMonsterForm,
    EditMonsterItemForm,
    UserForm,
    profileForm,
)
from .forms import EditMonsterVariablesKindForm, forms
from .custom_functions import (
    init_monster_item,
    create_user_deck,
    create_user_deck_group,
    copy_to_deck,
    copy_to_deck_text,
    create_user_deck_choice,
    create_default_deck,
    create_default_deck_group,
    copy_to_default_deck,
    create_default_deck_choice,
    create_enemy_deck,
    create_enemy_deck_group,
    create_enemy_deck_choice,
    copy_to_enemy_deck,
)
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .battle_functions import init_duel, init_ai_choosing,check_user_deck, check_in_other_room,check_in_other_room_num,check_enemy_deck,resetduel
from pprint import pprint
from django.db.models import Prefetch, Max
from time import time
from django.db.models import Q

import json

# Create your views here.
def monster(request):
    monster = Monster.objects.all()
    monster_item = MonsterItem()
    monster_variables = MonsterVariables.objects.order_by("-priority")
    tmps_val = {}
    tmps_sentence = {}
    tmps = {}
    # 	for tmp_val in monster_variables:
    # 		tmps_val[tmp_val.id]=(tmp_val.monster_variable_label)
    monster_variables_kind = MonsterVariablesKind.objects.all()
    for tmp_val in monster_variables_kind:
        tmps_sentence[tmp_val.id] = tmp_val.monster_variable_sentence
        tmps[tmp_val.id] = tmp_val.monster_variable_name
    return render(
        request,
        "tcgcreator/monster.html",
        {
            "Monster": monster,
            "MonsterItem": monster_item,
            "MonsterVariables": monster_variables,
            "MonsterVariablesSentences": tmps_sentence,
            "monster_variable_kind": tmps,
        },
    )


def monster_variables(request):
    monster_variables = MonsterVariables.objects.all()
    monster_variables_kind = MonsterVariablesKind.objects.all()
    tmps = {}
    tmps_sentence = {}
    for tmp in monster_variables_kind:
        tmps[tmp.id] = tmp.monster_variable_name
    monster_variables_kind = MonsterVariablesKind.objects.all()
    for tmp_val in monster_variables_kind:
        tmps_sentence[tmp_val.id] = tmp_val.monster_variable_sentence
    return render(
        request,
        "tcgcreator/monster_variables.html",
        {
            "MonsterVariables": monster_variables,
            "monster_variable_kind": tmps,
            "MonsterVariablesSentences": tmps_sentence,
        },
    )


def get_effect_kind(request):
    monster_kind = MonsterEffectKind.objects.all()
    i = 1
    result = ""
    result += '<option value="' + str(0) + '">特になし</option>'
    for tmp in monster_kind:
        result += (
            '<option value="' + str(i) + '">' + tmp.monster_effect_name + "</option>"
        )
        i += 1
    return HttpResponse(result)


def edit_monster_variables(request, monster_variables_id):
    monster_variable = get_object_or_404(MonsterVariables, id=monster_variables_id)
    if request.method == "POST":
        form = EditMonsterVariablesForm(request.POST, instance=monster_variable)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("tcgcreator:monster_variables"))
    else:
        form = EditMonsterVariablesForm(instance=monster_variable)
        context = {"form": form, "monster_variable": monster_variable}
        return TemplateResponse(
            request, "tcgcreator/edit_monster_variables.html", context=context
        )


def monster_variables_kind(request):
    monster_variables_kind = MonsterVariablesKind.objects.all()
    return render(
        request,
        "tcgcreator/monster_variables_kind.html",
        {"MonsterVariablesKind": monster_variables_kind},
    )


def edit_monster_variables_kind(request, monster_variables_kind_id):
    monster_variables_kind = get_object_or_404(
        MonsterVariablesKind, id=monster_variables_kind_id
    )
    if request.method == "POST":
        form = EditMonsterVariablesKindForm(
            request.POST, instance=monster_variables_kind
        )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("tcgcreator:monster_variables_kind"))
    else:
        form = EditMonsterVariablesKindForm(instance=monster_variables_kind)
        context = {"form": form, "monster_variables_kind": monster_variables_kind}
        return TemplateResponse(
            request, "tcgcreator/edit_monster_variables_kind.html", context=context
        )


def new_monster_variables_kind(request):
    if request.method == "POST":
        form = EditMonsterVariablesKindForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("tcgcreator:monster_variables_kind"))
    else:
        form = EditMonsterVariablesKindForm()
        context = {"form": form}
        return TemplateResponse(
            request, "tcgcreator/new_monster_variables_kind.html", context=context
        )


def new_monster_variables(request):
    if request.method == "POST":
        form = EditMonsterVariablesForm(request.POST)
        if form.is_valid():
            tmp = form.save()
            init_monster_item(request.POST, tmp)
            return HttpResponseRedirect(reverse("tcgcreator:monster_variables"))
    else:
        form = EditMonsterVariablesForm()
        context = {"form": form}
        return TemplateResponse(
            request, "tcgcreator/new_monster_variables.html", context=context
        )


def new_monster(request):
    if request.method == "POST":
        form = EditMonsterForm(request.POST)
        if form.is_valid():
            monster = form.save()
            monster_variables = MonsterVariables.objects.order_by("-priority")
            for tmp_val in monster_variables:
                formitem = EditMonsterItemForm(request.POST, prefix=tmp_val.id)
                monster_item = MonsterItem()
                monster_item.monster_item_text = request.POST[
                    str(tmp_val.id) + "-monster_item_text"
                ]
                monster_item.monster_variables_id = tmp_val
                monster_item.monster_id = monster
                monster_item.save()
            return HttpResponseRedirect(reverse("tcgcreator:monster"))

    else:
        form = EditMonsterForm()
        monster_variables = MonsterVariables.objects.order_by("-priority")
        formitems = []
        for tmp_val in monster_variables:
            formitem = EditMonsterItemForm(
                prefix=tmp_val.id, initial={"monster_variables_id": tmp_val}
            )
            formitem.fields["monster_item_text"].widget = forms.HiddenInput()
            formitem.fields["monster_variables_id"].widget = forms.HiddenInput()
            formitem.fields["monster_id"].widget = forms.HiddenInput()
            formitem.fields["monster_id"].widget.attrs["disabled"] = "disabled"
            formitems.append(formitem)
        context = {"form": form, "formitems": formitems}
        return TemplateResponse(request, "tcgcreator/new_monster.html", context=context)


def get_monster_specify(req):
    if req.method == "POST":
        monsters = Monster.objects.filter(monster_name__contains=req.POST["name"])
        result = '<option value="">全て</option>'
        for monster in monsters:
            result += (
                '<option  value="'
                + str(monster.id)
                + '">'
                + monster.monster_name
                + "</option>"
            )
    return HttpResponse(result)


# MonsterItemの種類を取得
def get_monster(req):
    monsters = Monster.objects.all()
    result = '<option value="">全て</option>'
    for monster in monsters:
        result += (
            '<option  value="'
            + str(monster.id)
            + '">'
            + monster.monster_name
            + "</option>"
        )
    return HttpResponse(result)


def get_monster_kind_type(req):
    monster_variable_kind_id = req.POST["monster_variable_kind_id"]
    monster_variable_kind = MonsterVariablesKind.objects.filter(
        id=monster_variable_kind_id
    )
    for tmp2 in monster_variable_kind:
        monster_variable_kind = tmp2
    tmp = monster_variable_kind.monster_variable_sentence.split("|")
    if req.POST["delete_flag"] == "1":
        result = (
            '<select id="id_default_value" name="default_value" onchange="deleteItem('
            + req.POST["delete_num"]
            + ')">'
        )
    else:
        result = '<select id="id_default_value" name="default_value">'
    i = 1
    for tmp_val in tmp:
        result += '<option value="' + str(i) + '">' + tmp_val + "</option>"
        i += 1
    result += "</select>"
    return HttpResponse(result)


def get_monster_kind_type_for_new_monster(req):
    prefix = req.POST["prefix"]
    tmp = int(prefix) + 1
    monster_variable = MonsterVariables.objects.all().filter(id=tmp)
    if not monster_variable:
        return HttpResponse(
            '<input type="number" id="id_'
            + prefix
            + '-monster_item_text" name="default_value" required>$1'
        )

    monster_variable_kind_id = str(monster_variable[0].monster_variable_kind_id.id)
    variable_name = monster_variable[0].monster_variable_name

    num = req.POST["num"]
    monster_variable_kind = MonsterVariablesKind.objects.filter(
        id=monster_variable_kind_id
    )

    for tmp2 in monster_variable_kind:
        monster_variable_kind = tmp2
    tmp = monster_variable_kind.monster_variable_sentence.split("|")
    if req.POST["delete_flag"] == "0":
        result = (
            '<select id="'
            + prefix
            + "-monster_item_text_"
            + num
            + '" name="'
            + prefix
            + "-monster_item_text_"
            + num
            + '" onchange="changeItemNum('
            + prefix
            + ')">'
        )
    i = 1
    for tmp_val in tmp:
        result += '<option value="' + str(i) + '">' + tmp_val + "</option>"
        i += 1
    result += "</select>"
    return HttpResponse(result + "$" + monster_variable_kind_id + "$" + variable_name)


def get_field_kind(req):
    field_kind = FieldKind.objects.all()
    if not field_kind:
        return HttpResponse("")
    num = req.POST["num"]
    tmp = []
    for tmp2 in field_kind:
        tmp.append(tmp2.field_kind_name)
    result = (
        '<select id="field_kind-'
        + num
        + '" name="field_kind-'
        + num
        + '" onchange="changeFieldNum()">'
    )
    i = 1
    for tmp_val in tmp:
        result += '<option value="' + str(i) + '">' + tmp_val + "</option>"
        i += 1
    result += "</select>"
    return HttpResponse(result)


def get_invalid_monster_kind(req):

    monster_kind = MonsterEffectKind.objects.all()
    if not monster_kind:
        return HttpResponse("")
    num = req.POST["num"]
    tmp = []
    for tmp2 in monster_kind:
        tmp.append(tmp2.monster_effect_name)
    result = (
        '<select id="invalid_monster_kind-'
        + num
        + '" name="invalid_monster_kind-'
        + num
        + '" onchange="changeInvalidMonsterKindNum()">'
    )
    i = 1
    for tmp_val in tmp:
        result += '<option value="' + str(i) + '">' + tmp_val + "</option>"
        i += 1
    result += "</select>"
    return HttpResponse(result)


def get_monster_kind(req):

    monster_kind = MonsterEffectKind.objects.all()
    if not monster_kind:
        return HttpResponse("")
    num = req.POST["num"]
    if "id" in req.POST:
        id = req.POST["id"]
        id2 = req.POST["id2"]
        mode = "1"
    else:
        id = "monster_kind"
        id2 = "monster_kind"
        mode = "0"
    tmp = []
    for tmp2 in monster_kind:
        tmp.append(tmp2.monster_effect_name)
    result = (
        '<select id="'
        + id2
        + "-"
        + num
        + '" name="monster_kind-'
        + num
        + '" onchange="changeMonsterKindNum(\''
        + id
        + "','"
        + id2
        + "',"
        + mode
        + ')">'
    )
    i = 1
    for tmp_val in tmp:
        result += '<option value="' + str(i) + '">' + tmp_val + "</option>"
        i += 1
    result += "</select>"
    return HttpResponse(result)


def get_monster_effect_kind(req):

    monster_kind = MonsterEffectKind.objects.all()
    if not monster_kind:
        return HttpResponse("")
    num = req.POST["num"]
    tmp = []
    for tmp2 in monster_kind:
        tmp.append(tmp2.monster_effect_name)
    result = (
        '<select id="monster_kind-'
        + num
        + '" name="monster_effect_kind-'
        + num
        + '" onchange="changeMonsterEffectKindNum()">'
    )
    i = 1
    for tmp_val in tmp:
        result += '<option value="' + str(i) + '">' + tmp_val + "</option>"
        i += 1
    result += "</select>"
    return HttpResponse(result)


def get_field_kind2(req):
    field_kind = FieldKind.objects.all()
    if not field_kind:
        return HttpResponse("")
    num = req.POST["num"]
    tmp = []
    for tmp2 in field_kind:
        tmp.append(tmp2.field_kind_name)
    result = (
        '<select id="field_kind-'
        + num
        + '" name="field_kind-'
        + num
        + '" onchange="changeCondtionFieldKind()">'
    )
    i = 1
    result += '<option value="' + str(0) + '">全て</option>'
    for tmp_val in tmp:
        result += '<option value="' + str(i) + '">' + tmp_val + "</option>"
        i += 1
    result += "</select>"
    return HttpResponse(result)


def pac_cost_diagram(request, pac_id):
    pac = PacCost.objects.get(id=pac_id)
    cost = pac.pac_cost_next
    cost_ary = []
    cost_id_ary = []
    pac_ary = []
    pac_id_ary = []
    cost_name = cost.cost_name
    cost_name = cost_name.replace(" ", "")
    cost_name = cost_name.replace("1", "1")
    cost_name = cost_name.replace("２", "2")
    cost_name = cost_name.replace("３", "3")
    cost_name = cost_name.replace("４", "4")
    cost_name = cost_name.replace("５", "5")
    cost_name = cost_name.replace("６", "6")
    cost_name = cost_name.replace("７", "7")
    cost_name = cost_name.replace("８", "8")
    cost_name = cost_name.replace("９", "9")
    cost_name = cost_name.replace("０", "0")
    cost_name = cost_name.replace("１", "0")
    cost_ary.append(cost_name)
    cost_id_ary.append(cost.id)
    result_html2 = "graph TD\n"
    result_html = ""
    if cost is not None:
        result_html += pac_cost_diagram_det(
            cost, cost_ary, cost_id_ary, pac_ary, pac_id_ary
        )
    result_html = result_html.replace("１", "1", 100)
    result_html = result_html.replace("２", "2", 100)
    result_html = result_html.replace("３", "3", 100)
    result_html = result_html.replace("４", "4", 100)
    result_html = result_html.replace("５", "5", 100)
    result_html = result_html.replace("６", "6", 100)
    result_html = result_html.replace("７", "7", 100)
    result_html = result_html.replace("８", "8", 100)
    result_html = result_html.replace("９", "9", 100)
    result_html = result_html.replace("０", "0", 100)
    result_html = result_html.replace(" ", "", 100)
    result_html = result_html2 + result_html

    context = {}
    context["cost_ary"] = cost_ary
    context["cost_id_ary"] = cost_id_ary
    context["pac_ary"] = pac_ary
    context["pac_id_ary"] = pac_id_ary
    context["result_html"] = result_html
    count = range(len(cost_id_ary))
    count_pac = range(len(pac_id_ary))
    context["count"] = count
    context["count_pac"] = count_pac

    return render(request, "admin/tcgcreator/pac_cost_diagram.html", context=context)


def pac_diagram(request, pac_id):
    pac = Pac.objects.get(id=pac_id)
    effect = pac.pac_next
    effect_ary = []
    effect_id_ary = []
    pac_ary = []
    pac_id_ary = []
    effect_name = effect.monster_effect_name
    effect_name = effect_name.replace(" ", "")
    effect_name = effect_name.replace("1", "1")
    effect_name = effect_name.replace("２", "2")
    effect_name = effect_name.replace("３", "3")
    effect_name = effect_name.replace("４", "4")
    effect_name = effect_name.replace("５", "5")
    effect_name = effect_name.replace("６", "6")
    effect_name = effect_name.replace("７", "7")
    effect_name = effect_name.replace("８", "8")
    effect_name = effect_name.replace("９", "9")
    effect_name = effect_name.replace("０", "0")
    effect_name = effect_name.replace("１", "0")
    effect_ary.append(effect_name)
    effect_id_ary.append(effect.id)
    result_html2 = "graph TD\n"
    result_html = ""
    if effect is not None:
        result_html += pac_diagram_det(
            effect, effect_ary, effect_id_ary, pac_ary, pac_id_ary
        )
    result_html = result_html.replace("１", "1", 100)
    result_html = result_html.replace("２", "2", 100)
    result_html = result_html.replace("３", "3", 100)
    result_html = result_html.replace("４", "4", 100)
    result_html = result_html.replace("５", "5", 100)
    result_html = result_html.replace("６", "6", 100)
    result_html = result_html.replace("７", "7", 100)
    result_html = result_html.replace("８", "8", 100)
    result_html = result_html.replace("９", "9", 100)
    result_html = result_html.replace("０", "0", 100)
    result_html = result_html.replace(" ", "", 100)
    result_html = result_html2 + result_html

    context = {}
    context["effect_ary"] = effect_ary
    context["effect_id_ary"] = effect_id_ary
    context["pac_ary"] = pac_ary
    context["pac_id_ary"] = pac_id_ary
    context["result_html"] = result_html
    count = range(len(effect_id_ary))
    count_pac = range(len(pac_id_ary))
    context["count"] = count
    context["count_pac"] = count_pac

    return render(request, "admin/tcgcreator/pac_diagram.html", context=context)


def trigger_cost_diagram(request, trigger_id):
    trigger = Trigger.objects.get(id=trigger_id)
    cost = trigger.trigger_cost
    result_html2 = "graph TD\n"
    result_html = ""
    cost_ary = []
    cost_id_ary = []
    pac_ary = []
    pac_id_ary = []
    if cost is not None:

        cost_ary.append(cost.cost_name)
        cost_id_ary.append(cost.id)
        result_html += pac_cost_diagram_det(
            cost, cost_ary, cost_id_ary, pac_ary, pac_id_ary
        )
    elif trigger.trigger_cost_pac is not None:
        pac_cost = trigger.trigger_cost_pac
        pac_ary.append(pac_cost.pac_cost_name)
        pac_id_ary.append(pac_cost.id)
        result_html += pac_cost_diagram_det2(
            pac_cost, cost_ary, cost_id_ary, pac_ary, pac_id_ary
        )
    else:
        return HttpResponse("")
    result_html = result_html.replace("１", "1")
    result_html = result_html.replace("２", "2")
    result_html = result_html.replace("３", "3")
    result_html = result_html.replace("４", "4")
    result_html = result_html.replace("５", "5")
    result_html = result_html.replace("６", "6")
    result_html = result_html.replace("７", "7")
    result_html = result_html.replace("８", "8")
    result_html = result_html.replace("９", "9")
    result_html = result_html.replace("０", "0")
    result_html = result_html2 + result_html
    context = {}
    context["result_html"] = result_html
    context["cost_ary"] = cost_ary
    context["cost_id_ary"] = cost_id_ary
    context["pac_ary"] = pac_ary
    context["pac_id_ary"] = pac_id_ary
    count = range(len(cost_id_ary))
    count_pac = range(len(pac_id_ary))
    context["count"] = count
    context["count_pac"] = count_pac

    return render(request, "admin/tcgcreator/trigger_cost_diagram.html", context=context)

def trigger_tag_monster(request,trigger_id):
    if request.user.is_superuser == False:
        return HttpResponse("error")
    if request.method == "POST":
        trigger = Trigger.objects.filter(id = request.POST["trigger"]).get()
        monsters = Monster.objects.all();
        result_monster = []
        monster_variables = MonsterVariables.objects.all()
        for monster in monsters:
            flag = True
            for monster_variable in monster_variables:
                monster_item = MonsterItem.objects.filter(monster_variables_id=monster_variable,monster_id=monster).get()
                if (monster_variable.monster_variable_kind_id.id == 1):
                    low = request.POST.get(str(monster_variable.id) + "_low")
                    high = request.POST.get(str(monster_variable.id) + "_high")
                    if low.isnumeric():
                        if not monster_item.monster_item_text.isnumeric():
                            flag =False
                            break
                        if int(monster_item.monster_item_text ) < int(low):
                            flag =False
                            break
                    if high.isnumeric() :
                        if not monster_item.monster_item_text.isnumeric():
                            flag =False
                            break
                        if int(monster_item.monster_item_text ) > int(high):
                            flag = False
                            break
                else:
                    val = request.POST.get(monster_variable.monster_variable_name)
                    if val is not None:
                        if monster_item.monster_item_text != val:
                            flag = False
                            break
            if flag is True:
                result_monster.append(monster)

        for monster in result_monster:
            monster.trigger.add(trigger)
        return HttpResponse("OK")


    monster_variables = MonsterVariables.objects.all()
    i=0
    context = {}
    context["monster_variables"] = []
    for monster_variable in monster_variables:
        tmp = {}
        tmp["name"] = monster_variable.monster_variable_name
        tmp["id"] = monster_variable.id
        if(monster_variable.monster_variable_kind_id.id == 1):
            tmp["type"] = "number";
        else:
            tmp["type"] = "name";
            tmp["kind"] = monster_variable.monster_variable_kind_id.monster_variable_sentence.split("|")
        context["monster_variables"].append(tmp)

    context["trigger"] = trigger_id
    return render(request, "admin/tcgcreator/tag_monster.html", context=context)
def trigger_tag_connect_monster(request):
    if request.user.is_superuser == False:
        return HttpResponse("error")
    monsters = request.POST["monsters"].split("_")
    trigger = Trigger.object.get(id=int(request.POST["trigger_id"]))
    for monster_id in monsters:
        monster = Monster.object.get(id=int(monster_id))
        monster.trigger.add(trigger)
    return HttpResponse("OK")

def trigger_diagram(request, trigger_id):
    trigger = Trigger.objects.get(id=trigger_id)
    effect = trigger.next_effect
    result_html2 = "graph TD\n"
    result_html = ""
    effect_ary = []
    effect_id_ary = []
    pac_ary = []
    pac_id_ary = []
    if effect is not None:
        effect_ary.append(effect.monster_effect_name)
        effect_id_ary.append(effect.id)
        result_html += pac_diagram_det(
            effect, effect_ary, effect_id_ary, pac_ary, pac_id_ary
        )
    elif trigger.pac is not None:
        pac = trigger.pac
        pac_ary.append(pac.pac_name)
        pac_id_ary.append(pac.id)
        result_html += pac_diagram_det2(
            pac, effect_ary, effect_id_ary, pac_ary, pac_id_ary
        )
    result_html = result_html.replace("１", "1")
    result_html = result_html.replace("２", "2")
    result_html = result_html.replace("３", "3")
    result_html = result_html.replace("４", "4")
    result_html = result_html.replace("５", "5")
    result_html = result_html.replace("６", "6")
    result_html = result_html.replace("７", "7")
    result_html = result_html.replace("８", "8")
    result_html = result_html.replace("９", "9")
    result_html = result_html.replace("０", "0")
    result_html = result_html2 + result_html
    context = {}
    context["result_html"] = result_html
    context["effect_ary"] = effect_ary
    context["effect_id_ary"] = effect_id_ary
    context["pac_ary"] = pac_ary
    context["pac_id_ary"] = pac_id_ary
    count = range(len(effect_id_ary))
    count_pac = range(len(pac_id_ary))
    context["count"] = count
    context["count_pac"] = count_pac
    result_html = result_html.strip();
    return render(request, "admin/tcgcreator/trigger_diagram.html", context=context)


def pac_cost_diagram_det2(pac, cost_ary, cost_id_ary, pac_ary, pac_id_ary):
    pac_name = pac.pac_cost_name
    pac_name = pac_name.replace(" ", "")
    pac_name = pac_name.replace("1", "1")
    pac_name = pac_name.replace("２", "2")
    pac_name = pac_name.replace("３", "3")
    pac_name = pac_name.replace("４", "4")
    pac_name = pac_name.replace("５", "5")
    pac_name = pac_name.replace("６", "6")
    pac_name = pac_name.replace("７", "7")
    pac_name = pac_name.replace("８", "8")
    pac_name = pac_name.replace("９", "9")
    pac_name = pac_name.replace("０", "0")
    pac_name = pac_name.replace("１", "1")
    result_html = ""

    if pac.pac_next is not None:
        pac_next = pac.pac_next
        pac_name1 = pac.pac_next.pac_cost_name
        pac_name1 = pac_name1.replace(" ", "")
        pac_name1 = pac_name1.replace("1", "1")
        pac_name1 = pac_name1.replace("２", "2")
        pac_name1 = pac_name1.replace("３", "3")
        pac_name1 = pac_name1.replace("４", "4")
        pac_name1 = pac_name1.replace("５", "5")
        pac_name1 = pac_name1.replace("６", "6")
        pac_name1 = pac_name1.replace("７", "7")
        pac_name1 = pac_name1.replace("８", "8")
        pac_name1 = pac_name1.replace("９", "9")
        pac_name1 = pac_name1.replace("０", "0")
        pac_name1 = pac_name1.replace("１", "1")
        result_html += pac_name + "-->" + pac_name1 + "\n"
        if not pac_next.id in pac_id_ary:
            pac_ary.append(pac_name1)
            pac_id_ary.append(pac_next.id)
            result_html += pac_cost_diagram_det2(
                pac_next, cost_ary, cost_id_ary, pac_ary, pac_id_ary
            )
    else:
        next_cost1 = pac.cost_next
        if next_cost1 is not None:
            next_cost_name1 = next_cost1.cost_name
            next_cost_name1 = next_cost_name1.replace(" ", "")
            next_cost_name1 = next_cost_name1.replace("1", "1")
            next_cost_name1 = next_cost_name1.replace("２", "2")
            next_cost_name1 = next_cost_name1.replace("３", "3")
            next_cost_name1 = next_cost_name1.replace("４", "4")
            next_cost_name1 = next_cost_name1.replace("５", "5")
            next_cost_name1 = next_cost_name1.replace("６", "6")
            next_cost_name1 = next_cost_name1.replace("７", "7")
            next_cost_name1 = next_cost_name1.replace("８", "8")
            next_cost_name1 = next_cost_name1.replace("９", "9")
            next_cost_name1 = next_cost_name1.replace("０", "0")
            next_cost_name1 = next_cost_name1.replace("１", "0")
            result_html += pac_name + "-->" + next_cost_name1 + "\n"
            if not next_cost1.id in cost_id_ary:
                cost_ary.append(next_cost_name1)
                cost_id_ary.append(next_cost1.id)
                result_html += pac_cost_diagram_det(
                    next_cost1, cost_ary, cost_id_ary, pac_ary, pac_id_ary
                )
    if pac.pac_next2 is not None:
        pac_next2 = pac.pac_next2
        pac_name2 = pac_next2.pac_cost_name
        pac_name2 = pac_name2.replace("1", "1")
        pac_name2 = pac_name2.replace("２", "2")
        pac_name2 = pac_name2.replace("３", "3")
        pac_name2 = pac_name2.replace("４", "4")
        pac_name2 = pac_name2.replace("５", "5")
        pac_name2 = pac_name2.replace("６", "6")
        pac_name2 = pac_name2.replace("７", "7")
        pac_name2 = pac_name2.replace("８", "8")
        pac_name2 = pac_name2.replace("９", "9")
        pac_name2 = pac_name2.replace("０", "0")
        pac_name2 = pac_name2.replace("１", "0")
        result_html += pac_name + "-->" + pac_name1 + "\n"
        if not pac_next2.id in pac_id_ary:
            pac_ary.append(pac_name1)
            pac_id_ary.append(pac_next.id)
            result_html += pac_cost_diagram_det2(
                pac_next2, cost_ary, cost_id_ary, pac_ary, pac_id_ary
            )
    else:
        next_cost2 = pac.cost_next2
        if next_cost2 is not None:
            next_cost_name2 = next_cost2.cost_name
            next_cost_name2 = next_cost_name2.replace(" ", "")
            next_cost_name2 = next_cost_name2.replace("1", "1")
            next_cost_name2 = next_cost_name2.replace("２", "2")
            next_cost_name2 = next_cost_name2.replace("３", "3")
            next_cost_name2 = next_cost_name2.replace("４", "4")
            next_cost_name2 = next_cost_name2.replace("５", "5")
            next_cost_name2 = next_cost_name2.replace("６", "6")
            next_cost_name2 = next_cost_name2.replace("７", "7")
            next_cost_name2 = next_cost_name2.replace("８", "8")
            next_cost_name2 = next_cost_name2.replace("９", "9")
            next_cost_name2 = next_cost_name2.replace("０", "0")
            next_cost_name2 = next_cost_name2.replace("１", "0")
            result_html += pac_name + "-->" + next_cost_name2 + "\n"
            if not next_cost2.id in cost_id_ary:
                cost_ary.append(next_cost_name2)
                cost_id_ary.append(next_cost2.id)
                result_html += pac_cost_diagram_det(
                    next_cost2, cost_ary, cost_id_ary, pac_ary, pac_id_ary
                )

    return result_html


def pac_diagram_det2(pac, effect_ary, effect_id_ary, pac_ary, pac_id_ary):
    pac_name = pac.pac_name
    pac_name = pac_name.replace(" ", "")
    pac_name = pac_name.replace("1", "1")
    pac_name = pac_name.replace("２", "2")
    pac_name = pac_name.replace("３", "3")
    pac_name = pac_name.replace("４", "4")
    pac_name = pac_name.replace("５", "5")
    pac_name = pac_name.replace("６", "6")
    pac_name = pac_name.replace("７", "7")
    pac_name = pac_name.replace("８", "8")
    pac_name = pac_name.replace("９", "9")
    pac_name = pac_name.replace("０", "0")
    pac_name = pac_name.replace("１", "1")
    result_html = ""

    if pac.pac_next is not None:
        pac_next = pac.pac_next
        pac_name1 = pac.pac_next.pac_name
        pac_name1 = pac_name1.replace(" ", "")
        pac_name1 = pac_name1.replace("1", "1")
        pac_name1 = pac_name1.replace("２", "2")
        pac_name1 = pac_name1.replace("３", "3")
        pac_name1 = pac_name1.replace("４", "4")
        pac_name1 = pac_name1.replace("５", "5")
        pac_name1 = pac_name1.replace("６", "6")
        pac_name1 = pac_name1.replace("７", "7")
        pac_name1 = pac_name1.replace("８", "8")
        pac_name1 = pac_name1.replace("９", "9")
        pac_name1 = pac_name1.replace("０", "0")
        pac_name1 = pac_name1.replace("１", "1")
        result_html += pac_name + "-->" + pac_name1 + "\n"
        if not pac_next.id in pac_id_ary:
            pac_ary.append(pac_name1)
            pac_id_ary.append(pac_next.id)
            result_html += pac_diagram_det2(
                pac_next, effect_ary, effect_id_ary, pac_ary, pac_id_ary
            )
    else:
        next_effect1 = pac.monster_effect_next
        if next_effect1 is not None:
            next_effect_name1 = next_effect1.monster_effect_name
            next_effect_name1 = next_effect_name1.replace(" ", "")
            next_effect_name1 = next_effect_name1.replace("1", "1")
            next_effect_name1 = next_effect_name1.replace("２", "2")
            next_effect_name1 = next_effect_name1.replace("３", "3")
            next_effect_name1 = next_effect_name1.replace("４", "4")
            next_effect_name1 = next_effect_name1.replace("５", "5")
            next_effect_name1 = next_effect_name1.replace("６", "6")
            next_effect_name1 = next_effect_name1.replace("７", "7")
            next_effect_name1 = next_effect_name1.replace("８", "8")
            next_effect_name1 = next_effect_name1.replace("９", "9")
            next_effect_name1 = next_effect_name1.replace("０", "0")
            next_effect_name1 = next_effect_name1.replace("１", "0")
            result_html += pac_name + "-->" + next_effect_name1 + "\n"
            if not next_effect1.id in effect_id_ary:
                effect_ary.append(next_effect_name1)
                effect_id_ary.append(next_effect1.id)
                result_html += pac_diagram_det(
                    next_effect1, effect_ary, effect_id_ary, pac_ary, pac_id_ary
                )
    if pac.pac_next2 is not None:
        pac_next2 = pac.pac_next2
        pac_name2 = pac_next2.pac_name
        pac_name2 = pac_name2.replace("1", "1")
        pac_name2 = pac_name2.replace("２", "2")
        pac_name2 = pac_name2.replace("３", "3")
        pac_name2 = pac_name2.replace("４", "4")
        pac_name2 = pac_name2.replace("５", "5")
        pac_name2 = pac_name2.replace("６", "6")
        pac_name2 = pac_name2.replace("７", "7")
        pac_name2 = pac_name2.replace("８", "8")
        pac_name2 = pac_name2.replace("９", "9")
        pac_name2 = pac_name2.replace("０", "0")
        pac_name2 = pac_name2.replace("１", "0")
        result_html += pac_name + "-->" + pac_name1 + "\n"
        if not pac_next2.id in pac_id_ary:
            pac_ary.append(pac_name1)
            pac_id_ary.append(pac_next.id)
            result_html += pac_diagram_det2(
                pac_next2, effect_ary, effect_id_ary, pac_ary, pac_id_ary
            )
    else:
        next_effect2 = pac.monster_effect_next2
        if next_effect2 is not None:
            next_effect_name2 = next_effect2.monster_effect_name
            next_effect_name2 = next_effect_name2.replace(" ", "")
            next_effect_name2 = next_effect_name2.replace("1", "1")
            next_effect_name2 = next_effect_name2.replace("２", "2")
            next_effect_name2 = next_effect_name2.replace("３", "3")
            next_effect_name2 = next_effect_name2.replace("４", "4")
            next_effect_name2 = next_effect_name2.replace("５", "5")
            next_effect_name2 = next_effect_name2.replace("６", "6")
            next_effect_name2 = next_effect_name2.replace("７", "7")
            next_effect_name2 = next_effect_name2.replace("８", "8")
            next_effect_name2 = next_effect_name2.replace("９", "9")
            next_effect_name2 = next_effect_name2.replace("０", "0")
            next_effect_name2 = next_effect_name2.replace("１", "0")
            result_html += pac_name + "-->" + next_effect_name2 + "\n"
            if not next_effect2.id in effect_id_ary:
                effect_ary.append(next_effect_name2)
                effect_id_ary.append(next_effect2.id)
                result_html += pac_diagram_det(
                    next_effect2, effect_ary, effect_id_ary, pac_ary, pac_id_ary
                )

    return result_html


def pac_cost_diagram_det(cost, cost_ary, cost_id_ary, pac_ary, pac_id_ary):
    cost_name = cost.cost_name
    cost_name = cost_name.replace(" ", "")
    cost_name = cost_name.replace("1", "1")
    cost_name = cost_name.replace("２", "2")
    cost_name = cost_name.replace("３", "3")
    cost_name = cost_name.replace("４", "4")
    cost_name = cost_name.replace("５", "5")
    cost_name = cost_name.replace("６", "6")
    cost_name = cost_name.replace("７", "7")
    cost_name = cost_name.replace("８", "8")
    cost_name = cost_name.replace("９", "9")
    cost_name = cost_name.replace("０", "0")
    cost_name = cost_name.replace("１", "0")
    result_html = ""

    if cost.pac is not None:
        pac_next = cost.pac
        pac_name1 = pac_next.pac_cost_name
        pac_name1 = pac_name1.replace(" ", "")
        pac_name1 = pac_name1.replace("1", "1")
        pac_name1 = pac_name1.replace("２", "2")
        pac_name1 = pac_name1.replace("３", "3")
        pac_name1 = pac_name1.replace("４", "4")
        pac_name1 = pac_name1.replace("５", "5")
        pac_name1 = pac_name1.replace("６", "6")
        pac_name1 = pac_name1.replace("７", "7")
        pac_name1 = pac_name1.replace("８", "8")
        pac_name1 = pac_name1.replace("９", "9")
        pac_name1 = pac_name1.replace("０", "0")
        pac_name1 = pac_name1.replace("１", "0")
        result_html += cost_name + "-->" + pac_name1 + "\n"
        if pac_next.id not in pac_id_ary:
            pac_ary.append(pac_name1)
            pac_id_ary.append(pac_next.id)
            result_html += pac_cost_diagram_det2(
                cost.pac, cost_ary, cost_id_ary, pac_ary, pac_id_ary
            )
    else:
        next_cost1 = cost.cost_next
        if next_cost1 is not None:
            next_cost_name1 = next_cost1.cost_name
            next_cost_name1 = next_cost_name1.replace(" ", "")
            next_cost_name1 = next_cost_name1.replace("1", "1")
            next_cost_name1 = next_cost_name1.replace("２", "2")
            next_cost_name1 = next_cost_name1.replace("３", "3")
            next_cost_name1 = next_cost_name1.replace("４", "4")
            next_cost_name1 = next_cost_name1.replace("５", "5")
            next_cost_name1 = next_cost_name1.replace("６", "6")
            next_cost_name1 = next_cost_name1.replace("７", "7")
            next_cost_name1 = next_cost_name1.replace("８", "8")
            next_cost_name1 = next_cost_name1.replace("９", "9")
            next_cost_name1 = next_cost_name1.replace("０", "0")
            next_cost_name1 = next_cost_name1.replace("１", "0")
            result_html += cost_name + "-->" + next_cost_name1 + "\n"
            if not next_cost1.id in cost_id_ary:
                cost_ary.append(next_cost_name1)
                cost_id_ary.append(next_cost1.id)
                result_html += pac_cost_diagram_det(
                    next_cost1, cost_ary, cost_id_ary, pac_ary, pac_id_ary
                )
    if cost.pac2 is not None:
        pac_next2 = cost.pac2
        pac_name2 = pac_next2.pac_cost_name
        pac_name2 = pac_name2.replace("1", "1")
        pac_name2 = pac_name2.replace("２", "2")
        pac_name2 = pac_name2.replace("３", "3")
        pac_name2 = pac_name2.replace("４", "4")
        pac_name2 = pac_name2.replace("５", "5")
        pac_name2 = pac_name2.replace("６", "6")
        pac_name2 = pac_name2.replace("７", "7")
        pac_name2 = pac_name2.replace("８", "8")
        pac_name2 = pac_name2.replace("９", "9")
        pac_name2 = pac_name2.replace("０", "0")
        pac_name2 = pac_name2.replace("１", "0")
        result_html += cost_name + "-->" + pac_name2 + "\n"
        if pac_next2.id not in pac_id_ary:
            pac_ary.append(pac_name2)
            pac_id_ary.append(pac_next2.id)
            result_html += pac_cost_diagram_det2(
                cost.pac2, cost_ary, cost_id_ary, pac_ary, pac_id_ary
            )
    else:
        next_cost2 = cost.cost_next2
        if next_cost2 is not None:
            next_cost_name2 = next_cost2.cost_name
            next_cost_name2 = next_cost_name2.replace(" ", "")
            next_cost_name2 = next_cost_name2.replace("1", "1")
            next_cost_name2 = next_cost_name2.replace("２", "2")
            next_cost_name2 = next_cost_name2.replace("３", "3")
            next_cost_name2 = next_cost_name2.replace("４", "4")
            next_cost_name2 = next_cost_name2.replace("５", "5")
            next_cost_name2 = next_cost_name2.replace("６", "6")
            next_cost_name2 = next_cost_name2.replace("７", "7")
            next_cost_name2 = next_cost_name2.replace("８", "8")
            next_cost_name2 = next_cost_name2.replace("９", "9")
            next_cost_name2 = next_cost_name2.replace("０", "0")
            next_cost_name2 = next_cost_name2.replace("１", "0")
            result_html += cost_name + "-->" + next_cost_name2 + "\n"
            if not next_cost2.id in cost_id_ary:
                cost_ary.append(next_cost_name2)
                cost_id_ary.append(next_cost2.id)
                result_html += pac_cost_diagram_det(
                    next_cost2, cost_ary, cost_id_ary, pac_ary, pac_id_ary
                )

    return result_html


def pac_diagram_det(effect, effect_ary, effect_id_ary, pac_ary, pac_id_ary):
    effect_name = effect.monster_effect_name
    effect_name = effect_name.replace(" ", "")
    effect_name = effect_name.replace("1", "1")
    effect_name = effect_name.replace("２", "2")
    effect_name = effect_name.replace("３", "3")
    effect_name = effect_name.replace("４", "4")
    effect_name = effect_name.replace("５", "5")
    effect_name = effect_name.replace("６", "6")
    effect_name = effect_name.replace("７", "7")
    effect_name = effect_name.replace("８", "8")
    effect_name = effect_name.replace("９", "9")
    effect_name = effect_name.replace("０", "0")
    effect_name = effect_name.replace("１", "0")
    result_html = ""

    if effect.pac is not None:
        pac_next = effect.pac
        pac_name1 = pac_next.pac_name
        pac_name1 = pac_name1.replace(" ", "")
        pac_name1 = pac_name1.replace("1", "1")
        pac_name1 = pac_name1.replace("２", "2")
        pac_name1 = pac_name1.replace("３", "3")
        pac_name1 = pac_name1.replace("４", "4")
        pac_name1 = pac_name1.replace("５", "5")
        pac_name1 = pac_name1.replace("６", "6")
        pac_name1 = pac_name1.replace("７", "7")
        pac_name1 = pac_name1.replace("８", "8")
        pac_name1 = pac_name1.replace("９", "9")
        pac_name1 = pac_name1.replace("０", "0")
        pac_name1 = pac_name1.replace("１", "0")
        result_html += effect_name + "-->" + pac_name1 + "\n"
        if pac_next.id not in pac_id_ary:
            pac_ary.append(pac_name1)
            pac_id_ary.append(pac_next.id)
            result_html += pac_diagram_det2(
                effect.pac, effect_ary, effect_id_ary, pac_ary, pac_id_ary
            )
    else:
        next_effect1 = effect.monster_effect_next
        if next_effect1 is not None:
            next_effect_name1 = next_effect1.monster_effect_name
            next_effect_name1 = next_effect_name1.replace(" ", "")
            next_effect_name1 = next_effect_name1.replace("1", "1")
            next_effect_name1 = next_effect_name1.replace("２", "2")
            next_effect_name1 = next_effect_name1.replace("３", "3")
            next_effect_name1 = next_effect_name1.replace("４", "4")
            next_effect_name1 = next_effect_name1.replace("５", "5")
            next_effect_name1 = next_effect_name1.replace("６", "6")
            next_effect_name1 = next_effect_name1.replace("７", "7")
            next_effect_name1 = next_effect_name1.replace("８", "8")
            next_effect_name1 = next_effect_name1.replace("９", "9")
            next_effect_name1 = next_effect_name1.replace("０", "0")
            next_effect_name1 = next_effect_name1.replace("１", "0")
            result_html += effect_name + "-->" + next_effect_name1 + "\n"
            if not next_effect1.id in effect_id_ary:
                effect_ary.append(next_effect_name1)
                effect_id_ary.append(next_effect1.id)
                result_html += pac_diagram_det(
                    next_effect1, effect_ary, effect_id_ary, pac_ary, pac_id_ary
                )
    if effect.pac2 is not None:
        pac_next2 = effect.pac2
        pac_name2 = pac_next2.pac_name
        pac_name2 = pac_name2.replace("1", "1")
        pac_name2 = pac_name2.replace("２", "2")
        pac_name2 = pac_name2.replace("３", "3")
        pac_name2 = pac_name2.replace("４", "4")
        pac_name2 = pac_name2.replace("５", "5")
        pac_name2 = pac_name2.replace("６", "6")
        pac_name2 = pac_name2.replace("７", "7")
        pac_name2 = pac_name2.replace("８", "8")
        pac_name2 = pac_name2.replace("９", "9")
        pac_name2 = pac_name2.replace("０", "0")
        pac_name2 = pac_name2.replace("１", "0")
        result_html += effect_name + "-->" + pac_name2 + "\n"
        if pac_next2.id not in pac_id_ary:
            pac_ary.append(pac_name2)
            pac_id_ary.append(pac_next2.id)
            result_html += pac_diagram_det2(
                effect.pac2, effect_ary, effect_id_ary, pac_ary, pac_id_ary
            )
    else:
        next_effect2 = effect.monster_effect_next2
        if next_effect2 is not None:
            next_effect_name2 = next_effect2.monster_effect_name
            next_effect_name2 = next_effect_name2.replace(" ", "")
            next_effect_name2 = next_effect_name2.replace("1", "1")
            next_effect_name2 = next_effect_name2.replace("２", "2")
            next_effect_name2 = next_effect_name2.replace("３", "3")
            next_effect_name2 = next_effect_name2.replace("４", "4")
            next_effect_name2 = next_effect_name2.replace("５", "5")
            next_effect_name2 = next_effect_name2.replace("６", "6")
            next_effect_name2 = next_effect_name2.replace("７", "7")
            next_effect_name2 = next_effect_name2.replace("８", "8")
            next_effect_name2 = next_effect_name2.replace("９", "9")
            next_effect_name2 = next_effect_name2.replace("０", "0")
            next_effect_name2 = next_effect_name2.replace("１", "0")
            result_html += effect_name + "-->" + next_effect_name2 + "\n"
            if not next_effect2.id in effect_id_ary:
                effect_ary.append(next_effect_name2)
                effect_id_ary.append(next_effect2.id)
                result_html += pac_diagram_det(
                    next_effect2, effect_ary, effect_id_ary, pac_ary, pac_id_ary
                )

    return result_html


def field_list_view(request):
    if request.user.is_superuser == False:
        return HttpResponse("error")
    field_size = get_object_or_404(FieldSize)
    field_x = field_size.field_x
    field_y = field_size.field_y
    context = {}
    context["field_x"] = range(field_x)
    context["field_y"] = range(field_y)
    context["tmp_structure"] = {}
    for x in range(field_x):
        context["tmp_structure"][x] = {}
        for y in range(field_y):
            tmp_structure = {}
            field = Field.objects.filter(x=x, y=y)
            mine_or_other = field[0].mine_or_other
            kind = field[0].kind.split("_")
            kinds = ""
            i = 0
            for tmp in kind:
                if tmp == "":
                    continue
                tmp2 = FieldKind.objects.filter(id=int(tmp))
                kinds += tmp2[0].field_kind_name + "<br>"
            if kinds != "":
                tmp_structure["kinds"] = kinds
            else:
                tmp_structure["kinds"] = "編集"

            tmp_structure["mine_or_other"] = mine_or_other
            tmp_structure["id"] = field[0].id
            context["tmp_structure"][x][y] = tmp_structure

    return render(request, "admin/tcgcreator/field_list.html", context=context)


def get_variable_kind(req):
    variables = GlobalVariable.objects.order_by("-priority")
    result = '<option value="0">なし</option>'
    result += '<option value="variable_turncount_1">ターンカウント</option>'
    result += '<option value="variable_chain_1">チェーン</option>'
    for variable in variables:
        if variable.mine_or_other == 0:
            result += (
                '<option value="variable_'
                + str(variable.variable_name)
                + '_1">自分'
                + variable.variable_name
                + "</option>"
            )
            result += (
                '<option value="variable_'
                + str(variable.variable_name)
                + '_2">相手'
                + variable.variable_name
                + "</option>"
            )
        else:
            result += (
                '<option value="variable_'
                + str(variable.variable_name)
                + '_3">共通'
                + variable.variable_name
                + "</option>"
            )

    return HttpResponse(result)


def get_hand_id(req):
    hands = Hand.objects.all()
    result = ""
    for hand in hands:
        result += '<option value="' + str(hand.id)+ '">' + hand.hand_name + "</option>"
    return HttpResponse(result)

def get_place_kind_to(req):
    decks = Deck.objects.all()
    hands = Hand.objects.all()
    graves = Grave.objects.all()
    fields = FieldKind.objects.all()
    result = ""
    i = 1
    result = '<option value="">なし</option>'
    for deck in decks:
        if deck.mine_or_other == 0:
            result += (
                '<option value="deck_'
                + str(i)
                + '_1">自分'
                + deck.deck_name
                + "</option>"
            )
            result += (
                '<option value="deck_'
                + str(i)
                + '_2">相手'
                + deck.deck_name
                + "</option>"
            )
            result += (
                '<option value="deck_'
                + str(i)
                + '_4">元々の持ち主'
                + deck.deck_name
                + "</option>"
            )
        else:
            result += (
                '<option value="deck_'
                + str(i)
                + '_3">共通'
                + deck.deck_name
                + "</option>"
            )
        i += 1
    i = 1
    for hand in hands:
        if hand.mine_or_other == 0:
            result += (
                '<option value="hand_'
                + str(i)
                + '_1">自分'
                + hand.hand_name
                + "</option>"
            )
            result += (
                '<option value="hand_'
                + str(i)
                + '_2">相手'
                + hand.hand_name
                + "</option>"
            )
            result += (
                '<option value="hand_'
                + str(i)
                + '_4">元々の持ち主'
                + hand.hand_name
                + "</option>"
            )
        else:
            result += (
                '<option value="hand_'
                + str(i)
                + '_3">共通'
                + hand.hand_name
                + "</option>"
            )
        i += 1
    i = 1
    for grave in graves:
        if grave.mine_or_other == 0:
            result += (
                '<option value="grave_'
                + str(i)
                + '_1">自分'
                + grave.grave_name
                + "</option>"
            )
            result += (
                '<option value="grave_'
                + str(i)
                + '_2">相手'
                + grave.grave_name
                + "</option>"
            )
            result += (
                '<option value="grave_'
                + str(i)
                + '_4">元々の持ち主'
                + grave.grave_name
                + "</option>"
            )
        else:
            result += (
                '<option value="grave_'
                + str(i)
                + '_3">共通'
                + grave.grave_name
                + "</option>"
            )
        i += 1
    i = 1
    for field in fields:
        if field.mine_or_other == 0:
            result += (
                '<option value="field_'
                + str(i)
                + '_1">自分'
                + field.field_kind_name
                + "</option>"
            )
            result += (
                '<option value="field_'
                + str(i)
                + '_2">相手'
                + field.field_kind_name
                + "</option>"
            )
            result += (
                '<option value="field_'
                + str(i)
                + '_4">元々の持ち主'
                + field.field_kind_name
                + "</option>"
            )
        else:
            result += (
                '<option value="field_'
                + str(i)
                + '_3">共通'
                + field.field_kind_name
                + "</option>"
            )
        i += 1
    return HttpResponse(result)


def get_place_kind(req, mode=0):
    decks = Deck.objects.all()
    hands = Hand.objects.all()
    graves = Grave.objects.all()
    fields = FieldKind.objects.all()
    mode2 = 0
    if req is not None:
        if "mode" in req.POST:
            mode2 = 1
    result = ""
    i = 1
    result = '<option value="">なし</option>'
    result += '<option value="player_1">プレイヤー(自分)</option>'
    result += '<option value="player_2">プレイヤー(相手)</option>'
    for deck in decks:
        if deck.mine_or_other == 0:
            result += (
                '<option value="deck_'
                + str(i)
                + '_1">自分'
                + deck.deck_name
                + "</option>"
            )
            result += (
                '<option value="deck_'
                + str(i)
                + '_2">相手'
                + deck.deck_name
                + "</option>"
            )
        else:
            result += (
                '<option value="deck_'
                + str(i)
                + '_3">共通'
                + deck.deck_name
                + "</option>"
            )
        i += 1
    i = 1
    for hand in hands:
        if hand.mine_or_other == 0:
            result += (
                '<option value="hand_'
                + str(i)
                + '_1">自分'
                + hand.hand_name
                + "</option>"
            )
            result += (
                '<option value="hand_'
                + str(i)
                + '_2">相手'
                + hand.hand_name
                + "</option>"
            )
        else:
            result += (
                '<option value="hand_'
                + str(i)
                + '_3">共通'
                + hand.hand_name
                + "</option>"
            )
        i += 1
    i = 1
    for grave in graves:
        if grave.mine_or_other == 0:
            result += (
                '<option value="grave_'
                + str(i)
                + '_1">自分'
                + grave.grave_name
                + "</option>"
            )
            result += (
                '<option value="grave_'
                + str(i)
                + '_2">相手'
                + grave.grave_name
                + "</option>"
            )
        else:
            result += (
                '<option value="grave_'
                + str(i)
                + '_3">共通'
                + grave.grave_name
                + "</option>"
            )
        i += 1
    i = 1
    if mode2 == 0:
        for field in fields:
            if field.mine_or_other == 0:
                result += (
                    '<option value="field_'
                    + str(i)
                    + '_1">自分'
                    + field.field_kind_name
                    + "</option>"
                )
                result += (
                    '<option value="field_'
                    + str(i)
                    + '_2">相手'
                    + field.field_kind_name
                    + "</option>"
                )
                result += (
                    '<option value="field_'
                    + str(i)
                    + '_4">under 自分'
                    + field.field_kind_name
                    + "</option>"
                )
                result += (
                    '<option value="field_'
                    + str(i)
                    + '_5">under 相手'
                    + field.field_kind_name
                    + "</option>"
                )
            else:
                result += (
                    '<option value="field_'
                    + str(i)
                    + '_3">共通'
                    + field.field_kind_name
                    + "</option>"
                )
                result += (
                    '<option value="field_'
                    + str(i)
                    + '_6">under 共通'
                    + field.field_kind_name
                    + "</option>"
                )
            i += 1
    if mode == 0:
        return HttpResponse(result)
    else:
        return result


def get_monster_trigger_condition(req):

    result = ""
    monster_variables = MonsterVariables.objects.all()

    result += 'フラグ<a class="show_flag" href="javascript:showFlag()">+</a><a style="display:none"  class="hide_flag" href="javascript:hideFlag()">-</a><div class="flag_box" style="display:none"><input type="text" id="flag">'
    result += '<select id="flag_equal"><option value="">全て</option><option value="=">=</option><option value="&">&</option><option value="^">^</option></select></div><br>'
    result += (
        'モンスター名<a class="show_monster_name" href="javascript:showMonsterName()">+</a><a style="display:none"  class="hide_monster_name" href="javascript:hideMonsterName()">-</a><div class="monster_name_box" style="display:none"> <input type="text" id="monster_name_0" onfocus="showMonsterNameEqual(\''
        + str(i)
        + "_0')\" >"
    )
    result += '<select id="get_monster_name_equal_0"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value="like">含む</option><option value="notlike">含まない</option><</select>'
    result += (
        '<select id="monster_name_and_or_0" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="monster_name_add_0" type="button" value="追加"  onclick="addMonsterName(\''
        + str(i)
        + "_0')\"><br>"
    )
    result += "</div><br>"
    result += 'モンスターID<a class="show_monster_id" href="javascript:showMonsterId()">+</a><a style="display:none"  class="hide_monster_id" href="javascript:hideMonsterId()">-</a><div class="monster_id_box" style="display:none">'
    result += 'モンスター位置ID<input type="text" id="monster_place_id_0_1_0"><br>'
    result += 'モンスターユニークID<input type="text" id="monster_unique_id_0_1_0">'
    result += "</div><br>"
    result += 'モンスターターンカウント<a class="show_monster_turn_count" href="javascript:showMonsterTurnCount()">+</a><a style="display:none"  class="hide_monster_turn_count" href="javascript:hideMonsterTurnCount()">-</a><div class="monster_turn_count_box" style="display:none">'
    result += '<input type="text" id="monster_turn_count_0_1_0" onfocus="showMonsterEquation(monster_turn_count_0_1_0"><br>'
    result += "</div><br>"
    result += 'モンスター変数条件<a class="show_monster_condition" href="javascript:showMonsterCondition()">+</a><a style="display:none"  class="hide_monster_condition" href="javascript:hideMonsterCondition()">-</a><div class="monster_condition_box" style="display:none">'
    for monster_variable in monster_variables:
        result += (
            monster_variable.monster_variable_name
            + '<a class="show_monster_variable_'
            + str(monster_variable.id)
            + '" href="javascript:showMonsterVariable('
            + str(monster_variable.id)
            + ')">+</a><a class="hide_monster_variable_'
            + str(monster_variable.id)
            + '" href="javascript:hideMonsterVariable('
            + str(monster_variable.id)
            + ')">-</a><div class="monster_variable_box'
            + str(monster_variable.id)
            + '" style="display:none">'
        )
        if (
            monster_variable.monster_variable_kind_id.monster_variable_name == "数値"
        ):
            result += (
                '<input type="text" onchange="changeToEqual("'+str(monster_variable.id)+'_0")" onfocus="showMonsterEquation(\'get_monster_variable_'
                + str(monster_variable.id)
                + '_0\')" id="get_monster_variable_'
                + str(monster_variable.id)
                + '_0">'
                )
            result += (
                '<input type="hidden" id="get_monster_variable_name_'
                + str(monster_variable.id)
                + '" value="'
                + monster_variable.monster_variable_name
                + '">'
            )
            result += (
                '<select id="get_monster_variable_equal_'
                + str(monster_variable.id)
                + '_0"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select>'
            )
            result += (
                '<select id="monster_variable_and_or_'
                + str(monster_variable.id)
                + '_0" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="monster_variable_add_'
                + str(monster_variable.id)
                + '_0" type="button" value="追加"  onclick="addMonsterEquation(\''
                + str(i)
                + "_"
                + str(monster_variable.id)
                + "_0')\"><br>"
            )
            result += (
                '<select id="monster_variable_init_'
                + str(monster_variable.id)
                + '_0" > <option value="0">現在の値</option><option value="1">元々の値</option> <option value="2">元々の元々の値</option> </select><input id="monster_variable_add_'
                + str(monster_variable.id)
                + '_0" type="button" value="追加"  onclick="addMonsterEquation(\''
                + str(i)
                + "_"
                + str(monster_variable.id)
                + "_0')\"><br>"
            )

        else:
            result += (
                '<input type="hidden" id="get_monster_variable_name_'
                + str(monster_variable.id)
                + '" value="'
                + monster_variable.monster_variable_name
                + '">'
            )
            result += (
                '<select id="get_monster_variable'
                + "_"
                + str(monster_variable.id)
                + '_0">'
            )
            result += '<option value="0">全て</option>'
            result += (
                '<select id="monster_variable_init_'
                + str(monster_variable.id)
                + '_0" > <option value="0">現在の値</option><option value="1">元々の値</option> <option value="2">元々の元々の値</option> </select><input id="monster_variable_add_'
                + str(monster_variable.id)
                + '_0" type="button" value="追加"  onclick="addMonsterEquation(\''
                + str(i)
                + "_"
                + str(monster_variable.id)
                + "_0')\"><br>"
            )

            kinds = monster_variable.monster_variable_kind_id.monster_variable_sentence
            kinds_org = kinds
            kinds = kinds.split("|")
            k = 1
            for kind in kinds:
                result += '<option value="' + str(k) + '">' + kind + "</option>"
                k += 1
            result += "</select>"
            result += (
                '<select id="monster_variable_and_or_'
                + str(monster_variable.id)
                + '_0" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="monster_variable_add'
                + "_"
                + str(monster_variable.id)
                + '_0" type="button" value="追加"  onclick="addMonsterEquation2(\''
                + str(i)
                + "_"
                + str(monster_variable.id)
                + "_0','"
                + kinds_org
                + "')\"><br>"
            )
    monster_effect_kind = MonsterEffectKind.objects.all()
    result += "</div><br>"
    result += "<div>"
    result += "モンスター効果valid"
    result += '<select id="monster_effect_kind">'
    i = 1
    result += '<option value="0">全て</option>'
    for tmp_val in monster_effect_kind:
        result += (
            '<option value="'
            + str(i)
            + '">'
            + tmp_val.monster_effect_name
            + "</option>"
        )
    result += "</select>"
    result += "</div><br>"
    return HttpResponse(result)


def get_monster_move(req):

    if "i" in req.POST:
        i = req.POST["i"]
        add_i = "_" + i
    else:
        add_i = ""

    result = ""
    monster_variables = MonsterVariables.objects.all()

    result += 'フラグ<a class="show_flag" href="javascript:showFlag()">+</a><a style="display:none" class="hide_flag" href="javascript:hideFlag()">-</a><div class="flag_box" style="display:none"><input type="text" id="flag">'
    result += (
        '<select id="flag_equal'
        + add_i
        + '"><option value="">全て</option><option value="=">=</option></select><option value="&">&</option><option value="^">^</option></div><br>'
    )
    result += (
        'モンスター名<a class="show_monster_name" href="javascript:showMonsterName()">+</a><a style="display:none"  class="hide_monster_name" href="javascript:hideMonsterName()">-</a><div class="monster_name_box" style="display:none"> <input type="text" id="monster_name'
        + add_i
        + '_0" onfocus="showMonsterNameEqual(\''
        + str(i)
        + "_0')\" >"
    )
    result += (
        '<select id="get_monster_name_equal'
        + add_i
        + '_0"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value="like">含む</option><option value="notlike">含まない</option><</select>'
    )
    result += (
        '<select id="monster_name_and_or'
        + add_i
        + '_0" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="monster_name_add'
        + add_i
        + '_0" type="button" value="追加"  onclick="addMonsterName(\''
        + str(i)
        + "_0')\"><br>"
    )
    result += "</div><br>"
    result += 'モンスターID<a class="show_monster_id" href="javascript:showMonsterId()">+</a><a style="display:none"  class="hide_monster_id" href="javascript:hideMonsterId()">-</a><div class="monster_id_box" style="display:none">'
    result += 'モンスター位置ID<input type="text" id="monster_place_id_0"><br>'
    result += 'モンスターユニークID<input type="text" id="monster_unique_id_0">'
    result += "</div><br>"
    result += 'モンスターターンカウント<a class="show_monster_turn_count" href="javascript:showMonsterTurnCount()">+</a><a style="display:none"  class="hide_monster_turn_count" href="javascript:hideMonsterTurnCount()">-</a><div class="monster_turn_count_box" style="display:none">'
    result += '<input type="text" id="monster_turn_count_0" onfocus="showMonsterEquation(monster_turn_count_0"><br>'
    result += "</div><br>"
    result += 'モンスター変数条件<a class="show_monster_condition" href="javascript:showMonsterCondition()">+</a><a style="display:none" class="hide_monster_condition" href="javascript:hideMonsterCondition()">-</a><div class="monster_condition_box" style="display:none">'
    for monster_variable in monster_variables:
        result += (
            monster_variable.monster_variable_name
            + '<a class="show_monster_variable_'
            + str(monster_variable.id)
            + '" href="javascript:showMonsterVariable('
            + str(monster_variable.id)
            + ')">+</a><a style="display:none" class="hide_monster_variable_'
            + str(monster_variable.id)
            + '" href="javascript:hideMonsterVariable('
            + str(monster_variable.id)
            + ')">-</a><div class="monster_variable_box'
            + str(monster_variable.id)
            + '" style="display:none">'
        )
        if (
            monster_variable.monster_variable_kind_id.monster_variable_name == "数値"
        ):
            result += (
                '<input type="hidden" id="get_monster_variable_name'
                + add_i
                + "_"
                + str(monster_variable.id)
                + '" value="'
                + monster_variable.monster_variable_name
                + '">'
            )
            result += (
                monster_variable.monster_variable_name
                + '<input type="text" onchange="chagneToEqual(\'get_monster_variable'
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0\')"' 
                + ' onfocus="showMonsterEquation(\'get_monster_variable'
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0\')" id="get_monster_variable'
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0">'
            )
            result += (
                '<select id="get_monster_variable_equal'
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select>'
            )
            result += (
                '<select id="monster_variable_and_or'
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="monster_variable_add'
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0" type="button" value="追加"  onclick="addMonsterEquation(\''
                + str(i)
                + "_"
                + str(monster_variable.id)
                + "_0')\"><br>"
            )
            result += (
                '<select id="monster_variable_init'
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0" > <option value="0">現在の値</option><option value="1">元々の値</option> <option value="2">元々の元々の値</option> </select><input id="monster_variable_add_'
                + str(monster_variable.id)
                + '_0" type="button" value="追加"  onclick="addMonsterEquation(\''
                + str(i)
                + "_"
                + str(monster_variable.id)
                + "_0')\"><br>"
            )

        else:
            result += (
                '<input type="hidden" id="get_monster_variable_name'
                + add_i
                + "_"
                + str(monster_variable.id)
                + '" value="'
                + monster_variable.monster_variable_name
                + '">'
            )
            result += (
                monster_variable.monster_variable_name
                + '<select id="get_monster_variable'
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0">'
            )
            result += '<option value="0">全て</option>'
            result += (
                '<select id="monster_variable_init'
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0" > <option value="0">現在の値</option><option value="1">元々の値</option> <option value="2">元々の元々の値</option> </select><input id="monster_variable_add_'
                + str(monster_variable.id)
                + '_0" type="button" value="追加"  onclick="addMonsterEquation(\''
                + str(i)
                + "_"
                + str(monster_variable.id)
                + "_0')\"><br>"
            )

            kinds = monster_variable.monster_variable_kind_id.monster_variable_sentence
            kinds_org = kinds
            kinds = kinds.split("|")
            k = 1
            for kind in kinds:
                result += '<option value="' + str(k) + '">' + kind + "</option>"
                k += 1
            result += "</select>"
            result += (
                '<select id="monster_variable_and_or'
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="monster_variable_add'
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0" type="button" value="追加"  onclick="addMonsterEquation2(\''
                + str(i)
                + "_"
                + str(monster_variable.id)
                + "_0','"
                + kinds_org
                + "')\"><br>"
            )
        result += "</div><br>"
    result += "</div><br>"
    return HttpResponse(result)


def get_monster_condition(req):

    if "i" in req.POST:
        i = req.POST["i"]
        add_i = "_" + i
    else:
        add_i = ""
    if "j" in req.POST:
        j = req.POST["j"]
        add_j = "_" + j
    else:
        add_j = ""

    result = ""
    monster_variables = MonsterVariables.objects.all()
    monsters = Monster.objects.all()

    result += (
        'フラグ<a class="show_flag" href="javascript:showFlag()">+</a><a style="display:none"  class="hide_flag" href="javascript:hideFlag()">-</a><div class="flag_box" style="display:none"><input type="text" id="flag'
        + add_j
        + add_i
        + '">'
    )
    result += (
        '<select id="flag_equal'
        + add_j
        + add_i
        + '"><option value="">全て</option><option value="=">=</option><option value="&">&</option><option value="^">^</option></select></div><br>'
    )
    result += (
        'モンスター名<a class="show_monster_name" href="javascript:showMonsterName()">+</a><a style="display:none"  class="hide_monster_name" href="javascript:hideMonsterName()">-</a><div class="monster_name_box" style="display:none"><input type="text" id="monster_name'
        + add_j
        + add_i
        + '_0" onfocus="showMonsterNameEqual(\''
        + str(j)
        + "_"
        + str(i)
        + "_0')\" >"
    )
    result += (
        '<select id="get_monster_name_equal'
        + add_j
        + add_i
        + '_0"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value="like">含む</option><option value="notlike">含まない</option><</select>'
    )
    result += (
        '<select id="monster_name_and_or'
        + add_j
        + add_i
        + '_0" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="monster_name_add'
        + add_j
        + add_i
        + '_0" type="button" value="追加"  onclick="addMonsterName(\''
        + str(j)
        + "_"
        + str(i)
        + "_0')\"><br>"
    )
    result += "</div><br>"
    result += 'モンスター<a class="show_monster" href="javascript:showMonster()">+</a><a style="display:none"  class="hide_monster" href="javascript:hideMonster()">-</a><div class="monster_box" style="display:none">'
    result += '<input id="get_monster'+add_j+add_i+'"><select id="get_monster_select' + add_j + add_i + '" onchange="javascript:putGetMonster('+j+','+i+')">'
    result += '<option  value="0">全て</option>'
    for monster in monsters:
        result += (
            '<option  value="'
            + str(monster.id)
            + '">'
            + monster.monster_name
            + "</option>"
        )
    result += (
        '</select><input type="text" id="get_monster'
        + add_j
        + add_i
        + '_specify"><input type="button" onclick="getMonsterSpecify(\'get_monster_select'
        + add_j
        + add_i
        + '\')" value="絞り込み">'
    )
    result += "</div><br>"
    result += 'モンスターID<a class="show_monster_id" href="javascript:showMonsterId()">+</a><a style="display:none"  class="hide_monster_id" href="javascript:hideMonsterId()">-</a><div class="monster_id_box" style="display:none">'
    result += (
        'モンスター位置ID<input type="text" id="monster_place_id' + add_j + add_i + '"><br>'
    )
    result += (
        'モンスターユニークID<input type="text" id="monster_unique_id' + add_j + add_i + '"><br>'
    )
    result += "</div><br>"
    result += 'モンスターターンカウント<a class="show_monster_turn_count" href="javascript:showMonsterTurnCount()">+</a><a style="display:none"  class="hide_monster_turn_count" href="javascript:hideMonsterTurnCount()">-</a><div class="monster_turn_count_box" style="display:none">'
    result += (
        '<input type="text" id="monster_turn_count'
        + add_j
        + add_i
        + '" onfocus="showMonsterEquation(\'monster_turn_count'
        + add_j
        + add_i
        + "')\"><br>"
    )
    result += "</div><br>"
    result += 'モンスター場所from<a class="show_monster_from" href="javascript:showMonsterFrom()">+</a><a style="display:none"  class="hide_monster_from" href="javascript:hideMonsterFrom()">-</a><div class="monster_from_box" style="display:none">'
    place_kind = get_place_kind(None, 1)
    result += (
        '<select id="monster_from'
        + add_j
        + add_i
        + '_0">'
        + place_kind
        + '</select><select id="monster_from_add_'
        + str(j)
        + "_"
        + str(i)
        + "_0\" onchange=\"addPlace('monster_from',"
        + str(j)
        + ","
        + str(i)
        + ',null,1)" class="monster_condition_place" style=""> <option value=""></option><option value="and"> <option value="or">または</option> </select>'
    )
    result += "</div><br>"
    result += 'モンスター変数条件<a class="show_monster_condition" href="javascript:showMonsterCondition()">+</a><a style="display:none"  class="hide_monster_condition" href="javascript:hideMonsterCondition()">-</a><div class="monster_condition_box" style="display:none">'
    for monster_variable in monster_variables:
        result += (
            monster_variable.monster_variable_name
            + '<a class="show_monster_variable_'
            + str(monster_variable.id)
            + '" href="javascript:showMonsterVariable('
            + str(monster_variable.id)
            + ')">+</a><a style="display:none" class="hide_monster_variable_'
            + str(monster_variable.id)
            + '" href="javascript:hideMonsterVariable('
            + str(monster_variable.id)
            + ')">-</a><div class="monster_variable_box'
            + str(monster_variable.id)
            + '" style="display:none">'
        )
        if (
            monster_variable.monster_variable_kind_id.monster_variable_name == "数値"
        ):
            result += (
                '<input type="hidden" id="get_monster_variable_name'
                + add_j
                + add_i
                + "_"
                + str(monster_variable.id)
                + '" value="'
                + monster_variable.monster_variable_name
                + '">'
            )
            result += (
                monster_variable.monster_variable_name
                + '<input type="text" onfocus="changeToEqual(\'get_monster_variable'
                + add_j
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0\') '
                + ' ;showMonsterEquation(\'get_monster_variable'
                + add_j
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0\')" id="get_monster_variable'
                + add_j
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0">'
            )
            result += (
               '<select onchange="deleteMonsterVariable(\'get_monster_variable'
                + add_j + add_i + "_" + str(monster_variable.id) + '_0\')"' 
                + ' id="get_monster_variable_equal'
                + add_j
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select>'
            )
            result += (
                '<select id="monster_variable_and_or'
                + add_j
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select>'
            )
            result += (
                '<select id="monster_variable_init'
                + add_j
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0" > <option value="0">現在の値</option><option value="1">元々の値</option> <option value="2">元々の元々の値</option> </select>'
            )
            result += (
                '<input id="monster_variable_add_'
                + str(j)
                + "_"
                + str(i)
                + "_"
                + str(monster_variable.id)
                + '_0" type="button" value="追加"  onclick="addMonsterEquation(\''
                + str(j)
                + "_"
                + str(i)
                + "_"
                + str(monster_variable.id)
                + "_0')\"><br>"
            )

        else:
            result += (
                '<input type="hidden" id="get_monster_variable_name'
                + add_j
                + add_i
                + "_"
                + str(monster_variable.id)
                + '" value="'
                + monster_variable.monster_variable_name
                + '">'
            )
            result += (
                monster_variable.monster_variable_name
                + '<select id="get_monster_variable'
                + add_j
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0">'
            )
            result += '<option value="0">全て</option>'

            kinds = monster_variable.monster_variable_kind_id.monster_variable_sentence
            kinds_org = kinds
            kinds = kinds.split("|")
            k = 1
            for kind in kinds:
                result += '<option value="' + str(k) + '">' + kind + "</option>"
                k += 1
            result += "</select>"
            result += (
                '<select id="monster_variable_and_or'
                + add_j
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select>'
            )
            result += (
                '<select id="monster_variable_init'
                + add_j
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0" > <option value="0">現在の値</option><option value="1">元々の値</option> <option value="2">元々の元々の値</option> </select>'
            )
            result += (
                '<input id="monster_variable_add_'
                + str(j)
                + "_"
                + str(i)
                + "_"
                + str(monster_variable.id)
                + '_0" type="button" value="追加"  onclick="addMonsterEquation2(\''
                + str(j)
                + "_"
                + str(i)
                + "_"
                + str(monster_variable.id)
                + "_0','"
                + kinds_org
                + "')\"><br>"
            )
        result += "</div><br>"
    result += "</div><br>"
    result += 'カスタムモンスター変数条件<a class="show_custom_monster_condition" href="javascript:showCustomMonsterCondition()">+</a><a style="display:none"  class="hide_custom_monster_condition" href="javascript:hideCustomMonsterCondition()">-</a><div class="custom_monster_condition_box" style="display:none">'
    result += (
        '<input type="button" value="カスタム追加" id="custom_add_'
        + str(j)
        + "_"
        + str(i)
        + '_0_0" class="custom_add" onclick="addCustomMonsterCondition(\''
        + str(j)
        + "_"
        + str(i)
        + "_0_0')\">"
    )
    result += "</div><br>"
    result += '<div>under<a class="show_under" href="javascript:showUnder()">+</a><a style="display:none"  class="hide_under" href="javascript:hideUnder()">-</a>'
    result += '<div class="under" style="display:none">'
    result += (
        'under フラグ<a class="show_under_flag" href="javascript:showUnderFlag()">+</a><a style="display:none"  class="hide_under_flag" href="javascript:hideUnderFlag()">-</a><div class="flag_under_box" style="display:none"><input type="text" id="under_flag'
        + add_j
        + add_i
        + '">'
    )
    result += (
        '<select id="under_flag_equal'
        + add_j
        + add_i
        + '"><option value="">全て</option><option value="=">=</option><option value="&">&</option><option value="^">^</option></select></div><br>'
    )

    result += (
        'under モンスター名<a class="show_under_name" href="javascript:showUnderName()">+</a><a style="display:none"  class="hide_under_name" href="javascript:hideUnderName()">-</a><div class="under_name_box" style="display:none"> <input type="text" id="under_name'
        + add_j
        + add_i
        + '_0" onfocus="showUnderNameEqual(\''
        + str(i)
        + "_0')\" >"
    )
    result += (
        '<select id="get_under_name_equal'
        + add_j
        + add_i
        + '_0"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value="like">含む</option><option value="notlike">含まない</option><</select>'
    )
    result += (
        '<select id="under_name_and_or_0" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select><input id="under_name_add_0" type="button" value="追加"  onclick="addUnderName(\''
        + str(i)
        + "_0')\"><br>"
    )
    result += "</div><br>"
    result += 'under モンスター<a class="show_under_monster" href="javascript:showUnderMonster()">+</a><a style="display:none"  class="hide_under_monster" href="javascript:hideUnderMonster()">-</a><div class="under_monster_box" style="display:none">'
    result += '<select id="get_under' + add_j + add_i + '">'
    result += '<option  value="0">全て</option>'
    for monster in monsters:
        result += (
            '<option  value="'
            + str(monster.id)
            + '">'
            + monster.monster_name
            + "</option>"
        )
    result += "</select>"
    result += "</div><br>"
    result += 'under モンスター条件<a class="show_under_condition" href="javascript:showUnderCondition()">+</a><a style="display:none"  class="hide_under_condition" href="javascript:hideUnderCondition()">-</a><div class="under_condition_box" style="display:none">'
    for monster_variable in monster_variables:
        result += (
            monster_variable.monster_variable_name
            + '<a class="show_under_variable_'
            + str(monster_variable.id)
            + '" href="javascript:showUnderVariable('
            + str(monster_variable.id)
            + ')">+</a><a class="hide_under_variable_'
            + str(monster_variable.id)
            + '" href="javascript:hideUnderVariable('
            + str(monster_variable.id)
            + ')">-</a><div class="under_variable_box'
            + str(monster_variable.id)
            + '" style="display:none">'
        )
        if (
            monster_variable.monster_variable_kind_id.monster_variable_name == "数値"
        ):
            result += (
                '<input type="text" onfocus="showUnderEquation(\'get_under_variable_'
                + str(monster_variable.id)
                + '_0\')" id="get_under_variable'
                + add_j
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0">'
            )
            result += (
                '<input type="hidden" id="get_under_variable_name'
                + add_j
                + add_i
                + "_"
                + str(monster_variable.id)
                + '" value="'
                + monster_variable.monster_variable_name
                + '">'
            )
            result += (
                '<select id="get_under_variable_equal'
                + add_j
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select>'
            )
            result += (
                '<select id="under_variable_and_or'
                + add_j
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select>'
            )
            result += (
                '<select id="under_variable_init'
                + add_j
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0" > <option value="0">現在の値</option><option value="1">元々の値</option> <option value="2">元々の元々の値</option> </select>'
            )
            result += (
                '<input id="under_variable_add_'
                + str(j)
                + "_"
                + str(i)
                + "_"
                + str(monster_variable.id)
                + '_0" type="button" value="追加"  onclick="addUnderEquation(\''
                + str(j)
                + "_"
                + str(i)
                + "_"
                + str(monster_variable.id)
                + "_0')\"><br>"
            )
            result += "</div><br>"

        else:
            result += (
                '<input type="hidden" id="get_under_variable_name'
                + add_j
                + add_i
                + "_"
                + str(monster_variable.id)
                + '" value="'
                + monster_variable.monster_variable_name
                + '">'
            )
            result += (
                '<select id="get_under_variable'
                + add_j
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0">'
            )
            result += '<option value="0">全て</option>'

            kinds = monster_variable.monster_variable_kind_id.monster_variable_sentence
            kinds_org = kinds
            kinds = kinds.split("|")
            k = 1
            for kind in kinds:
                result += '<option value="' + str(k) + '">' + kind + "</option>"
                k += 1
            result += "</select>"
            result += (
                '<select id="under_variable_init'
                + add_j
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0" > <option value="0">現在の値</option><option value="1">元々の値</option> <option value="2">元々の元々の値</option> </select>'
            )
            result += (
                '<select id="under_variable_and_or'
                + add_j
                + add_i
                + "_"
                + str(monster_variable.id)
                + '_0" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select>'
            )
            result += (
                '<input id="under_variable_add_'
                + str(j)
                + "_"
                + str(i)
                + "_"
                + str(monster_variable.id)
                + '_0" type="button" value="追加"  onclick="addUnderEquation2(\''
                + str(j)
                + "_"
                + str(i)
                + "_"
                + str(monster_variable.id)
                + "_0','"
                + kinds_org
                + "')\"><br>"
            )
            result += "</div><br>"
    result_tmp = ""
    for monster_variable in monster_variables:
        result_tmp += (
            '<option value="'
            + str(monster_variable.monster_variable_name)
            + '">'
            + monster_variable.monster_variable_name
            + "</option>"
        )
    result += "</div><br>"
    result += 'under モンスターの数<a class="show_under_equation" href="javascript:showUnderEquation()">+</a><a style="display:none" class="hide_under_equation" href="javascript:hideUnderEquation()">-</a>'
    result += '<div style="display:none" class="under_equation">'
    result += (
        '演算子<select id="get_under_equation_det_'
        + str(j)
        + '"><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select><br>'
    )
    result += (
        '種類<select id="get_under_equation_kind_'
        + str(j)
        + '"><option value="number">数</option><option value="kind">種類</option><option value="same_name">同名</option><option value="x">x</option><option value="y">y</option>'
        + result_tmp
        + "</select><br>"
    )
    result += (
        'min<input type="text" id="under_min_equation_number_'
        + str(j)
        + '" value="" onfocus="showMinEquation('
        + str(j)
        + ')">'
    )
    result += (
        'max<input type="text" id="under_max_equation_number_'
        + str(j)
        + '" value="" onfocus="showMaxEquation('
        + str(j)
        + ')">'
    )
    result += "</div><br>"
    result += "</div><br>"
    result += 'リレーション<a class="show_relation" href="javascript:showRelation()">+</a><a style="display:none"  class="hide_relation" href="javascript:hideRelation()">-</a><div class="relation_box" style="display:none">'
    result += (
        '<input type="button" value="リレーション追加" id="relation_add_'
        + str(j)
        + "_"
        + str(i)
        + '_0_0" class="relation_add" onclick="addRelation(\''
        + str(j)
        + "_"
        + str(i)
        + "_0_0')\">"
    )
    result += "</div><br>"
    result += "<div>"
    result += "モンスター効果valid"
    result += (
        '<input type="text" id="monster_effect_kind_'
        + str(j)
        + "_"
        + str(i)
        + '"><select id="monster_effect_kind_choose_'
        + str(j)
        + "_"
        + str(i)
        + '">'
    )
    k = 1
    result += '<option value="0">全て</option>'
    monster_effect_kind = MonsterEffectKind.objects.all()
    for tmp_val in monster_effect_kind:
        result += (
            '<option value="'
            + str(k)
            + '">'
            + tmp_val.monster_effect_name
            + "</option>"
        )
        k += 1
    result += (
        '</select><input type="button" value="追加" onclick="changeMonsterEffectValidKind('
        + str(j)
        + ","
        + str(i)
        + ')" >'
    )
    result += "</div><br>"
    return HttpResponse(result)


def get_variables_condition_for_copy(req):
    if "id" in req.POST:
        id = req.POST["id"]
    monster_variables = MonsterVariables.objects.all()

    result = (
        'コピーモンスター変数<a class="show_'
        + id
        + '_variable" href="javascript:showMonsterVariableForCopy(\''
        + id
        + '\')">+</a><a style="display:none"  class="hide_'
        + id
        + '_variable" href="javascript:hideMonsterVariableForCopy(\''
        + id
        + '\')">-</a><div class="variable_box_'
        + id
        + '" style="display:none">'
    )
    i = 0
    for monster_variable in monster_variables:
        result += monster_variable.monster_variable_name
        result += (
            '<input type="checkbox" id="'
            + id
            + "_"
            + str(i)
            + '" value="'
            + monster_variable.monster_variable_name
            + '"">'
        )
        result += (
            '元々From<input type="checkbox" id="'
            + id
            + "_"
            + str(i)
            + '_init_from" value="1">'
        )
        result += (
            '元々To<input type="checkbox" id="'
            + id
            + "_"
            + str(i)
            + '_init_to" value="1">'
        )
        result += (
            '<input type="hidden" id="monster_variable_name'
            + "_"
            + id
            + "_"
            + str(i)
            + '" value="'
            + monster_variable.monster_variable_name
            + '">'
        )
        result += "<br>"
        i += 1
    result += "</div><br>"
    result += "コピーカスタムモンスター変数"
    result += (
        '<input type="button" value="カスタム追加" id="'
        + id
        + '_custom_add" class="custom_add" onclick="addCustomVariable(\''
        + id
        + "')\">"
    )
    return HttpResponse(result)


def get_monster_to(req):

    result = ""
    monster_variables = MonsterVariables.objects.all()

    result += 'モンスター名 <input type="text" id="monster_name_to">'
    result += '<select id="get_monster_name_equal_to"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value="like">含む</option><option value="notlike">含まない</option><</select><br>'
    for monster_variable in monster_variables:
        if (
            monster_variable.monster_variable_kind_id.monster_variable_name == "数値"
        ):
            result += (
                '<input type="hidden" id="get_monster_variable_name_'
                + str(monster_variable.id)
                + '" value="'
                + monster_variable.monster_variable_name
                + '">'
            )
            result += (
                monster_variable.monster_variable_name
                + '<input type="number" id="get_monster_variable_'
                + str(monster_variable.id)
                + '_to">'
            )
            result += (
                '<select id="get_monster_variable_equal_'
                + str(monster_variable.id)
                + '_to"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select><br>'
            )
            result += (
                '<select id="monster_variable_init_'
                + str(monster_variable.id)
                + '_0" > <option value="0">現在の値</option><option value="1">元々の値</option> <option value="2">元々の元々の値</option> </select><input id="monster_variable_add_'
                + str(monster_variable.id)
                + '_0" type="button" value="追加"  onclick="addMonsterEquation(\''
                + str(i)
                + "_"
                + str(monster_variable.id)
                + "_0')\"><br>"
            )

        else:
            result += (
                '<input type="hidden" id="get_monster_variable_name_'
                + str(monster_variable.id)
                + '" value="'
                + monster_variable.monster_variable_name
                + '">'
            )
            result += (
                monster_variable.monster_variable_name
                + '<select id="get_monster_variable_'
                + str(monster_variable.id)
                + '_to">'
            )
            result += '<option value="0">全て</option>'
            result += (
                '<select id="monster_variable_init_'
                + str(monster_variable.id)
                + '_0" > <option value="0">現在の値</option><option value="1">元々の値</option> <option value="2">元々の元々の値</option> </select><input id="monster_variable_add_'
                + str(monster_variable.id)
                + '_0" type="button" value="追加"  onclick="addMonsterEquation(\''
                + str(i)
                + "_"
                + str(monster_variable.id)
                + "_0')\"><br>"
            )

            kinds = monster_variable.monster_variable_kind_id.monster_variable_sentence
            kinds = kinds.split("|")
            i = 1
            for kind in kinds:
                result += '<option value="' + str(i) + '">' + kind + "</option>"
                i += 1
            result += "</select><br>"
    return HttpResponse(result)


def get_phase_and_turn(req):
    phases = Phase.objects.all()
    timings = Timing.objects.all()
    result = ""
    result += '<option value="chain_1">チェーン終了時</option>'
    result += '<option value="turn_1">自分ターン開始時</option>'
    result += '<option value="turn_2">相手ターン開始時</option>'
    result += '<option value="turn_3">両方ターン開始時</option>'
    for phase in phases:
        if phase.id == 1:
            continue
        result += (
            '<option value="phase_1_'
            + str(phase.id)
            + '">自分'
            + phase.phase_name
            + "開始時</option>"
        )
        result += (
            '<option value="phase_2_'
            + str(phase.id)
            + '">相手'
            + phase.phase_name
            + "開始時</option>"
        )
        result += (
            '<option value="phase_3_'
            + str(phase.id)
            + '">両方'
            + phase.phase_name
            + "開始時</option>"
        )
        result += (
            '<option value="phaseend_1_'
            + str(phase.id)
            + '">自分'
            + phase.phase_name
            + "終了時</option>"
        )
        result += (
            '<option value="phaseend_2_'
            + str(phase.id)
            + '">相手'
            + phase.phase_name
            + "終了時</option>"
        )
        result += (
            '<option value="phaseend_3_'
            + str(phase.id)
            + '">両方'
            + phase.phase_name
            + "終了時</option>"
        )
    for timing in timings:
        result += (
            '<option value="timingbegin_1_'
            + str(timing.id)
            + '">自分'
            + timing.timing_name
            + "開始時</option>"
        )
        result += (
            '<option value="timingbegin_2_'
            + str(timing.id)
            + '">相手'
            + timing.timing_name
            + "開始時<</option>"
        )
        result += (
            '<option value="timingbegin_3_'
            + str(timing.id)
            + '">両方'
            + timing.timing_name
            + "開始時<</option>"
        )
        result += (
            '<option value="timing_1_'
            + str(timing.id)
            + '">自分'
            + timing.timing_name
            + "終了時</option>"
        )
        result += (
            '<option value="timing_2_'
            + str(timing.id)
            + '">相手'
            + timing.timing_name
            + "終了時<</option>"
        )
        result += (
            '<option value="timing_3_'
            + str(timing.id)
            + '">両方'
            + timing.timing_name
            + "終了時<</option>"
        )
    return HttpResponse(result)


def get_timing(req):
    phases = Phase.objects.all()
    result = ""
    for phase in phases:
        result += (
            '<option value="' + str(phase.id) + '">' + phase.phase_name + "</option>"
        )
    return HttpResponse(result)


"""
def get_monster_variable_change_condition(req):
    
    result = ""
    monster_variables = MonsterVariables.objects.all()
    
    for monster_variable in monster_variables:
        if (monster_variable.monster_variable_kind_id.id == 0 or monster_variable.monster_variable_kind_id.id == 1):
            result+=monster_variable.monster_variable_name+"<input type=\"number\" id=\"get_monster_variable_change_variable_"+str(monster_variable.id)+"\">"
            result+='<select id="get_monster_variable_variable_equal_'+str(monster_variable.id)+'"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select><br>'

        else:
            result+=monster_variable.monster_variable_name+"<select id=\"get_monster_variable_variable_"+str(monster_variable.id)+"\">"
            result+="<option value=\"0\">全て</option>"

            kinds = monster_variable.monster_variable_kind_id.monster_variable_sentence
            kinds = kinds.split("|")
            i=1
            for kind in kinds:
                result+="<option value=\""+str(i)+"\">"+kind+"</option>"
                i+=1
            result+="</select><br>"
    return HttpResponse(result)
"""


def get_trigger(req):

    result = ""
    monster_variables = MonsterVariables.objects.all()

    for monster_variable in monster_variables:
        if (
            monster_variable.monster_variable_kind_id.monster_variable_name == "数値"
        ):
            result += (
                monster_variable.monster_variable_name
                + '<input type="number" id="get_trigger_variable_'
                + str(monster_variable.id)
                + '">'
            )
            result += (
                '<input type="hidden" id="get_trigger_variable_name_'
                + str(monster_variable.id)
                + '" value="'
                + monster_variable.monster_variable_name
                + '">'
            )
            result += (
                '<select id="get_trigger_variable_equal_'
                + str(monster_variable.id)
                + '"><option value="">全て</option><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select><br>'
            )
            result += (
                '<select id="trigger_variable_init_'
                + str(monster_variable.id)
                + '_0" > <option value="0">現在の値</option><option value="1">元々の値</option> <option value="2">元々の元々の値</option> </select><input id="monster_variable_add_'
                + str(monster_variable.id)
                + '_0" type="button" value="追加"  onclick="addMonsterEquation(\''
                + str(i)
                + "_"
                + str(monster_variable.id)
                + "_0')\"><br>"
            )

        else:
            result += (
                monster_variable.monster_variable_name
                + '<select id="get_trigger_variable_'
                + str(monster_variable.id)
                + '">'
            )
            result += (
                '<input type="hidden" id="get_trigger_variable_name_'
                + str(monster_variable.id)
                + '" value="'
                + monster_variable.monster_variable_name
                + '">'
            )
            result += '<option value="0">全て</option>'
            result += (
                '<select id="trigger_variable_init_'
                + str(monster_variable.id)
                + '_0" > <option value="0">現在の値</option><option value="1">元々の値</option> <option value="2">元々の元々の値</option> </select><input id="monster_variable_add_'
                + str(monster_variable.id)
                + '_0" type="button" value="追加"  onclick="addMonsterEquation(\''
                + str(i)
                + "_"
                + str(monster_variable.id)
                + "_0')\"><br>"
            )

            kinds = monster_variable.monster_variable_kind_id.monster_variable_sentence
            kinds = kinds.split("|")
            i = 1
            for kind in kinds:
                result += '<option value="' + str(i) + '">' + kind + "</option>"
                i += 1
            result += "</select><br>"
    return HttpResponse(result)


def get_equation_0():
    monster_variables = MonsterVariables.objects.all()
    result = ""
    result += '種類<select id="get_equation_kind"><option value="number">数</option><option value="kind">種類</option><option value="same_name">同名</option><option value="x">x</option><option value="y">y</option>'
    for monster_variable in monster_variables:
        result += (
            "<option value=num_"
            + str(monster_variable.monster_variable_name)
            + ">"
            + monster_variable.monster_variable_name
            + " 数</option>"
        )
        result += (
            "<option value=kind_"
            + str(monster_variable.monster_variable_name)
            + ">"
            + monster_variable.monster_variable_name
            + " 種類</option>"
        )
    result += "</select><br>"
    return HttpResponse(result)


def get_equation_to(req):
    result = ""
    result += '種類<select id="get_equation_kind_to"><option value="number">数</option><option value="kind">種類</option></select><br>'
    result += 'min<input type="text" id="min_equation_number_to" value="1" onfocus="showMinEquationTo()">'
    result += 'max<input type="text" id="max_equation_number_to" value="1" onfocus="showMaxEquationTo()">'
    return HttpResponse(result)


def get_equation(req):
    if "c" in req.POST:
        c = req.POST["c"]
    monster_variables = MonsterVariables.objects.all()
    result_tmp = ""
    for monster_variable in monster_variables:
        result_tmp += (
            '<option value="'
            + str(monster_variable.monster_variable_name)
            + '">'
            + monster_variable.monster_variable_name
            + "</option>"
        )
    result = 'モンスターの数<a class="show_equation" href="javascript:showEquation()">+</a><a style="display:none" class="hide_equation" href="javascript:hideEquation()">-</a>'
    result += '<div style="display:none" class="monster_equation">'
    result += (
        '演算子<select id="get_equation_det_'
        + c
        + '"><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select><br>'
    )
    result += (
        '種類<select id="get_equation_kind_'
        + c
        + '"><option value="number">数</option><option value="kind">種類</option><option value="same_name">同名</option><option value="x">x</option><option value="y">y</option>'
        + result_tmp
        + "</select><br>"
    )
    #    result+='数<input type="number" id="get_equation_number_'+c+'">';
    result += (
        'min<input type="text" id="min_equation_number_'
        + c
        + '" value="1" onfocus="showMinEquation('
        + c
        + ')">'
    )
    result += (
        'max<input type="text" id="max_equation_number_'
        + c
        + '" value="1" onfocus="showMaxEquation('
        + c
        + ')">'
    )
    result += "</div>"
    return HttpResponse(result)


def get_field_x_and_y(req):
    if "c" in req.POST:
        c = req.POST["c"]
    if "id" in req.POST:
        field_id = req.POST["id"]

    result = 'フィールドx位置<input id="' + field_id + "_field_x_" + c + '_0" style="">'
    result += (
        '演算子<select id="get_field_x_det_'
        + c
        + '_0"><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select><br>'
    )
    result += (
        '<select id="get_field_x_and_or_'
        + c
        + '_0" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select>'
    )
    result += (
        '<input type="button" value="追加" id="add_field_x_'
        + c
        + '_0" onclick="addFieldX('
        + c
        + ",1,'"
        + field_id
        + "')\"><br>"
    )

    result += 'フィールドy位置<input id="' + field_id + "_field_y_" + c + '_0" style="">'
    result += (
        '演算子<select id="get_field_y_det_'
        + c
        + '_0"><option value="=">=</option><option value="!=">!=</option><option value=">=">&gt;=</option><option value="<=">&lt;=</option></select><br>'
    )
    result += (
        '<select id="get_field_y_and_or_'
        + c
        + '_0" > <option value=""></option> <option value="and">かつ</option> <option value="or">または</option> </select>'
    )
    result += (
        '<input type="button" value="追加" id="add_field_y_'
        + c
        + '_0" onclick="addFieldY('
        + c
        + ",1,'"
        + field_id
        + "')\"><br>"
    )
    return HttpResponse(result)

def from_out_ai(request):
    config = Config.objects.get();
    room_time = config.room_time
    limit_time = config.limit_time
    duel_1 = Duel.objects.filter(id=1).get()
    duel_2 = Duel.objects.filter(id=2).get()
    duel_3 = Duel.objects.filter(id=3).get()
    if duel_1.winner == 0 and time() - duel_1.time_1 > limit_time + 30:
        resetduel(duel_1)
    if duel_2.winner == 0 and time() - duel_2.time_1 > limit_time + 30:
        resetduel(duel_2)
    if duel_3.winner == 0 and time() - duel_3.time_1 > limit_time + 30:
        resetduel(duel_3)
    wait_kind1 = 0
    wait_kind2 = 0
    wait_kind3 = 0
    if not "ID" in request.COOKIES and not request.user.is_authenticated:
        ID = str(uuid.uuid4())
        response = redirect('tcgcreator:from_out')
        response.set_cookie('ID', ID,max_age=3600*24*3)
        if "guest_name" in request.GET:
            guest_name = format_html(request.GET["guest_name"])
            response.set_cookie('guest_name', guest_name)
        if "default_deck_id" in request.GET:
            response.set_cookie('default_deck_id', request.GET["default_deck_id"])
        get_params = request.GET.urlencode()
        response['location'] += '?'+get_params
        return response
    elif request.user.is_authenticated:
        user = request.user
    else:
        ID = request.COOKIES["ID"]
        guest_flag = True
        user = None
    room_number =  check_in_other_room_num(user,ID)
    if room_number == 1:
        return init_battle1(request)
    elif room_number == 2:
        return init_battle2(request)
    elif room_number == 3:
        return init_battle3(request)
    if duel_1.winner == 0 and duel_1.waiting == True and (duel_1.user_1 or duel_1.guest_flag):
        if (duel_1.guest_flag is True and duel_1.guest_id == ID) or (duel_1.user_1 is not None and duel_1.user_1 == user):
            return init_battle1(request)
        else:
            wait_kind1 = 1
    elif duel_1.waiting == True:
        wait_kind1 = 0
    elif duel_1.winner != 0 and time() - duel_1.end_time > room_time:
        duel_1.waiting = True
        duel_1.save()
        wait_kind1 = 0
    elif duel_1.winner != 0:
        wait_kind1 = 1
    elif duel_1.winner == 0 :
        if (duel_1.guest_flag is True and duel_1.guest_id == ID) or (duel_1.user_1 is not None and duel_1.user_1 == user):
            tr =  HttpResponseRedirect(reverse("tcgcreator:battle1"))
            return tr
        else:
            wait_kind1 = 1
    if wait_kind1 == 0:
        return init_battle1(request)
    if duel_2.winner == 0 and duel_2.waiting == True and (duel_2.user_1 or duel_2.guest_flag):
        if (duel_2.guest_flag is True and duel_2.guest_id == ID) or (duel_2.user_1 is not None and duel_2.user_1 == user):
            return init_battle2(request)
        else:
            wait_kind2 = 1
    elif duel_2.waiting == True:
        wait_kind2 = 0
    elif duel_2.winner != 0 and time() - duel_2.end_time > room_time:
        duel_2.waiting = True
        duel_2.save()
        wait_kind2 = 0
    elif duel_2.winner != 0:
        wait_kind2 = 1
    elif duel_2.winner == 0 :
        if (duel_2.guest_flag is True and duel_2.guest_id == ID) or (duel_2.user_1 is not None and duel_2.user_1 == user):
            return init_battle3(request)
        wait_kind2 = 1
    if wait_kind2 == 0:
        return init_battle2(request)
    if duel_3.winner == 0 and duel_3.waiting == True and (duel_3.user_1 or duel_3.guest_flag):
        if (duel_3.guest_flag is True and duel_3.guest_id == ID) or (duel_3.user_1 is not None and duel_3.user_1 == user):
            return init_battle3(request)
        else:
            wait_kind3 = 1
    elif duel_3.waiting == True:
        wait_kind3 = 0
    elif duel_3.winner != 0 and time() - duel_3.end_time > room_time:
        duel_3.waiting = True
        duel_3.save()
        wait_kind3 = 0
    elif duel_3.winner != 0:
        wait_kind3 = 1
    elif duel_3.winner == 0 :
        if (duel_3.guest_flag is True and duel_3.guest_id == ID) or (duel_3.user_1 is not None and duel_3.user_1 == user):
            return init_battle3(request)
        else:
            wait_kind3 = 1
    if wait_kind3 == 0:
        return init_battle3(request)
    return HttpResponse("部屋がいっぱいです")
def from_out(request):
    wait_kind1 = 0
    wait_kind2 = 0
    wait_kind3 = 0
    if("ai" in request.GET and request.GET["ai"] =="1"):
        return from_out_ai(request)
    if not "ID" in request.COOKIES:
        ID = str(uuid.uuid4())
        response = redirect('tcgcreator:from_out')
        response.set_cookie('ID', ID,max_age=3600*24*3)
        if "guest_name" in request.GET:
            guest_name = format_html(request.GET["guest_name"])
            response.set_cookie('guest_name', guest_name)
        if "default_deck_id" in request.GET:
            response.set_cookie('default_deck_id', request.GET["default_deck_id"])
        get_params = request.GET.urlencode()
        response['location'] += '?'+get_params
        return response
    else:
        ID = request.COOKIES["ID"]
    config = Config.objects.get();
    duel_1 = Duel.objects.filter(id=1).get()
    duel_2 = Duel.objects.filter(id=2).get()
    duel_3 = Duel.objects.filter(id=3).get()
    room_time = config.room_time
    limit_time = config.limit_time
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    if duel_1.winner == 0 and time() - duel_1.time_1 > limit_time * 2:
        resetduel(duel_1)
    if duel_2.winner == 0 and time() - duel_2.time_1 > limit_time * 2:
        resetduel(duel_2)
    if duel_3.winner == 0 and time() - duel_3.time_1 > limit_time * 2:
        resetduel(duel_3)
    room_number =  check_in_other_room_num(user,ID)
    if room_number == 1:
        return init_battle1(request)
    elif room_number == 2:
        return init_battle2(request)
    elif room_number == 3:
        return init_battle3(request)
    if duel_1.waiting == True and (duel_1.user_1 or duel_1.guest_flag is True and (not duel_1.user_2 and not duel_1.guest_flag2)):
        return init_battle1(request)
    if duel_2.waiting == True and (duel_2.user_1 or duel_2.guest_flag is True and (not duel_2.user_2 and not duel_2.guest_flag2)):
        return init_battle2(request)
    if duel_3.waiting == True and (duel_3.user_1 or duel_3.guest_flag is True and (not duel_3.user_2 and not duel_3.guest_flag2)):
        return init_battle3(request)
    if duel_1.winner == 0 and duel_1.waiting == True and (duel_1.user_1 or duel_1.guest_flag):
        if time() - duel_1.wait_time > limit_time:
            resetduel(duel_1)
        else:
            return init_battle1(request)
    elif duel_2.winner == 0 and duel_2.waiting == True and (duel_2.user_1 or duel_2.guest_flag):
        if time() - duel_2.wait_time > limit_time:
            resetduel(duel_2)
        else:
            return init_battle2(request)
    elif duel_3.winner == 0 and duel_3.waiting == True and (duel_3.user_1 or duel_3.guest_flag):
        if time() - duel_3.wait_time > limit_time:
            resetduel(duel_3)
        else:
            return init_battle3(request)
    if duel_1.waiting == True:
        wait_kind1 = 0
    elif duel_1.winner != 0 and time() - duel_1.end_time > room_time:
        duel_1.waiting = True
        duel_1.save()
        wait_kind1 = 0
    elif duel_1.winner != 0:
        wait_kind1 = 1
    elif duel_1.winner == 0:

        wait_kind1 = 1
    if wait_kind1 == 0:
        return init_battle1(request)
    if duel_2.waiting == True:
        wait_kind2 = 0
    elif duel_2.winner != 0 and time() - duel_2.end_time > room_time:
        duel_2.waiting = True
        duel_2.save()
        wait_kind2 = 0
    elif duel_2.winner != 0:
        wait_kind2 = 1
    elif duel_2.winner == 0:

        wait_kind2 = 1
    if wait_kind2 == 0:
        return init_battle2(request)
    if duel_3.waiting == True:
        wait_kind3 = 0
    elif duel_3.winner != 0 and time() - duel_3.end_time > room_time:
        duel_3.waiting = True
        duel_3.save()
        wait_kind3 = 0
    elif duel_3.winner != 0:
        wait_kind3 = 1
    elif duel_3.winner == 0:
        wait_kind3 = 1
    if wait_kind3 == 0:
        return init_battle3(request)
    return HttpResponse("部屋がいっぱいです")

def init_battle1(request):
    return init_battle(request, 1)


def init_battle2(request):
    return init_battle(request, 2)


def init_battle3(request):
    return init_battle(request, 3)


def init_battle(request, room_number):
    guest_flag = False
    guest_name = ""
    ai_choosing = False
    user_choosing = False
    duel = Duel.objects.filter(id=room_number).first()
    ID=""
    if "ai_id" in request.GET and request.GET["ai_id"]:
        ai_id = request.GET["ai_id"]
        ai = True
    else:
        ai_id = None
        ai = False
    redirect_flag = False
    deck_id_flag = False
    guest_name_flag = False
    default_deck_id_flag = False
    id_flag = False
    if not request.user.is_authenticated:
        if not "ID" in request.COOKIES:
            return HttpResponse("error")
        if request.COOKIES["ID"] == -1:
            return HttpResponse("error2")
        guest_flag = True
        if "guest_name" not in request.GET or not request.GET["guest_name"]:
            if "guest_name" not in request.COOKIES:
                guest_name = ""
            else:
                guest_name = format_html(request.COOKIES["guest_name"])
        else:
            guest_name = format_html(request.GET["guest_name"])
            guest_name_flag = True
            redirect_flag = True
        if "default_deck_id" not in request.GET or not request.GET["default_deck_id"]:
            #user_choosing = True
            if duel.is_ai:
                ai_choosing = True
        else:
            ai_choosing = False
            default_deck_id = request.GET["default_deck_id"]
            redirect_flag = True
            default_deck_id_flag = True
        if not "ID" in request.COOKIES:
            redirect_flag = True
            id_flag = True
            ID = str(uuid.uuid4())
        else:
            ID = request.COOKIES["ID"]

    else:
        ai_choosing=False
        if not "deck_id" in request.GET:

            tmp = UserDeckChoice.objects.filter(user=request.user).first()
            deck_id = tmp.user_deck.user_deck_id
            duel.save()
        else:
            deck_id= int(request.GET["deck_id"])
            tmp = UserDeckGroup.objects.filter(user_deck_id=deck_id,user=request.user).first()
            if tmp is None:
                return HttpResponse("error")
            if not ai:
                redirect_flag = True
                deck_id_flag = True
    config = Config.objects.get()
    if config.ai == False:
        ai = False
    duel.wait_time = time()
    duel.ai_choosing = False
    if duel.waiting == True and (duel.user_2 is not  None or duel.is_ai is True or duel.guest_flag2 is True):
        duel.winner = 0
        resetduel(duel)
    if (duel.user_1 is not None and duel.user_1 == request.user and duel.guest_flag is False)or(duel.guest_id == ID and duel.guest_flag is True):
        if duel.is_ai is True or duel.user_2 or (duel.guest_flag2 is True ):
            tr= HttpResponseRedirect(reverse("tcgcreator:battle"+str(room_number)))
        else:
            tr= HttpResponseRedirect(reverse("tcgcreator:wait_battle"+str(room_number)))
        if redirect_flag is True:
            if id_flag is True:
                tr.set_cookie('ID', ID,max_age=3600*24*3)
            if guest_name_flag is True:
                tr.set_cookie('guest_name', guest_name)
            if default_deck_id_flag is True:
                tr.set_cookie('default_deck_id', default_deck_id)
            if deck_id_flag is True:
                tr.set_cookie('deck_id', deck_id)
        return tr
    if (duel.user_2 == request.user and duel.user_2 is not None and duel.guest_flag2 is False) or (guest_flag is True and duel.guest_flag2 is True and duel.guest_id2 == ID):
        tr =  HttpResponseRedirect(reverse("tcgcreator:battle"+str(room_number)))
        if redirect_flag is True:
            if id_flag is True:
                tr.set_cookie('ID', ID,max_age=3600*24*3)
            if guest_name_flag is True:
                tr.set_cookie('guest_name', guest_name)
            if default_deck_id_flag is True:
                tr.set_cookie('default_deck_id', default_deck_id)
        return tr
    if not duel.user_1 and duel.guest_flag is False:
        if check_in_other_room(request.user, room_number,ID):
            tr = HttpResponse("他の部屋に入室しています")
            if redirect_flag is True:
                if id_flag is True:
                    tr.set_cookie('ID', ID,max_age=3600*24*3)
                if guest_name_flag is True:
                    tr.set_cookie('guest_name', guest_name)
                if default_deck_id_flag is True:
                    tr.set_cookie('default_deck_id', default_deck_id)
            return tr
        if  guest_flag is False and not ai and user_choosing is False:
            tmp = check_user_deck(request.user,deck_id)
            if tmp:
                tr = HttpResponse(tmp)
                if redirect_flag is True:
                    if id_flag is True:
                        tr.set_cookie('ID', ID,max_age=3600*24*3)
                    if guest_name_flag is True:
                        tr.set_cookie('guest_name', guest_name)
                    if default_deck_id_flag is True:
                        tr.set_cookie('default_deck_id', default_deck_id)
                return tr
        if ai and ai_id:
            tmp2 = check_enemy_deck(request.user,ai_id)
            if tmp2:
                tr =  HttpResponse(tmp2)
                if redirect_flag is True:
                    if id_flag is True:
                        tr.set_cookie('ID', ID,max_age=3600*24*3)
                    if guest_name_flag is True:
                        tr.set_cookie('guest_name', guest_name)
                    if default_deck_id_flag is True:
                        tr.set_cookie('default_deck_id', default_deck_id)
                return tr
        if(guest_flag is False):
            duel.user_1 = request.user
        else:
            duel.guest_flag = True
            duel.guest_name = guest_name
            duel.guest_id = ID
        if user_choosing is True:
            duel.deck_choose_flag1 = True
            if ai_choosing is False:
                if(guest_flag is False):
                    duel.user_1 = request.user
        else:
            duel.deck_choose_flag1 = False
            if ai_choosing is False:
                if(guest_flag is False):
                    duel.user_1 = request.user
                    tmp2 = UserDeckChoice.objects.filter(user=request.user).first()
                    if tmp2 is not None:
                        tmp2.user_deck = UserDeckGroup.objects.get(user_deck_id=deck_id)
                        tmp2.save()
                else:
                    duel.default_deck1 = DefaultDeckGroup.objects.get(default_deck_id=default_deck_id)
        if ai:
            duel.is_ai = True
            duel.deck_choose_flag2 = False
            if ai_choosing is False :
                if guest_flag is False:
                    duel.user_deck1 = tmp2
                    duel.save()
            if ai_choosing is False and ai_id:
                tmp3 = EnemyDeckChoice.objects.first()

                tmp3.enemy_deck = EnemyDeckGroup.objects.get(enemy_deck_id=ai_id)
                tmp3.save()
                duel.ai_deck2 = tmp3
                duel.save()
                tmp = init_duel(room_number, request.user)
                if tmp:
                    tr =  HttpResponse(tmp)
                else:
                    tr = HttpResponseRedirect(reverse("tcgcreator:battle" + str(room_number)))
                if redirect_flag is True:
                    if id_flag is True:
                        tr.set_cookie('ID', ID,max_age=3600*24*3)
                    if guest_name_flag is True:
                        tr.set_cookie('guest_name', guest_name)
                    if default_deck_id_flag is True:
                        tr.set_cookie('default_deck_id', default_deck_id)
                return tr
            else:
                duel.ai_choosing = True
                duel.waiting = False
                duel.winner = 0
                duel.cost_log = ""
                duel.current_log = ""
                duel.message_log = ""
                duel.log = "デュエルID " + duel.duel_id + "\n"
                duel.log_turn = duel.log
                start_phase = Phase.objects.order_by("-priority").first()
                duel.phase = start_phase
                duel.audio = ""
                duel.chain = 0
                duel.alt_global = ""
                duel.accumulate_global = []
                duel.chain_det = ""
                duel.chain_user = ""
                duel.chain_variable = "{}"
                duel.time_1 = time()
                duel.time_2 = time()
                duel.save()
                tr = HttpResponseRedirect(reverse("tcgcreator:battle" + str(room_number)))
                if redirect_flag is True:
                    if id_flag is True:
                        tr.set_cookie('ID', ID,max_age=3600*24*3)
                    if guest_name_flag is True:
                        tr.set_cookie('guest_name', guest_name)
                    if default_deck_id_flag is True:
                        tr.set_cookie('default_deck_id', default_deck_id)
                return tr
        else:
            duel.is_ai = False
        if user_choosing is True:
            duel.deck_choose_flag2 = True
        else:
            duel.deck_choose_flag2 = False
        duel.save()
        tr =  HttpResponseRedirect(reverse("tcgcreator:wait_battle"+str(room_number)))
        if redirect_flag is True:
            if id_flag is True:
                tr.set_cookie('ID', ID,max_age=3600*24*3)
            if guest_name_flag is True:
                tr.set_cookie('guest_name', guest_name)
            if default_deck_id_flag is True:
                tr.set_cookie('default_deck_id', default_deck_id)
        return tr

    if duel.is_ai is True:
        if (duel.user_1 == request.user and duel.user_1 is not None and duel.guest_flag is False) or (duel.guest_flag is True and ID == duel.guest_id):
            tr= HttpResponseRedirect(reverse("tcgcreator:battle" + str(room_number)))

        else:

            if check_in_other_room(request.user, room_number,ID):
                return HttpResponse("他の部屋に入室しています")
            else:
                tr =  HttpResponseRedirect(reverse("tcgcreator:watch"+str(room_number)))
        if redirect_flag is True:
            if id_flag is True:
                tr.set_cookie('ID', ID,max_age=3600*24*3)
            if guest_name_flag is True:
                tr.set_cookie('guest_name', guest_name)
            if default_deck_id_flag is True:
                tr.set_cookie('default_deck_id', default_deck_id)
        return tr
    if not duel.user_2 and duel.guest_flag2 is False:
        if check_in_other_room(request.user, room_number,ID):
            return HttpResponse("他の部屋に入室しています")
        if user_choosing is False:
            if guest_flag is False:
                tmp = check_user_deck(request.user,deck_id)
                if tmp:
                    return HttpResponse(tmp)
            if guest_flag is False:
                tmp2 = UserDeckChoice.objects.filter(user=request.user).first()
                tmp2.user_deck = UserDeckGroup.objects.get(user_deck_id=deck_id)
                tmp2.save()
                duel.user_deck2 = tmp2
                duel.save()
            else:
                duel.guest_flag2 = True
                duel.guest_id2 = ID
                duel.guest_name2 = guest_name
                duel.default_deck2 = DefaultDeckGroup.objects.get(default_deck_id=default_deck_id)
                duel.save()
        else:
            #duel.deck_choose_flag2 = True
            duel.deck_choose_flag2 = False
            if guest_flag is True:
                duel.guest_flag2 = True
                duel.guest_id2 = ID
                duel.guest_name2 = guest_name
            duel.save()
        tmp = init_duel(room_number, request.user)
        if tmp:
            tr = HttpResponse(tmp)
        else:
            tr =  HttpResponseRedirect(reverse("tcgcreator:battle" + str(room_number)))
        if redirect_flag is True:
            if id_flag is True:
               tr.set_cookie('ID', ID,max_age=3600*24*3)
            if guest_name_flag is True:
                tr.set_cookie('guest_name', guest_name)
            if default_deck_id_flag is True:
                tr.set_cookie('default_deck_id', default_deck_id)
        return tr
    else:
        tr = HttpResponseRedirect(reverse("tcgcreator:watch"+str(room_number)))
        if redirect_flag is True:
            if id_flag is True:
                tr.set_cookie('ID', ID,max_age=3600*24*3)
            if guest_name_flag is True:
                tr.set_cookie('guest_name', guest_name)
            if default_deck_id_flag is True:
                tr.set_cookie('default_deck_id', default_deck_id)
        return tr


def exit(request):
    room_number = request.POST["room_number"]
    duel = Duel.objects.filter(id=room_number).first()
    duelobj = DuelObj(room_number)
    duelobj.duel = duel
    duelobj.room_number = room_number
    duelobj.in_execute = False
    user_1 = duel.user_1
    user_2 = duel.user_2
    if "ID" in request.COOKIES:
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    if (request.user == user_1 and duel.guest_flag is False) or (ID == duel.guest_id and duel.guest_flag is True):
        duelobj.user = 1
        user = 1
        other_user = 2
    else:
        return HttpResponse("error")
    duelobj.init_all(user, other_user, room_number)
    if duel.winner != 0:
        return HttpResponse("error")
    if duel.is_ai is False:
        return HttpResponse("error")
    resetduel(duel)
    #duelobj.save_all(user, other_user, room_number)
    return HttpResponse("")

def send_lose(request):
    room_number = request.POST["room_number"]
    duel = Duel.objects.filter(id=room_number).first()
    duelobj = DuelObj(room_number)
    duelobj.duel = duel
    duelobj.room_number = room_number
    duelobj.in_execute = False
    user_1 = duel.user_1
    user_2 = duel.user_2
    if "ID" in request.COOKIES:
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    if duel.guest_flag is True:
        user1_name = duel.guest_name
    else:
        user1_name = duel.user_1.first_name
    if duel.guest_flag2 is True:
        user2_name = duel.guest_name2
    elif duel.is_ai is True:
        user2_name = "NPC"
    else:
        user2_name = duel.user_2.first_name
    if (request.user == user_1 and duel.guest_flag is False)or (ID == duel.guest_id and duel.guest_flag is True):
        duelobj.user = 1
        user = 1
        other_user = 2
    if (request.user == user_2 and duel.guest_flag2 is False) or (ID == duel.guest_id2 and duel.guest_flag2 is True):
        duelobj.user = 2
        user = 2
        other_user = 1
    duelobj.init_all(user, other_user, room_number)
    if duel.winner != 0:
        return HttpResponse("error")
    if (duel.user_1 == request.user and duel.guest_flag is False) or (ID == duel.guest_id and duel.guest_flag is True):

        duelobj.duel.log += user1_name + "は降参した"
        duelobj.duel.log_turn += user1_name + "は降参した"
        duelobj.duel.winner = 2
        duelobj.duel.end_time = time()
        user_point = UserPoint.objects.filter(user = duel.user_2).first()
        if user_point is None:
            user_point = UserPoint()
            user_point.user = duel.user_2
        user_point.win += 1
        user_point.point += 5
        user_point.save()
        user_point2 = UserPoint.objects.filter(user = duel.user_1).first()
        if user_point2 is None:
            user_point2 = UserPoint()
            user_point2.user = duel.user_1
        user_point2.lose += 1
        user_point2.save()
    if (duel.user_2 == request.user and duel.guest_flag2 is False) or (ID == duel.guest_id2 and duel.guest_flag2 is True):
        duelobj.duel.log += user2_name + "は降参した"
        duelobj.duel.log_turn += user2_name + "は降参した"
        duelobj.duel.winner = 1
        duelobj.duel.end_time = time()
        user_point = UserPoint.objects.filter(user = duel.user_1).first()
        if user_point is None:
            user_point = UserPoint()
            user_point.user = duel.user_1
        user_point.win += 1
        user_point.point += 5
        user_point.save()
        user_point2 = UserPoint.objects.filter(user = duel.user_2).first()
        if user_point2 is None:
            user_point2 = UserPoint()
            user_point2.user = duel.user_2
        user_point2.lose += 1
        user_point2.save()
    duelobj.turn_changed = True
    duelobj.save_all(user, other_user, room_number)
    return HttpResponse("")


def leave_battle1(request):
    return leave_battle(request, 1)


def leave_battle2(request):
    return leave_battle(request, 2)


def leave_battle3(request):
    return leave_battle(request, 3)


def wait_battle1(request):
    return wait_battle(request, 1)


def wait_battle2(request):
    return wait_battle(request, 2)


def wait_battle3(request):
    return wait_battle(request, 3)


def wait_battle(request, room_number):
    duel = Duel.objects.filter(id=room_number).first()
    duel.wait_time = time()
    duel.save()
    if "ID" in request.COOKIES:
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    if ((request.user == duel.user_1 and duel.guest_flag is False) or (duel.guest_id == ID and duel.guest_flag is True)) and duel.waiting == True :
        return render(request, "tcgcreator/wait_battle.html", {"room_number": room_number})
    else:
        return HttpResponseRedirect(reverse("tcgcreator:choose"))


def leave_battle(request, room_number):
    if "ID" in request.COOKIES:
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    duel = Duel.objects.filter(id=room_number).first()
    config = Config.objects.get()
    if duel.waiting == True and ((duel.user_1 == request.user and duel.guest_flag is False) or (duel.guest_id == ID and duel.guest_flag is True)):
        resetduel(duel)
        duel.save()
        return HttpResponseRedirect(config.return_url)
    else:
        return HttpResponse("エラーが発生しました。")


def battle(request):
    duel = Duel.objects.all()
    if request.user is None:
        return HttpResponse("Please Login")

    if duel.user_1 == request.user:
        return HttpResponse("Success")

    if duel.user_2 == request.user:
        return HttpResponse("Success")
    return HttpResponseRedirect(reverse("accounts:login"))


def enemy_deck(req):
    if req.user.is_superuser == False:
        return HttpResponse("error")
    monster_variables = MonsterVariables.objects.all().filter(
        ~Q(monster_variable_show=0)
    )
    decks = Deck.objects.all()
    where_sql = ""
    join_sql = ""
    add_variable = []
    deck_group = EnemyDeckChoice.objects.first()
    if not deck_group:
        create_enemy_deck_group(1, "デッキ")
        enemy_deck_group = EnemyDeckGroup.objects.all().first()
        create_enemy_deck_choice(enemy_deck_group)
        deck_group = EnemyDeckChoice.objects.all().filter().first()
    else:
        enemy_deck_group = deck_group.enemy_deck
    # 新規デッキ追加
    if "deck_name" in req.GET:
        enemy_deck_group_max = EnemyDeckGroup.objects.all().aggregate(
            Max("enemy_deck_id")
        )
        deck_group_num = enemy_deck_group_max["enemy_deck_id__max"] + 1
        create_enemy_deck_group(deck_group_num, req.GET["deck_name"])
        enemy_deck_group = (
            EnemyDeckGroup.objects.all().filter(enemy_deck_id=deck_group_num).first()
        )
        deck_group.enemy_deck = enemy_deck_group
        deck_group.save()
    elif "deck_group" in req.GET:
        if "deck_group" in req.GET and req.GET["deck_group"] != "":
            deck_group_id = req.GET["deck_group"]
            enemy_deck_group = (
                EnemyDeckGroup.objects.all()
                    .filter(enemy_deck_id=int(deck_group_id))
                    .first()
            )
            deck_group.enemy_deck = enemy_deck_group
            deck_group.save()
    else:
        # デッキグループを選択
        if "deck_group" in req.POST and req.POST["deck_group"] != "":
            deck_group_id = req.POST["deck_group"]
            enemy_deck_group = (
                EnemyDeckGroup.objects.all()
                    .filter(enemy_deck_id=int(deck_group_id))
                    .first()
            )
            deck_group.enemy_deck = enemy_deck_group
            deck_group.save()
        elif "deck_name" in req.POST and req.POST["deck_name"] != "":
            enemyy_deck_group = deck_group.enemy_deck
            deck_name = req.POST["deck_name"]
            enemy_deck_group.deck_name = deck_name
            enemy_deck_group.save()
        else:
            enemy_deck_group = deck_group.enemy_deck

    enemy_deck_groups = EnemyDeckGroup.objects.filter()

    for deck in decks:
        enemy_decks = EnemyDeck.objects.all().filter(
            deck_type__id=deck.id, deck_group=enemy_deck_group
        )
        if not enemy_decks:
            create_enemy_deck(deck, enemy_deck_group)

    if req.method == "POST":
        check = copy_to_enemy_deck(req.POST, enemy_deck_group)
        if check != "":
            return HttpResponse(check)
        i = 0
        for monster_variable in monster_variables:
            if req.POST["monster_variable" + str(monster_variable.id)] != "":
                if monster_variable.monster_variable_kind_id.monster_variable_name == "数値":
                    join_sql += (
                            " left join tcgcreator_monsteritem as i"
                            + str(i)
                            + " on m.id = i"
                            + str(i)
                            + ".monster_id_id"
                    )
                    if req.POST[str(monster_variable.id) + "_how"] == "least":
                        if where_sql != "":
                            where_sql += " and "
                        where_sql += (
                                "(i"
                                + str(i)
                                + ".monster_item_text >= "
                                + req.POST["monster_variable" + str(monster_variable.id)]
                                + " and i"
                                + str(i)
                                + ".monster_variables_id_id = "
                                + str(monster_variable.id)
                                + ")"
                        )
                    elif req.POST[str(monster_variable.id) + "_how"] == "same":
                        if where_sql != "":
                            where_sql += " and "
                        where_sql += (
                                "(i"
                                + str(i)
                                + ".monster_item_text = "
                                + req.POST["monster_variable" + str(monster_variable.id)]
                                + " and i"
                                + str(i)
                                + ".monster_variables_id_id = "
                                + str(monster_variable.id)
                                + ")"
                        )
                        # monster = monster.filter(monster_item__monster_item_text = int(req.POST["monster_variable"+str(monster_variable.id)]))
                    elif req.POST[str(monster_variable.id) + "_how"] == "utmost":
                        if where_sql != "":
                            where_sql += " and "
                        where_sql += (
                                "(i"
                                + str(i)
                                + ".monster_item_text <= "
                                + req.POST["monster_variable" + str(monster_variable.id)]
                                + " and i"
                                + str(i)
                                + ".monster_variables_id_id = "
                                + str(monster_variable.id)
                                + ")"
                        )
                        # monster = monster.filter(monster_item__monster_item_text <= int(req.POST["monster_variable"+str(monster_variable.id)]))
                else:
                    if req.POST["monster_variable" + str(monster_variable.id)] != "0":
                        join_sql += (
                                " left join tcgcreator_monsteritem as i"
                                + str(i)
                                + " on m.id = i"
                                + str(i)
                                + ".monster_id_id"
                        )
                        if where_sql != "":
                            where_sql += " and "
                        where_sql += (
                                "(i"
                                + str(i)
                                + ".monster_item_text like %s and i"
                                + str(i)
                                + ".monster_variables_id_id = "
                                + str(monster_variable.id)
                                + ")"
                        )
                        add_variable.append(
                            "%"
                            + req.POST["monster_variable" + str(monster_variable.id)]
                            + "%"
                        )
                        # monster = monster.filter(monster_item__monster_item_text__contains = (req.POST["monster_variable"+str(monster_variable.id)]),monster_item__monster_variables_id = int(monster_variable.id))
            i += 1
    if where_sql == "":
        where_sql = "1"
    monster = Monster.objects.raw(
        "select * from tcgcreator_monster as m " + join_sql + " where " + where_sql,
        add_variable,
        )
    enemy_deck = EnemyDeck.objects.all().filter(deck_group=enemy_deck_group)
    # sql = "select * from tcgcreator_monster as m "+ join_sql + " where "+ where_sql
    return render(
        req,
        "admin/tcgcreator/makedeck_enemy.html",
        {
            "MonsterVariables": monster_variables,
            "Monster": monster,
            "EnemyDeck": enemy_deck,
            "Deck": decks,
            "EnemyDeckGroup": enemy_deck_group,
            "EnemyDeckGroups": enemy_deck_groups,
        },
    )

def default_deck(req):
    if not req.user.is_superuser:
        return HttpResponse("error")
    monster_variables = MonsterVariables.objects.all().filter(
        ~Q(monster_variable_show=0)
    )
    decks = Deck.objects.all()
    deck_group = 1
    where_sql = ""
    join_sql = ""
    add_variable = []
    deck_group = DefaultDeckChoice.objects.first()
    if not deck_group:
        create_default_deck_group(1, "デッキ")
        default_deck_group = DefaultDeckGroup.objects.all().first()
        create_default_deck_choice(default_deck_group)
        deck_group = DefaultDeckChoice.objects.all().filter().first()
    else:
        default_deck_group = deck_group.default_deck
    # 新規デッキ追加
    if "deck_name" in req.GET:
        default_deck_group_max = DefaultDeckGroup.objects.all().aggregate(
            Max("default_deck_id")
        )
        deck_group_int = default_deck_group_max["default_deck_id__max"] + 1
        create_default_deck_group(deck_group_int, req.GET["deck_name"])
        default_deck_group = (
            DefaultDeckGroup.objects.all().filter(default_deck_id=deck_group_int).first()
        )
        deck_group.default_deck = default_deck_group
        deck_group.save()
    elif "deck_group" in req.GET:
        if "deck_group" in req.GET and req.GET["deck_group"] != "":
            deck_group_id = req.GET["deck_group"]
            default_deck_group = (
                DefaultDeckGroup.objects.all()
                .filter(default_deck_id=int(deck_group_id))
                .first()
            )
            deck_group.default_deck = default_deck_group
            deck_group.save()
    else:
        # デッキグループを選択
        if "deck_group" in req.POST and req.POST["deck_group"] != "":
            deck_group_id = req.POST["deck_group"]
            default_deck_group = (
                DefaultDeckGroup.objects.all()
                .filter(default_deck_id=int(deck_group_id))
                .first()
            )
            deck_group.default_deck = default_deck_group
            deck_group.save()
        elif "deck_name" in req.POST and req.POST["deck_name"] != "":
            default_deck_group = deck_group.default_deck
            deck_name = req.POST["deck_name"]
            default_deck_group.deck_name = deck_name
            default_deck_group.save()
        else:
            default_deck_group = deck_group.default_deck

    default_deck_groups = DefaultDeckGroup.objects.filter()

    for deck in decks:
        default_decks = DefaultDeck.objects.all().filter(
            deck_type__id=deck.id, deck_group=default_deck_group
        )
        if not default_decks:
            create_default_deck(deck, default_deck_group)

    if req.method == "POST":
        check = copy_to_default_deck(req.POST, default_deck_group)
        if check != "":
            return HttpResponse(check)
        i = 0
        for monster_variable in monster_variables:
            if ("monster_variable" + str(monster_variable.id)) in req.POST and req.POST["monster_variable" + str(monster_variable.id)] != "":
                if monster_variable.monster_variable_kind_id.monster_variable_name == "数値":
                    join_sql += (
                        " left join tcgcreator_monsteritem as i"
                        + str(i)
                        + " on m.id = i"
                        + str(i)
                        + ".monster_id_id"
                    )
                    if req.POST[str(monster_variable.id) + "_how"] == "least":
                        if where_sql != "":
                            where_sql += " and "
                        where_sql += (
                            "(i"
                            + str(i)
                            + ".monster_item_text >= "
                            + req.POST["monster_variable" + str(monster_variable.id)]
                            + " and i"
                            + str(i)
                            + ".monster_variables_id_id = "
                            + str(monster_variable.id)
                            + ")"
                        )
                    elif req.POST[str(monster_variable.id) + "_how"] == "same":
                        if where_sql != "":
                            where_sql += " and "
                        where_sql += (
                            "(i"
                            + str(i)
                            + ".monster_item_text = "
                            + req.POST["monster_variable" + str(monster_variable.id)]
                            + " and i"
                            + str(i)
                            + ".monster_variables_id_id = "
                            + str(monster_variable.id)
                            + ")"
                        )
                        # monster = monster.filter(monster_item__monster_item_text = int(req.POST["monster_variable"+str(monster_variable.id)]))
                    elif req.POST[str(monster_variable.id) + "_how"] == "utmost":
                        if where_sql != "":
                            where_sql += " and "
                        where_sql += (
                            "(i"
                            + str(i)
                            + ".monster_item_text <= "
                            + req.POST["monster_variable" + str(monster_variable.id)]
                            + " and i"
                            + str(i)
                            + ".monster_variables_id_id = "
                            + str(monster_variable.id)
                            + ")"
                        )
                        # monster = monster.filter(monster_item__monster_item_text <= int(req.POST["monster_variable"+str(monster_variable.id)]))
                else:
                    if req.POST["monster_variable" + str(monster_variable.id)] != "0":
                        join_sql += (
                            " left join tcgcreator_monsteritem as i"
                            + str(i)
                            + " on m.id = i"
                            + str(i)
                            + ".monster_id_id"
                        )
                        if where_sql != "":
                            where_sql += " and "
                        where_sql += (
                            "(i"
                            + str(i)
                            + ".monster_item_text like %s and i"
                            + str(i)
                            + ".monster_variables_id_id = "
                            + str(monster_variable.id)
                            + ")"
                        )
                        add_variable.append(
                            "%"
                            + req.POST["monster_variable" + str(monster_variable.id)]
                            + "%"
                        )
                        # monster = monster.filter(monster_item__monster_item_text__contains = (req.POST["monster_variable"+str(monster_variable.id)]),monster_item__monster_variables_id = int(monster_variable.id))
            i += 1
    if where_sql == "":
        where_sql = "1"
    monster = Monster.objects.raw(
        "select * from tcgcreator_monster as m " + join_sql + " where " + where_sql,
        add_variable,
    )
    default_deck = DefaultDeck.objects.all().filter(deck_group=default_deck_group)
    # sql = "select * from tcgcreator_monster as m "+ join_sql + " where "+ where_sql
    return render(
        req,
        "admin/tcgcreator/makedeck.html",
        {
            "MonsterVariables": monster_variables,
            "Monster": monster,
            "DefaultDeck": default_deck,
            "Deck": decks,
            "DefaultDeckGroup": default_deck_group,
            "DefaultDeckGroups": default_deck_groups,
        },
    )


def makedecktext(req):
    config = Config.objects.first();
    monster_variables = MonsterVariables.objects.all().select_related(
        "monster_variable_kind_id"
    )
    decks_show = Deck.objects.filter(makedeckshow=True)
    decks = Deck.objects.all()
    deck_group = 1
    where_sql = " m.token_flag = false "
    join_sql = ""
    add_variable = []
    if not req.user.is_authenticated:
        return HttpResponse("Please Login")
    deck_group = UserDeckChoice.objects.filter(user=req.user).first()
    if not deck_group:
        create_user_deck_group(1, req.user, "デッキ")
        user_deck_group = (
            UserDeckGroup.objects.all().filter(user_deck_id=1, user=req.user).first()
        )
        create_user_deck_choice(user_deck_group, req.user)
        deck_group = UserDeckChoice.objects.all().filter(user=req.user).first()
        for deck in decks:
            create_user_deck(req.user, deck, user_deck_group, 1)
    else:
        user_deck_group = deck_group.user_deck
    # 新規デッキ追加
    if "deck_name" in req.GET:
        user_deck_group_max = UserDeckGroup.objects.all().aggregate(Max("user_deck_id"))
        if(user_deck_group_max["user_deck_id__max"] is None):
            deck_group2 = 1
        else:
            deck_group2 = user_deck_group_max["user_deck_id__max"] + 1
        create_user_deck_group(deck_group2, req.user, html.escape(req.GET["deck_name"]))
        user_deck_group = (
            UserDeckGroup.objects.all()
            .filter(user_deck_id=deck_group2, user=req.user)
            .first()
        )
        deck_group.user_deck = user_deck_group
        deck_group.save()
        for deck in decks:
            create_user_deck(req.user, deck, user_deck_group, req.GET["structure_deck"])
    elif "deck_group" in req.GET:
        if "deck_group" in req.GET and req.GET["deck_group"] != "":
            deck_group_id = req.GET["deck_group"]
            user_deck_group = (
                UserDeckGroup.objects.all()
                .filter(user_deck_id=int(deck_group_id), user=req.user)
                .first()
            )
            deck_group.user_deck = user_deck_group
            deck_group.save()
    else:
        # デッキグループを選択
        if "deck_group" in req.POST and req.POST["deck_group"] != "":
            deck_group_id = req.POST["deck_group"]
            user_deck_group = (
                UserDeckGroup.objects.all()
                .filter(user_deck_id=int(deck_group_id), user=req.user)
                .first()
            )
            deck_group.user_deck = user_deck_group
            deck_group.save()
        elif "deck_name" in req.POST and req.POST["deck_name"] != "":
            user_deck_group = deck_group.user_deck
            deck_name = html.escape(req.POST["deck_name"])
            user_deck_group.deck_name = deck_name
            user_deck_group.save()
        else:
            user_deck_group = deck_group.user_deck

    user_deck_groups = UserDeckGroup.objects.filter(user_id=req.user)

    default_deck_groups = DefaultDeckGroup.objects.all()
    for deck in decks:
        user_decks = UserDeck.objects.all().filter(
            user=req.user, deck_type__id=deck.id, deck_group=user_deck_group
        )

    if req.method == "POST":
        check = copy_to_deck_text(req.user, req.POST, user_deck_group)
        if check != "":
            return HttpResponse(check)

        i = 0
        for monster_variable in monster_variables:
            if (
                "monster_variable" + str(monster_variable.id) in req.POST
                and req.POST["monster_variable" + str(monster_variable.id)] != ""
            ):
                if monster_variable.monster_variable_kind_id.monster_variable_name == "数値":
                    join_sql += (
                        " left join tcgcreator_monsteritem as i"
                        + str(i)
                        + " on m.id = i"
                        + str(i)
                        + ".monster_id_id"
                    )
                    if req.POST[str(monster_variable.id) + "_how"] == "least":
                        if where_sql != "":
                            where_sql += " and "
                        where_sql += (
                            "(i"
                            + str(i)
                            + ".monster_item_text >= "
                            + req.POST["monster_variable" + str(monster_variable.id)]
                            + " and i"
                            + str(i)
                            + ".monster_variables_id_id = "
                            + str(monster_variable.id)
                            + ")"
                        )
                    elif req.POST[str(monster_variable.id) + "_how"] == "same":
                        if where_sql != "":
                            where_sql += " and "
                        where_sql += (
                            "(i"
                            + str(i)
                            + ".monster_item_text = "
                            + req.POST["monster_variable" + str(monster_variable.id)]
                            + " and i"
                            + str(i)
                            + ".monster_variables_id_id = "
                            + str(monster_variable.id)
                            + ")"
                        )
                        # monster = monster.filter(monster_item__monster_item_text = int(req.POST["monster_variable"+str(monster_variable.id)]))
                    elif req.POST[str(monster_variable.id) + "_how"] == "utmost":
                        if where_sql != "":
                            where_sql += " and "
                        where_sql += (
                            "(i"
                            + str(i)
                            + ".monster_item_text <= "
                            + req.POST["monster_variable" + str(monster_variable.id)]
                            + " and i"
                            + str(i)
                            + ".monster_variables_id_id = "
                            + str(monster_variable.id)
                            + ")"
                        )
                        # monster = monster.filter(monster_item__monster_item_text <= int(req.POST["monster_variable"+str(monster_variable.id)]))
                else:
                    if req.POST["monster_variable" + str(monster_variable.id)] != "0":
                        join_sql += (
                            " left join tcgcreator_monsteritem as i"
                            + str(i)
                            + " on m.id = i"
                            + str(i)
                            + ".monster_id_id"
                        )
                        if where_sql != "":
                            where_sql += " and "
                        where_sql += (
                            "(i"
                            + str(i)
                            + ".monster_item_text like %s and i"
                            + str(i)
                            + ".monster_variables_id_id = "
                            + str(monster_variable.id)
                            + ")"
                        )
                        add_variable.append(
                            "%"
                            + req.POST["monster_variable" + str(monster_variable.id)]
                            + "%"
                        )
                        # monster = monster.filter(monster_item__monster_item_text__contains = (req.POST["monster_variable"+str(monster_variable.id)]),monster_item__monster_variables_id = int(monster_variable.id))
            i += 1
    if "monster_name" in req.POST and req.POST["monster_name"]:
        if where_sql != "":
            where_sql += " and "
        where_sql += " m.monster_name like %s "
        add_variable.append(
            "%"
            + req.POST["monster_name"]
            + "%"
        )
    if where_sql == "":
        where_sql = "1"
    if "sort" not in req.POST or req.POST["sort"] == "0":
        sort = Config.objects.first().default_sort
        if(sort is None):
            sort = 1
        else:
            sort = sort.id
    else:
        sort = int(req.POST["sort"])
    if "desc" in req.POST and req.POST["desc"] == "1":
        desc = "desc"
    else:
        desc = ""
    if where_sql != "":
        where_sql += " and "
    where_sql += " for_order.monster_variables_id_id = " + str(sort) + " "
    join_sql += (
        " left join tcgcreator_monsteritem as for_order on m.id = for_order.monster_id_id"
    )
    order_by = " order by for_order.monster_item_text " + desc

    monster = Monster.objects.raw(
        "select distinct m.id,m.*, for_order.monster_item_text from tcgcreator_monster as m "
        + join_sql
        + " where "
        + where_sql
        + order_by,
        add_variable,
    )
    user_deck = UserDeck.objects.all().filter(user=req.user, deck_group=user_deck_group)
    # sql = "select * from tcgcreator_monster as m "+ join_sql + " where "+ where_sql
    return render(
        req,
        "tcgcreator/makedecktext.html",
        {
            "MonsterVariables": monster_variables,
            "Monster": monster,
            "UserDeck": user_deck,
            "Deck": decks_show,
            "UserDeckGroup": user_deck_group,
            "UserDeckGroups": user_deck_groups,
            "DefaultDeckGroups": default_deck_groups,
            "sort": sort,
            "desc": desc,
            "return_url" : config.return_url
        },
    )


def makedeck(req):
    config = Config.objects.first();
    monster_variables = MonsterVariables.objects.all().select_related(
        "monster_variable_kind_id"
    )
    decks_show = Deck.objects.filter(makedeckshow=True)
    decks= Deck.objects.all()
    deck_group = 1
    where_sql = " m.token_flag = false "
    join_sql = ""
    add_variable = []
    if not req.user.is_authenticated:
        return HttpResponse("Please Login")
    deck_group = UserDeckChoice.objects.filter(user=req.user).first()
    if not deck_group:
        initial_flag = True
        default_decks = DefaultDeckGroup.objects.all()
        default_deck_id = -1
        for default_deck in default_decks:
            if default_deck_id == int(default_deck.default_deck_id):
                continue
            else:
                default_deck_id = int(default_deck.default_deck_id)
            user_deck_group_max = UserDeckGroup.objects.all().aggregate(Max("user_deck_id"))
            if(user_deck_group_max["user_deck_id__max"] is None):
                deck_group2 = 1
            else:
                deck_group2 = user_deck_group_max["user_deck_id__max"] + 1
            create_user_deck_group(deck_group2, req.user, default_deck.deck_name)
            user_deck_group = (
                UserDeckGroup.objects.all().filter(user_deck_id=deck_group2, user=req.user).first()
            )
            if initial_flag is True:
                create_user_deck_choice(user_deck_group, req.user)
                initial_flag = False
            deck_group = UserDeckChoice.objects.all().filter(user=req.user).first()
            for deck in decks:
                create_user_deck(req.user, deck, user_deck_group, default_deck_id)
    else:
        user_deck_group = deck_group.user_deck
    # 新規デッキ追加
    if "deck_name" in req.GET:
        user_deck_group_max = UserDeckGroup.objects.all().aggregate(Max("user_deck_id"))
        if(user_deck_group_max["user_deck_id__max"] is None):
            deck_group2 = 1
        else:
            deck_group2 = user_deck_group_max["user_deck_id__max"] + 1
        create_user_deck_group(deck_group2, req.user, html.escape(req.GET["deck_name"]))
        user_deck_group = (
            UserDeckGroup.objects.all()
            .filter(user_deck_id=deck_group2, user=req.user)
            .first()
        )
        deck_group.user_deck = user_deck_group
        deck_group.save()
        for deck in decks:
            create_user_deck(req.user, deck, user_deck_group, req.GET["structure_deck"])
    elif "deck_group" in req.GET:
        if "deck_group" in req.GET and req.GET["deck_group"] != "":
            deck_group_id = req.GET["deck_group"]
            user_deck_group = (
                UserDeckGroup.objects.all()
                .filter(user_deck_id=int(deck_group_id), user=req.user)
                .first()
            )
            deck_group.user_deck = user_deck_group
            deck_group.save()
    else:
        # デッキグループを選択
        if "deck_group" in req.POST and req.POST["deck_group"] != "":
            deck_group_id = req.POST["deck_group"]
            user_deck_group = (
                UserDeckGroup.objects.all()
                .filter(user_deck_id=int(deck_group_id), user=req.user)
                .first()
            )
            deck_group.user_deck = user_deck_group
            deck_group.save()
        elif "deck_name" in req.POST and req.POST["deck_name"] != "":
            user_deck_group = deck_group.user_deck
            deck_name = html.escape(req.POST["deck_name"])
            user_deck_group.deck_name = deck_name
            user_deck_group.save()
        else:
            user_deck_group = deck_group.user_deck

    user_deck_groups = UserDeckGroup.objects.filter(user_id=req.user)

    default_deck_groups = DefaultDeckGroup.objects.all()
    for deck in decks:
        user_decks = UserDeck.objects.all().filter(
            user=req.user, deck_type__id=deck.id, deck_group=user_deck_group
        )

    if req.method == "POST":
        check = copy_to_deck(req.user, req.POST, user_deck_group)
        if check != "":
            return HttpResponse(check)

        i = 0
        for monster_variable in monster_variables:
            if (
                "monster_variable" + str(monster_variable.id) in req.POST
                and req.POST["monster_variable" + str(monster_variable.id)] != ""
            ):
                if monster_variable.monster_variable_kind_id.monster_variable_name == "数値" :
                    join_sql += (
                        " left join tcgcreator_monsteritem as i"
                        + str(i)
                        + " on m.id = i"
                        + str(i)
                        + ".monster_id_id"
                    )
                    if str(monster_variable.id) + "_how" in req.POST and req.POST[str(monster_variable.id) + "_how"] == "least":
                        if where_sql != "":
                            where_sql += " and "
                        where_sql += (
                            "(i"
                            + str(i)
                            + ".monster_item_text >= "
                            + req.POST["monster_variable" + str(monster_variable.id)]
                            + " and i"
                            + str(i)
                            + ".monster_variables_id_id = "
                            + str(monster_variable.id)
                            + ")"
                        )
                    elif str(monster_variable.id) + "_how" in req.POST and req.POST[str(monster_variable.id) + "_how"] == "same":
                        if where_sql != "":
                            where_sql += " and "
                        where_sql += (
                            "(i"
                            + str(i)
                            + ".monster_item_text = "
                            + req.POST["monster_variable" + str(monster_variable.id)]
                            + " and i"
                            + str(i)
                            + ".monster_variables_id_id = "
                            + str(monster_variable.id)
                            + ")"
                        )
                        # monster = monster.filter(monster_item__monster_item_text = int(req.POST["monster_variable"+str(monster_variable.id)]))
                    elif str(monster_variable.id) + "_how" in req.POST and req.POST[str(monster_variable.id) + "_how"] == "utmost":
                        if where_sql != "":
                            where_sql += " and "
                        where_sql += (
                            "(i"
                            + str(i)
                            + ".monster_item_text <= "
                            + req.POST["monster_variable" + str(monster_variable.id)]
                            + " and i"
                            + str(i)
                            + ".monster_variables_id_id = "
                            + str(monster_variable.id)
                            + ")"
                        )
                        # monster = monster.filter(monster_item__monster_item_text <= int(req.POST["monster_variable"+str(monster_variable.id)]))
                else:
                    if req.POST["monster_variable" + str(monster_variable.id)] != "0":
                        join_sql += (
                            " left join tcgcreator_monsteritem as i"
                            + str(i)
                            + " on m.id = i"
                            + str(i)
                            + ".monster_id_id"
                        )
                        if where_sql != "":
                            where_sql += " and "
                        where_sql += (
                            "(i"
                            + str(i)
                            + ".monster_item_text like %s and i"
                            + str(i)
                            + ".monster_variables_id_id = "
                            + str(monster_variable.id)
                            + ")"
                        )
                        add_variable.append(
                            "%"
                            + req.POST["monster_variable" + str(monster_variable.id)]
                            + "%"
                        )
                        # monster = monster.filter(monster_item__monster_item_text__contains = (req.POST["monster_variable"+str(monster_variable.id)]),monster_item__monster_variables_id = int(monster_variable.id))
            i += 1
    if "monster_name" in req.POST and req.POST["monster_name"]:
        if where_sql != "":
            where_sql += " and "
        where_sql += " m.monster_name like %s "
        add_variable.append(
            "%"
            + req.POST["monster_name"]
            + "%"
        )
    if where_sql == "":
        where_sql = "1"
    if "sort" not in req.POST or req.POST["sort"] == "0":
        sort = Config.objects.first().default_sort
        if(sort is None):
            sort = 1
        else:
            sort = sort.id
    else:
        sort = int(req.POST["sort"])
    if "desc" in req.POST and req.POST["desc"] == "1":
        desc = "desc"
    else:
        desc = ""
    if where_sql != "":
        where_sql += " and "
    where_sql += " for_order.monster_variables_id_id = " + str(sort) + " "
    join_sql += (
        " left join tcgcreator_monsteritem as for_order on m.id = for_order.monster_id_id"
    )
    order_by = " order by for_order.monster_item_text " + desc

    monster = Monster.objects.raw(
        "select distinct m.id,m.*, for_order.monster_item_text from tcgcreator_monster as m "
        + join_sql
        + " where "
        + where_sql
        + order_by,
        add_variable,
    )
    user_deck = UserDeck.objects.all().filter(user=req.user, deck_group=user_deck_group)
    # sql = "select * from tcgcreator_monster as m "+ join_sql + " where "+ where_sql
    return render(
        req,
        "tcgcreator/makedeck.html",
        {
            "MonsterVariables": monster_variables,
            "Monster": monster,
            "UserDeck": user_deck,
            "Deck": decks_show,
            "UserDeckGroup": user_deck_group,
            "UserDeckGroups": user_deck_groups,
            "DefaultDeckGroups": default_deck_groups,
            "sort": sort,
            "desc": desc,
            "return_url" : config.return_url
        },
    )


def get_monster_deck_type(req):
    num = req.POST["num"]
    decks = Deck.objects.all()
    result = (
        '<select id="monster_deck_text_'
        + num
        + '" name="monster_item_text_'
        + num
        + '" onchange="changeDeckNum()">'
    )
    for deck in decks:
        result += '<option value="' + str(deck.id) + '">' + deck.deck_name + "</option>"
    result += "</select>"
    return HttpResponse(result)


def get_phase(req):
    phases = Phase.objects.all()
    return_html = ""
    for phase in phases:
        return_html += (
            '<option value="' + str(phase.id) + '">' + phase.phase_name + "</option>"
        )
    return HttpResponse(return_html)


def get_trigger(req):
    triggers = Trigger.objects.filter(trigger_none_monster=True)
    return_html = ""
    for trigger in triggers:
        return_html += (
            '<option value="'
            + str(trigger.id)
            + '">'
            + trigger.trigger_name
            + "</option>"
        )
    return HttpResponse(return_html)


def get_trigger_with_monster(req):
    triggers = Trigger.objects.all()
    return_html = ""
    for trigger in triggers:
        return_html += (
            '<option value="'
            + str(trigger.id)
            + '">'
            + trigger.trigger_name
            + "</option>"
        )
    return HttpResponse(return_html)


def get_monster_effect_wrapper(req):
    effects = MonsterEffectWrapper.objects.all()
    return_html = '<option value="0">選択</option>'
    for effect in effects:
        return_html += (
            '<option value="'
            + str(effect.id)
            + '">'
            + effect.monster_effect_name
            + "</option>"
        )
    return HttpResponse(return_html)


def get_pac_wrapper(req):
    pacs = PacWrapper.objects.all()
    return_html = '<option value="0">選択</option>'
    for pac in pacs:
        return_html += (
            '<option value="' + str(pac.id) + '">' + pac.pac_name + "</option>"
        )
    return HttpResponse(return_html)


def choose(request):
    if "ID" in request.COOKIES:
        ID = request.COOKIES["ID"]
    else:
        if not request.user.is_authenticated:
            response = redirect('tcgcreator:choose')
            ID = str(uuid.uuid4())
            response.set_cookie('ID', ID,max_age=3600*24*3)
            return response
    reenter1 = 0
    reenter2 = 0
    reenter3 = 0
    ai1 = True
    ai2 = True
    ai3 = True
    duel_1 = Duel.objects.filter(id=1).get()
    if duel_1.user_2 is None and duel_1.is_ai == False and duel_1.guest_flag2 is False:
        duel_1.winner = 0
        watch_1 = 0
    else:
        watch_1 = 1
    duel_2 = Duel.objects.filter(id=2).get()
    if duel_2.user_2 is None and duel_2.is_ai == False and duel_2.guest_flag2 is False:
        duel_2.winner = 0
        watch_2 = 0
    else:
        watch_2 = 1
    duel_3 = Duel.objects.filter(id=3).get()
    if duel_3.user_2 is None and duel_3.is_ai == False and duel_3.guest_flag2 is False:
        duel_3.winner = 0
        watch_3 = 0
    else:
        watch_3 = 1
    if duel_1.guest_flag is True:    
        user1_1_name = duel_1.guest_name
    elif duel_1.user_1:
        user1_1_name = duel_1.user_1.first_name
    else:
        user1_1_name = ""
    if duel_2.guest_flag is True:
        user2_1_name = duel_2.guest_name
    elif duel_2.user_1:
        user2_1_name = duel_2.user_1.first_name
    else:
        user2_1_name = ""
    if duel_3.guest_flag is True:
        user3_1_name = duel_3.guest_name
    elif duel_3.user_1:
        user3_1_name = duel_3.user_1.first_name
    else:
        user3_1_name = ""
    if duel_1.guest_flag2 is True:
        user1_2_name = duel_1.guest_name2
    elif duel_2.is_ai == True:
        user1_2_name = "NPC"
    elif duel_1.user_2:
        user1_2_name = duel_1.user_2.first_name
    else:
        user1_2_name = ""
    if duel_2.guest_flag2 is True:
        user2_2_name = duel_2.guest_name2
    elif duel_2.is_ai == True:
        user2_2_name = "NPC"
    elif duel_2.user_2:
        user2_2_name = duel_2.user_2.first_name
    else:
        user2_2_name = ""
    if duel_3.guest_flag2 is True:    
        user3_2_name = duel_3.guest_name2
    elif duel_3.is_ai == True:
        user3_2_name = "NPC"
    elif duel_3.user_2:
        user3_2_name = duel_3.user_2.first_name
    else:
        user3_2_name = ""
    if duel_1.guest_flag is True:    
        user1_1_name = duel_1.guest_name
    if duel_1.is_ai == True:
        user1_2_name = "NPC"
    elif duel_1.user_2 is not None:
        user1_2_name = duel_1.user_2.first_name
    config = Config.objects.get()
    decks = Deck.objects.all()
    limit_time = config.limit_time
    room_time = config.room_time
    room_text1 = ""
    room_text2 = ""
    room_text3 = ""
    if user1_1_name == "":
        user1_1_name = "ゲスト"
    if user1_2_name == "":
        user1_2_name = "ゲスト"
    if user2_1_name == "":
        user2_1_name = "ゲスト"
    if user2_2_name == "":
        user2_2_name = "ゲスト"
    if user3_1_name == "":
        user3_1_name = "ゲスト"
    if user3_2_name == "":
        user3_2_name = "ゲスト"
    '''    
    if duel_1.user_1 is not None or duel_1.guest_flag is True:
            room_text1 += user1_1_name + "対" + user1_2_name + "\n"
    if duel_1.winner == 1:
            room_text1 += user1_1_name + "の勝利\n"
    elif duel_1.winner == 2:
            room_text1 += user1_2_name + "の勝利\n"
    elif duel_1.winner == 3:
            room_text1 += "引き分け"
    if duel_2.user_1 is not None or duel_2.guest_flag is True:
            room_text2 += user2_1_name + "対" + user2_2_name + "\n"
    if duel_2.winner == 1:
        room_text2 += user2_1_name + "の勝利\n"
    elif duel_2.winner == 2:
        room_text2 += user2_2_name + "の勝利\n"
    elif duel_2.winner == 3:
            room_text1 += "引き分け"
    if duel_3.user_1 is not None or duel_3.guest_flag is True:
            room_text3 += user3_1_name + "対" + user3_2_name + "\n"
    if duel_3.winner == 1:
        room_text3 += user3_1_name + "の勝利\n"
    elif duel_3.winner == 2:
        room_text3 += user3_2_name + "の勝利\n"
    elif duel_2.winner == 3:
            room_text1 += "引き分け"
    '''
    if duel_1.waiting == True:
        wait_kind1 = 0
    elif duel_1.winner != 0 and time() - duel_1.end_time > room_time:
        duel_1.waiting = True
        duel_1.save()
        wait_kind1 = 0
    elif duel_1.winner != 0:
        room_text1 += str(int(room_time - (time() - duel_1.end_time))) + "後に開放"
        wait_kind1 = 1
    elif duel_1.winner == 0 and time() - duel_1.time_1 > limit_time * 2:
        resetduel(duel_1)
        wait_kind1 = 0
    elif duel_1.winner == 0:
        ai1 = False
        room_text1 += "対戦中" + user1_1_name + "対" + user1_2_name
        if (request.user.is_authenticated  and (request.user == duel_1.user_1 or request.user == duel_1.user_2)) or ((not request.user.is_authenticated) and ((duel_1.guest_id == ID and duel_1.guest_flag is True)or (duel_1.guest_id2 == ID and duel_1.guest_flag2 is True))):
            reenter1 = 1
        wait_kind1 = 2
    if duel_2.waiting == True:
        wait_kind2 = 0
    elif duel_2.winner != 0 and time() - duel_2.end_time > room_time:
        duel_2.waiting = True
        duel_2.save()
        wait_kind2 = 0
    elif duel_2.winner != 0:
        room_text2 += str(int(room_time - (time() - duel_2.end_time))) + "後に開放"
        wait_kind2 = 1
    elif duel_2.winner == 0 and time() - duel_2.time_1 > limit_time * 2:
        resetduel(duel_2)
        duel_2.waiting = True
        duel_2.save()
        wait_kind2 = 0
    elif duel_2.winner == 0:
        ai2 = False
        room_text2 += "対戦中" + user2_1_name + "対" + user2_2_name
        if (request.user.is_authenticated  and (request.user == duel_2.user_1 or request.user == duel_2.user_2)) or ((not request.user.is_authenticated) and ((duel_2.guest_id == ID and duel_2.guest_flag is True)or (duel_2.guest_id2 == ID and duel_2.guest_flag2 is True))):
            reenter2 = 1
        wait_kind2 = 2
    if duel_3.waiting == True:
        wait_kind3 = 0
    elif duel_3.winner != 0 and time() - duel_3.end_time > room_time:
        duel_3.waiting = True
        duel_3.save()
        wait_kind3 = 0
    elif duel_3.winner != 0:
        room_text3 += str(int(room_time - (time() - duel_3.end_time))) + "後に開放"
        wait_kind3 = 1
    elif duel_3.winner == 0 and time() - duel_3.time_1 > limit_time * 2:
        resetduel(duel_3)
        duel_3.waiting = True
        duel_3.save()
        wait_kind3 = 0
    elif duel_3.winner == 0:
        ai3 = False
        room_text3 += "対戦中" + user3_1_name + "対" + user3_2_name
        if (request.user.is_authenticated  and (request.user == duel_3.user_1 or request.user == duel_3.user_2)) or ((not request.user.is_authenticated) and ((duel_3.guest_id == ID and duel_3.guest_flag is True)or (duel_3.guest_id2 == ID and duel_3.guest_flag2 is True))):
            reenter3 = 1
        wait_kind3 = 2
    if duel_1.winner == 0 and duel_1.waiting == True and (duel_1.user_1 or duel_1.guest_flag):
        if time() - duel_1.wait_time > limit_time:
            duel_1.user_1 = None
            duel_1.guest_id = -1
            duel_1.guest_flag = False
            duel_1.save();
        else:
            if duel_1.user_1:
                room_text1 += duel_1.user_1.first_name
            else:
                room_text1 += "ゲスト"
            room_text1 += "待機中"
            ai1 = False
    if duel_2.winner == 0 and duel_2.waiting == True and (duel_2.user_1 or duel_2.guest_flag ):
        if time() - duel_2.wait_time > limit_time:
            duel_2.user_1 = None
            duel_2.guest_id = -1
            duel_2.guest_flag = False
            duel_2.save();
        else:
            if duel_2.user_1:
                room_text2 += duel_2.user_1.first_name
            else:
                room_text2 += "ゲスト"
            room_text2 += "待機中"
            ai2 = False
    if duel_3.winner == 0 and duel_3.waiting == True and (duel_3.user_1 or duel_3.guest_flag):
        if time() - duel_3.wait_time > limit_time:
            duel_3.user_1 = None
            duel_3.guest_id = -1
            duel_3.guest_flag = False
            duel_3.save();
        else:
            if duel_3.user_1:
                room_text3 += duel_3.user_1.first_name
            else:
                room_text3 += "ゲスト"
            room_text3 += "待機中"
            ai3 = False
    if request.user.is_authenticated:
        deck_group = UserDeckChoice.objects.filter(user=request.user).first()
        if not deck_group:
            initial_flag = True
            default_decks = DefaultDeckGroup.objects.all()
            default_deck_id = -1
            for default_deck in default_decks:
                if default_deck_id == int(default_deck.default_deck_id):
                    continue
                else:
                    default_deck_id = int(default_deck.default_deck_id)
                user_deck_group_max = UserDeckGroup.objects.all().aggregate(Max("user_deck_id"))
                if(user_deck_group_max["user_deck_id__max"] is None):
                    deck_group2 = 1
                else:
                    deck_group2 = user_deck_group_max["user_deck_id__max"] + 1
                create_user_deck_group(deck_group2, request.user, default_deck.deck_name)
                user_deck_group = (
                    UserDeckGroup.objects.all().filter(user_deck_id=deck_group2, user=request.user).first()
                )
                if initial_flag is True:
                    create_user_deck_choice(user_deck_group, request.user)
                    initial_flag = False
                deck_group = UserDeckChoice.objects.all().filter(user=request.user).first()
                for deck in decks:
                    create_user_deck(request.user, deck, user_deck_group, default_deck_id)
        else:
            user_deck_group = deck_group.user_deck
        user_deck_groups = UserDeckGroup.objects.filter(user_id=request.user)
        guest_flag = False
        default_deck_groups = {}
    else:
        default_deck_groups = DefaultDeckGroup.objects.all()
        user_deck_group = {}
        user_deck_groups = []
        guest_flag = True
    config  = Config.objects.first()
    background = Background.objects.order_by("?")[0]
    background_file_name = background.file_name
    enemy_deck_groups = EnemyDeckGroup.objects.filter()
    enemy_deck_group = EnemyDeckChoice.objects.filter().first()

    return render(
        request,
        "tcgcreator/choose.html",
        {
            "Background": background_file_name,
            "room_text1": room_text1,
            "room_text2": room_text2,
            "room_text3": room_text3,
            "wait_kind1": wait_kind1,
            "wait_kind2": wait_kind2,
            "wait_kind3": wait_kind3,
            "watch_1": watch_1,
            "watch_2": watch_2,
            "watch_3": watch_3,
            "reenter1": reenter1,
            "reenter2": reenter2,
            "reenter3": reenter3,
            "ai1": ai1,
            "ai2": ai2,
            "ai3": ai3,
            "UserDeckGroup": user_deck_group,
            "UserDeckGroups": user_deck_groups,
            "DefaultDeckGroups": default_deck_groups,
            "EnemyDeckGroup": enemy_deck_group,
            "EnemyDeckGroups": enemy_deck_groups,
            "Config": config,
            "guest_flag":guest_flag
        },
    )


def get_tcg_timing(req):
    timings = Timing.objects.all()
    return_html = ""
    for timing in timings:
        return_html += (
            '<option value="' + str(timing.id) + '">' + timing.timing_name + "</option>"
        )
    return HttpResponse(return_html)


def index(request):
    if request.user.is_authenticated:
        user_flag = True
    else:
        user_flag = False
    config = Config.objects.get();
    return render(request, "tcgcreator/index.html", {"user_flag": user_flag,"config":config})


def howto(request):
    return render(request, "tcgcreator/howto.html")


def user_info_change(request):
    config = Config.objects.first();
    if not request.user.is_authenticated:
        return HttpResponse("ログインしてください")
    if request.method == "POST":
        form = profileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(config.return_url)
    else:
        form = profileForm(initial={'first_name': request.user.first_name})
        user = UserPoint.objects.filter(user = request.user).first()
        if user is None:
            user = UserPoint(user = request.user)
            user.save()
        return render(request, "tcgcreator/user_info_change.html", {"form": form,"user":user,"return_url":config.return_url})

def login_user(request):    
    config = Config.objects.first();

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(config.return_url)

    return HttpResponseRedirect(reverse("tcgcreator:signup"))
def logout_user(request):
    config = Config.objects.first();
    logout(request)
    return redirect(config.return_url)
def signup(request):
    config = Config.objects.first();
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid() and request.POST["first_name"]:
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(config.return_url)
    else:
        form = UserForm()
    return render(request, "tcgcreator/signup.html", {"form": form})


def get_last_monster_effect(request):
    return_html = "<option value>-------------</option>"
    if request.method == "POST":
        monster_effects = MonsterEffect.objects.order_by('-id' )[:5]
        for monster_effect in monster_effects:
            return_html += (
                    '<option value="'
                    + str(monster_effect.id)
                    + '">'
                    + monster_effect.monster_effect_name
                    + "</option>"
            )
        return HttpResponse(return_html)
def get_monster_effect(request):
    return_html = "<option value>-------------</option>"
    if request.method == "POST":
        monster_effects = MonsterEffect.objects.filter(
            monster_effect_name__contains=request.POST["name"]
        )
        for monster_effect in monster_effects:
            return_html += (
                '<option value="'
                + str(monster_effect.id)
                + '">'
                + monster_effect.monster_effect_name
                + "</option>"
            )
        return HttpResponse(return_html)


def get_last_trigger_specify(req):
    return_html = "<option value>-------------</option>"
    if req.method == "POST":
        triggers = Trigger.objects.order_by('-id')[:5]
        for trigger in triggers:
            return_html += (
                    '<option value="'
                    + str(trigger.id)
                    + '">'
                    + trigger.trigger_name
                    + "</option>"
            )
        return HttpResponse(return_html)


def get_trigger_specify(req):
    return_html = "<option value>-------------</option>"
    if req.method == "POST":
        triggers = Trigger.objects.filter(trigger_name__contains=req.POST["name"])
        if req.POST["trigger_val"] != "0":
            triggers = triggers.filter(
                Q(trigger_kind__contains="_" + req.POST["trigger_val"] + "_")
                | Q(trigger_kind__startswith=req.POST["trigger_val"] + "_")
                | Q(trigger_kind__endswith="_" + req.POST["trigger_val"])
                | Q(trigger_kind=req.POST["trigger_val"])
            )

        for trigger in triggers:
            return_html += (
                '<option value="'
                + str(trigger.id)
                + '">'
                + trigger.trigger_name
                + "</option>"
            )
        return HttpResponse(return_html)


def get_last_monster_effect_wrapper_specify(request):
    return_html = "<option value>-------------</option>"
    if request.method == "POST":
        monster_effects = MonsterEffectWrapper.objects.order_by('-id')[:5]
        for monster_effect in monster_effects:
            return_html += (
                    '<option value="'
                    + str(monster_effect.id)
                    + '">'
                    + monster_effect.monster_effect_name
                    + "</option>"
            )
        return HttpResponse(return_html)

def get_last_pac_specify(request):
    return_html = "<option value>-------------</option>"
    if request.method == "POST":
        pacs = Pac.objects.order_by('-id')[:5]
        for pac in pacs:
            return_html += (
                    '<option value="' + str(pac.id) + '">' + pac.pac_name + "</option>"
            )
        return HttpResponse(return_html)

def get_pac_specify(request):
    return_html = "<option value>-------------</option>"
    if request.method == "POST":
        monster_effects = Pac.objects.filter(
            pac_name__contains=request.POST["name"]
        )
        for monster_effect in monster_effects:
            return_html += (
                    '<option value="'
                    + str(monster_effect.id)
                    + '">'
                    + monster_effect.pac_name
                    + "</option>"
            )
        return HttpResponse(return_html)


def get_monster_effect_wrapper_specify(request):
    return_html = "<option value>-------------</option>"
    if request.method == "POST":
        monster_effects = MonsterEffectWrapper.objects.filter(
            monster_effect_name__contains=request.POST["name"]
        )
        if request.POST["monster_effect_val"] != "0" and request.POST["monster_effect_val"] != "null":
            monster_effects = monster_effects.filter(
                Q(
                    monster_effect_kind__contains="_"
                    + request.POST["monster_effect_val"]
                    + "_"
                )
                | Q(
                    monster_effect_kind__startswith=request.POST["monster_effect_val"]
                    + "_"
                )
                | Q(
                    monster_effect_kind__endswith="_"
                    + request.POST["monster_effect_val"]
                )
                | Q(monster_effect_kind=request.POST["monster_effect_val"])
            )

        for monster_effect in monster_effects:
            return_html += (
                '<option value="'
                + str(monster_effect.id)
                + '">'
                + monster_effect.monster_effect_name
                + "</option>"
            )
        return HttpResponse(return_html)


def get_last_pac_wrapper_specify(request):
    return_html = "<option value>-------------</option>"
    if request.method == "POST":
        pacs = PacWrapper.objects.order_by('-id')[:5]
        for pac in pacs:
            return_html += (
                    '<option value="' + str(pac.id) + '">' + pac.pac_name + "</option>"
            )
        return HttpResponse(return_html)
def get_pac_wrapper_specify(request):
    return_html = "<option value>-------------</option>"
    if request.method == "POST":
        pacs = PacWrapper.objects.filter(pac_name__contains=request.POST["name"])
        if request.POST["pac_val"] != "0":
            pacs = pacs.filter(
                Q(monster_effect_kind__contains="_" + request.POST["pac_val"] + "_")
                | Q(monster_effect_kind__startswith=request.POST["pac_val"] + "_")
                | Q(monster_effect_kind__endswith=request.POST["pac_val"] + "_")
                | Q(monster_effect_kind=request.POST["pac_val"])
            )

        for pac in pacs:
            return_html += (
                '<option value="' + str(pac.id) + '">' + pac.pac_name + "</option>"
            )
        return HttpResponse(return_html)


def get_last_pac_cost_wrapper_specify(request):
    return_html = "<option value>-------------</option>"
    if request.method == "POST":
        pacs = PacCostWrapper.objects.order_by('-id')[:5]
        for pac in pacs:
            return_html += (
                    '<option value="' + str(pac.id) + '">' + pac.pac_cost_name + "</option>"
            )
        return HttpResponse(return_html)
def get_pac_cost_wrapper_specify(request):
    return_html = "<option value>-------------</option>"
    if request.method == "POST":
        costs = PacCostWrapper.objects.filter(
            pac_cost_name__contains=request.POST["name"]
        )
        if request.POST["cost_val"] != "0":
            costs = costs.filter(
                Q(monster_effect_kind__contains="_" + request.POST["cost_val"] + "_")
                | Q(monster_effect_kind__startswith=request.POST["cost_val"] + "_")
                | Q(monster_effect_kind__endswith=request.POST["cost_val"] + "_")
                | Q(monster_effect_kind=request.POST["cost_val"])
            )

        for cost in costs:
            return_html += (
                '<option value="'
                + str(cost.id)
                + '">'
                + cost.pac_cost_name
                + "</option>"
            )
        return HttpResponse(return_html)


def get_last_cost_wrapper_specify(request):
    return_html = "<option value>-------------</option>"
    if request.method == "POST":
        costs = CostWrapper.objects.order_by('-id')[:5]
        for cost in costs:
            return_html += ( '<option value="' + str(cost.id) + '">' + cost.cost_name + "</option>" )
        return HttpResponse(return_html)
def get_cost_wrapper_specify(request):
    return_html = "<option value>-------------</option>"
    if request.method == "POST":
        costs = CostWrapper.objects.filter(cost_name__contains=request.POST["name"])
        if request.POST["cost_val"] != "0":
            costs = costs.filter(
                Q(cost_kind__contains="_" + request.POST["cost_val"] + "_")
                | Q(cost_kind__startswith=request.POST["cost_val"] + "_")
                | Q(cost_kind__endswith=request.POST["cost_val"] + "_")
                | Q(cost_kind=request.POST["cost_val"])
            )

        for cost in costs:
            return_html += (
                '<option value="' + str(cost.id) + '">' + cost.cost_name + "</option>"
            )
        return HttpResponse(return_html)


def get_last_cost(request):
    return_html = "<option value>-------------</option>"
    if request.method == "POST":
        costs = Cost.objects.order_by('-id')[:5]

        for cost in costs:
            return_html += (
                    '<option value="' + str(cost.id) + '">' + cost.cost_name + "</option>"
            )
        return HttpResponse(return_html)
def get_cost(request):
    return_html = "<option value>-------------</option>"
    if request.method == "POST":
        costs = Cost.objects.filter(cost_name__contains=request.POST["name"])

        for cost in costs:
            return_html += (
                '<option value="' + str(cost.id) + '">' + cost.cost_name + "</option>"
            )
        return HttpResponse(return_html)
def save_unit(request):
    if not request.user.is_staff:
        return HttpResponse("error")
    pwd = os.path.dirname(__file__)
    data_file = open(pwd + "/data.csv", mode="r", encoding="utf-8")
    data2 = data_file.readlines()
    for data in data2 :
        datas = data.split(",")
        monster = Monster()
        monster.monster_name = datas[2]
        monster.monster_sentence = datas[9]
        monster.limit = 2
        monster.deck = 1
        monster_variables = MonsterVariables.objects.order_by("priority")
        i = 8
        monster.save()
        for monster_variable  in monster_variables:
            if i == 8:
                i=6
                if(datas[8] == "クイーンサイド"):
                    monster_item = MonsterItem(
                        monster_id=monster,
                        monster_variables_id=monster_variable,
                        monster_item_text="1"
                    )
                    monster_item.save()
                elif(datas[8] == "パイロマンサー"):
                     monster_item = MonsterItem(
                        monster_id=monster,
                        monster_variables_id=monster_variable,
                         monster_item_text="2"
                    )
                     monster_item.save()
                elif(datas[8] == "ディシプリン"):
                     monster_item = MonsterItem(
                        monster_id=monster,
                        monster_variables_id=monster_variable,
                         monster_item_text="3"
                    )
                     monster_item.save()
                elif(datas[8] == "ナイトパクト"):
                     monster_item = MonsterItem(
                        monster_id=monster,
                        monster_variables_id=monster_variable,
                         monster_item_text="4"
                    )
                     monster_item.save()
                elif(datas[8] == "ルクスリアス"):
                     monster_item = MonsterItem(
                        monster_id=monster,
                        monster_variables_id=monster_variable,
                         monster_item_text="5"
                    )
                     monster_item.save()
                else:
                     monster_item = MonsterItem(
                        monster_id=monster,
                        monster_variables_id=monster_variable,
                         monster_item_text="0"
                    )
                     monster_item.save()
            elif i == 6:
                i=5
                if(datas[6] == "ヒーロー"):
                    monster_item = MonsterItem(
                        monster_id=monster,
                        monster_variables_id=monster_variable,
                        monster_item_text="1"
                    )
                    monster_item.save()
                elif(datas[6] == "ユニット"):
                    monster_item = MonsterItem(
                        monster_id=monster,
                        monster_variables_id=monster_variable,
                        monster_item_text="2"
                    )
                    monster_item.save()
                elif(datas[6] == "上官・ユニット"):
                    monster_item = MonsterItem(
                        monster_id=monster,
                        monster_variables_id=monster_variable,
                        monster_item_text="3"
                    )
                    monster_item.save()
                elif(datas[6] == "マーシャル・ロウ"):
                    monster_item = MonsterItem(
                        monster_id=monster,
                        monster_variables_id=monster_variable,
                        monster_item_text="4"
                    )
                    monster_item.save()
                elif(datas[6] == "紅蓮炸裂"):
                    monster_item = MonsterItem(
                        monster_id=monster,
                        monster_variables_id=monster_variable,
                        monster_item_text="5"
                    )
                    monster_item.save()
                elif(datas[6] == "尊行・ユニット"):
                    monster_item = MonsterItem(
                        monster_id=monster,
                        monster_variables_id=monster_variable,
                        monster_item_text="6"
                    )
                    monster_item.save()
                elif(datas[6] == "アビリティ"):
                    monster_item = MonsterItem(
                        monster_id=monster,
                        monster_variables_id=monster_variable,
                        monster_item_text="7"
                    )
                    monster_item.save()
                elif(datas[6] == "尊行"):
                    monster_item = MonsterItem(
                        monster_id=monster,
                        monster_variables_id=monster_variable,
                        monster_item_text="8"
                    )
                    monster_item.save()
            elif i == 5:
                i=4
                if datas[5] != "":
                    monster_item = MonsterItem(
                        monster_id=monster,
                        monster_variables_id=monster_variable,
                        monster_item_text=datas[5]
                    )
                    monster_item.save()
                else:
                    monster_item = MonsterItem(
                        monster_id=monster,
                        monster_variables_id=monster_variable,
                        monster_item_text="0"
                    )
                    monster_item.save()
            elif i == 4:
                i=3
                if datas[4] != "":
                    monster_item = MonsterItem(
                        monster_id=monster,
                        monster_variables_id=monster_variable,
                        monster_item_text=datas[4]
                    )
                    monster_item.save()
                else:
                    monster_item = MonsterItem(
                        monster_id=monster,
                        monster_variables_id=monster_variable,
                        monster_item_text="0"
                    )
                    monster_item.save()
            elif i == 3:
                if datas[3] != "":
                    monster_item = MonsterItem(
                        monster_id=monster,
                        monster_variables_id=monster_variable,
                        monster_item_text=datas[3]
                    )
                    monster_item.save()
                else:
                    monster_item = MonsterItem(
                        monster_id=monster,
                        monster_variables_id=monster_variable,
                        monster_item_text="0"
                    )
                    monster_item.save()

    HttpResponse("OK")

