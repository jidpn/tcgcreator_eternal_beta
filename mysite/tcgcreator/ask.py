from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .battle_det import battle_det, answer_ai_choose_trigger
from .models import (
    Config,
    Trigger,
    FieldSize,
    Deck,
    Grave,
    Hand,
    Duel,
    MonsterEffectWrapper,
    DuelGrave,
    DuelHand,
    CostWrapper,
    Monster,
)
from pprint import pprint
import json
from .duel import DuelObj
import uuid


def ask_place(request):
    decks = Deck.objects.all()
    graves = Grave.objects.all()
    hands = Hand.objects.all()
    room_number = int(request.POST["room_number"])
    duel = Duel.objects.filter(id=room_number).get()
    duelobj = DuelObj(room_number)
    duelobj.duel = duel
    duelobj.room_number = room_number
    if duel.guest_flag is False:
        ID1 = -1
    else:
        ID1 = duel.guest_id
    if duel.guest_flag2 is False:
        ID2 = -1
    else:
        ID2 = duel.guest_id2
    if "ID" in request.COOKIES :
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    if duel.user_1 != request.user and duel.user_2 != request.user:
        if (ID1 == ID and duel.guest_flag) or (ID2 == ID and duel.guest_flag2):
            pass
        else:
            return HttpResponseRedirect(reverse("watch_battle"))
    if duel.winner != 0 or duel.winner_ai != 0:
        return HttpResponse("end")

    if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag):
        user = 1
        other_user = 2
        duelobj.user = 1
        if duel.ask2 == 4 and duel.ask == 0 and duel.retrieve == 0:
            if duel.user_turn == 1 :
                duel.ask2 = 5
                return choose_trigger(duel, 1, room_number, duel.ask2, decks, graves, hands)
            else:
                if duel.is_ai is True:
                    duelobj.init_all(user, other_user, room_number)
                    duelobj.check_eternal_effect( decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
                    answer_ai_choose_trigger(duelobj,duel, 2, room_number, duel.ask2, decks, graves, hands)
                    duelobj.save_all(user, other_user, room_number)
                    return battle_det(request, duelobj)
                return wait_choose_trigger(duel, 1, room_number, duel.ask2, decks, graves, hands)
        elif duel.ask2 == 5 and duel.ask == 0 and duel.retrieve == 0:
            if duel.user_turn == 1:
                return choose_trigger(duel, 1, room_number, duel.ask2, decks, graves, hands)
            else:
                if duel.is_ai is True:
                    duelobj.init_all(user, other_user, room_number)
                    duelobj.check_eternal_effect( decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
                    answer_ai_choose_trigger(duelobj,duel, 2, room_number, duel.ask2, decks, graves, hands)
                    duelobj.save_all(user, other_user, room_number)
                    return battle_det(request, duelobj)
                return wait_choose_trigger(duel, 1, room_number, duel.ask, decks, graves, hands)
        elif duel.ask2 == 6  and duel.ask == 0 and duel.retrieve == 0:
            if duel.user_turn == 2:
                return choose_trigger(duel, 1, room_number, duel.ask2, decks, graves, hands)
            else:
                if duel.is_ai is True:
                    duelobj.init_all(user, other_user, room_number)
                    duelobj.check_eternal_effect( decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
                    answer_ai_choose_trigger(duelobj,duel, 2, room_number, duel.ask2, decks, graves, hands)
                    duelobj.save_all(user, other_user, room_number)
                    return battle_det(request, duelobj)
                return wait_choose_trigger(duel, 1, room_number, duel.ask2, decks, graves, hands)
       
    if duel.user_2 == request.user or (ID2 == ID and duel.guest_flag2) or duel.is_ai is True:
        user = 2
        other_user = 1
        duelobj.user = 2
        if duel.ask2 == 4 and duel.ask == 0 and duel.retrieve == 0:
            if duel.user_turn == 2:
                duel.ask2 = 5
                if duel.is_ai is False:
                    return choose_trigger(duel, 2, room_number, duel.ask2, decks, graves, hands)
                else:
                    duelobj.init_all(user, other_user, room_number)
                    duelobj.check_eternal_effect( decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
                    answer_ai_choose_trigger(duelobj,duel, 2, room_number, duel.ask2, decks, graves, hands)
                    duelobj.save_all(user, other_user, room_number)
                    return HttpResponse("ai")
            else:
                return wait_choose_trigger(duel, 2, room_number, duel.ask2, decks, graves, hands)
        elif duel.ask2 == 5  and duel.ask == 0 and duel.retrieve == 0:
            if duel.user_turn == 2:
                if duel.is_ai is False:
                    return choose_trigger(duel, 2, room_number, duel.ask2, decks, graves, hands)
                else:
                    duelobj.init_all(user, other_user, room_number)
                    duelobj.check_eternal_effect( decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
                    answer_ai_choose_trigger(duelobj,duel, 2, room_number, duel.ask2, decks, graves, hands)
                    duelobj.save_all(user, other_user, room_number)
                    return HttpResponse("ai")
            else:
                return wait_choose_trigger(duel, 2, room_number, duel.ask, decks, graves, hands)
        elif duel.ask2 == 6 and duel.ask == 0 and duel.retrieve == 0:
            if duel.user_turn == 1:
                if duel.is_ai is False:
                    return choose_trigger(duel, 2, room_number, duel.ask2, decks, graves, hands)
                else:
                    duelobj.init_all(user, other_user, room_number)
                    duelobj.check_eternal_effect( decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
                    answer_ai_choose_trigger(duelobj,duel, 2, room_number, duel.ask2, decks, graves, hands)
                    duelobj.save_all(user, other_user, room_number)
                    return HttpResponse("ai")
            else:
                return wait_choose_trigger(duel, 2, room_number, duel.ask, decks, graves, hands)
    if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag):
        if duel.user_turn == 1:
            if duel.ask == 1 or duel.ask == 3:
                return show(duel, 1, room_number, duel.ask, decks, graves, hands)
        else:
            if duel.ask == 2 or duel.ask == 3:
                return show(duel, 1, room_number, duel.ask, decks, graves, hands)
    elif duel.user_2 == request.user or (ID2 == ID and duel.guest_flag2):
        if duel.user_turn == 2:
            if duel.ask == 1 or duel.ask == 3:
                return show(duel, 2, room_number, duel.ask, decks, graves, hands)
        else:
            if duel.ask == 2 or duel.ask == 3:
                return show(duel, 2, room_number, duel.ask, decks, graves, hands)
    return HttpResponse("error")


def show(duel, user, room_number, ask, decks, graves, hands):
    ask_fields = []
    ask_whether_0 = []
    ask_under = []
    field_size = FieldSize.objects.get(id=1)
    current_and_or = "and"
    own_player = False
    other_player = False
    other_user_flag = False
    duelobj = DuelObj(room_number)
    duelobj.duel = duel
    duelobj.room_number = room_number
    if user == 1:
        other_user = 2
    elif user == 2:
        other_user = 1
    duelobj.user = user
    duelobj.other_user = other_user
    duelobj.init_all(user, other_user, room_number)
    field = duelobj.field
    duelobj.check_eternal_effect(
        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
    if duel.in_copying is True:
        duelobj.tmp_chain = str(duel.chain - 1)
    else:
        duelobj.tmp_chain = str(duel.chain)
    if int(duelobj.tmp_chain) > 0:
        duelobj.retrieve = 1
    duelobj.check_eternal_effect(
        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
    cost = duelobj.cost
    mess = duelobj.mess
    if duel.in_cost is True:
        if str(duel.chain) in cost:
            cost_chain = cost[str(duel.chain)]
        else:
            cost_chain = []
    else:
        if str(duel.chain - 1) in cost:
            cost_chain = cost[str(duel.chain - 1)]
        else:
            cost_chain = []
    if str(duel.chain - 1) in mess:
        mess = mess[str(duel.chain - 1)]
    else:
        mess = []
    counter = 0
    effect_kind = duel.ask_kind
    if duel.in_cost is True:
        cost_det = duel.cost_det
        effect_user = duel.cost_user
        cost = CostWrapper.objects.get(id=int(cost_det))
        cost_det = cost.cost
        if cost.prompt == "" and cost.sentence == "":
            prompt = cost_det.prompt
            sentence = cost_det.sentence
        else:
            prompt = cost.prompt
            sentence = cost.sentence
        if cost_det.cost != "":
            monster_effect_text_org = json.loads(cost_det.cost)
        if cost_det.cost_val == 28 or cost_det.cost_val == 64:
            return_value = {}
            return_value["chain_variable"] = True
            return_value["min"] = duelobj.calculate_boland(
                monster_effect_text_org["min_equation_number"],None,True
            )
            return_value["max"] = duelobj.calculate_boland(
                monster_effect_text_org["max_equation_number"],None,True
            )
            return_value["prompt"] = duelobj.write_prompt(prompt,user)
            return_value["sentence"] = sentence
            return HttpResponse(json.dumps(return_value))
        if cost_det.cost_val == 26:
            return_value = {}
            return_value["chain_variable"] = True
            return_value["min"] = duelobj.calculate_boland(
                monster_effect_text_org["min_equation_number"]
            )
            return_value["max"] = duelobj.calculate_boland(
                monster_effect_text_org["max_equation_number"]
            )
            return_value["prompt"] = duelobj.write_prompt(prompt,user)
            return_value["sentence"] = sentence
            return HttpResponse(json.dumps(return_value))
        elif cost_det.cost_val == 27 or cost_det.cost_val == 63:
            return_value = {}
            return_value["chain_variable"] = True
            return_value["min"] = duelobj.calculate_boland(
                monster_effect_text_org["min_equation_number"]
            )
            return_value["max"] = duelobj.calculate_boland(
                monster_effect_text_org["max_equation_number"]
            )
            return_value["prompt"] = duelobj.write_prompt(prompt,user)
            return_value["sentence"] = sentence
            return HttpResponse(json.dumps(return_value))
        elif cost_det.cost_val == 3:
            if duel.user_turn == effect_user:
                ask_org = 1
            else:
                ask_org = 2
        elif cost_det.cost_val == 4:
            other_user_flag = True
            if duel.user_turn == effect_user:
                ask_org = 2
            else:
                ask_org = 1
        elif cost_det.cost_val == 16:
            return_value = {}
            return_value["yes_or_no"] = True
            if prompt.find("@"):
                cost = duelobj.cost
                if str(duel.chain ) in cost:
                    cost = cost[str(duel.chain)]
                else:
                    cost = []
                if "~trigger" in cost:
                    monster_name = cost["~trigger"][0]["det"]["monster_name"]
                    prompt = prompt.replace("(@)", monster_name)
            return_value["sentence"] = sentence
            return_value["prompt"] = duelobj.write_prompt(prompt,user)
            return HttpResponse(json.dumps(return_value))
        elif cost_det.cost_val == 48:
            return_value = {}
            return_value["yes_or_no"] = True
            if prompt.find("@"):
                cost = duelobj.cost
                if str(duel.chain ) in cost:
                    cost = cost[str(duel.chain)]
                else:
                    cost = []
                if "~trigger" in cost:
                    monster_name = cost["~trigger"][0]["det"]["monster_name"]
                    prompt = prompt.replace("(@)", monster_name)
            return_value["sentence"] = sentence
            return_value["prompt"] = duelobj.write_prompt(prompt,user)
            return HttpResponse(json.dumps(return_value))
        elif cost_det.cost_val == 26:
            return_value = {}
            return_value["yes_or_no"] = True
            return_value["sentence"] = sentence
            return_value["prompt"] = duelobj.write_prompt(prompt,user)
            return HttpResponse(json.dumps(return_value))
        elif cost_det.cost_val == 5:
            if duelobj.user != effect_user:
                other_user_flag = True
            ask_org = 3
        else:
            ask_org = 0
    elif duel.in_trigger_waiting is True and (duel.force == 0):

        return_value = {}
        return_value["yes_or_no"] = True
        return_value["sentence"] = ""
        return_value["prompt"] = duel.trigger_name
        return HttpResponse(json.dumps(return_value))
    else:
        chain_det = json.loads(duel.chain_det)
        chain_user = json.loads(duel.chain_user)
        effect_user = chain_user[str(duel.chain - 1)]
        monster_effect = MonsterEffectWrapper.objects.get(
            id=int(chain_det[str(duel.chain - 1)])
        )
        monster_effect_det2 = monster_effect.monster_effect
        if monster_effect.prompt != "" or monster_effect.sentence:
            prompt = monster_effect.prompt
            sentence = monster_effect.sentence
        else:
            prompt = monster_effect_det2.prompt
            sentence = monster_effect_det2.sentence
        monster_condition = monster_effect_det2.monster_condition
        if monster_condition != "":
            monster_condition = json.loads(monster_condition)
            monster_condition = monster_condition["monster"][0]["monster"]
        if monster_effect_det2.monster_effect_val == 54:
            return_value = {}
            acc_global = duelobj.acc_global
            acc_val = []
            for tmp in acc_global:
                acc_val_tmp = {}
                acc_val_tmp["monster_name"] = tmp["monster"]["det"]["monster_name"]
                acc_val_tmp["change_val"] = tmp["change_val"]
                acc_val.append(acc_val_tmp)
            return_value["variables"] = acc_val
            return_value["prompt"] = duelobj.write_prompt(prompt,user)
            return HttpResponse(json.dumps(return_value))
        elif monster_effect_det2.monster_effect_val == 76:
            return_value = {}
            chain_det_ary = json.loads(duelobj.duel.chain_det_trigger)
            chain_det = chain_det_ary[str(duelobj.duel.chain - 1)]
            trigger = Trigger.objects.get(id=chain_det)
            return_value["fusion"] = True
            return_value["user"] = user
            return_value["monster"] = duelobj.get_fusion_monster(trigger.fusion_monster, user, trigger,0,1)
            return_value["field_info"] = field
            return HttpResponse(json.dumps(return_value))
        elif monster_effect_det2.monster_effect_val == 77:
            return_value = {}
            chain_det_ary = json.loads(duelobj.duel.chain_det_trigger)
            chain_det = chain_det_ary[str(duelobj.duel.chain - 1)]
            trigger = Trigger.objects.get(id=chain_det)
            return_value["fusion_material"] = True
            return_value["user"] = user
            return_value["monster"] = duelobj.get_fusion_material(monster_effect_det2,user, trigger,1,1)
            return_value["field_info"] = field
            return HttpResponse(json.dumps(return_value))

        elif monster_effect_det2.monster_effect_val == 55:
            return_value = {}
            acc_global = duelobj.acc_global
            acc_val = []
            for tmp in acc_global:
                acc_val_tmp = {}
                acc_val_tmp["monster_name"] = tmp["monster"]["det"]["monster_name"]
                acc_val_tmp["change_val"] = tmp["change_val"]
                acc_val.append(acc_val_tmp)
            return_value["variables"] = acc_val
            return_value["val_order"] = True
            return_value["prompt"] = duelobj.write_prompt(prompt,user)
            return HttpResponse(json.dumps(return_value))
        elif monster_effect_det2.monster_effect_val == 16:
            return_value = {}
            return_value["yes_or_no"] = True
            if prompt.find("@"):
                mess = duelobj.mess
                if str(duel.chain - 1) in mess:
                    mess = mess[str(duel.chain - 1)]
                else:
                    mess = []
                if "trigger" in mess:
                    monster_name = mess["trigger"][0]["det"]["monster_name"]
                    prompt = prompt.replace("(@)", monster_name)

            return_value["prompt"] = duelobj.write_prompt(prompt,user)
            return_value["sentence"] = sentence
            return HttpResponse(json.dumps(return_value))
        elif monster_effect_det2.monster_effect_val == 66:
            return_value = {}
            return_value["multiple_choice"] = True
            if prompt.find("@"):
                mess = duelobj.mess
                if str(duel.chain - 1) in mess:
                    mess = mess[str(duel.chain - 1)]
                else:
                    mess = []
                if "trigger" in mess:
                    monster_name = mess["trigger"][0]["det"]["monster_name"]
                    prompt = prompt.replace("(@)", monster_name)
            return_value["multiple_det"] = json.loads(monster_effect_det2.monster_effect)
            return_value["prompt"] = duelobj.write_prompt(prompt,user)
            return_value["sentence"] = sentence
            return HttpResponse(json.dumps(return_value))
        elif monster_effect_det2.monster_effect_val == 26:
            return_value = {}
            return_value["yes_or_no"] = True
            if prompt.find("@"):
                mess = duelobj.mess
                if str(duel.chain - 1) in mess:
                    mess = mess[str(duel.chain - 1)]
                else:
                    mess = []
                if "trigger" in mess:
                    monster_name = mess["trigger"][0]["det"]["monster_name"]
                    prompt = prompt.replace("(@)", monster_name)
            return_value["sentence"] = sentence
            return_value["prompt"] = duelobj.write_prompt(prompt,user)
            return HttpResponse(json.dumps(return_value))
        elif monster_effect_det2.monster_effect_val == 67:
            return_value = {}
            return_value["multiple_choice"] = True
            if prompt.find("@"):
                mess = duelobj.mess
                if str(duel.chain - 1) in mess:
                    mess = mess[str(duel.chain - 1)]
                else:
                    mess = []
                if "trigger" in mess:
                    monster_name = mess["trigger"][0]["det"]["monster_name"]
                    prompt = prompt.replace("(@)", monster_name)
            return_value["multiple_det"] = json.loads(monster_effect_det2.monster_effect)
            return_value["prompt"] = duelobj.write_prompt(prompt,user)
            return_value["sentence"] = sentence
            return HttpResponse(json.dumps(return_value))
        monster_effect_text_org = json.loads(monster_effect_det2.monster_effect)
        if monster_effect_det2.monster_effect_val == 28 or  monster_effect_det2.monster_effect_val == 64:
            return_value = {}
            return_value["chain_variable"] = True
            return_value["min"] = duelobj.calculate_boland(
                monster_effect_text_org["min_equation_number"],None,True
            )
            return_value["max"] = duelobj.calculate_boland(
                monster_effect_text_org["max_equation_number"],None,True
            )
            return_value["prompt"] = duelobj.write_prompt(prompt,user)
            return_value["sentence"] = sentence
            return HttpResponse(json.dumps(return_value))
        elif monster_effect_det2.monster_effect_val == 27 or monster_effect_det2.monster_effect_val == 63:
            return_value = {}
            return_value["chain_variable"] = True
            return_value["min"] = duelobj.calculate_boland(
                monster_effect_text_org["min_equation_number"]
            )
            return_value["max"] = duelobj.calculate_boland(
                monster_effect_text_org["max_equation_number"]
            )
            return_value["prompt"] = duelobj.write_prompt(prompt,user)
            return_value["sentence"] = sentence
            return HttpResponse(json.dumps(return_value))
        elif (
            monster_effect_det2.monster_effect_val == 30
            or monster_effect_det2.monster_effect_val == 31
        ):
            sentence = sentence
            prompt = prompt
            return show_multiple(
                duelobj,
                user,
                effect_kind,
                monster_effect_text_org,
                monster_condition,
                sentence,
                prompt,
            )
        if monster_effect_det2.monster_effect_val == 57:
            return show_as(
                duelobj,
                user,
                effect_kind,
                monster_effect_text_org,
                monster_condition,
                sentence,
                prompt,
            )
        elif monster_effect_det2.monster_effect_val == 65:
            return show_as_under(
                duelobj,
                user,
                effect_kind,
                monster_effect_text_org,
                monster_condition,
                sentence,
                prompt,
            )
        elif monster_effect_det2.monster_effect_val == 59:
            return show_force(
                duelobj,
                user,
                effect_kind,
                monster_effect_det2.monster_effect,
                sentence,
                prompt
            )
        if (
            monster_effect_det2.monster_effect_val == 3
            or monster_effect_det2.monster_effect_val == 44
        ):
            if duel.user_turn == effect_user:
                ask_org = 1
            else:
                ask_org = 2
        elif monster_effect_det2.monster_effect_val == 4:
            other_user_flag = True
            if duel.user_turn == effect_user:
                ask_org = 2
            else:
                ask_org = 1
        elif monster_effect_det2.monster_effect_val == 5:
            if duelobj.user != effect_user:
                other_user_flag = True
            ask_org = 3
        else:
            ask_org = 0
    tmp_val = {}
    return_val = []
    if "whether_monster" in monster_effect_text_org:
        whether_monster = monster_effect_text_org["whether_monster"]
    else:
        whether_monster = 0
    monster_effect_text = monster_effect_text_org["monster"]
    exclude = monster_effect_text_org["exclude"]
    if "all_flag" in monster_effect_text_org:
        all_flag = monster_effect_text_org["all_flag"]
    else:
        all_flag = False
    for monster_effect_det in monster_effect_text:
        monster_effect_det_monster = monster_effect_det["monster"]
        counter += 1

        if duel.user_turn == user:
            if (counter == 1 and ask_org == 3) or ask_org == 1:
                place_array = []
                place_tmp = monster_effect_det_monster["place"]
                tmp_place_counter = 0
                for place_key in range(len(place_tmp)):
                    place_and_or = place_tmp[place_key]["and_or"]
                    place_det = place_tmp[place_key]["det"]
                    if place_and_or == "":
                        place_and_or = "or"
                    place_array.append([])
                    place_array[tmp_place_counter].append(place_det)
                    if place_and_or == "and":
                        place_key += 1
                        place_and_or = place_tmp[place_key]["and_or"]
                        place_det = place_tmp[place_key]["det"]
                        place_array[tmp_place_counter][1] = place_det
                        if place_and_or == "and":
                            place_key += 1
                            place_and_or = place_tmp[place_key]["and_or"]
                            place_det = place_tmp[place_key]["det"]
                            place_array[tmp_place_counter][2] = place_det
                            if place_and_or == "and":
                                place_key += 1
                                place_and_or = place_tmp[place_key]["and_or"]
                                place_det = place_tmp[place_key]["det"]
                                place_array[tmp_place_counter][3] = place_det
                                if place_and_or == "and":
                                    place_key += 1
                                    place_and_or = place_tmp[place_key]["and_or"]
                                    place_det = place_tmp[place_key]["det"]
                                    place_array[tmp_place_counter][4] = place_det
                    tmp_place_counter += 1
                for place_each in place_array:
                    place_tmp = place_each[0].split("_")
                    if place_tmp[0] == "player" and place_tmp[1] == "1":
                        own_player = True
                    elif place_tmp[0] == "player" and place_tmp[1] == "2":
                        other_player = True
                    elif place_tmp[0] == "deck":
                        deck = Deck.objects.get(id=place_tmp[1])
                        if deck.mine_or_other == 1:
                            return_val.append(
                                return_deck(
                                    duelobj,
                                    duel,
                                    deck.id,
                                    3,
                                    place_tmp[2],
                                    deck.deck_name,
                                    room_number,
                                    exclude,
                                    monster_effect_det,
                                )
                            )
                        else:
                            return_val.append(
                                return_deck(
                                    duelobj,
                                    duel,
                                    deck.id,
                                    user,
                                    place_tmp[2],
                                    deck.deck_name,
                                    room_number,
                                    exclude,
                                    monster_effect_det,
                                )
                            )
                    elif place_tmp[0] == "grave":
                        grave = Grave.objects.get(id=place_tmp[1])
                        if grave.mine_or_other == 1:
                            return_val.append(
                                return_grave(
                                    duelobj,
                                    duel,
                                    grave.id,
                                    3,
                                    place_tmp[2],
                                    grave.grave_name,
                                    room_number,
                                    exclude,
                                    monster_effect_det,
                                )
                            )
                        else:
                            return_val.append(
                                return_grave(
                                    duelobj,
                                    duel,
                                    grave.id,
                                    user,
                                    place_tmp[2],
                                    grave.grave_name,
                                    room_number,
                                    exclude,
                                    monster_effect_det,
                                )
                            )
                    elif place_tmp[0] == "hand":
                        hand = Hand.objects.get(id=place_tmp[1])
                        if hand.mine_or_other == 1:
                            return_val.append(
                                return_hand(
                                    duelobj,
                                    duel,
                                    hand.id,
                                    3,
                                    place_tmp[2],
                                    hand.hand_name,
                                    room_number,
                                    exclude,
                                    monster_effect_det,
                                )
                            )
                        else:
                            return_val.append(
                                return_hand(
                                    duelobj,
                                    duel,
                                    hand.id,
                                    user,
                                    place_tmp[2],
                                    hand.hand_name,
                                    room_number,
                                    exclude,
                                    monster_effect_det,
                                )
                            )
                    elif place_tmp[0] == "field":
                        current_and_or = "or"
                        if duelobj.field_free is True:
                            field_x = 20
                        else:
                            field_x = field_size.field_x
                        for x in range(field_x):
                            for y in range(field_size.field_y):
                                if whether_monster == 0 and field[x][y]["det"] is None:
                                    flag_field_place = False
                                    if duelobj.field_free is False:
                                        kind = field[x][y]["kind"]
                                    else:
                                        kind = field[0][y]["kind"]
                                    if kind != "":
                                        tmp = kind.split("_")
                                    else:
                                        tmp = []
                                    if current_and_or == "and":
                                        if place_tmp[1] in tmp:
                                            if flag_field_place is True:
                                                flag_field_place = True
                                        else:
                                            flag_field_place = False
                                    elif current_and_or == "or":
                                        if place_tmp[1] in tmp:
                                            flag_field_place = True
                                        else:
                                            if flag_field_place is False:
                                                flag_field_place = False
                                    mine_or_other = int(place_tmp[2])
                                    if (
                                            (mine_or_other == 1
                                            and user == 1)
                                            or (mine_or_other == 2
                                            and user == 2)
                                    ):
                                        mine_or_other = 1
                                    elif (
                                            (mine_or_other == 1
                                            and user == 2)
                                            or (mine_or_other == 2
                                            and user == 1)
                                    ):
                                        mine_or_other = 2
                                    else:
                                        mine_or_other = 3

                                    if flag_field_place is False:
                                        continue
                                    if field[x][y]["mine_or_other"] != mine_or_other:
                                        continue
                                    tmp = str(x)+"_"+str(y)
                                    ask_whether_0.append(tmp)
                                if field[x][y]["det"] is not None and user != field[x][y]["mine_or_other"] and int(duelobj.check_change_val(
                                        field[x][y]["det"],
                                        field[x][y]["mine_or_other"],
                                        "field",
                                        0,
                                        x,
                                        y,
                                        "show",
                                        field[x][y]["mine_or_other"],
                                        int(field[x][y]["det"]["variables"]["show"]["value"])
                                )) == 1:
                                    field[x][y]["det"] = None
                                    if duelobj.config.sort is True:
                                        field = self.sortField(field,y)
                                    field[x][y]["hide"] = True
                                flag_field_place = False
                                if duelobj.field_free is False:
                                    kind = field[x][y]["kind"]
                                else:
                                    kind = field[0][y]["kind"]
                                if kind != "":
                                    tmp = kind.split("_")
                                else:
                                    tmp = []
                                if current_and_or == "and":
                                    if place_tmp[1] in tmp:
                                        if flag_field_place is True:
                                            flag_field_place = True
                                    else:
                                        flag_field_place = False
                                elif current_and_or == "or":
                                    if place_tmp[1] in tmp:
                                        flag_field_place = True
                                    else:
                                        if flag_field_place is False:
                                            flag_field_place = False
                                mine_or_other = int(place_tmp[2])
                                if (
                                        mine_or_other == 1
                                        and user == 1
                                        or mine_or_other == 2
                                        and user == 2
                                ):
                                    mine_or_other = 1
                                elif (
                                        mine_or_other == 1
                                        and user == 2
                                        or mine_or_other == 2
                                        and user == 1
                                ):
                                    mine_or_other = 2
                                else:
                                    mine_or_other = 3

                                if flag_field_place is False:
                                    continue
                                if field[x][y]["mine_or_other"] != mine_or_other:
                                    continue
                                if field[x][y]["det"] is not None:
                                    if duelobj.check_no_choose(
                                            field[x][y]["det"],
                                            user,
                                            effect_kind,
                                            "field",
                                            0,
                                            x,
                                            y,
                                            field[x][y]["mine_or_other"],
                                    ):
                                        continue
                                    tmp2 = {}
                                    tmp2["det"] = field[x][y]["det"]
                                    tmp2["mine_or_other"] = field[x][y]["mine_or_other"]
                                    tmp2["user"] = user
                                    tmp2["place"] = "field"
                                    tmp2["deck_id"] = 0
                                    tmp2["x"] = x
                                    tmp2["y"] = y
                                    tmp3  = field[x][y]["det"]["place_unique_id"]
                                    tmp2["place_unique_id"] = field[x][y]["det"][
                                        "place_unique_id"
                                    ]
                                    if not duelobj.check_monster_condition_det(
                                        monster_effect_det, field[x][y]["det"], user, effect_kind, 1, "field", 0,x, y
                                    ):
                                        continue
                                    ask_fields.append(tmp3)
                    elif place_tmp[0] == "under":
                        current_and_or = "or"
                        if duelobj.field_free is True:
                            field_x = 20
                        else:
                            field_x = field_size.field_x
                        for x in range(field_x):
                            for y in range(field_size.field_y):
                                if field[x][y]["det"] is not None and user != field[x][y]["mine_or_other"] and int(duelobj.check_change_val(
                                        field[x][y]["det"],
                                        field[x][y]["mine_or_other"],
                                        "field",
                                        0,
                                        x,
                                        y,
                                        "show",
                                        field[x][y]["mine_or_other"],
                                        int(field[x][y]["det"]["variables"]["show"]["value"])
                                )) == 1:
                                    field[x][y]["det"] = None
                                    if duelobj.config.sort is True:
                                        field = self.sortField(field,y)
                                    field[x][y]["hide"] = True
                                flag_field_place = False
                                if duelobj.field_free is False:
                                    kind = field[x][y]["kind"]
                                else:
                                    kind = field[0][y]["kind"]
                                if kind != "":
                                    tmp = kind.split("_")
                                else:
                                    tmp = []
                                if current_and_or == "and":
                                    if place_tmp[1] in tmp:
                                        if flag_field_place is True:
                                            flag_field_place = True
                                    else:
                                        flag_field_place = False
                                elif current_and_or == "or":
                                    if place_tmp[1] in tmp:
                                        flag_field_place = True
                                    else:
                                        if flag_field_place is False:
                                            flag_field_place = False
                                mine_or_other = int(place_tmp[2])
                                if (
                                        mine_or_other == 1
                                        and user == 1
                                        or mine_or_other == 2
                                        and user == 2
                                ):
                                    mine_or_other = 1
                                elif (
                                        mine_or_other == 1
                                        and user == 2
                                        or mine_or_other == 2
                                        and user == 1
                                ):
                                    mine_or_other = 2
                                else:
                                    mine_or_other = 3

                                if flag_field_place is False:
                                    continue
                                if field[x][y]["mine_or_other"] != mine_or_other:
                                    continue
                                if field[x][y]["det"] is not None:
                                    if duelobj.check_not_effected(
                                            field[x][y]["det"],
                                            user,
                                            effect_kind,
                                            "field",
                                            0,
                                            x,
                                            y,
                                            field[x][y]["mine_or_other"],
                                    ):
                                        continue
                                    if not duelobj.check_monster_condition_det(
                                           monster_effect_det, field[x][y]["det"], user, effect_kind, 1, "field", x, y, 0
                                    ):
                                       continue
                                    if "under" not in field[x][y]["det"]:
                                        continue
                                    for under in field[x][y]["det"]["under"]:
                                        tmp2 = {}
                                        tmp2["det"] = under
                                        tmp2["mine_or_other"] = field[x][y]["mine_or_other"]
                                        tmp2["user"] = user
                                        tmp2["place"] = "under"
                                        tmp2["deck_id"] = 0
                                        tmp2["x"] = x
                                        tmp2["y"] = y
                                        tmp3  = under["place_unique_id"]
                                        tmp2["place_unique_id"] = under[
                                            "place_unique_id"
                                        ]
                                        ask_under.append(tmp3)
            break
        else:
            if (counter == 2 and ask_org == 3) or ask_org == 2:
                place_array = []
                place_tmp = monster_effect_det_monster["place"]
                tmp_place_counter = 0
                for place_key in range(len(place_tmp)):
                    place_and_or = place_tmp[place_key]["and_or"]
                    place_det = place_tmp[place_key]["det"]
                    if place_and_or == "":
                        place_and_or = "or"
                    place_array.append([])
                    place_array[tmp_place_counter].append(place_det)
                    if place_and_or == "and":
                        place_key += 1
                        place_and_or = place_tmp[place_key]["and_or"]
                        place_det = place_tmp[place_key]["det"]
                        place_array[tmp_place_counter][1] = place_det
                        if place_and_or == "and":
                            place_key += 1
                            place_and_or = place_tmp[place_key]["and_or"]
                            place_det = place_tmp[place_key]["det"]
                            place_array[tmp_place_counter][2] = place_det
                            if place_and_or == "and":
                                place_key += 1
                                place_and_or = place_tmp[place_key]["and_or"]
                                place_det = place_tmp[place_key]["det"]
                                place_array[tmp_place_counter][3] = place_det
                                if place_and_or == "and":
                                    place_key += 1
                                    place_and_or = place_tmp[place_key]["and_or"]
                                    place_det = place_tmp[place_key]["det"]
                                    place_array[tmp_place_counter][4] = place_det
                    tmp_place_counter += 1
                for place_each in place_array:
                    place_tmp = place_each[0].split("_")
                    if place_tmp[0] == "deck":
                        deck = Deck.objects.get(id=place_tmp[1])
                        if deck.mine_or_other == 1:
                            return_val.append(
                                return_deck(
                                    duelobj,
                                    duel,
                                    deck.id,
                                    3,
                                    place_tmp[2],
                                    deck.deck_name,
                                    room_number,
                                    exclude,
                                    monster_effect_det,
                                )
                            )
                        else:
                            return_val.append(
                                return_deck(
                                    duelobj,
                                    duel,
                                    deck.id,
                                    user,
                                    place_tmp[2],
                                    deck.deck_name,
                                    room_number,
                                    exclude,
                                    monster_effect_det,
                                )
                            )
                    elif place_tmp[0] == "grave":
                        grave = Grave.objects.get(id=place_tmp[1])
                        if grave.mine_or_other == 1:
                            return_val.append(
                                return_grave(
                                    duelobj,
                                    duel,
                                    grave.id,
                                    3,
                                    place_tmp[2],
                                    grave.grave_name,
                                    room_number,
                                    exclude,
                                    monster_effect_det,
                                )
                            )
                        else:
                            return_val.append(
                                return_grave(
                                    duelobj,
                                    duel,
                                    grave.id,
                                    user,
                                    place_tmp[2],
                                    grave.grave_name,
                                    room_number,
                                    exclude,
                                    monster_effect_det,
                                )
                            )
                    elif place_tmp[0] == "hand":
                        hand = Hand.objects.get(id=place_tmp[1])
                        if hand.mine_or_other == 1:
                            return_val.append(
                                return_hand(
                                    duelobj,
                                    duel,
                                    hand.id,
                                    3,
                                    place_tmp[2],
                                    hand.hand_name,
                                    room_number,
                                    exclude,
                                    monster_effect_det,
                                )
                            )
                        else:
                            return_val.append(
                                return_hand(
                                    duelobj,
                                    duel,
                                    hand.id,
                                    user,
                                    place_tmp[2],
                                    hand.hand_name,
                                    room_number,
                                    exclude,
                                    monster_effect_det,
                                )
                            )
                    elif place_tmp[0] == "field":
                        current_and_or = "or"
                        if duelobj.field_free is True:
                            field_x = 20
                        else:
                            field_x = field_size.field_x
                        for x in range(field_x):
                            for y in range(field_size.field_y):
                                if whether_monster == 0 and field[x][y]["det"] is None:
                                    flag_field_place = False
                                    if duelobj.field_free is False:
                                        kind = field[x][y]["kind"]
                                    else:
                                        kind = field[0][y]["kind"]
                                    if kind != "":
                                        tmp = kind.split("_")
                                    else:
                                        tmp = []
                                    if current_and_or == "and":
                                        if place_tmp[1] in tmp:
                                            if flag_field_place is True:
                                                flag_field_place = True
                                        else:
                                            flag_field_place = False
                                    elif current_and_or == "or":
                                        if place_tmp[1] in tmp:
                                            flag_field_place = True
                                        else:
                                            if flag_field_place is False:
                                                flag_field_place = False
                                    mine_or_other = int(place_tmp[2])
                                    if (
                                            (mine_or_other == 1
                                            and user == 1)
                                            or (mine_or_other == 2
                                            and user == 2)
                                    ):
                                        mine_or_other = 1
                                    elif (
                                            (mine_or_other == 1
                                            and user == 2)
                                            or (mine_or_other == 2
                                            and user == 1)
                                    ):
                                        mine_or_other = 2
                                    else:
                                        mine_or_other = 3

                                    if flag_field_place is False:
                                        continue
                                    if field[x][y]["mine_or_other"] != mine_or_other:
                                        continue
                                    tmp = str(x)+"_"+str(y)
                                    ask_whether_0.append(tmp)
                                if  field[x][y]["det"] is not None and user != field[x][y]["mine_or_other"] and int(duelobj.check_change_val(
                                        field[x][y]["det"],
                                        field[x][y]["mine_or_other"],
                                        "field",
                                        0,
                                        x,
                                        y,
                                        "show",
                                        field[x][y]["mine_or_other"],
                                        int(field[x][y]["det"]["variables"]["show"]["value"])
                                )) == 1:
                                    field[x][y]["det"] = None
                                    if duelobj.config.sort is True:
                                        field = self.sortField(field,y)
                                    field[x][y]["hide"] = True
                                flag_field_place = False
                                if duelobj.field_free is False:
                                    kind = field[x][y]["kind"]
                                else:
                                    kind = field[0][y]["kind"]
                                if kind != "":
                                    tmp = kind.split("_")
                                else:
                                    tmp = []
                                if current_and_or == "and":
                                    if place_tmp[1] in tmp:
                                        if flag_field_place is True:
                                            flag_field_place = True
                                    else:
                                        flag_field_place = False
                                elif current_and_or == "or":
                                    if place_tmp[1] in tmp:
                                        flag_field_place = True
                                    else:
                                        if flag_field_place is False:
                                            flag_field_place = False
                                mine_or_other = int(place_tmp[2])
                                if (
                                        mine_or_other == 1
                                        and user == 1
                                        or mine_or_other == 2
                                        and user == 2
                                ):
                                    mine_or_other = 1
                                elif (
                                        mine_or_other == 1
                                        and user == 2
                                        or mine_or_other == 2
                                        and user == 1
                                ):
                                    mine_or_other = 2
                                else:
                                    mine_or_other = 3

                                if flag_field_place is False:
                                    continue
                                if field[x][y]["mine_or_other"] != mine_or_other:
                                    continue
                                if field[x][y]["det"] is not None:
                                    if duelobj.check_not_effected(
                                            field[x][y]["det"],
                                            user,
                                            effect_kind,
                                            "field",
                                            0,
                                            x,
                                            y,
                                            field[x][y]["mine_or_other"],
                                    ):
                                        continue
                                    tmp2 = {}
                                    tmp2["det"] = field[x][y]["det"]
                                    tmp2["mine_or_other"] = field[x][y]["mine_or_other"]
                                    tmp2["user"] = user
                                    tmp2["place"] = "field"
                                    tmp2["deck_id"] = 0
                                    tmp2["x"] = x
                                    tmp2["y"] = y
                                    tmp3  = field[x][y]["det"]["place_unique_id"]
                                    tmp2["place_unique_id"] = field[x][y]["det"][
                                        "place_unique_id"
                                    ]
                                    if not duelobj.check_monster_condition_det(
                                            monster_effect_det, field[x][y]["det"], user, effect_kind, 1, "field", x, y, 0
                                    ):
                                        continue
                                    ask_fields.append(tmp3)
                    elif place_tmp[0] == "under":
                        current_and_or = "or"
                        if duelobj.field_free is True:
                            field_x = 20
                        else:
                            field_x = field_size.field_x
                        for x in range(field_x):
                            for y in range(field_size.field_y):
                                flag_field_place = False
                                if duelobj.field_free is False:
                                    kind = field[x][y]["kind"]
                                else:
                                    kind = field[0][y]["kind"]
                                if kind != "":
                                    tmp = kind.split("_")
                                else:
                                    tmp = []
                                if current_and_or == "and":
                                    if place_tmp[1] in tmp:
                                        if flag_field_place is True:
                                            flag_field_place = True
                                    else:
                                        flag_field_place = False
                                elif current_and_or == "or":
                                    if place_tmp[1] in tmp:
                                        flag_field_place = True
                                    else:
                                        if flag_field_place is False:
                                            flag_field_place = False
                                mine_or_other = int(place_tmp[2])
                                if (
                                        mine_or_other == 1
                                        and user == 1
                                        or mine_or_other == 2
                                        and user == 2
                                ):
                                    mine_or_other = 1
                                elif (
                                        mine_or_other == 1
                                        and user == 2
                                        or mine_or_other == 2
                                        and user == 1
                                ):
                                    mine_or_other = 2
                                else:
                                    mine_or_other = 3

                                if flag_field_place is False:
                                    continue
                                if field[x][y]["mine_or_other"] != mine_or_other:
                                    continue
                                if field[x][y]["det"] is not None:
                                    if duelobj.check_not_effected(
                                            field[x][y]["det"],
                                            user,
                                            effect_kind,
                                            "field",
                                            0,
                                            x,
                                            y,
                                            field[x][y]["mine_or_other"],
                                    ):
                                        continue
                                    if not duelobj.check_monster_condition_det(
                                            monster_effect_det, field[x][y]["det"], user, effect_kind, 1, "field", x, y, 0
                                    ):
                                        continue
                                    if "under" not in field[x][y]["det"]:
                                        continue
                                    for under in field[x][y]["det"]["under"]:
                                        tmp2 = {}
                                        tmp2["det"] = under
                                        tmp2["mine_or_other"] = field[x][y]["mine_or_other"]
                                        tmp2["user"] = user
                                        tmp2["place"] = "under"
                                        tmp2["deck_id"] = 0
                                        tmp2["x"] = x
                                        tmp2["y"] = y
                                        tmp3  = under["place_unique_id"]
                                        tmp2["place_unique_id"] = under[
                                            "place_unique_id"
                                        ]
                                        ask_under.append(tmp3)
    if ask_fields:
        tmp_val["ask_field"] = ask_fields
        tmp_val["field_info"] = field
    if ask_whether_0:
        tmp_val["ask_whether_0"] = ask_whether_0
        tmp_val["field_info"] = field
    if ask_under:
        tmp_val["ask_under"] = under
        tmp_val["field_info"] = field
    tmp_val["return_val"] = return_val
    tmp_val["equation"] = monster_effect_det["equation"]["equation"]
    tmp_val["equation_kind"] = monster_effect_det["equation"]["equation_kind"]
    # tmp_val["equation_number"] = monster_effect_det["equation"]["equation_number"]
    tmp_val["min_equation_number"] = duelobj.calculate_boland(
        monster_effect_det["min_equation_number"], None, other_user_flag
    )
    tmp_val["max_equation_number"] = duelobj.calculate_boland(
        monster_effect_det["max_equation_number"], None, other_user_flag
    )
    if monster_effect_det["equation"]["equation_kind"] == "number":
        tmp_val["kind_flag"] = False
    else:
        tmp_val["kind_flag"] = True
        
    tmp_val["whether_monster"] = whether_monster
    tmp_val["sentence"] = sentence
    tmp_val["prompt"] = duelobj.write_prompt(prompt,user)
    tmp_val["monster_name_kind"] = monster_effect_det_monster["monster_name_kind"]
    if "flag" in monster_effect_det_monster:
        tmp_val["flag"] = monster_effect_det_monster["flag"]
    if "monster_condition" in monster_effect_det_monster:
        tmp_val["variables"] = monster_effect_det_monster["monster_condition"]
    val_exclude = []
    timing_mess = duel.timing_mess
    if exclude != "":
        excludes = exclude.split(",")
        for exclude_det in excludes:

            if exclude_det[0] == "%":
                if exclude_det in timing_mess:
                    for timing_det in timing_mess[exclude_det]:
                        val_exclude.append(timing_det["place_unique_id"])
            if exclude_det[0] == "~":
                if exclude_det in cost_chain:
                    for cost_det in cost_chain[exclude_det]:
                        val_exclude.append(cost_det["place_unique_id"])
            if exclude_det in mess:
                for mess_det in mess[exclude_det]:
                    val_exclude.append(mess_det["place_unique_id"])
    tmp_val["exclude"] = val_exclude
    tmp_val["player"] = own_player
    tmp_val["other_player"] = other_player
    tmp_val["user"] = duelobj.user
    tmp_val["all_flag"] = all_flag
    if "from_left" not in monster_effect_text_org or monster_effect_text_org["from_left"] is False:
        tmp_val["from_left"] = False
    else:
        tmp_val["from_left"] = True
    return HttpResponse(json.dumps(tmp_val))


def return_deck(
    duelobj,
    duel,
    deck_id,
    user,
    mine_or_other,
    deck_name,
    room_number,
    exclude="",
    monster_effect_det=None,
):
    mine_or_other = int(mine_or_other)
    html = {}
    html["deck_id"] = deck_id
    html["mine_or_other_val"] = mine_or_other
    cost = duelobj.cost
    mess = duelobj.mess
    effect_kind = duel.ask_kind
    if duel.in_cost is True:
        if str(duel.chain) in cost:
            cost_chain = cost[str(duel.chain)]
        else:
            cost_chain = []
    else:
        if str(duel.chain - 1) in cost:
            cost_chain = cost[str(duel.chain - 1)]
        else:
            cost_chain = []
    if str(duel.chain - 1) in mess:
        mess = mess[str(duel.chain - 1)]
    else:
        mess = []
    if mine_or_other == 1:
        html["mine_or_other"] = "自分の" + deck_name
    elif mine_or_other == 2:
        html["mine_or_other"] = "相手の" + deck_name
        if user == 1:
            user = 2
        elif user == 2:
            user = 1
    else:
        html["mine_or_other"] = "共通の" + deck_name
    if mine_or_other == 1:
        tmp = duelobj.decks[deck_id]["mydeck"]
    elif mine_or_other == 2:
        tmp = duelobj.decks[deck_id]["otherdeck"]
    elif mine_or_other == 3 or mine_or_other == 0:
        tmp = duelobj.decks[deck_id]["commondeck"]
    user_decks = tmp
    html["cards"] = []
    for user_deck in user_decks:
        flag = True
        if exclude != "":
            excludes = exclude.split(",")
            for exclude_det in excludes:

                if exclude_det in cost_chain:
                    for cost_det in cost_chain[exclude_det]:
                        if user_deck["place_unique_id"] == cost_det["place_unique_id"]:
                            flag = False
                            continue
                if exclude_det in mess:
                    for mess_det in mess[exclude_det]:
                        if user_deck["place_unique_id"] == mess_det["place_unique_id"]:
                            flag = False
                            continue
        if not duelobj.check_monster_condition_det(
            monster_effect_det, user_deck, user, effect_kind, 1, "deck", deck_id, 0, 0
        ):
            flag = False
        if flag is True:
            tmp = user_deck
            html["cards"].append(tmp)
    return html


def return_grave(
    duelobj,
    duel,
    grave_id,
    user,
    mine_or_other,
    grave_name,
    room_number,
    exclude="",
    monster_effect_det=None,
):
    mine_or_other = int(mine_or_other)
    cost = json.loads(duel.cost)
    mess = json.loads(duel.mess)
    effect_kind = duel.ask_kind
    html = {}
    html["grave_id"] = grave_id
    html["mine_or_other_val"] = mine_or_other
    if mine_or_other == 1:
        html["mine_or_other"] = "自分の" + grave_name
    elif mine_or_other == 2:
        html["mine_or_other"] = "相手の" + grave_name
        if user == 1:
            user = 2
        elif user == 2:
            user = 1
    else:
        html["mine_or_other"] = "共通の" + grave_name
    if user == 1:
        tmp = DuelGrave.objects.get(
            room_number=room_number, mine_or_other=1, grave_id=grave_id
        )
    elif user == 2:
        tmp = DuelGrave.objects.get(
            room_number=room_number, mine_or_other=2, grave_id=grave_id
        )
    elif user == 3:
        tmp = DuelGrave.objects.get(
            room_number=room_number, mine_or_other=3, grave_id=grave_id
        )
    user_graves = json.loads(tmp.grave_content)
    html["grave"] = []
    for user_grave in user_graves:
        flag = True
        if exclude != "":
            excludes = exclude.split(",")
            for exclude_det in excludes:

                if exclude_det in cost:
                    for cost_det in cost[exclude_det]:
                        if user_grave["place_unique_id"] == cost_det["place_unique_id"]:
                            flag = False
                            continue
                if exclude_det in mess:
                    for mess_det in mess[exclude_det]:
                        if user_grave["place_unique_id"] == mess_det["place_unique_id"]:
                            flag = False
                            continue
        if (
            duelobj.check_monster_condition_det(
                monster_effect_det,
                user_grave,
                user,
                effect_kind,
                1,
                "grave",
                grave_id,
                0,
                0,
            )
            is False
        ):
            flag = False
        if flag is True:
            tmp = user_grave
            html["grave"].append(tmp)
    return html


def return_hand(
    duelobj,
    duel,
    hand_id,
    user,
    mine_or_other,
    hand_name,
    room_number,
    exclude="",
    monster_effect_det=None,
):
    mine_or_other = int(mine_or_other)
    html = {}
    html["hand_id"] = hand_id
    html["mine_or_other_val"] = mine_or_other
    cost = json.loads(duel.cost)
    mess = json.loads(duel.mess)
    timing_mess = json.loads(duel.timing_mess)
    effect_kind = duel.ask_kind
    if mine_or_other == 1:
        html["mine_or_other"] = "自分の" + hand_name
    elif mine_or_other == 2:
        html["mine_or_other"] = "相手の" + hand_name
        if user == 1:
            user = 2
        elif user == 2:
            user = 1
    else:
        html["mine_or_other"] = "共通の" + hand_name
    if user == 1:
        tmp = DuelHand.objects.get(
            room_number=room_number, mine_or_other=1, hand_id=hand_id
        )
    elif user == 2:
        tmp = DuelHand.objects.get(
            room_number=room_number, mine_or_other=2, hand_id=hand_id
        )
    elif user == 3:
        tmp = DuelHand.objects.get(
            room_number=room_number, mine_or_other=3, hand_id=hand_id
        )
    user_hands = json.loads(tmp.hand_content)
    html["hand"] = []
    for user_hand in user_hands:
        flag = True
        if exclude != "":
            excludes = exclude.split(",")
            for exclude_det in excludes:

                if exclude_det[0] == "~":
                    if exclude_det in cost:
                        for cost_det in cost[exclude_det]:
                            if (
                                user_hand["place_unique_id"]
                                == cost_det["place_unique_id"]
                            ):
                                flag = False
                                continue
                elif exclude_det[0] == "%":
                    if exclude_det in timing_mess:
                        for timing_det in timing_mess[exclude_det]:
                            if (
                                user_hand["place_unique_id"]
                                == timing_det["place_unique_id"]
                            ):
                                flag = False
                                continue
                elif exclude_det in mess:
                    for mess_det in mess[exclude_det]:
                        if user_hand["place_unique_id"] == mess_det["place_unique_id"]:
                            flag = False
                            continue
        if (
            duelobj.check_monster_condition_det(
                monster_effect_det,
                user_hand,
                user,
                effect_kind,
                1,
                "hand",
                hand_id,
                0,
                0,
            )
            is False
        ):
            flag = False
        if flag is True:
            tmp = user_hand
            html["hand"].append(tmp)
    return html


def show_force(
        duelobj, user, effect_kind, monster_effect,sentence, prompt
):
    det = json.loads(monster_effect)
    deck_id = det["deck_id"]
    ignore_timing = det["ignore_timing"]
    if user == 1:
        other_user = 2
    else:
        other_user = 1
    mine_or_other = other_user
    duel = duelobj.duel
    return_value = []
    hand = duelobj.hands[deck_id]["otherhand"]
    user_hands = hand
    i=0
    for user_hand in user_hands:
        id = duelobj.get_monster_id(
            user_hand, "hand", other_user,i, 0, 0, mine_or_other
        )
        monster_det = Monster.objects.get(id=id)
        triggers = monster_det.trigger.all()
        triggers = triggers.filter(trigger_timing=False)
        phase = duel.phase
        turn = duel.user_turn
        place_unique_id = user_hand["place_unique_id"]
        tmp2 = {}
        tmp2["det"] = user_hand
        tmp2["mine_or_other"] = mine_or_other
        tmp2["user"] = user
        tmp2["place"] = "hand"
        tmp2["deck_id"] = deck_id
        tmp2["x"] = 0
        tmp2["y"] = 0
        tmp2["place_unique_id"] = user_hand["place_unique_id"]
        tmp2["able"] = 0
        if user_hand["flag"]== 0:
            for trigger in triggers:
                if duelobj.check_launch_trigger_ignore_chain_and_timing(
                        trigger,
                        phase,
                        turn,
                        other_user,
                        user,
                        mine_or_other,
                        "hand",
                        place_unique_id,
                        deck_id,
                        ignore_timing
                ):
                    tmp2["able"] = 1
        return_value.append(tmp2)
    tmp_val = {}
    tmp_val["return_val"] = return_value
    tmp_val["force_effect"] = 1
    tmp_val["user"] = duelobj.user
    tmp_val["sentence"] = sentence
    tmp_val["prompt"] = duelobj.write_prompt(prompt,user)
    return HttpResponse(json.dumps(tmp_val))

def show_as(
    duelobj, user, effect_kind, monster_effect_text, monster_condition, sentence, prompt
):
    ask_fields = []
    ask_under = []
    duel = duelobj.duel
    field = duelobj.field
    return_value = []
    for monster_effect_det in monster_effect_text["monster"]:
        if (
            "as_monster_condition" in monster_effect_det
            and monster_effect_det["as_monster_condition"] != ""
        ):
            as_monsters = monster_effect_det["as_monster_condition"]
            if not isinstance(as_monsters, list):
                tmp_monster = []
                tmp_monster.append(as_monsters)
                as_monsters = tmp_monster
            for as_monster in as_monsters:
                if as_monster[0] == "~":
                    tmp = duelobj.cost
                    tmp = tmp[str(int(duel.chain))]
                    if as_monster not in tmp:
                        continue
                    place1 = tmp[as_monster]
                elif as_monster[0] == "%":
                    tmp = duelobj.timing_mess
                    if as_monster not in tmp:
                        continue
                    place1 = tmp[as_monster]
                else:
                    tmp = duelobj.mess
                    tmp = tmp[str(int(duel.chain - 1))]
                    if as_monster not in tmp:
                        continue
                    place1 = tmp[as_monster]
                for place2 in place1:
                    if monster_condition != "":
                        if not duelobj.validate_answer(
                            place2, monster_condition, "", duel
                        ):
                            continue
                    if place2["place"] == "field":
                        x = place2["x"]
                        y = place2["y"]
                        if duelobj.check_not_effected(
                                field[x][y]["det"],
                                user,
                                effect_kind,
                                "field",
                                0,
                                x,
                                y,
                                field[x][y]["mine_or_other"],
                        ):
                            continue
                        tmp2 = {}
                        tmp2["det"] = field[x][y]["det"]
                        tmp2["mine_or_other"] = field[x][y]["mine_or_other"]
                        tmp2["user"] = user
                        tmp2["place"] = "field"
                        tmp2["deck_id"] = 0
                        tmp2["x"] = x
                        tmp2["y"] = y
                        tmp3  = field[x][y]["det"]["place_unique_id"]
                        tmp2["place_unique_id"] = field[x][y]["det"][
                            "place_unique_id"
                        ]
                        if not duelobj.check_monster_condition_det(
                                monster_effect_det, field[x][y]["det"], user, effect_kind, 1, "field", x, y, 0
                        ):
                            continue
                        ask_fields.append(tmp3)
                    if place2["place"] == "under":
                        x = place2["x"]
                        y = place2["y"]
                        if duelobj.check_not_effected(
                                field[x][y]["det"],
                                user,
                                effect_kind,
                                "field",
                                0,
                                x,
                                y,
                                field[x][y]["mine_or_other"],
                        ):
                            continue
                        if not duelobj.check_monster_condition_det(
                                monster_effect_det, field[x][y]["det"], user, effect_kind, 1, "field", x, y, 0
                        ):
                            continue
                        if "under" not in field[x][y]["det"]:
                            continue
                        for under in field[x][y]["det"]["under"]:
                            tmp2 = {}
                            tmp2["det"] = under
                            tmp2["mine_or_other"] = field[x][y]["mine_or_other"]
                            tmp2["user"] = user
                            tmp2["place"] = "under"
                            tmp2["deck_id"] = 0
                            tmp2["x"] = x
                            tmp2["y"] = y
                            tmp3  = under["place_unique_id"]
                            tmp2["place_unique_id"] = under[
                                "place_unique_id"
                            ]
                            ask_under.append(tmp3)
    tmp_val = {}
    if ask_fields:
        tmp_val["ask_field"] = ask_fields
        tmp_val["field_info"] = field
    if ask_under:
        tmp_val["ask_under"] = ask_under
        tmp_val["field_info"] = field
    tmp_val["return_val"] = return_value
    tmp_val["min_equation_number"] = duelobj.calculate_boland(
        monster_effect_det["min_equation_number"]
    )
    tmp_val["max_equation_number"] = duelobj.calculate_boland(
        monster_effect_det["max_equation_number"]
    )
    tmp_val["user"] = duelobj.user
    tmp_val["whether_monster"] = 1
    tmp_val["exclude"] = []
    tmp_val["sentence"] = sentence
    tmp_val["prompt"] = duelobj.write_prompt(prompt,user)
    return HttpResponse(json.dumps(tmp_val))


def show_as_under(
        duelobj, user, effect_kind, monster_effect_text, monster_condition, sentence, prompt
):
    ask_under = []
    duel = duelobj.duel
    field = duelobj.field
    return_value = []
    for monster_effect_det in monster_effect_text["monster"]:
        if (
                "as_monster_condition" in monster_effect_det
                and monster_effect_det["as_monster_condition"] != ""
        ):
            as_monsters = monster_effect_det["as_monster_condition"]
            if not isinstance(as_monsters, list):
                tmp_monster = []
                tmp_monster.append(as_monsters)
                as_monsters = tmp_monster
            for as_monster in as_monsters:
                if as_monster[0] == "~":
                    tmp = duelobj.cost
                    tmp = tmp[str(int(duel.chain))]
                    if as_monster not in tmp:
                        continue
                    place1 = tmp[as_monster]
                elif as_monster[0] == "%":
                    tmp = duelobj.timing_mess
                    if as_monster not in tmp:
                        continue
                    place1 = tmp[as_monster]
                else:
                    tmp = duelobj.mess
                    tmp = tmp[str(int(duel.chain - 1))]
                    if as_monster not in tmp:
                        continue
                    place1 = tmp[as_monster]
                for place2 in place1:
                    if monster_condition != "":
                        if not duelobj.validate_answer(
                                place2, monster_condition, "", duel
                        ):
                            continue
                    if place2["place"] == "field":
                        x = place2["x"]
                        y = place2["y"]
                        if duelobj.check_not_effected(
                                field[x][y]["det"],
                                user,
                                effect_kind,
                                "field",
                                0,
                                x,
                                y,
                                field[x][y]["mine_or_other"],
                        ):
                            continue
                        tmp2 = {}
                        tmp2["det"] = field[x][y]["det"]
                        tmp2["mine_or_other"] = field[x][y]["mine_or_other"]
                        tmp2["user"] = user
                        tmp2["place"] = "field"
                        tmp2["deck_id"] = 0
                        tmp2["x"] = x
                        tmp2["y"] = y
                        tmp3  = field[x][y]["det"]["place_unique_id"]
                        tmp2["place_unique_id"] = field[x][y]["det"][
                            "place_unique_id"
                        ]
                        if not duelobj.check_monster_condition_det(
                                monster_effect_det, field[x][y]["det"], user, effect_kind, 1, "field", x, y, 0
                        ):
                            continue
                        if "under" not in field[x][y]["det"]:
                            continue
                        for under in field[x][y]["det"]["under"]:
                            tmp2 = {}
                            tmp2["det"] = under
                            tmp2["mine_or_other"] = field[x][y]["mine_or_other"]
                            tmp2["user"] = user
                            tmp2["place"] = "under"
                            tmp2["deck_id"] = 0
                            tmp2["x"] = x
                            tmp2["y"] = y
                            tmp3  = under["place_unique_id"]
                            tmp2["place_unique_id"] = under[
                                "place_unique_id"
                            ]
                            ask_under.append(tmp3)
    tmp_val = {}
    if ask_under:
        tmp_val["ask_under"] = ask_under
        tmp_val["field_info"] = field
    tmp_val["return_val"] = return_value
    tmp_val["min_equation_number"] = duelobj.calculate_boland(
        monster_effect_det["min_equation_number"]
    )
    tmp_val["max_equation_number"] = duelobj.calculate_boland(
        monster_effect_det["max_equation_number"]
    )
    tmp_val["user"] = duelobj.user
    tmp_val["whether_monster"] = 1
    tmp_val["exclude"] = []
    tmp_val["sentence"] = sentence
    tmp_val["prompt"] = duelobj.write_prompt(prompt,user)
    return HttpResponse(json.dumps(tmp_val))

def show_multiple(
    duelobj, user, effect_kind, monster_effect_text, monster_condition, sentence, prompt
):
    duel = duelobj.duel
    if "whether_monster" in monster_effect_text:
        whether_monster = monster_effect_text["whether_monster"]
    exclude = monster_effect_text["exclude"]
    return_value = []
    tmp0 = []
    tmp1 = []
    return_value.append(tmp0)
    return_value.append(tmp1)
    counter = 0
    for monster_effect_det in monster_effect_text["monster"]:
        counter += 1
        if counter == 2:
            effect_kind = monster_effect_text["multiple_effect_kind"]
        monster_effect_det_monster = monster_effect_det["monster"]
        if (
            "as_monster_condition" in monster_effect_det
            and monster_effect_det["as_monster_condition"] != ""
        ):
            as_monsters = monster_effect_det["as_monster_condition"]
            if not isinstance(as_monsters, list):
                tmp_monster = []
                tmp_monster.append(as_monsters)
                as_monsters = tmp_monster
            for as_monster in as_monsters:
                if as_monster[0] == "~":
                    tmp = duelobj.cost
                    tmp = tmp[str(int(duel.chain))]
                    if as_monster not in tmp:
                        continue
                    place1 = tmp[as_monster]
                elif as_monster[0] == "%":
                    tmp = duelobj.timing_mess
                    if as_monster not in tmp:
                        continue
                    place1 = tmp[as_monster]
                else:
                    tmp = duelobj.mess
                    tmp = tmp[str(int(duel.chain - 1))]
                    if as_monster not in tmp:
                        continue
                    place1 = tmp[as_monster]
                for place2 in place1:
                    if monster_condition != "":
                        if not duelobj.validate_answer(
                            place2, monster_condition, "", duel
                        ):
                            continue
                    if counter == 1:
                        return_value[0].append(place2)
                    else:
                        return_value[1].append(place2)
        else:
            place_array_tmp = []
            for place in monster_effect_det_monster["place"]:
                place_tmp = place["det"].split("_")
                if place["and_or"] != "" and place_tmp[0] == "field":
                    tmptmp = {}
                    tmptmp["and_or"] = place["and_or"]
                    tmptmp["det"] = place["det"]
                    place_array_tmp.append(tmptmp)
                    continue
                else:
                    tmptmp = {}
                    tmptmp["and_or"] = place["and_or"]
                    tmptmp["det"] = place["det"]
                    place_array_tmp.append(tmptmp)
                    place_array = place_array_tmp
                    place_array_tmp = []
                if place_tmp[2] == "1":
                    mine_or_other2 = 1
                elif place_tmp[2] == "2":
                    mine_or_other2 = 2
                elif place_tmp[2] == "3":
                    mine_or_other2 = 3
                if user == 1:
                    mine_or_other = mine_or_other2
                else:
                    if mine_or_other2 == 1:
                        mine_or_other = 2
                    elif mine_or_other2 == 2:
                        mine_or_other = 1
                    else:
                        mine_or_other = mine_or_other2
                deck_id = int(place_tmp[1])
                if place_tmp[0] == "deck":
                    if mine_or_other2 == 1:
                        deck = duelobj.decks[deck_id]["mydeck"]
                    elif mine_or_other2 == 2:
                        deck = duelobj.decks[deck_id]["otherdeck"]
                    elif mine_or_other2 == 3:
                        deck = duelobj.decks[deck_id]["commondeck"]
                    user_decks = deck
                    for user_deck in user_decks:
                        tmp2 = {}
                        tmp2["det"] = user_deck
                        tmp2["mine_or_other"] = mine_or_other
                        tmp2["user"] = user
                        tmp2["place"] = "deck"
                        tmp2["deck_id"] = deck_id
                        tmp2["x"] = 0
                        tmp2["y"] = 0
                        tmp2["place_unique_id"] = user_deck["place_unique_id"]
                        if counter == 1:
                            return_value[0].append(tmp2)
                        else:
                            return_value[1].append(tmp2)
                elif place_tmp[0] == "grave":
                    if mine_or_other2 == 1:
                        grave = duelobj.graves[deck_id]["mygrave"]
                    elif mine_or_other2 == 2:
                        grave = duelobj.graves[deck_id]["othergrave"]
                    elif mine_or_other2 == 3:
                        grave = duelobj.graves[deck_id]["commongrave"]
                    user_graves = grave
                    for user_grave in user_graves:
                        tmp2 = {}
                        tmp2["det"] = user_grave
                        tmp2["mine_or_other"] = mine_or_other
                        tmp2["user"] = user
                        tmp2["place"] = "grave"
                        tmp2["deck_id"] = deck_id
                        tmp2["x"] = 0
                        tmp2["y"] = 0
                        tmp2["place_unique_id"] = user_grave["place_unique_id"]
                        if counter == 1:
                            return_value[0].append(tmp2)
                        else:
                            return_value[1].append(tmp2)
                elif place_tmp[0] == "hand":
                    if mine_or_other2 == 1:
                        hand = duelobj.hands[deck_id]["myhand"]
                    elif mine_or_other2 == 2:
                        hand = duelobj.hands[deck_id]["otherhand"]
                    elif mine_or_other2 == 3:
                        hand = duelobj.hands[deck_id]["commonhand"]
                    user_hands = hand
                    for user_hand in user_hands:
                        tmp2 = {}
                        tmp2["det"] = user_hand
                        tmp2["mine_or_other"] = mine_or_other
                        tmp2["user"] = user
                        tmp2["place"] = "hand"
                        tmp2["deck_id"] = deck_id
                        tmp2["x"] = 0
                        tmp2["y"] = 0
                        tmp2["place_unique_id"] = user_hand["place_unique_id"]
                        if counter == 1:
                            return_value[0].append(tmp2)
                        else:
                            return_value[1].append(tmp2)
                elif place_tmp[0] == "field":
                    field_size = FieldSize.objects.get(id=1)
                    field = duelobj.field
                    if duelobj.field_free is True:
                        field_x = 20
                    else:
                        field_x = field_size.field_x
                    for x in range(field_x):
                        for y in range(field_size.field_y):
                            flag_field_place = True
                            current_and_or = "and"
                            mine_or_others = []
                            for place_tmp2 in place_array:
                                and_or = place_tmp2["and_or"]
                                det = place_tmp2["det"]
                                splitted_det = det.split("_")
                                kind2 = splitted_det[1]
                                if duelobj.field_free is False:
                                    kind = field[x][y]["kind"]
                                else:
                                    kind = field[0][y]["kind"]
                                if kind != "":
                                    tmp = kind.split("_")
                                else:
                                    tmp = []
                                if current_and_or == "and":
                                    if kind2 in tmp:
                                        if flag_field_place is True:
                                            flag_field_place = True
                                    else:
                                        flag_field_place = False
                                elif current_and_or == "or":
                                    if kind2 in tmp:
                                        flag_field_place = True
                                    else:
                                        if flag_field_place is False:
                                            flag_field_place = False
                                mine_or_other = int(splitted_det[2])
                                if (
                                    mine_or_other == 1
                                    and user == 1
                                    or mine_or_other == 2
                                    and user == 2
                                ):
                                    mine_or_other = 1
                                elif (
                                    mine_or_other == 1
                                    and user == 2
                                    or mine_or_other == 2
                                    and user == 1
                                ):
                                    mine_or_other = 2
                                else:
                                    mine_or_other = 3
                                mine_or_others.append(mine_or_other)

                            if flag_field_place is False:
                                continue
                            if field[x][y]["mine_or_other"] not in mine_or_others:
                                continue
                            if field[x][y]["det"] is not None:
                                if duelobj.check_not_effected(
                                    field[x][y]["det"],
                                    user,
                                    effect_kind,
                                    "field",
                                    0,
                                    x,
                                    y,
                                    field[x][y]["mine_or_other"],
                                ):
                                    continue
                                tmp2 = {}
                                tmp2["det"] = field[x][y]["det"]
                                tmp2["mine_or_other"] = field[x][y]["mine_or_other"]
                                tmp2["user"] = user
                                tmp2["place"] = "field"
                                tmp2["deck_id"] = 0
                                tmp2["x"] = x
                                tmp2["y"] = y
                                tmp2["place_unique_id"] = field[x][y]["det"][
                                    "place_unique_id"
                                ]
                                if not duelobj.validate_answer(
                                        tmp2, monster_effect_det["monster"], exclude, duel
                                ):
                                        continue
                                '''
                                if "under" not in field[x][y]["det"]:
                                    continue
                                for under in field[x][y]["det"]["under"]:
                                    if not duelobj.validate_answer(
                                        tmp2, monster_effect_det["monster"], exclude, duel
                                    ):
                                        continue
                                '''
                            if whether_monster == 0:
                                if field[x][y]["det"] is not None:
                                    continue
                                tmp2 = {}
                                tmp2["det"] = field[x][y]["det"]
                                if duelobj.field_free is True:
                                    tmp2["mine_or_other"] = field[0][y]["mine_or_other"]
                                elif duelobj.field_free is False:
                                    tmp2["mine_or_other"] = field[x][y]["mine_or_other"]
                                tmp2["hide"] = (
                                    field["hide"] if ("hide" in field[x][y]) else False
                                )
                                tmp2["x"] = x
                                tmp2["y"] = y
                                tmp2["deck_id"] = 0
                                tmp2["user"] = user
                                tmp2["place"] = "field"
                                if counter == 1:
                                    return_value[0].append(tmp2)
                                else:
                                    return_value[1].append(tmp2)
                            else:
                                if field[x][y]["det"] is None:
                                    continue
                                tmp2 = {}
                                tmp2["det"] = field[x][y]["det"]
                                if duelobj.field_free is True:
                                    tmp2["mine_or_other"] = field[0][y]["mine_or_other"]
                                elif duelobj.field_free is False:
                                    tmp2["mine_or_other"] = field[x][y]["mine_or_other"]
                                tmp2["hide"] = (
                                    field["hide"] if ("hide" in field[x][y]) else False
                                )
                                tmp2["x"] = x
                                tmp2["y"] = y
                                tmp2["deck_id"] = 0
                                tmp2["user"] = user
                                tmp2["place"] = "field"
                                if counter == 1:
                                    return_value[0].append(tmp2)
                                else:
                                    return_value[1].append(tmp2)
    tmp_val = {}
    tmp_val["return_val"] = return_value
    tmp_val["multiple"] = True
    if "auto_select" not in monster_effect_text:
        tmp_val["auto_select"] = ""
    else:
        tmp_val["auto_select"] = monster_effect_text["auto_select"]
    if "double" not in monster_effect_text:
        tmp_val["double"] = False
    else:
        tmp_val["double"] =  monster_effect_text["double"]
    tmp_val["min_equation_number"] = duelobj.calculate_boland(
        monster_effect_det["min_equation_number"]
    )
    tmp_val["max_equation_number"] = duelobj.calculate_boland(
        monster_effect_det["max_equation_number"]
    )
    tmp_val["user"] = duelobj.user
    tmp_val["sentence"] = sentence
    tmp_val["prompt"] = duelobj.write_prompt(prompt,user)
    return HttpResponse(json.dumps(tmp_val))
def choose_trigger(duel, user, room_number, ask, decks, graves, hands):
     duelobj = DuelObj(room_number)
     duelobj.duel = duel
     config = Config.objects.get()
     order = config.order
     trigger_waiting_json = json.loads(duelobj.duel.trigger_waiting)
     tmp_return  = {}
     return_trigger = []
     i = 0
     force = False
     if len(trigger_waiting_json) == 0:
         return HttpResponse("error")
     priority = trigger_waiting_json[0]["priority"]
     if duel.already_choosed == 1:
         return HttpResponse("error")
     for trigger_waiting in trigger_waiting_json[:]:
        trigger = Trigger.objects.get(id=trigger_waiting["trigger"])
        if "who" not in trigger_waiting:
            who = 0
        else:
            who = trigger_waiting["who"]
        if who == 0:
            mine_or_other = str(trigger_waiting["mine_or_other"])
        elif who == 1:
            mine_or_other = str(trigger_waiting["mine_or_other_exist"])
        elif who == 2:
            if "null_relate" in trigger_waiting:
                mine_or_other = trigger_waiting["null_relate"]["mine_or_other"]
            else:
                mine_or_other = str(trigger_waiting["mine_or_other_relate"])
        uuid_str = str(uuid.uuid4())
        trigger_waiting_json[i]["uuid"] = uuid_str
        i+=1
        if int(mine_or_other) != user and order != 1:
            continue;
        if trigger_waiting["priority"] != priority:
            continue
        tmp = {}
        tmp["name"] = trigger.trigger_sentence
        tmp["id"] = trigger.id
        if int(mine_or_other) != user:
            tmp["other"] = True
        else:
            tmp["other"] = False
        tmp["uuid"] = uuid_str
        if trigger.force == True:
            force = True
        return_trigger.append( tmp)
     duelobj.duel.trigger_waiting = json.dumps(trigger_waiting_json)
     tmp_return  = {}

     tmp_return["trigger_choosing"] = True
     tmp_return["return_trigger"] = return_trigger
     tmp_return["force"] = force
     if len(return_trigger) == 0:
        if len(trigger_waiting_json) == 0:
            duel.ask2 = 0
        else:
            if duel.user_turn == user:
                duel.ask2 = 6
            else:
                duel.ask2 = 5
        duel.save()
        return HttpResponse("wait_choose_trigger")

     duel.save()
     return HttpResponse(json.dumps(tmp_return))
def wait_choose_trigger(duel, user, room_number, ask, decks, graves, hands):
    return HttpResponse("wait_choose_trigger")
