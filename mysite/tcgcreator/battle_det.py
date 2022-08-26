from .models import (
    Deck,
    Duel,
    Grave,
    Hand,
    CostWrapper,
    Config,
    Trigger,
    Lock
)
from html import escape
from django.http import HttpResponse
from django.utils.html import format_html
from django.db.models import Q
from .duel import DuelObj
from django.db import connection
import json
import copy
from time import time
from pprint import pprint
from .battle_functions import init_duel


def send_message(request):
    room_number = int(request.POST["room_number"])
    duel = Duel.objects.get(id=room_number)
    duelobj = DuelObj(room_number)
    duelobj.duel = duel
    duelobj.room_number = room_number
    duelobj.in_execute = False
    user_1 = None
    user_2 = None
    if "ID" in request.COOKIES :
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    if duel.guest_flag == False:
        user_1 = duel.user_1
        ID1 = "-1"
    else:
        ID1 = duel.guest_id
    if duel.guest_flag2 == False:
        user_2 = duel.user_2
        ID2 = "-1"
    else:
        ID2 = duel.guest_id2
    if request.user != user_1 and request.user != user_2 :
        if (ID1 == ID and duel.guest_flag) or (ID2 == ID and duel.guest_flag2):
            pass
        else:
            return HttpResponse("error")
    if request.user == user_1 or (ID1 == ID and duel.guest_flag is True):
        duelobj.user = 1
        user = 1
    if request.user == user_2 or (ID2 == ID and duel.guest_flag2 is True):
        duelobj.user = 2
        user = 2
    if user == 1:
        if duel.guest_flag is False:
            tmp = user_1.first_name + ":「" + request.POST["message"] + "」\n"
        else:    
            tmp = duel.guest_name + ":「" + request.POST["message"] + "」\n"
    else:
        if duel.guest_flag2 is False:
            tmp = user_2.first_name + ":「" + request.POST["message"] + "」\n"
        else:    
            tmp = duel.guest_name2 + ":「" + request.POST["message"] + "」\n"
    tmp = format_html(escape(tmp))
    log_turn = duel.log_turn + tmp
    log = duel.log + tmp
    message_log = escape(duel.message_log) + tmp
    current_log = escape(duel.current_log) + tmp
    cursor = connection.cursor()
    cursor.execute(
        "update tcgcreator_duel set log_turn = '"
        + log_turn
        + "',log = '"
        + log
        + "',current_log = '"
        + current_log
        + "',message_log = '"
        + message_log
        + "' where id = "
        + str(room_number)
    )
    return_value =  {}
    return_value["log"] = log_turn
    return_value["message_log"] = message_log
    return_value["current_log"] = current_log
    return HttpResponse(json.dumps(return_value))


def battle_det(request, duelobj=None, choices=None):
    room_number = int(request.POST["room_number"])
    lock = Lock.objects.get()
    if duelobj is None:
        duel = Duel.objects.get(id=room_number)
        duelobj = DuelObj(room_number)
        duelobj.duel = duel
        duelobj.room_number = room_number
        duelobj.in_execute = False

        tmp_flag = True
    else:
        duel = duelobj.duel
        tmp_flag = False
    if "ID" in request.COOKIES :
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    ID1 = duel.guest_id
    ID2 = duel.guest_id2
    user_1 = duel.user_1
    user_2 = duel.user_2
    if (user_1 is not None and request.user == user_1) or (ID1 == ID and duel.guest_flag):
        user = 1
        other_user = 2
    elif (user_2 is not None and request.user == user_2) or (ID2 == ID and duel.guest_flag2):
        user = 2
        other_user = 1
    else:
        return HttpResponse("error")
    if duel.winner == 0:
        if user == 1:
            if duel.guest_flag is True and duel.guest_name == "":
                return HttpResponse("choose_name")
            if duel.deck_choose_flag1 is True and duel.is_ai is False:
                return HttpResponse("choosing_deck")
            if duel.is_ai is False and duel.deck_choose_flag2 is True or (duel.guest_flag2 is True   and duel.guest_name2 == ""):
                config = Config.objects.get();
                limit_time = config.limit_time
                if time() - duel.time_2 > limit_time:
                    duelobj.win_the_game()
                    return HttpResponse("true")
                return HttpResponse("waiting_choosing_deck")
        if user == 2:
            if duel.guest_flag2 is True and duel.guest_name2== "":
                return HttpResponse("choose_name")
            if duel.deck_choose_flag2 is True:
                return HttpResponse("choosing_deck")
            if duel.deck_choose_flag1 is True or (duel.guest_flag is True  and duel.guest_name == ""):
                config = Config.objects.get();
                limit_time = config.limit_time
                if time() - duel.time_1 > limit_time:
                    duelobj.win_the_game()
                    return HttpResponse("true")
                return HttpResponse("waiting_choosing_deck")
    if "wait_ai" in request.POST:
        if duel.user_turn == 2 and duel.ask == 0 and duel.is_ai is True:
            decks = Deck.objects.all()
            graves = Grave.objects.all()
            hands = Hand.objects.all()
            duelobj.user = 1
            duelobj.other_user = 2
            duelobj.init_all(1,2, room_number)
            return battle_det_return_org_ai(
                duelobj, decks, graves, hands, 1, 2, choices, room_number
            )
        else:
            return HttpResponse("waiting")
    # 相手番でも一回は様子をみる
    if room_number == 1:
        if lock.lock_1 is True and time() - lock.time_1 < 20:
            if duel.is_ai == False or not "wait_ai" in request.POST or duel.user_turn == 1 or duel.ask != 0:
                return HttpResponse("waiting")
            else:
                decks = Deck.objects.all()
                graves = Grave.objects.all()
                hands = Hand.objects.all()
                user_1 = duel.user_1
                user_2 = duel.user_2
                if request.user != user_1 and request.user != user_2 and ID1 != ID and ID2 != ID:
                    if (ID1 == ID and duel.guest_flag) or (ID2 == ID and duel.guest_flag2):
                        pass
                    else:
                        return HttpResponse("error")
                if request.user == user_1 or (ID1 == ID and duel.guest_flag):  
                    duelobj.user = 1
                    user = 1
                    other_user = 2
                if request.user == user_2 or (ID2 == ID and duel.guest_flag2):
                    duelobj.user = 2
                    user = 2
                    other_user = 1
                duelobj.init_all(user, other_user, room_number)
                return battle_det_return_org_ai(
                    duelobj, decks, graves, hands, user, other_user, choices, room_number
                )
        else:
            lock.lock_1 = True
            lock.time_1 = time();
            lock.save()
    elif room_number == 2:
        if lock.lock_2 is True and time() - lock.time_2 < 20:
            if duel.is_ai == False or not "wait_ai" in request.POST or duel.user_turn == 1 or duel.ask != 0:
                return HttpResponse("waiting")
            else:
                decks = Deck.objects.all()
                graves = Grave.objects.all()
                hands = Hand.objects.all()
                user_1 = duel.user_1
                user_2 = duel.user_2
                if request.user != user_1 and request.user != user_2 and ID1 != ID and ID2 != ID:
                    if (ID1 == ID and duel.guest_flag) or (ID2 == ID and duel.guest_flag2):
                        pass
                    else:
                        return HttpResponse("error")
                if request.user == user_1 or (ID1 == ID and duel.guest_flag):  
                    duelobj.user = 1
                    user = 1
                    other_user = 2
                if request.user == user_2 or (ID2 == ID and duel.guest_flag2):
                    duelobj.user = 2
                    user = 2
                    other_user = 1
                duelobj.init_all(user, other_user, room_number)
                return battle_det_return_org_ai(
                    duelobj, decks, graves, hands, user, other_user, choices, room_number
                )
        else:
            lock.lock_2 = True
            lock.time_2 = time();
            lock.save()
    elif room_number == 3:
        if lock.lock_3 is True and time() - lock.time_3 < 20:
            if duel.is_ai == False or not "wait_ai" in request.POST or duel.user_turn == 1 or duel.ask != 0:
                return HttpResponse("waiting")
            else:
                decks = Deck.objects.all()
                graves = Grave.objects.all()
                hands = Hand.objects.all()
                user_1 = duel.user_1
                user_2 = duel.user_2
                if request.user != user_1 and request.user != user_2 and ID1 != ID and ID2 != ID:
                    if (ID1 == ID and duel.guest_flag) or (ID2 == ID and duel.guest_flag2):
                        pass
                    else:
                        return HttpResponse("error")
                if request.user == user_1 or (ID1 == ID and duel.guest_flag):  
                    duelobj.user = 1
                    user = 1
                    other_user = 2
                if request.user == user_2 or (ID2 == ID and duel.guest_flag2):
                    duelobj.user = 2
                    user = 2
                    other_user = 1
                duelobj.init_all(user, other_user, room_number)
                return battle_det_return_org_ai(
                    duelobj, decks, graves, hands, user, other_user, choices, room_number
                )
        else:
            lock.lock_3 = True
            lock.time_3 = time();
            lock.save()
    user_1 = duel.user_1
    user_2 = duel.user_2
    if request.user != user_1 and request.user != user_2 and ID1 != ID and ID2 != ID:
        if (ID1 == ID and duel.guest_flag) or (ID2 == ID and duel.guest_flag2):
            pass
        else:
            return HttpResponse("error")
    if request.user == user_1 or (ID1 == ID and duel.guest_flag): 
        duelobj.user = 1
        user = 1
        other_user = 2
    if request.user == user_2 or (ID2 == ID and duel.guest_flag2):
        duelobj.user = 2
        user = 2
        other_user = 1
    if tmp_flag is True:
        duelobj.init_all(user, other_user, room_number)
    decks = Deck.objects.all()
    graves = Grave.objects.all()
    hands = Hand.objects.all()
    turn = duel.user_turn
    duelobj.update = False
    if duel.is_ai is True:
        if duel.user_turn == 1:
            if duel.ask == 6:
                    duelobj.check_eternal_effect(
                        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                    )
                    answer_ai_choose_trigger(duelobj,duel, 2, room_number, duel.ask, decks, graves, hands)
        if duel.user_turn == 2:
            if duel.ask == 5:
                    duelobj.check_eternal_effect(
                        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                    )
                    answer_ai_choose_trigger(duelobj,duel, 2, room_number, duel.ask, decks, graves, hands)

#    chain_user = duelobj.get_current_chain_user()
    if choices is None:
        choices = []
        choices.append(None)
        choices.append(10000)
    if duel.winner != 0 or duel.winner_ai != 0:
        if room_number == 1:
            lock.lock_1 = False
            lock.save()
        elif room_number == 2:
            lock.lock_2 = False
            lock.save()
        elif room_number == 3:
            lock.lock_3 = False
            lock.save()
        return battle_det_return_org(
            duelobj, decks, graves, hands, user, other_user, choices, room_number
        )
    duelobj.check_eternal_effect(
        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
    choices = duelobj.check_trigger(
        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
    choices2 = duelobj.check_trigger(
        decks, graves, hands, duel.phase, duel.user_turn, other_user, user
    )
    if (
        duel.is_ai == False
        and duel.appoint != user
        and ((choices2[0] is not None and duelobj.check_wait(other_user)) or duel.ask > 0)
        and ((turn == user and (duel.ask != 1)) or (turn != user and duel.ask == 2))
        and duel.ask != 3
    ):
        if room_number == 1:
            lock.lock_1 = False
            lock.save()
        elif room_number == 2:
            lock.lock_2 = False
            lock.save()
        elif room_number == 3:
            lock.lock_3 = False
            lock.save()

        return battle_det_return(
            duelobj, decks, graves, hands, user, other_user, choices, room_number
        )
    if (
        duel.appoint == user
        and duel.ask > 0
        and ((turn == user and duel.ask == 2) or (turn != user and duel.ask == 1))
    ):
        if room_number == 1:
            lock.lock_1 = False
            lock.save()
        elif room_number == 2:
            lock.lock_2 = False
            lock.save()
        elif room_number == 3:
            lock.lock_3 = False
            lock.save()
        return battle_det_return(
            duelobj, decks, graves, hands, user, other_user, choices, room_number
        )
    trigger_waiting = json.loads(duel.trigger_waiting)
    if duel.in_trigger_waiting is True:
        flag = False
    else:
        flag = True
    if (
            (duel.chain == 0 or duel.in_trigger_waiting is True)
            and duel.trigger_waiting != "[]"
            and duel.in_cost is False
            and duel.ask == 0
    ):
        if choices2[0] == None and  choices[0] == None:
            tmp_priority = min(choices[1],choices2[1])
        elif choices2[0] == None:
            tmp_priority = choices[1]
        elif choices[0] == None:
            tmp_priority = choices2[1]
        else:
            tmp_priority = duelobj.max2(choices,choices2)
        duelobj.invoke_trigger_waiting(duel.trigger_waiting, tmp_priority)
        duelobj.update = True
        flag = True
        duelobj.check_eternal_effect(
            decks, graves, hands, duel.phase, duel.user_turn, user, other_user
        )
        choices = duelobj.check_trigger(
            decks, graves, hands, duel.phase, duel.user_turn, user, other_user
        )
        choices2 = duelobj.check_trigger(
            decks, graves, hands, duel.phase, duel.user_turn, other_user, user
        )
    flag_3 = False
    ai_flag = False
    while flag is True and (duel.winner == 0 and duel.winner_ai == 0):
        flag = False
        lll_flag = False
        if duel.in_cost >= 1 and duelobj.in_execute is False and duel.appoint == user:
            cost = CostWrapper.objects.get(id=duel.cost_det)
            trigger = Trigger.objects.get(id=duel.current_trigger)
            duelobj.pay_cost(cost, user,duel.chain,trigger,False)
            duelobj.update = True
        elif duel.in_cost is False:
            choices = duelobj.check_trigger(
                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
            )
            while duel.winner == 0 and duel.winner_ai == 0:
                if flag_3 is True:
                    break
                flag_2 = False
                if (choices[1] < choices2[1]) or (choices[0] is None and choices2[0] is not None):
                    duel.appoint = other_user
                if duel.appoint == other_user:

                    while duel.winner == 0 and duel.winner_ai == 0:

                        choices2 = duelobj.check_trigger(
                            decks,
                            graves,
                            hands,
                            duel.phase,
                            duel.user_turn,
                            other_user,
                            user,
                        )
                        if duel.appoint == user:
                            break
                        if choices2[0] is not None and duelobj.check_wait(other_user) and duel.is_ai is False:
                            flag_2 = True
                            break
                        else:
                            choices = duelobj.check_trigger(
                                decks,
                                graves,
                                hands,
                                duel.phase,
                                duel.user_turn,
                                user,
                                other_user,
                            )
                            if choices[0] is not None and duelobj.check_wait(user):
                                #duel.current_priority = duelobj.max2(choices,choices2)
                                duelobj.update = True
                                if duel.none == False:
                                    if duel.appoint == 1:
                                        duel.appoint = 2
                                    else:
                                        duel.appoint = 1
                                    duel.none = True
                                else:
                                    duel.current_priority = duelobj.max2(choices,choices2)
                                    duelobj.update = True
                                    if duel.appoint == 1:
                                        duel.appoint = 2
                                    else:
                                        duel.appoint = 1
                                    duel.none = False
                            elif choices2[0] is not None and duelobj.check_wait(other_user) and duel.is_ai is False:
                                if ai_flag is False:
                                    duel.current_priority = duelobj.max2(choices,choices2)
                                    ai_flag = False
                                duelobj.update = True
                                if duel.none == False:
                                    if duel.appoint == 1:
                                        duel.appoint = 2
                                    else:
                                        duel.appoint = 1
                                    duel.none = True
                                else:
                                    duel.current_priority = duelobj.max2(choices,choices2)
                                    duelobj.update = True
                                    if duel.appoint == 1:
                                        duel.appoint = 2
                                    else:
                                        duel.appoint = 1
                                    duel.none = False
                                break
                            elif lll_flag is False:
                                lll_flag = True
                            else:
                                lll_flag = False
                                tmp_current_priority = duel.current_priority
                                duel.current_priority = duelobj.max2(choices,choices2)
                                if tmp_current_priority != duel.current_priority:
                                    duelobj.update = True
                                if duel.current_priority == 0 and duel.in_trigger_waiting == 1 and duel.ask == 0 and duel.in_cost is False :
                                    duelobj.invoke_trigger_waiting(duel.trigger_waiting)
                                    if duel.in_cost is False:
                                        if duel.is_ai == True:
                                            ai_flag = True
                                        duelobj.retrieve_chain(
                                            decks,
                                            graves,
                                            hands,
                                            duel.phase,
                                            duel.user_turn,
                                            user,
                                            other_user,
                                        )
                                        if duel.chain == 0:
                                            duel.current_priority = 10000
                                            duelobj.invoke_after_chain_effect(
                                                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                                            )
                                            duelobj.invoke_trigger_waiting(duel.trigger_waiting)
                                        duelobj.check_eternal_effect(
                                            decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                                        )
                                        if duel.chain == 0:
                                            duel.current_priority = 10000
                                            if duel.timing3 is not None and duel.chain == 0:
                                                if duel.timing3.timing_auto is True:
                                                    if duel.timing_fresh is False:
                                                        duel.timing3 = duel.timing3.next_timing
                                                        duel.timing_fresh = True
                                                    else:
                                                        duel.timing_fresh = False
                                                if duel.timing is None and duel.timing2 is None and duel.timing3 is None:
                                                    duelobj.timing_mess = {}
                                                if duel.mute == 1:
                                                    duelobj.unmute()
                                                duel.mute = 0
                                            elif duel.timing2 is not None and duel.chain == 0:
                                                if duel.timing2.timing_auto is True:
                                                    if duel.timing_fresh is False:
                                                        duel.timing2 = duel.timing2.next_timing
                                                        duel.timing_fresh = True
                                                        duelobj.check_eternal_effect(
                                                            decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                                                        )
                                                    else:
                                                        duel.timing_fresh = False
                                                if duel.timing is None and duel.timing2 is None:
                                                    duelobj.timing_mess = {}
                                                if duel.mute == 1:
                                                    duelobj.unmute()
                                                duel.mute = 0
                                            elif duel.timing is not None and duel.chain == 0:
                                                if duel.timing.timing_auto is True:
                                                    if duel.timing_fresh is False:
                                                        duel.timing = duel.timing.next_timing
                                                        duel.timing_fresh = True
                                                        duelobj.check_eternal_effect(
                                                            decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                                                        )
                                                    else:
                                                        duel.timing_fresh = False
                                                if duel.timing is None:
                                                    duelobj.timing_mess = {}
                                                if duel.mute == 1:
                                                    duelobj.unmute()
                                                duel.mute = 0
                                        if duel.change_appoint_flag  == 0:
                                            duel.appoint = duel.user_turn
                                        duel.appoint_flag = False
                                        tmp = {}
                                        duel.mess = json.dumps(tmp)
                                        duel.cost_result = json.dumps(tmp)
                                        duel.cost = json.dumps(tmp)
                                        if duel.appoint == other_user and duel.is_ai == False:
                                            flag_2 = True
                                    break
                                elif duel.current_priority == 0 and duel.in_cost is False :
                                    if (duel.ask == 0 ):
                                        duelobj.invoke_trigger_waiting(duel.trigger_waiting)
                                    if duel.chain != 0 and duel.current_priority == 0:

                                        duelobj.retrieve_chain(
                                            decks,
                                            graves,
                                            hands,
                                            duel.phase,
                                            duel.user_turn,
                                            user,
                                            other_user,
                                        )
                                        if duel.chain == 0:
                                            duelobj.invoke_after_chain_effect(
                                                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                                            )
                                            duelobj.invoke_trigger_waiting(duel.trigger_waiting)
                                        
                                            duel.current_priority  = 10000
                                        duelobj.check_eternal_effect(
                                            decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                                        )
                                    else:
                                        duel.timing_fresh = False
                                    if duel.chain == 0:
                                        duel.current_priority  = 10000
                                        if duel.timing3 is not None and duel.chain == 0:
                                            if duel.timing3.timing_auto is True:
                                                if duel.timing_fresh is False:
                                                    duel.timing3 = duel.timing3.next_timing
                                                    duel.timing_fresh = True
                                                    duelobj.check_eternal_effect(
                                                        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                                                    )
                                                else:
                                                    duel.timing_fresh = False
                                                if duel.timing is None and duel.timing2 is None and duel.timing3 is None:
                                                    duelobj.timing_mess = {}
                                            if duel.mute == 1:
                                                duelobj.unmute()
                                        if duel.timing2 is not None and duel.chain == 0:
                                            if duel.timing2.timing_auto is True:
                                                if duel.timing_fresh is False:
                                                    duel.timing2 = duel.timing2.next_timing
                                                    duel.timing_fresh = True
                                                else:
                                                    duel.timing_fresh = False
                                                if duel.timing is None and duel.timing2 is None:
                                                    duelobj.timing_mess = {}
                                            if duel.mute == 1:
                                                duelobj.unmute()
                                        elif duel.timing is not None and duel.chain == 0:
                                            if duel.timing.timing_auto is True:
                                                if duel.timing_fresh is False:
                                                    duel.timing = duel.timing.next_timing
                                                    duel.timing_fresh = True
                                                    duelobj.check_eternal_effect(
                                                        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                                                    )
                                                else:
                                                    duel.timing_fresh = False
                                                if duel.timing is None:
                                                    duelobj.timing_mess = {}
                                            if duel.mute == 1:
                                                duelobj.unmute()
                                            duel.mute = 0
                                        tmp = {}
                                        duel.mess = json.dumps(tmp)
                                        duel.cost_result = json.dumps(tmp)
                                        duel.cost = json.dumps(tmp)
                                        if duel.change_appoint_flag == 0:
                                            duel.appoint = duel.user_turn
                                        duel.appoint_flag = False
                                    if duel.appoint == other_user and duelobj.check_wait(other_user) and duel.is_ai == False:
                                        flag_2 = True
                                    break
                if duel.appoint == user:
                    choices = duelobj.check_trigger(
                        decks,
                        graves,
                        hands,
                        duel.phase,
                        duel.user_turn,
                        user,
                        other_user,
                    )
                    choices2 = duelobj.check_trigger(
                        decks,
                        graves,
                        hands,
                        duel.phase,
                        duel.user_turn,
                        other_user,
                        user,
                    )
                    while (choices[0] is None and choices[1] == choices2[1] and choices2[0] is None and duel.current_priority != 0):
                        choices = duelobj.check_trigger(
                        decks,
                        graves,
                        hands,
                        duel.phase,
                        duel.user_turn,
                        user,
                        other_user,
                        )
                        choices2 = duelobj.check_trigger(
                        decks,
                        graves,
                        hands,
                        duel.phase,
                        duel.user_turn,
                        other_user,
                        user,
                        )
                        if(choices[0] is None and choices2[0] is None):
                            duel.current_priority = max(choices[1] ,choices2[1])
                    if (choices2[1] > choices[1] and choices2[1] is not None) or (
                        choices2[0] is not None and choices[0] is None
                    ):
                        if not duelobj.check_wait(other_user) or duel.is_ai is True:

                            duel.current_priority = choices2[1]
                            duelobj.update = True
                        elif duel.none == False:
                            if duel.appoint == 1:
                                duel.appoint = 2
                            else:
                                duel.appoint = 1
                            duel.none = True
                            break
                        else:
                            duel.current_priority = duelobj.max2(choices,choices2)
                            if duel.appoint == 1:
                                duel.appoint = 2
                            else:
                                duel.appoint = 1
                            duel.none = False
                            duelobj.update = True
                            break
                    if choices[0] != "monster_trigger":
                        if (
                            choices[0] is None and choices2[0] is not None
                        ):  # and duel.appoint == duel.user_turn):
                            duelobj.update = True
                            if not duelobj.check_wait(other_user):
                                duel.current_priority = choices2[1]
                            elif duel.none == False:
                                if duel.appoint == 1:
                                    duel.appoint = 2
                                else:
                                    duel.appoint = 1
                                duel.none = True
                                break
                            else:
                                duel.current_priority = duelobj.max2(choices,choices2)
                                if duel.appoint == 1:
                                    duel.appoint = 2
                                else:
                                    duel.appoint = 1
                                duel.none = False
                        elif (
                            choices[0] is None
                            and choices2[0] is not None
                            and duel.appoint != duel.user_turn
                        ):
                            duel.current_priority = choices2[1]
                            duelobj.update = True
                        elif duel.in_cost is False and \
                            (duel.ask == 0 and (
                            (choices[0] is None or choices[0] is True)
                            and choices2[0] is None
                            and duel.appoint == duel.user_turn
                            and duel.chain == 0
                            and (duel.timing is not None or duel.timing2 is not None or duel.timing3 is not None)
                            and choices[1] == 0
                        ) or (
                            choices[1] == 0
                            and choices2[1] == 0
                            and (duel.timing is not None or duel.timing2 is not None or duel.timing3 is not None)
                        )):
                            duelobj.invoke_trigger_waiting(duel.trigger_waiting)
                            if duel.in_cost is False:
                                duelobj.retrieve_chain(
                                    decks,
                                    graves,
                                    hands,
                                    duel.phase,
                                    duel.user_turn,
                                    user,
                                    other_user,
                                )
                                if duel.chain == 0:
                                   duelobj.invoke_after_chain_effect(
                                       decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                                   )
                                   duelobj.invoke_trigger_waiting(duel.trigger_waiting)
                                duelobj.check_eternal_effect(
                                    decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                                )
                                if duel.chain == 0:
                                    duel.current_priority = 10000
                                    #duel.current_priority = choices[1]
                                    if duel.timing3 is not None:
                                        if duel.timing3.timing_auto is True:
                                            if duel.timing_fresh is False:
                                                duel.timing3 = duel.timing3.next_timing
                                                duel.timing_fresh = True
                                            else:
                                                duel.timing_fresh = False
                                        if duel.timing3 is None and duel.timing2 is None and duel.timing is None:
                                            duelobj.timing_mess = {}
                                        if duel.mute == 1:
                                            duelobj.unmute()
                                        duel.mute = 0
                                    elif duel.timing2 is not None:
                                        if duel.timing2.timing_auto is True:
                                            if duel.timing_fresh is False:
                                                duel.timing2 = duel.timing2.next_timing
                                                duel.timing_fresh = True
                                                duelobj.check_eternal_effect(
                                                    decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                                                )
                                            else:
                                                duel.timing_fresh = False
                                        if duel.timing2 is None and duel.timing is None:
                                            duelobj.timing_mess = {}
                                        if duel.mute == 1:
                                            duelobj.unmute()
                                        duel.mute = 0
                                    elif duel.timing is not None:
                                        if duel.timing.timing_auto is True:
                                            if duel.timing_fresh is False:
                                                duel.timing = duel.timing.next_timing
                                                duel.timing_fresh = True
                                                duelobj.check_eternal_effect(
                                                    decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                                                )
                                            else:
                                                duel.timing_fresh = False
                                        if duel.timing is None:
                                            duelobj.timing_mess = {}
                                        if duel.mute == 1:
                                            duelobj.unmute()
                                        duel.mute = 0
                                    tmp = {}
                                    duel.mess = json.dumps(tmp)
                                    duel.cost_result = json.dumps(tmp)
                                    duel.cost = json.dumps(tmp)
                                if duel.change_appoint_flag == 0:
                                    duel.appoint = duel.user_turn
                                duel.appoint_flag = False
                                duel.current_priority = 10000
                            duelobj.update = True
                        elif (
                            (choices[0] is None or choices[0] is True)
                            and (choices2[0] is None
                            or choices[0] is True) and duel.chain == 0 and duel.in_cost is False):
                            duel.current_priority = choices[1]
                            duelobj.update = True
                            if duel.current_priority == 0 and duel.ask == 0:
                                duel.current_priority = 10000
                                duelobj.invoke_trigger_waiting(duel.trigger_waiting)
                                if duel.in_cost is False:
                                    duelobj.retrieve_chain(
                                    decks,
                                    graves,
                                    hands,
                                    duel.phase,
                                    duel.user_turn,
                                    user,
                                    other_user,
                                    )
                                    if duel.chain == 0:
                                       duelobj.invoke_after_chain_effect(
                                           decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                                       )
                                       duelobj.invoke_trigger_waiting(duel.trigger_waiting)
                                    duelobj.check_eternal_effect(
                                        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                                    )
                                    if duel.change_appoint_flag == 0:
                                        duel.appoint = duel.user_turn
                                    duel.appoint_flag = False
                                    duel.current_priority = 10000
                                    choices = duelobj.check_trigger(
                                    decks,
                                    graves,
                                    hands,
                                    duel.phase,
                                    duel.user_turn,
                                    user,
                                    other_user,
                                )
                                    if choices[0] is None:
                                        break
                        elif (
                            choices[0] is None
                            and choices2[0] is None
                            and duel.chain != 0
                            and duel.ask == 0
                            and duel.in_trigger_waiting is True
                        ):
                            if (
                                (duel.chain == 0 or duel.in_trigger_waiting is True)
                                and duel.trigger_waiting != "[]"
                                and duel.in_cost is False
                                and duel.ask == 0
                            ):
                                duel.current_priority = duelobj.max2(choices,choices2)
                                flag2 = duelobj.invoke_trigger_waiting(duel.trigger_waiting, duel.current_priority)
                                duelobj.update = True
                                if duel.current_priority == 0:
                                    duel.current_priority = 10000
                                    choices = duelobj.check_trigger(
                                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                                )
                                    choices2 = duelobj.check_trigger(
                                decks, graves, hands, duel.phase, duel.user_turn, other_user, user
                                )
                                if not flag2:
                                    duel.in_trigger_waiting = False
                                continue
                            break
                        duelobj.invoke_trigger_waiting(duel.trigger_waiting)
                        if (
                            choices[0] is None
                            and choices2[0] is None
                            and duel.chain != 0
                            and duel.ask == 0
                            and duel.in_cost is False
                            and duel.in_trigger_waiting is False
                        ):
                            duelobj.check_eternal_effect(
                                decks,
                                graves,
                                hands,
                                duel.phase,
                                duel.user_turn,
                                user,
                                other_user,
                            )
                            duelobj.invoke_trigger_waiting(duel.trigger_waiting)
                            duelobj.update = True
                            if duel.in_cost is False and duel.current_priority == 0:
                                duelobj.retrieve_chain(
                                    decks,
                                    graves,
                                    hands,
                                    duel.phase,
                                    duel.user_turn,
                                    user,
                                    other_user,
                                )
                                if duel.chain == 0:
                                    duelobj.invoke_after_chain_effect(
                                        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                                    )
                                    duelobj.invoke_trigger_waiting(duel.trigger_waiting)
                                duelobj.check_eternal_effect(
                                    decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                                )
                                if duel.chain == 0:
                                    if duel.change_appoint_flag  == 0:
                                        duel.appoint = duel.user_turn
                                    duel.appoint_flag = False
                                    if duel.timing3 is not None:
                                        if duel.timing3.timing_auto is True:
                                            if duel.timing_fresh is False:
                                                duel.timing3 = duel.timing3.next_timing
                                                duel.timing_fresh = True
                                            else:
                                                duel.timing_fresh = False
                                        if duel.timing is None and duel.timing2 is None and duel.timing3 is None:
                                            duelobj.timing_mess = {}
                                            if duel.mute == 1:
                                                duelobj.unmute()
                                            duel.mute = 0
                                            duelobj.check_eternal_effect(
                                                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                                            )
                                    if duel.timing2 is not None:
                                        if duel.timing2.timing_auto is True:
                                            if duel.timing_fresh is False:
                                                duel.timing2 = duel.timing2.next_timing
                                                duel.timing_fresh = True
                                                duelobj.check_eternal_effect(
                                                    decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                                                )
                                            else:
                                                duel.timing_fresh = False
                                        if duel.timing is None and duel.timing2 is None:
                                            duelobj.timing_mess = {}
                                            if duel.mute == 1:
                                                duelobj.unmute()
                                            duel.mute = 0
                                            duelobj.check_eternal_effect(
                                                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                                            )
                                    elif duel.timing is not None:
                                        if duel.timing.timing_auto is True:
                                            if duel.timing_fresh is False:
                                                duel.timing = duel.timing.next_timing
                                                duel.timing_fresh = True
                                                duelobj.check_eternal_effect(
                                                    decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                                                )
                                            else:
                                                duel.timing_fresh = False
                                        if duel.timing is None:
                                            duelobj.timing_mess = {}
                                            if duel.mute == 1:
                                                duelobj.unmute()
                                            duel.mute = 0
                                            if duel.timing is None:
                                                duelobj.timing_mess = {}
                                            duelobj.check_eternal_effect(
                                                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                                            )
                                    tmp = {}
                                    duel.mess = json.dumps(tmp)
                                    duel.cost_result = json.dumps(tmp)
                                    duel.cost = json.dumps(tmp)
                                    duel.current_priority = 10000
                                    choices = duelobj.check_trigger(
                                        decks,
                                        graves,
                                        hands,
                                        duel.phase,
                                        duel.user_turn,
                                        user,
                                        other_user,
                                    )
                                    choices2 = duelobj.check_trigger(
                                        decks,
                                        graves,
                                        hands,
                                        duel.phase,
                                        duel.user_turn,
                                        other_user,
                                        user,
                                    )

                if (
                    (duel.chain == 0 or duel.in_trigger_waiting is True)
                    and duel.trigger_waiting != "[]"
                    and duel.in_cost is False
                    and duel.ask == 0
                    and choices[0] is None 
                    and choices2[0] is None 
                ):
                    duel.current_priority = duelobj.max2(choices,choices2)
                    if duel.current_priority == 0:
                        duel.current_priority = 10000
                        choices = duelobj.check_trigger(
                    decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                    )
                        choices2 = duelobj.check_trigger(
                    decks, graves, hands, duel.phase, duel.user_turn, other_user, user
                    )
                    flag2 = duelobj.invoke_trigger_waiting(duel.trigger_waiting, duel.current_priority)
                    duelobj.update = True
                    if not flag2:
                        duel.in_trigger_waiting = False
                    '''
                    現状意味不明
                    if duelobj.check_wait(user) and duel.is_ai is True:
                        choices = duelobj.check_trigger(
                                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
                            )
                        if choices[0]:
                            duel.appoint = 1
                            flag = False
                            flag_3 = True
                            break
                    '''
                if flag_2 is True:
                    break
                if( choices[0] is not None
                     and choices[0] is not True
                     and duel.appoint == user
                     and not duelobj.check_wait(user)):
                    duelobj.update = True
                    break

                elif (
                    duel.in_cost is True
                    or
                        (choices[0] is not None
                         and choices[0] is not True
                         and duel.appoint == user
                         and duelobj.check_wait(user))
                    or duel.ask != 0
                    or duel.winner != 0
                    or duel.winner_ai != 0
                ):
                    break


    if (
        (duel.chain == 0 or duel.in_trigger_waiting is True)
        and duel.trigger_waiting != "[]"
        and duel.in_cost is False
        and duel.ask == 0
        and choices[0] is None
        and choices2[0] is None
    ):
        duel.current_priority = duelobj.max2(choices, choices2)
        if duel.current_priority == 0:
            duel.current_priority = 10000
            choices = duelobj.check_trigger(
        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
        )
        flag2 = duelobj.invoke_trigger_waiting(duel.trigger_waiting, duel.current_priority)
        duelobj.update = True
        if not flag2:
            duel.in_trigger_waiting = False
            if choices[1] >= choices2[1]:
                duel.appoint = 1
            else:
                duel.appoint = 2
    if(choices[0] is not None and choices2[0] is None):
        duel.appoint = user
    if(choices2[0] is not None and choices[0] is None):
        duel.appoint = other_user
            
    if room_number == 1:
        lock.lock_1 = False
        lock.save()
    elif room_number == 2:
        lock.lock_2 = False
        lock.save()
    elif room_number == 3:
        lock.lock_3 = False
        lock.save()
    return battle_det_return(
        duelobj, decks, graves, hands, user, other_user, choices, room_number
    )


def battle_det_return(
    duelobj, decks, graves, hands, user, other_user, choices, room_number
):
    recal = False
    duel = duelobj.duel
    if duel.winner != 0 or duel.winner_ai != 0:
        return battle_det_return_org(
            duelobj, decks, graves, hands, user, other_user, choices, room_number
        )
    return_value = {}
    if duelobj.current_log != "":
        return_value["current_log"] = escape(duelobj.current_log)
    else:
        return_value["current_log"] = escape(duel.current_log)
    return_value["variable"] = duelobj.get_variables()
    return_value["phase"] = duel.phase.id
    if duelobj.user == 1:
        return_value["turn"] = duel.user_turn
    else:
        if(duel.user_turn == 1):
            return_value["turn"] = 2
        else:
            return_value["turn"] = 1
    return_value["log"] = escape(duel.log_turn)
    return_value["message_log"] = escape(duel.message_log)
    if duelobj.user == 1:
        if duel.guest_flag is False:
            return_value["user_name1"] = escape(duel.user_1.first_name)
        else:    
            return_value["user_name1"] = escape(duel.guest_name)

        if duel.is_ai  is False:
            if duel.guest_flag2 is False:
                return_value["user_name2"] = escape(duel.user_2.first_name)
            else:
                return_value["user_name2"] = escape(duel.guest_name2)
        else:
            return_value["user_name2"] = "NPC"
    else:
        if duel.is_ai  is False:
            if duel.guest_flag2 is False:
                return_value["user_name1"] = escape(duel.user_2.first_name)
            else:
                return_value["user_name1"] = escape(duel.guest_name2)
        else:
            return_value["user_name1"] = "NPC"
        if duel.guest_flag is False:
            return_value["user_name2"] = escape(duel.user_1.first_name)
        else:    
            return_value["user_name2"] = escape(duel.guest_name)
    return_value["user"] = user
    return_value["other_user"] = other_user
    if duel.appoint == user:
        return_value["appoint"] = True
    elif duel.appoint == other_user:
        return_value["appoint"] = False

    if duel.change_appoint_flag != 0:
        duel.appoint = duel.change_appoint_flag
    none_force = duelobj.check_trigger(
        decks, graves, hands, duel.phase, duel.user_turn, user, other_user,True
    )
    deck_info = duelobj.get_deck_info(decks, user, other_user, 1)
    return_value["deck_info"] = copy.deepcopy(deck_info)
    if duel.appoint != user and duel.is_ai is True:
        duelobj.invoke_trigger_waiting(None,0,2)
    if duel.appoint == user:
        deck_info = duelobj.modify_deck_info(
            return_value["deck_info"], duelobj.count_deck(decks), user, other_user, choices[1]
        )
        return_value["deck_info"] = deck_info[0]
        deck_force = deck_info[1]
    else:
        deck_force = 0
    return_value["grave_info"] = duelobj.get_grave_info(graves, user, other_user, 1)
    if duel.appoint == user:
        grave_info = duelobj.modify_grave_info(
            return_value["grave_info"], graves.count(), user, other_user, choices[1]
        )
        return_value["grave_info"] = grave_info[0]
        grave_force = grave_info[1]
    else:
        grave_force = 0
    hand_info = duelobj.get_hand_info(hands, user, other_user, 1)
    return_value["hand_info"] = copy.deepcopy(hand_info)
    if duel.appoint == user:
        hand_info = duelobj.modify_hand_info(
            return_value["hand_info"], hands.count(), user, other_user, choices[1]
        )
        return_value["hand_info"] = hand_info[0]
        hand_force = hand_info[1]
    else:
        hand_force = 0
    field = duelobj.field
    return_value["field_info"] = copy.deepcopy(field)
    if duel.appoint == user:
        field_info = duelobj.modify_field_info(
            return_value["field_info"], user, other_user, choices[1]
        )
    else:
        field_info = duelobj.modify_field_info(
            return_value["field_info"], user, other_user, choices[1]
        )

    return_value["field_info"] = field_info[0]
    field_force = field_info[1]
    if duel.appoint == user:
        if(deck_force == 1 and grave_force == 0 and hand_force == 0 and field_force == 0 and none_force == 0):
            recal =  True
            duelobj.modify_deck_info(
                return_value["deck_info"], duelobj.count_deck(decks), user, other_user, choices[1],2)
            duel.ask = 0
        if(deck_force == 0 and grave_force == 1 and hand_force == 0 and field_force == 0 and none_force == 0):
            recal =  True
            duelobj.modify_grave_info(
                return_value["deck_info"], duelobj.count_deck(decks), user, other_user, choices[1],2)
            duel.ask = 0
        if(deck_force == 0 and grave_force == 0 and hand_force == 1 and field_force == 0 and none_force == 0):
            recal =  True
            duelobj.modify_hand_info(
                return_value["deck_info"], duelobj.count_deck(decks), user, other_user, choices[1],2)
            duel.ask = 0
        if(deck_force == 0 and grave_force == 0 and hand_force == 0 and field_force == 1 and none_force == 0):
            recal =  True
            duelobj.modify_field_info(
                return_value["deck_info"], duelobj.count_deck(decks), user, other_user, choices[1],2)
            duel.ask = 0
        if(deck_force == 0 and grave_force == 0 and hand_force == 0 and field_force == 0 and none_force == 1):
            recal =  True
            duelobj.check_trigger(
            decks, graves, hands, duel.phase, duel.user_turn, user, other_user,2)
            duel.ask = 0
    if recal is True:
        deck_info = duelobj.get_deck_info(decks, user, other_user, 1)
        return_value["deck_info"] = copy.deepcopy(deck_info)
        if duel.appoint == user:
            deck_info = duelobj.modify_deck_info(
                return_value["deck_info"], duelobj.count_deck(decks), user, other_user, choices[1]
            )
            return_value["deck_info"] = deck_info[0]
            deck_info = deck_info[1]
        return_value["grave_info"] = duelobj.get_grave_info(graves, user, other_user, 1)
        if duel.appoint == user:
            grave_info = duelobj.modify_grave_info(
                return_value["grave_info"], graves.count(), user, other_user, choices[1]
            )
            return_value["grave_info"] = grave_info[0]
            grave_info = grave_info[1]
        hand_info = duelobj.get_hand_info(hands, user, other_user, 1)
        return_value["hand_info"] = copy.deepcopy(hand_info)
        if duel.appoint == user:
            hand_info = duelobj.modify_hand_info(
                return_value["hand_info"], hands.count(), user, other_user, choices[1]
            )
            return_value["hand_info"] = hand_info[0]
            hand_info = hand_info[1]
        field = duelobj.field
        return_value["field_info"] = copy.deepcopy(field)
        if duel.appoint == user:
            field_info = duelobj.modify_field_info(
                return_value["field_info"], user, other_user, choices[1]
            )
        else:
            field_info = duelobj.modify_field_info(
                return_value["field_info"], user, other_user, choices[1]
            )

        return_value["field_info"] = field_info[0]
        choices = duelobj.check_trigger(
            decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
    if (
            (
        (duel.timing is not None and duel.timing.pri is True)
        or  (duel.timing2 is not None and duel.timing2.pri is True)
        or  (duel.timing3 is not None and duel.timing3.pri is True))
        and duel.appoint == user
        and duel.ask == 0
        and choices[0] is not None
        and duelobj.check_wait(user)
    ) or (duel.chain > 0 and duel.ask == 0 and duel.appoint == user)\
    or (duel.ask == 0 and duel.appoint == user and duel.phase.pri is True):
        if choices[0] != "force":
            return_value["pri"] = True
    else:
        return_value["pri"] = False
    return_value["choices"] = choices[0]
    if user == 1:
        if duel.sound_effect_1 != "":
            return_value["sound_effect"] = duel.sound_effect_1
            duel.sound_effect_1 = ""
            duel.save();
        else:
            return_value["sound_effect"] = ""
    elif user == 2:
        if duel.sound_effect_2 != "":
            return_value["sound_effect"] = duel.sound_effect_2
            duel.sound_effect_2 = ""
            duel.save();
        else:
            return_value["sound_effect"] = ""
    return_value["audio"] = duel.audio
    config = Config.objects.get()
    limit_time = config.limit_time
    if duel.mute ==0 :
        return_value["koka"] = duelobj.get_koka()
    else:
        return_value["koka"] = {}
    if user == 1:
        return_value["time_1"] = limit_time - (time() - duel.time_1)
        return_value["time_2"] = limit_time - (time() - duel.time_2)
    else:
        return_value["time_1"] = limit_time - (time() - duel.time_2)
        return_value["time_2"] = limit_time - (time() - duel.time_1)
    return_value["winner"] = False
    if user == 1:
        return_value["effect"] = duelobj.effect
    elif user == 2:
        return_value["effect"] = duelobj.effect2
    duelobj.save_all(user, other_user, room_number)
    if duel.ask > 0:
        return_value["ask_org"] = True
    else:
        return_value["ask_org"] = False
    if duelobj.user == duel.user_turn:
        if duel.ask == 1 or duel.ask == 3 or duel.ask == 4 or duel.ask == 5:
            return_value["ask"] = True
        else:
            return_value["ask"] = False

    else:
        if duel.ask == 2 or duel.ask == 3 or duel.ask == 4 or duel.ask == 6:
            return_value["ask"] = True
        else:
            return_value["ask"] = False
    return_value["ask_det"] = duel.ask_det
    return HttpResponse(json.dumps(return_value))


def battle_det_return_org(
    duelobj, decks, graves, hands, user, other_user, choices, room_number
):
    if choices is None:
        choices = []
        choices.append(None)
        choices.append(10000)
    duel = duelobj.duel
    return_value = {}
    if duelobj.current_log != "":
        return_value["current_log"] = escape(duelobj.current_log)
    else:
        return_value["current_log"] = escape(duel.current_log)
    return_value["variable"] = duelobj.get_variables()
    return_value["phase"] = duel.phase.id
    return_value["turn"] = duel.user_turn
    return_value["log"] = escape(duel.log_turn)
    return_value["message_log"] = escape(duel.message_log)
    if duel.ask > 0:
        return_value["ask_org"] = True
    else:
        return_value["ask_org"] = False
    if duelobj.user == 1:
        if duel.guest_flag is False:
            return_value["user_name1"] = escape(duel.user_1.first_name)
        else:    
            return_value["user_name1"] = escape(duel.guest_name)
        if duel.is_ai  is False:
            if duel.guest_flag2 is False:
                return_value["user_name2"] = escape(duel.user_2.first_name)
            else:
                return_value["user_name2"] = escape(duel.guest_name2)
        else: 
            return_value["user_name2"] = "NPC"
    else:
        if duel.is_ai  is False:
            if duel.guest_flag2 is False:
                return_value["user_name1"] = escape(duel.user_2.first_name)
            else:
                return_value["user_name1"] = escape(duel.guest_name2)
        else:
            return_value["user_name1"] = "NPC"
        if duel.guest_flag is False:
            return_value["user_name2"] = escape(duel.user_1.first_name)
        else:    
            return_value["user_name2"] = escape(duel.guest_name)
    return_value["ask_det"] = duel.ask_det
    return_value["user"] = user
    return_value["other_user"] = other_user
    if duel.appoint == user:
        return_value["appoint"] = True
    elif duel.appoint == other_user:
        return_value["appoint"] = False
    deck_info = duelobj.get_deck_info(decks, user, other_user, 1)
    return_value["deck_info"] = copy.deepcopy(deck_info)
    return_value["grave_info"] = duelobj.get_grave_info(graves, user, other_user, 1)
    hand_info = duelobj.get_hand_info(hands, user, other_user, 3)
    return_value["hand_info"] = copy.deepcopy(hand_info)
    field = duelobj.field
    return_value["field_info"] = copy.deepcopy(field)
    if (
            ((duel.timing is not None and duel.timing.pri is True)
            or (duel.timing2 is not None and duel.timing2.pri is True)
            or (duel.timing3 is not None and duel.timing3.pri is True))
        and duel.appoint == user
        and duel.ask == 0
        and choices[0] is not None and duelobj.check_wait(user)
    ) or (duel.chain > 0 and duel.ask == 0 and duel.appoint == user)\
    or (duel.ask == 0 and duel.user_turn != user and duel.appoint == user and duel.phase.pri is True):
        return_value["pri"] = True
    else:
        return_value["pri"] = False
    if choices is not None:
        if choices[0] == "monster_trigger":
            return_value["choices"] = None
        else:
            return_value["choices"] = choices[0]
    else:
        return_value["choices"] = None
    if user == 1:
        if duel.sound_effect_1 != "":
            return_value["sound_effect"] = duel.sound_effect_1
            duel.sound_effect_1 = ""
            duel.save();
        else:
            return_value["sound_effect"] = ""
    elif user == 2:
        if duel.sound_effect_2 != "":
            return_value["sound_effect"] = duel.sound_effect_2
            duel.sound_effect_2 = ""
            duel.save();
        else:
            return_value["sound_effect"] = ""
    return_value["audio"] = duel.audio
    return_value["koka"] = duelobj.get_koka()
    return_value["time_1"] = 0
    return_value["time_2"] = 0
    return_value["winner"] = True
    if duel.winner != 0:
        return_value["winner_who"] = duel.winner
    else:
        return_value["winner_who"] = duel.winner_ai
    if user == 1:
        if duel.effect != "":
            return_value["effect"] = duelobj.effect
    elif user == 2:
        if duel.effect2 != "":
            return_value["effect"] = duelobj.effect2
    return HttpResponse(json.dumps(return_value))

def battle_det_return_org_ai(
        duelobj, decks, graves, hands, user, other_user, choices, room_number
):
    duel = duelobj.duel
    duelobj.check_eternal_effect(
        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
    return_value = {}
    if duelobj.current_log != "":
        return_value["current_log"] = escape(duelobj.current_log)
    else:
        return_value["current_log"] = escape(duel.current_log)
    return_value["variable"] = duelobj.get_variables()
    return_value["phase"] = duel.phase.id
    return_value["turn"] = duel.user_turn
    return_value["log"] = escape(duel.log_turn)
    return_value["message_log"] = escape(duel.message_log)
    return_value["ask_org"] = False
    return_value["ask"] = False
    if duelobj.user == 1:
        if duel.guest_flag is False:
            return_value["user_name1"] = escape(duel.user_1.first_name)
        else:    
            return_value["user_name1"] = escape(duel.guest_name)
        return_value["user_name2"] = "NPC"
    else:
        if duel.is_ai is False:
            if duel.guest_flag2 is False:
                return_value["user_name1"] = escape(duel.user_2.first_name)
            else:
                return_value["user_name1"] = escape(duel.guest_name2)
        else:
            return_value["user_name1"] = "NPC"
        if duel.guest_flag is False:
            return_value["user_name2"] = escape(duel.user_1.first_name)
        else:    
            return_value["user_name2"] = escape(duel.guest_name)
    return_value["ask_det"] = 0
    return_value["user"] = user
    return_value["other_user"] = other_user
    if duel.appoint == user:
        return_value["appoint"] = True
    elif duel.appoint == other_user:
        return_value["appoint"] = False
    if duel.appoint == othere_user and duel.is_ai is True:
        duelobj.invoke_ai_trigger()
    deck_info = duelobj.get_deck_info(decks, user, other_user, 1)
    return_value["deck_info"] = copy.deepcopy(deck_info)
    return_value["grave_info"] = duelobj.get_grave_info(graves, user, other_user, 1)
    hand_info = duelobj.get_hand_info(hands, user, other_user, 1)
    return_value["hand_info"] = copy.deepcopy(hand_info)
    field = duelobj.field
    return_value["field_info"] = copy.deepcopy(field)
    return_value["pri"] = False
    return_value["choices"] = None
    if user == 1:
        if duel.sound_effect_1 != "":
            return_value["sound_effect"] = duel.sound_effect_1
            duel.sound_effect_1 = ""
        else:
            return_value["sound_effect"] = ""
    elif user == 2:
        if duel.sound_effect_2 != "":
            return_value["sound_effect"] = duel.sound_effect_2
            duel.sound_effect_2 = ""
        else:
            return_value["sound_effect"] = ""
    return_value["audio"] = duel.audio
    return_value["koka"] = []
    return_value["time_1"] = 0
    return_value["time_2"] = 0
    return_value["waiting_ai"]  = 1
    return_value["effect"] = str(duelobj.effect)
    return HttpResponse(json.dumps(return_value))
def answer_ai_choose_trigger(duelobj,duel,user,room_number,ask,decks,graves,hands,config= None):
    
     if user == 1:
        other_user = 2
     else:
        other_user = 1
     trigger_waitings = json.loads(duelobj.duel.trigger_waiting)
     if len(trigger_waitings) == 0:
             duel.already_choosed = 1
             duel.trigger_waiting = "[]"
             duel.ask = 0
             return
     tmp_priority = trigger_waitings[0]["priority"]
     if config is None:
         config = Config.objects.get()
     order = config.order
     i=0
     for trigger_waiting in trigger_waitings[:]:
         trigger = Trigger.objects.get(id=trigger_waiting["trigger"])
         if trigger.priority != tmp_priority:
                 break
         flag = True
         monster = trigger_waiting["monster"]
         if "who" not in trigger_waiting:
             who = 0
         else:
             who = trigger_waiting["who"]
         if "change_val" in trigger_waiting:
             change_val = trigger_waiting["change_val"]
         else:
             change_val = 0
         if "null_relate" in trigger_waiting:
             null_relate = trigger_waiting["null_relate"]
         else:
             null_relate = None
         if "move_from" in trigger_waiting:
             move_from = trigger_waiting["move_from"]
         else:
             move_from = None
         if "monster_relate" in trigger_waiting:
             monster_relate = trigger_waiting["monster_relate"]
             place_unique_id_relate = trigger_waiting["place_unique_id_relate"]
             mine_or_other_relate = str(trigger_waiting["mine_or_other_relate"])
             x_relate = trigger_waiting["x_relate"]
             y_relate = trigger_waiting["y_relate"]
             place_relate = trigger_waiting["place_relate"]
             deck_id_relate = trigger_waiting["deck_id_relate"]
         else:
             monster_relate = None
             mine_or_other_relate = None
             x_relate = None
             y_relate = None
             place_relate = None
             deck_id_relate = None
         if "monster_exist" in trigger_waiting:
             monster_exist = trigger_waiting["monster_exist"]
             place_unique_id_exist = trigger_waiting["place_unique_id_exist"]
             mine_or_other_exist = str(trigger_waiting["mine_or_other_exist"])
             x_exist = trigger_waiting["x_exist"]
             y_exist = trigger_waiting["y_exist"]
             place_exist = trigger_waiting["place_exist"]
             deck_id_exist = trigger_waiting["deck_id_exist"]
         else:
             monster_exist = None
             place_unique_id_exist = None
             mine_or_other_exist = None
             x_exist = None
             y_exist = None
             place_exist = None
             deck_id_exist = None
         if "move_from_relate" in trigger_waiting:
             move_from_relate = trigger_waiting["move_from_relate"]
             place_from_relate = trigger_waiting["place_from_relate"]
             deck_id_from_relate = trigger_waiting["deck_id_from_relate"]
             from_x_relate = trigger_waiting["from_x_relate"]
             from_y_relate = trigger_waiting["from_y_relate"]
         else:
             place_from_relate = None
             deck_id_from_relate = None
             from_x_relate = None
             from_y_relate = None
         if "move_from_relate" in trigger_waiting:
             move_from_relate = trigger_waiting["move_from_relate"]
         else:
             move_from_relate = None
         if monster:
             place_unique_id = monster["place_unique_id"]
         else:
             place_unique_id = None
         mine_or_other = str(trigger_waiting["mine_or_other"])
         place = trigger_waiting["place"]
         deck_id = trigger_waiting["deck_id"]
         if "place_from" in trigger_waiting:
             place_from = trigger_waiting["place_from"]
             deck_id_from = trigger_waiting["deck_id_from"]
         else:
             place_from = None
             deck_id_from = None

         x = trigger_waiting["x"]
         y = trigger_waiting["y"]
         if(move_from is None):
             from_x = trigger_waiting["x"]
             from_y = trigger_waiting["y"]
         else:
             from_x = move_from["x"]
             from_y = move_from["y"]
         monster_from = {}
         monster_from["x"] = from_x
         monster_from["y"] = from_y
         monster_from["deck_id"] = deck_id_from
         monster_from["place"] = place_from
         if move_from is not None:
             monster_from["place_unique_id"] = move_from["det"]["place_unique_id"]
             if "user" not in move_from :
                 monster_from["user"] = duelobj.user
             monster_from["mine_or_other"] = move_from["mine_or_other"]
             monster_from["det"] = move_from["det"]
         else:
             monster_from["place_unique_id"] = None
             monster_from["user"] = None
             monster_from["mine_or_other"] = None
             monster_from["det"] = None
         if who == 0:
             if order != 1 and int(mine_or_other) != user:
                 continue
             if not duelobj.check_launch_trigger(
                 trigger,
                 duel.phase,
                 duel.user_turn,
                 user,
                 other_user,
                 mine_or_other,
                 place,
                 place_unique_id,
                 deck_id,
                 x,
                 y,
                 True,
                 move_from,
                 place_from,
                 deck_id_from,
                 from_x,
                 from_y,
                 monster,
                 place_unique_id_exist,
             ):
                 trigger_waitings.remove(trigger_waiting)
                 i+=1
                 #remove_waitings.append(trigger_waiting)
                 if len(trigger_waitings) == 0:
                     duel.in_trigger_waiting = False
                 continue
             else:
                 prompt_monster = monster

         elif who == 1:
             if order != 1 and int(mine_or_other_exist) != user:
                 continue
             if not duelobj.check_launch_trigger(
                     trigger,
                 
                     duel.phase,
                     duel.user_turn,
                     user,
                     other_user,
                     mine_or_other_exist,
                     place_exist,
                     place_unique_id_exist,
                     deck_id_exist,
                     x_exist,
                     y_exist,
                     True
             ):
                 trigger_waitings.remove(trigger_waiting)
                 i+=1
                 #remove_waitings.append(trigger_waiting)

                 if len(trigger_waitings) == 0:
                     duel.in_trigger_waiting = False
                 continue
             else:
                 prompt_monster = monster_exist
         elif who == 2:
             if null_relate is not None:
                 if order != 1 and int(null_relate["mine_or_other"]) != user:
                     continue
                 if not duelobj.check_launch_trigger(
                         trigger,
                         duel.phase,
                         duel.user_turn,
                         user,
                         other_user,
                         null_relate["mine_or_other"],
                         null_relate["place"],
                         null_relate["place_unique_id"],
                         null_relate["deck_id"],
                         null_relate["x"],
                         null_relate["y"],
                         True
                 ):
                     trigger_waitings.remove(trigger_waiting)
                     i+=1
                     #remove_waitings.append(trigger_waiting)
                     if len(trigger_waitings) == 0:
                        duel.in_trigger_waiting = False
                 continue
             elif monster_relate is not None:
                 if order != 1 and int(mine_or_other_relate) != user:
                     continue
                 if not duelobj.check_launch_trigger(
                         trigger,
                         duel.phase,
                         duel.user_turn,
                         user,
                         other_user,
                         mine_or_other_relate,
                         place_relate,
                         place_unique_id_relate,
                         deck_id_relate,
                         x_relate,
                         y_relate,
                         True
                 ):
                    trigger_waitings.remove(trigger_waiting)
                    i+=1
                    #remove_waitings.append(trigger_waiting)

                    prompt_monster = monster_relate
                    if len(trigger_waitings) == 0:
                        duel.in_trigger_waiting = False
                    continue
             else:
                    prompt_monster = monster_relate
         flag = duelobj.invoke_trigger        (
             trigger,
             place,
             monster,
             mine_or_other,
             user,
             deck_id,
             x,
             y,
             monster_from,
             place_from,
             deck_id_from,
             from_x,
             from_y,
             0,
             null_relate,
             change_val,
             place_relate,
             monster_relate,
             mine_or_other_relate,
             deck_id_relate,
             x_relate,
             y_relate,
             move_from_relate,
             place_from_relate,
             deck_id_from_relate,
             from_x_relate,
             from_y_relate,
             place_exist,
             monster_exist,
             mine_or_other_exist,
             deck_id_exist,
             x_exist,
             y_exist,
             who=who,
             waiting = True
         )
         trigger_waitings.remove(trigger_waiting)
         i+=1
         if order == 3:
             break
     '''
     remove_waitings.append(trigger_waiting)
     trigger_waitings2 = json.loads(duel.trigger_waiting)
     for remove_waiting in remove_waitings:
         trigger_waitings2.remove(remove_waiting)
     '''
     duel.trigger_waiting = json.dumps(trigger_waitings)
     if duel.ask == 5:
        duel.ask = 6
     else:
        duel.ask = 5
     if i == 0:
         if duel.already_choosed == 2:
             duel.already_choosed = 1
             duel.trigger_waiting = "[]"
             duel.ask = 0
         else:
             duel.already_choosed = 2
     if len(trigger_waitings) == 0:
             duel.already_choosed = 1
             duel.trigger_waiting = "[]"
             duel.ask = 0
    
