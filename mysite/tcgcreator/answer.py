from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from time import time
from .battle_functions import init_duel
from django.db import connection
import os

from .models import (
    Monster,
    FieldSize,
    Deck,
    Grave,
    Hand,
    Duel,
    Config,
    MonsterEffectWrapper,
    CostWrapper,
    Trigger,
    PacWrapper,
    Lock,
    DefaultDeck,
    UserDeck,
    UserDeckGroup,
    DuelDeck
)
from pprint import pprint
from .battle_det import battle_det
from .choices import lock_lock
from .custom_functions import cheat_get, create_user_deck_det
import json
import copy
from .duel import DuelObj

check_array = []

def cheat2(request):
    room_number = int(request.POST["room_number"])
    user_turn = int(request.POST["user_turn"])
    config = Config.objects.get()
    pwd = os.path.dirname(__file__)
    if config.cheat is False:
        return
    game_name = config.game_name
    if(user_turn == 1):
        log2 = open(pwd + "/logger2_" + game_name, mode="r", encoding="utf-8")
    else:
        log2 = open(pwd + "/logger3_" + game_name, mode="r", encoding="utf-8")
    with connection.cursor() as cursor:
        cursor.execute(log2.read())
    connection.commit()
    duel = Duel.objects.filter(id=room_number).get()
    duelobj = DuelObj(room_number)
    duelobj.duel = duel
    duelobj.room_number = room_number
    duelobj.user = 1
    duelobj.init_all(1, 2, room_number)

    return battle_det(request, duelobj)
def answer_cost(duelobj, duel, request, room_number, lock):
    if duel.guest_flag == False:
        ID1 = -1
    else:
        ID1 = duel.guest_id
    if duel.guest_flag2 == False:
        ID2 = -1
    else:
        ID2 = duel.guest_id2
    if "ID" in request.COOKIES :
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    answer = json.loads(request.POST["answer"])

    if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag):
        if (
            duel.cost_user == 1
            and duel.user_turn == 1
            or duel.cost_user == 2
            and duel.user_turn == 2
        ):
            if duel.ask == 1 or duel.ask == 3:
                return answer_det_cost(
                    duelobj, duel, 1, answer, request, 1, room_number, lock,ID1,ID2
                )
        else:
            if duel.ask == 2 or duel.ask == 3:
                return answer_det_cost(
                    duelobj, duel, 1, answer, request, 2, room_number, lock,ID1,ID2
                )
    elif duel.user_2 == request.user or (ID2 == ID and duel.guest_flag2):  
        if (
            duel.cost_user == 2
            and duel.user_turn == 2
            or duel.cost_user == 1
            and duel.user_turn == 1
        ):
            if duel.ask == 1 or duel.ask == 3:
                return answer_det_cost(
                    duelobj, duel, 2, answer, request, 1, room_number, lock,ID1,ID2
                )
        else:
            if duel.ask == 2 or duel.ask == 3:
                return answer_det_cost(
                    duelobj, duel, 2, answer, request, 2, room_number, lock,ID1,ID2
                )
    free_lock(room_number, lock)
    return HttpResponse("error")


def chooseguestname(request):
    config = Config.objects.get();
    room_time = config.room_time
    limit_time = config.limit_time
    room_number = int(request.POST["room_number"])
    duel = Duel.objects.filter(id=room_number).get()
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
    if ID1 == ID and duel.guest_flag is True:
        user = 1
    elif duel.user_1 is not None and duel.user_1 == request.user:
        user = 1
    elif ID2 == ID and duel.guest_flag2 is True:
        user = 2
    elif duel.user_2 is not None and duel.user_2 == request.user:
        user = 2
    if user == 1 and duel.guest_name != "":
        return HttpResponse("error")
    elif user == 2 and duel.guest_name2 != "":
        return HttpResponse("error")
    if user == 1:
        if time() - duel.time_2 > limit_time * 2:
            duel.winner = user
            duel.save()
            return HttpResponse("time")
        duel.guest_name = format_html(request.POST["guest_name"])
        duel.time_1 = time()
    elif user == 2:
        if time() - duel.time_1 > limit_time * 2:
            duel.winner = user
            duel.save()
            return HttpResponse("time")
        duel.guest_name2 = format_html(request.POST["guest_name"])
        duel.time_2 = time()
    duel.save()
    return HttpResponse("true")
def chooseuserdeck(request):
    config = Config.objects.get();
    room_time = config.room_time
    limit_time = config.limit_time
    room_number = int(request.POST["room_number"])
    duel = Duel.objects.filter(id=room_number).get()
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
    if time() - duel.time_1 > limit_time * 2:
        return HttpResponse("time")
    if ID1 == ID and duel.guest_flag is True:
        user = 1
    elif duel.user_1 is not None and duel.user_1 == request.user:
        user = 1
    elif ID2 == ID and duel.guest_flag2 is True:
        user = 2
    elif duel.user_2 is not None and duel.user_2 == request.user:
        user = 2
    if user == 1 and duel.deck_choose_flag1 is False:
        return HttpResponse("error")
    elif user == 2 and duel.deck_choose_flag2 is False:
        return HttpResponse("error")
    decks = Deck.objects.all()
    user_deck  = int(request.POST["user_deck"])
    user_decks = UserDeck.objects.filter(deck_group__id=user_deck)
    i = 1
    for deck in decks:
        user_deck = user_decks.filter(deck_type=deck).first()
        if not user_deck:
            if not user_decks:
                return HttpResponse("error")
        else:
            user_deck_det = user_deck.deck.split("_")
            user_deck_det = create_user_deck_det(user_deck.deck, i, user)
            if deck.mine_or_other == 1:
                DuelDeck.objects.filter(
                    room_number=room_number, mine_or_other=3, deck_id=i
                ).delete()
                DuelDeck(
                    room_number=room_number,
                    mine_or_other=3,
                    deck_id=i,
                    deck_content=user_deck_det,
                    id=i*100+room_number*10+3

                ).save()
            else:
                DuelDeck.objects.filter(
                    room_number=room_number, mine_or_other=user, deck_id=i
                ).delete()
                DuelDeck(
                    room_number=room_number,
                    mine_or_other=user,
                    deck_id=i,
                    deck_content=user_deck_det,
                    id=i*100+room_number*10+user
                ).save()
        i += 1
    if user == 1:
        duel.deck_choose_flag1 = False
        duel.time_1 = time()
    elif user == 2:
        duel.deck_choose_flag2 = False
        duel.time_2 = time()
    duel.save()
    return HttpResponse("true")
def choosedeck(request):
    config = Config.objects.get();
    room_time = config.room_time
    limit_time = config.limit_time
    room_number = int(request.POST["room_number"])
    duel = Duel.objects.filter(id=room_number).get()
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
    if time() - duel.time_1 > limit_time * 2:
        return HttpResponse("time")
    if ID1 == ID and duel.guest_flag is True:
        user = 1
    elif duel.user_1 is not None and duel.user_1 == request.user:
        user = 1
    elif ID2 == ID and duel.guest_flag2 is True:
        user = 2
    elif duel.user_2 is not None and duel.user_2 == request.user:
        user = 2
    if user == 1 and duel.deck_choose_flag1 is False:
        return HttpResponse("error")
    elif user == 2 and duel.deck_choose_flag2 is False:
        return HttpResponse("error")
    decks = Deck.objects.all()
    default_deck  = request.POST["default_deck"]
    user_decks = DefaultDeck.objects.filter(deck_group__id=default_deck)
    i = 1
    for deck in decks:
        user_deck = user_decks.filter(deck_type=deck).first()
        if not user_deck:
            if not user_decks:
                return HttpResponse("error")
        else:
            user_deck_det = user_deck.deck.split("_")
            user_deck_det = create_user_deck_det(user_deck.deck, i, user)
            if deck.mine_or_other == 1:
                DuelDeck.objects.filter(
                    room_number=room_number, mine_or_other=3, deck_id=i
                ).delete()
                DuelDeck(
                    room_number=room_number,
                    mine_or_other=3,
                    deck_id=i,
                    deck_content=user_deck_det,
                    id=i*100+room_number*10+3

                ).save()
            else:
                DuelDeck.objects.filter(
                    room_number=room_number, mine_or_other=user, deck_id=i
                ).delete()
                DuelDeck(
                    room_number=room_number,
                    mine_or_other=user,
                    deck_id=i,
                    deck_content=user_deck_det,
                    id=i*100+room_number*10+user
                ).save()
        i += 1
    if user == 1:
        duel.deck_choose_flag1 = False
        duel.time_1 = time()
    elif user == 2:
        duel.deck_choose_flag2 = False
        duel.time_2 = time()
    duel.save()
    return HttpResponse("true")
def chooseai(request):
    config = Config.objects.get();
    room_time = config.room_time
    limit_time = config.limit_time
    room_number = int(request.POST["room_number"])
    duel = Duel.objects.filter(id=room_number).get()
    if duel.guest_flag is False:
        ID1 = -1
    else:
        ID1 = duel.guest_id
    if "ID" in request.COOKIES :
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    if time() - duel.time_1 > limit_time * 2:
        return HttpResponse("time")
    if ID1 != ID and duel.user_1 != request.user:
        return HttpResponse("error")
    default_deck  = request.POST["default_deck"]
    if(default_deck == "-1"):
        default_deck = None
    #user_deck = request.POST["user_deck"]
    #if(user_deck == "-1"):
    user_deck = None
    enemy_deck = request.POST["enemy_deck"]
    if(init_duel(room_number,request.user,default_deck,enemy_deck,False,False,False,user_deck,1)):
        return HttpResponse("error")
    else:
        return HttpResponse("true")
def cheat(request):
    room_number = int(request.POST["room_number"])
    duel = Duel.objects.filter(id=room_number).get()
    if duel.guest_flag == False:
        ID1 = -1
    else:
        ID1 = duel.guest_id
    if duel.guest_flag2 == False:
        ID2 = -1
    else:
        ID2 = duel.guest_id2
    if "ID" in request.COOKIES :
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    place = request.POST["place"]
    deck_id = int(request.POST["deck_id"])
    monster_id = request.POST["monster_id"].split("_")
    if len(monster_id) >=2:
        bottom = True
    else:
        bottom = False
    id = int(monster_id[0])
    mine_or_other = int(request.POST["mine_or_other"])
    config = Config.objects.get()
    if config.cheat is False:
        return
    duelobj = DuelObj(room_number)
    duelobj.duel = duel
    duelobj.room_number = room_number
    if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag is True):
        user = 1
        duelobj.user = 1
        other_user = 2
    elif duel.user_2 == request.user or (ID2 == ID and duel.guest_flag2 is True):
        user = 2
        duelobj.user = 2
        other_user = 1
    duelobj.init_all(user, other_user, room_number)
    if mine_or_other == 2:
        owner = other_user
    else:
        owner = user
    card = cheat_get(id, deck_id, owner, place)
    if place == "deck":
        if mine_or_other == 1:
            deck = duelobj.decks[deck_id]["mydeck"]
        elif mine_or_other == 2:
            deck = duelobj.decks[deck_id]["otherdeck"]
        else:
            deck = duelobj.decks[deck_id]["commondeck"]
        user_decks = deck
        if bottom == True:
            user_decks.append(card)
        else:
            user_decks.insert(0, card)
        if mine_or_other == 1:
            duelobj.decks[deck_id]["mydeck"] = user_decks
        elif mine_or_other == 2:
            duelobj.decks[deck_id]["otherdeck"] = user_decks
        else:
            duelobj.decks[deck_id]["commondeck"] = user_decks
    elif place == "grave":
        if mine_or_other == 1:
            grave = duelobj.graves[deck_id]["mygrave"]
        elif mine_or_other == 2:
            grave = duelobj.graves[deck_id]["othergrave"]
        else:
            grave = duelobj.graves[deck_id]["commongrave"]
        user_graves = grave
        if bottom == True:
            user_graves.append( card)
        else:
            user_graves.insert(0, card)
        if mine_or_other == 1:
            duelobj.graves[deck_id]["mygrave"] = user_graves
        elif mine_or_other == 2:
            duelobj.graves[deck_id]["othergrave"] = user_graves
        else:
            duelobj.graves[deck_id]["commongrave"] = user_graves
    elif place == "hand":
        if mine_or_other == 1:
            hand = duelobj.hands[deck_id]["myhand"]
        elif mine_or_other == 2:
            hand = duelobj.hands[deck_id]["otherhand"]
        else:
            hand = duelobj.hands[deck_id]["commonhand"]
        user_hands = hand
        if bottom == True:
            user_hands.append( card)
        else:
            user_hands.insert(0, card)
        if mine_or_other == 1:
            duelobj.hands[deck_id]["myhand"] = user_hands
        elif mine_or_other == 2:
            duelobj.hands[deck_id]["otherhand"] = user_hands
        else:
            duelobj.hands[deck_id]["commonhand"] = user_hands
    duelobj.save_all(user, other_user, room_number)
    return battle_det(request, duelobj)


def cancel(request):
    room_number = int(request.POST["room_number"])
    lock = Lock.objects.get()
    lock_flag = lock_lock(room_number, lock,request)
    if lock_flag != "OK":
        return HttpResponse("waiting")
    duel = Duel.objects.filter(id=room_number).get()
    duelobj = DuelObj(room_number)
    duelobj.duel = duel
    duelobj.room_number = room_number
    ID1 = duel.guest_id
    ID2 = duel.guest_id2
    if "ID" in request.COOKIES :
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    if request.user != duel.user_1 and request.user != duel.user_2 :
        if (ID1 == ID and duel.guest_flag) or (ID2 == ID and duel.guest_flag2):
            pass
        else:
            free_lock(room_number, lock)
            return HttpResponse("Please Login")
    if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag): 
        user = 1
        duelobj.user = 1
        other_user = 2
    else:
        duelobj.user = 2
        user = 2
        other_user = 1
    duelobj.init_all(user, other_user, room_number)
    if duel.in_cost is False or duel.in_trigger_waiting is True or duel.in_cost_cancel is False or duel.in_cost_force is True:
        free_lock(room_number, lock)
        return HttpResponse("error")
    if duel.in_cost == 1 or duel.in_cost is True:
        in_pac = json.loads(duel.in_pac)
        in_pac[str(duel.chain - 1)] = []
        duel.in_cost = False
        duelobj.in_execute = False
        cost = duelobj.cost
        if duel.chain == 0:
            del cost[str(duelobj.tmp_chain)]
        elif duel.chain >0:
            del cost[str(duel.chain)]
        duelobj.cost = cost
        duelobj.cost_result = {}
        '''
        if duel.chain > 0:
            chain_det_trigger_json = json.loads(duel.chain_det_trigger)
            del chain_det_trigger_json[str(duel.chain)]
            duel.chain_det_trigger = json.dumps(chain_det_trigger_json)
            trigger_id = chain_det_trigger_json[str(duel.chain - 1)]
            trigger = Trigger.objects.get(id=trigger_id)
            if trigger.pac:
                in_pac[str(duel.chain - 1)].append(trigger.pac.id)
                duel.in_pac = json.dumps(in_pac)
        '''

    duel.in_pac_cost = "[]"
    duel.cost_log = ""
    duel.ask = 0
    duel.canbechained = True
    duel.tmponce_per_turn1  = ""           
    duel.tmponce_per_turn_group1 = ""
    duel.tmponce_per_turn_group2 = ""
    duel.tmponce_per_turn2 = ""
    duel.tmponce_per_turn_monster1 = ""
    duel.tmponce_per_turn_monster2 = ""
    duel.tmponce_per_turn_exist1 = ""
    duel.tmponce_per_turn_exist2 = ""
    duel.tmponce_per_turn_relate1 = ""
    duel.tmponce_per_turn_relate2 = ""
    duelobj.save_all(user, other_user, room_number)
    free_lock(room_number, lock)
    return HttpResponse("OK")


def none(request):
    room_number = int(request.POST["room_number"])
    lock = Lock.objects.get()
    lock_flag = lock_lock(room_number, lock,request)
    if lock_flag != "OK":
        return HttpResponse("waiting")
    duel = Duel.objects.filter(id=room_number).get()
    decks = Deck.objects.all()
    graves = Grave.objects.all()
    hands = Hand.objects.all()
    if duel.ask > 0:
        free_lock(room_number, lock)
        return HttpResponse("error")
    duelobj = DuelObj(room_number)
    duelobj.duel = duel
    duelobj.room_number = room_number
    if "ID" in request.COOKIES :
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    ID1 = duel.guest_id
    ID2 = duel.guest_id2
    if request.user != duel.user_1 and request.user != duel.user_2 :
        if (ID1 == ID and duel.guest_flag) or (ID2 == ID and duel.guest_flag2):
            pass
        else:
            free_lock(room_number, lock)
            return HttpResponse("Please Login")
    if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag):
        user = 1
        duelobj.user = 1
        other_user = 2
    else:
        duelobj.user = 2
        user = 2
        other_user = 1
    duelobj.init_all(user, other_user, room_number)
    duelobj.check_eternal_effect(
        duelobj.decks,
        duelobj.graves,
        duelobj.hands,
        duel.phase,
        duel.user_turn,
        user,
        other_user,
    )
    chain_user = duelobj.get_current_chain_user()
    choices = duelobj.check_trigger(
        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
    choices2 = duelobj.check_trigger(
        decks, graves, hands, duel.phase, duel.user_turn, other_user, user
    )
    if duel.in_cost is True:
        free_lock(room_number, lock)
        return HttpResponse("error")
    if duel.user_1 != request.user and duel.user_2 != request.user:
        if (ID1 == ID and duel.guest_flag) or (ID2 == ID and duel.guest_flag2):
            pass
        else:
            free_lock(room_number, lock)
            return HttpResponseRedirect(reverse("tcgcreator:watch_battle"))
    if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag):
        user = 1
        other_user = 2
        if duel.appoint != 1:
            free_lock(room_number, lock)
            return HttpResponse("error")
        if duel.none == False:
            duel.appoint = 2
            duel.none = True
            duel.timing_fresh = False
        else:
            duel.current_priority = max(choices[1], choices2[1])
            duel.appoint = 2
            duel.none = False
            if duel.is_ai is True:
                duel.timing_fresh = False
        duelobj.save_all(user, other_user, room_number)
    if duel.user_2 == request.user or (ID2 == ID and duel.guest_flag2):
        user = 2
        other_user = 1
        if duel.appoint != 2:
            free_lock(room_number, lock)
            return HttpResponse("error")
        if duel.none == False:
            duel.appoint = 1
            duel.none = True
            duel.timing_fresh = False
        else:
            duel.current_priority = max(choices[1], choices2[1])
            duel.appoint = 1
            duel.none = False
            if duel.is_ai is True:
                duel.timing_fresh = False
        '''
        if duel.chain == 0 and duel.user_turn == user:
            if choices2[0] is None:
                duel.current_priority = max(choices[1], choices2[1])
            duel.appoint = 1
        elif duel.chain > 0 and chain_user != user:
            if choices2[0] is None or choices2[1] :
                duel.current_priority = max(choices[1], choices2[1])
            duel.appoint = 1
        elif duel.user_turn == user:
            duel.current_priority = max(choices[1], choices2[1])
            duel.appoint = 1
        else:
            duel.current_priority = max(choices[1], choices2[1])
            duel.appoint = 1
        '''
        duelobj.save_all(user, other_user, room_number)
    free_lock(room_number, lock)
    data = {}
    data["sound_effect"] = duelobj.sound_effect
    data["OK"] = True
    return HttpResponse(json.dumps(data))


def multiple_answer_det(
    duelobj, duel, user, answer_json, request, del_ask, room_number, lock
):
    global check_array
    if "ID" in request.COOKIES :
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    ID1 = duel.guest_id
    ID2 = duel.guest_id2
    answer = json.loads(answer_json)
    room_number = int(request.POST["room_number"])
    chain_det = json.loads(duel.chain_det)
    chain_user = json.loads(duel.chain_user)
    chain_user = int(chain_user[str(duel.chain - 1)])
    if duel.in_copying is True:
        duelobj.tmp_chain = str(duel.chain - 1)
    else:
        duelobj.tmp_chain = str(duel.chain)
    if chain_user == 0:
        if request.user == duel.user_1 or (ID1 == ID and duel.guest_flag):
            chain_user = 1
        else:
            chain_user = 2
    if user == 1:
        other_user = 2
    else:
        other_user = 1
    monster_effect_wrapper = MonsterEffectWrapper.objects.get(
        id=int(chain_det[str(duel.chain - 1)])
    )
    monster_effect = monster_effect_wrapper.monster_effect
    monster_condition = monster_effect.monster_condition
    if monster_condition != "":
        monster_condition = json.loads(monster_condition)
        monster_condition = monster_condition["monster"][0]["monster"]

    monster_effect_text = json.loads(monster_effect.monster_effect)
    if "double" not in monster_effect_text or monster_effect_text["double"] is False:
        for tmp in answer:
            for tmp3 in tmp:
                if tmp.count(tmp3) > 2:
                    return HttpResponse("error")
    exclude = monster_effect_text["exclude"]
    if "whether_monster" in monster_effect_text:
        whether_monster = monster_effect_text["whether_monster"]
    effect_kind = monster_effect_wrapper.monster_effect_kind
    to_effect_kind = monster_effect_text["multiple_effect_kind"]
    from_monster_effect_det = monster_effect_text["monster"][0]
    to_monster_effect_det = monster_effect_text["monster"][1]
    from_monster_effect_det_monster = from_monster_effect_det["monster"]
    to_monster_effect_det_monster = to_monster_effect_det["monster"]
    i = 0
    field = duel.field
    to_monsters = []
    if (
        "as_monster_condition" in to_monster_effect_det
        and to_monster_effect_det["as_monster_condition"] != ""
    ):
        as_monsters = to_monster_effect_det["as_monster_condition"]
        if not isinstance(as_monsters, list):
            tmp_monster = []
            tmp_monster.append(as_monsters)
            as_monsters = tmp_monster
        for as_monster in as_monsters:
            if as_monster[0] == "~":
                tmp = duelobj.cost
                tmp = tmp[str(int(duel.chain))]
                place1 = tmp[as_monster]
            elif as_monster[0] == "%":
                tmp = duelobj.timing_mess
                place1 = tmp[as_monster]
            else:
                tmp = duelobj.mess
                tmp = tmp[str(int(duel.chain - 1))]
                place1 = tmp[as_monster]
            for place2 in place1:
                place2["place_unique_id"] = place2["det"]["place_unique_id"]
    else:
        place_array_tmp = []
        for place in to_monster_effect_det_monster["place"]:
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
                mine_or_other = 1
            elif place_tmp[2] == "2":
                mine_or_other = 2
            elif place_tmp[2] == "3":
                mine_or_other = 3
            if user == 1:
                mine_or_other2 = mine_or_other
            else:
                if mine_or_other == 1:
                    mine_or_other2 = 2
                elif mine_or_other == 2:
                    mine_or_other2 = 1
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
                    to_monsters.append(tmp2)
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
                    to_monsters.append(tmp2)
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
                    to_monsters.append(tmp2)
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
                                
                        current_and_or = and_or
                        if flag_field_place is False:
                            continue
                        if field[x][y]["mine_or_other"] not in mine_or_others:
                            continue
                        if field[x][y]["det"] is not None:
                            if duelobj.check_not_effected(
                                field[x][y]["det"],
                                user,
                                to_effect_kind,
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
                            tmp2["user"] = chain_user
                            tmp2["place"] = "field"
                            tmp2["deck_id"] = 0
                            tmp2["x"] = x
                            tmp2["y"] = y
                            tmp2["place_unique_id"] = field[x][y]["det"][
                                "place_unique_id"
                            ]

                            if not duelobj.validate_answer(
                                tmp2,
                                to_monster_effect_det["monster"],
                                exclude,
                                duel,
                                1,
                                0,
                                effect_kind,
                                user,
                            ):

                                continue
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
                            to_monsters.append(tmp2)
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
                            tmp2["place_unique_id"] = field[x][y]["det"][
                                "place_unique_id"
                            ]
                            tmp2["place"] = "field"
                            to_monsters.append(tmp2)
    to_monsters = copy.deepcopy(to_monsters)
    for key in range(len(to_monsters)):
        to_monsters[key]["det"]["rel"] = None
    if (
        "as_monster_condition" in from_monster_effect_det
        and from_monster_effect_det["as_monster_condition"] != ""
    ):
        relation_name = from_monster_effect_det_monster["relation"][0]
        relation_to = int(from_monster_effect_det_monster["relation_to"][0])
        relation_kind = from_monster_effect_det_monster["relation_kind"][0]
        if relation_to == 0:
            relation_from = 1
        elif relation_to == 1:
            relation_from = 0
        as_monsters = from_monster_effect_det["as_monster_condition"]
        if not isinstance(as_monsters, list):
            tmp_monster = []
            tmp_monster.append(as_monsters)
            as_monsters = tmp_monster
        for as_monster in as_monsters:
            if as_monster[0] == "~":
                tmp = duelobj.cost
                tmp = tmp[str(int(duel.chain))]
                tmp = duelobj.timing_mess
                if as_monster in tmp:
                    place1 = tmp[as_monster]
                else:
                    place1 = []
            elif as_monster[0] == "%":
                tmp = duelobj.timing_mess
                if as_monster in tmp:
                    place1 = tmp[as_monster]
                else:
                    place1 = []
            else:
                tmp = duelobj.mess
                tmp = tmp[str(int(duel.chain - 1))]
                if as_monster in tmp:
                    place1 = tmp[as_monster]
                else:
                    place1 = []
            for place2 in place1:
                if not duelobj.validate_answer(
                    place2, monster_condition, "", duel, 1, 0, effect_kind, user
                ):
                    continue
                if place2["place"] == "field":
                    x = place2["x"]
                    y = place2["y"]
                    if "rel" not in field[x][y]["det"]:
                        field[x][y]["det"]["rel"] = {}
                    if relation_kind not in field[x][y]["det"]["rel"]:
                        field[x][y]["det"]["rel"][relation_kind] = []

                    for tmp in answer[i]:
                        tmp2 = {}
                        tmp2["monster"] = to_monsters[int(tmp)]
                        tmp2["to"] = relation_to
                        tmp2["name"] = relation_name
                        field[x][y]["det"]["rel"][relation_kind].append(tmp2)
                        duelobj.field = field
                        tmp2 = {}
                        tmp2["det"] = field[x][y]["det"]
                        tmp2["mine_or_other"] = field[x][y]["mine_or_other"]
                        tmp2["user"] = user
                        tmp2["place"] = "field"
                        tmp2["deck_id"] = 0
                        tmp2["x"] = x
                        tmp2["y"] = y
                        tmp2["place_unique_id"] = field[x][y]["det"]["place_unique_id"]
                        duelobj.set_relation(
                            relation_name,
                            to_monsters[int(tmp)],
                            relation_kind,
                            relation_from,
                            tmp2,
                            to_monsters[int(tmp)]["det"]["place_unique_id"],
                            x,
                            y,
                            0,
                        )
                i += 1
    else:
        relation_name = from_monster_effect_det_monster["relation"][0]
        relation_to = int(from_monster_effect_det_monster["relation_to"][0])
        relation_kind = from_monster_effect_det_monster["relation_kind"][0]
        if relation_to == 0:
            relation_from = 1
        elif relation_to == 1:
            relation_from = 0
        place_array_tmp = []
        for place in from_monster_effect_det_monster["place"]:
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
            place_tmp = place["det"].split("_")
            if place_tmp[2] == "1":
                mine_or_other = 1
            elif place_tmp[2] == "2":
                mine_or_other = 2
            elif place_tmp[2] == "3":
                mine_or_other = 3
            if user == 1:
                mine_or_other = mine_or_other2
            else:
                if mine_or_other == 1:
                    mine_or_other2 = 2
                elif mine_or_other == 2:
                    mine_or_other2 = 1
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
                for key in range(len(user_decks)):
                    if "rel" not in user_decks[key]:
                        user_decks[key]["rel"] = {}
                    if relation_kind not in user_decks[key]["rel"]:
                        user_decks[key]["rel"][relation_kind] = []
                    for tmp in answer[i]:
                        tmp2 = {}
                        tmp2["monster"] = to_monsters[int(tmp)]
                        tmp2["to"] = relation_to
                        tmp2["name"] = relation_name
                        user_decks[key]["rel"][relation_kind].append(tmp2)
                        tmp2 = {}
                        tmp2["det"] = user_decks[key]
                        tmp2["mine_or_other"] = mine_or_other
                        tmp2["user"] = user
                        tmp2["place"] = "deck"
                        tmp2["deck_id"] = deck_id
                        tmp2["x"] = 0
                        tmp2["y"] = 0
                        tmp2["place_unique_id"] = user_decks[key]["place_unique_id"]
                        duelobj.set_relation(
                            relation_name,
                            to_monsters[int(tmp)],
                            relation_kind,
                            relation_from,
                            tmp2,
                            to_monsters[int(tmp)]["place_unique_id"],
                            0,
                            0,
                            deck_id,
                        )
                    i += 1
                if mine_or_other2 == 1:
                    duelobj.decks[deck_id]["mydeck"] = user_decks
                elif mine_or_other2 == 2:
                    duelobj.decks[deck_id]["otherdeck"] = user_decks
                elif mine_or_other2 == 3:
                    duelobj.decks[deck_id]["commondeck"] = user_decks
            elif place_tmp[0] == "grave":
                if mine_or_other2 == 1:
                    grave = duelobj.graves[deck_id]["mygrave"]
                elif mine_or_other2 == 2:
                    grave = duelobj.graves[deck_id]["othergrave"]
                elif mine_or_other2 == 3:
                    grave = duelobj.graves[deck_id]["commongrave"]
                user_graves = grave
                for key in range(len(user_graves)):
                    if "rel" not in user_graves[key]:
                        user_graves[key]["rel"] = {}
                    if relation_kind not in user_graves[key]["rel"]:
                        user_graves[key]["rel"][relation_kind] = []
                    for tmp in answer[i]:
                        tmp2 = {}
                        tmp2["monster"] = to_monsters[int(tmp)]
                        tmp2["to"] = relation_to
                        tmp2["name"] = relation_name
                        user_graves[key]["rel"][relation_kind].append(tmp2)
                        tmp2 = {}
                        tmp2["det"] = user_graves[key]
                        tmp2["mine_or_other"] = mine_or_other
                        tmp2["user"] = user
                        tmp2["place"] = "deck"
                        tmp2["deck_id"] = deck_id
                        tmp2["x"] = 0
                        tmp2["y"] = 0
                        tmp2["place_unique_id"] = user_graves[key]["place_unique_id"]
                        duelobj.set_relation(
                            relation_name,
                            to_monsters[int(tmp)],
                            relation_kind,
                            relation_from,
                            tmp2,
                            to_monsters[int(tmp)]["place_unique_id"],
                            0,
                            0,
                            deck_id,
                        )
                    i += 1
                if mine_or_other2 == 1:
                    duelobj.graves[deck_id]["mygrave"] = user_graves
                elif mine_or_other2 == 2:
                    duelobj.graves[deck_id]["othergrave"] = user_graves
                elif mine_or_other2 == 3:
                    duelobj.graves[deck_id]["commongrave"] = user_graves
            elif place_tmp[0] == "hand":
                if mine_or_other2 == 1:
                    hand = duelobj.hands[deck_id]["myhand"]
                elif mine_or_other2 == 2:
                    hand = duelobj.hands[deck_id]["otherhand"]
                elif mine_or_other2 == 3:
                    hand = duelobj.hands[deck_id]["commonhand"]
                user_hands = hand
                for key in range(len(user_hands)):
                    if "rel" not in user_hands[key]:
                        user_hands[key]["rel"] = {}
                    if relation_kind not in user_hands[key]["rel"]:
                        user_hands[key]["rel"][relation_kind] = []
                    for tmp in answer[i]:
                        tmp2 = {}
                        tmp2["monster"] = to_monsters[int(tmp)]
                        tmp2["to"] = relation_to
                        tmp2["name"] = relation_name
                        user_hands[key]["rel"][relation_kind].append(tmp2)
                        tmp2["det"] = user_hands[key]
                        tmp2["mine_or_other"] = mine_or_other
                        tmp2["user"] = user
                        tmp2["place"] = "deck"
                        tmp2["deck_id"] = deck_id
                        tmp2["x"] = 0
                        tmp2["y"] = 0
                        tmp2["place_unique_id"] = user_hands[key]["place_unique_id"]
                        duelobj.set_relation(
                            relation_name,
                            to_monsters[int(tmp)],
                            relation_kind,
                            relation_from,
                            tmp2,
                            to_monsters[int(tmp)]["place_unique_id"],
                            0,
                            0,
                            deck_id,
                        )
                    i += 1
                if mine_or_other2 == 1:
                    duelobj.hands[deck_id]["myhand"] = user_hands
                elif mine_or_other2 == 2:
                    duelobj.hands[deck_id]["otherhand"] = user_hands
                elif mine_or_other2 == 3:
                    duelobj.hands[deck_id]["commonhand"] = user_hands
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
                            current_and_or = and_or
                        if flag_field_place is False:
                            continue
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
                        if field[x][y]["mine_or_other"] != mine_or_other:
                            continue
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
                        tmp2["user"] = chain_user
                        tmp2["place"] = "field"
                        tmp2["deck_id"] = 0
                        tmp2["x"] = x
                        tmp2["y"] = y
                        tmp2["place_unique_id"] = field[x][y]["det"]["place_unique_id"]

                        if not duelobj.validate_answer(
                            tmp2,
                            to_monster_effect_det["monster"],
                            exclude,
                            duel,
                            1,
                            0,
                            effect_kind,
                            user,
                        ):

                            continue
                        if whether_monster == 0:
                            if field[x][y]["det"] is not None:
                                continue
                            if "rel" not in field[x][y]:
                                field[x][y]["rel"] = {}
                            if relation_kind not in field[x][y]["det"]["rel"]:
                                field[x][y]["rel"][relation_kind] = []
                            for tmp in answer[i]:
                                tmp2 = {}
                                tmp2["monster"].append(to_monsters[int(tmp)])
                                tmp2["to"] = relation_to
                                tmp2["name"] = relation_name
                                field[x][y]["rel"][relation_kind].append(tmp2)
                                tmp2 = {}
                                tmp2["det"] = None
                                tmp2["mine_or_other"] = field[x][y]["mine_or_other"]
                                tmp2["user"] = user
                                tmp2["place"] = "field"
                                tmp2["deck_id"] = 0
                                tmp2["x"] = x
                                tmp2["y"] = y
                                tmp2["place_unique_id"] = 0
                                duelobj.set_relation(
                                    relation_name,
                                    to_monsters[int(tmp)],
                                    relation_kind,
                                    relation_from,
                                    tmp2,
                                    0,
                                    x,
                                    y,
                                    0,
                                )
                            i += 1

                        else:
                            if field[x][y]["det"] is None:
                                continue
                            if "rel" not in field[x][y]["det"]:
                                field[x][y]["det"]["rel"] = {}
                            if relation_kind not in field[x][y]["det"]["rel"]:
                                field[x][y]["det"]["rel"][relation_kind] = []
                            for tmp in answer[i]:
                                tmp2 = {}
                                tmp2["monster"] = to_monsters[int(tmp)]
                                tmp2["to"] = relation_to
                                tmp2["name"] = relation_name
                                field[x][y]["det"]["rel"][relation_kind].append(tmp2)
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
                                duelobj.set_relation(
                                    relation_name,
                                    to_monsters[int(tmp)],
                                    relation_kind,
                                    relation_from,
                                    tmp2,
                                    field[x][y]["det"]["place_unique_id"],
                                    x,
                                    y,
                                    0,
                                )
                            i += 1
    duel.field = field
    duel.ask -= del_ask
    choices = None
    if duel.ask == 0:
        chain_det = json.loads(duel.chain_det)
        current_chain = chain_det[str(duel.chain - 1)]
        effect = MonsterEffectWrapper.objects.get(id=current_chain)
        if effect.pac:
            next_effect = duelobj._pac(effect.pac)
        else:
            next_effect = effect.monster_effect_next
        if next_effect != 0 and next_effect is not None:
            chain_det[str(duel.chain - 1)] = next_effect.id
        else:
            pac = json.loads(duel.in_pac)
            if str(duel.chain - 1) in pac and pac[str(duel.chain - 1)] != []:
                pac_id = pac[str(duel.chain - 1)].pop()
                duel.in_pac = json.dumps(pac)
                pac = PacWrapper.objects.get(id=pac_id)
                next_effect = pac.monster_effect_next
                if next_effect is None:
                    trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
                    if trigger.chain_flag is True:
                        duel.virtual_chain -= 1
                    duel.chain -= 1
                else:
                    chain_det[str(duel.chain - 1)] = next_effect.id
            else:
                trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
                if trigger.chain_flag is True:
                    duel.virtual_chain -= 1
                duel.chain -= 1
        duel.chain_det = json.dumps(chain_det)
        decks = Deck.objects.all()
        graves = Grave.objects.all()
        hands = Hand.objects.all()
        duelobj.check_eternal_effect(
            decks, graves, hands, duel.phase, duel.user_turn, user, other_user
        )
        duelobj.retrieve_chain(
            decks, graves, hands, duel.phase, duel.user_turn, user, other_user
        )
        if duel.chain == 0:
            duelobj.invoke_after_chain_effect(
                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
            )
            duel.appoint = duel.user_turn
            tmp = {}
            duel.mess = json.dumps(tmp)
            duel.cost_result = json.dumps(tmp)
            duel.cost = json.dumps(tmp)
            duelobj.invoke_trigger_waiting(duel.trigger_waiting)
            duel.current_priority = 10000
            choices = duelobj.check_trigger(
                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
            )
    # if monster_effect.monster_condition != "":
    #    if not check_condition(duel,monster_effect.monster_condition,duelobj):
    #        return HttpResponse("error")
    duelobj.save_all(user, other_user, room_number)
    free_lock(room_number, lock)
    return battle_det(request, duelobj, choices)


def multiple_answer(request):
    room_number = int(request.POST["room_number"])
    lock = Lock.objects.get()
    lock_flag = lock_lock(room_number, lock,request)
    if lock_flag != "OK":
        return HttpResponse("waiting")
    duelobj = DuelObj(room_number)
    duel = Duel.objects.filter(id=room_number).get()
    if "ID" in request.COOKIES :
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    ID1 = duel.guest_id
    ID2 = duel.guest_id2
    if duel.user_1 != request.user and duel.user_2 != request.user:
        if (ID1 == ID and duel.guest_flag) or (ID2 == ID and duel.guest_flag2):
            pass
        else:
            free_lock(room_number, lock)
            return HttpResponseRedirect(reverse("tcgcreator:watch_battle"))
    duelobj.duel = duel
    duelobj.room_number = room_number
    if duel.user_1 == request.user or ( ID1 == ID and duel.guest_flag):
        user = 1
        other_user = 2
        duelobj.user = 1
    else:
        duelobj.user = 2
        user = 2
        other_user = 1
    duelobj.init_all(user, other_user, room_number)
    decks = Deck.objects.all()
    graves = Grave.objects.all()
    hands = Hand.objects.all()
    duelobj.check_eternal_effect(
        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
    answer = request.POST["answer"]
    if duel.user_1 == request.user or ( ID1 == ID and duel.guest_flag):
        if duel.user_turn == 1:
            if duel.ask == 1 or duel.ask == 3:
                return_value = multiple_answer_det(
                    duelobj, duel, 1, answer, request, 1, room_number, lock
                )
                free_lock(room_number, lock)
                return return_value
        else:
            if duel.ask == 2 or duel.ask == 3:
                return_value = multiple_answer_det(
                    duelobj, duel, 1, answer, request, 2, room_number, lock
                )
                free_lock(room_number, lock)
                return return_value
    elif duel.user_2 == request.user or ( ID2 == ID and duel.guest_flag2):
        if duel.user_turn == 2:
            if duel.ask == 1 or duel.ask == 3:
                return_value = multiple_answer_det(
                    duelobj, duel, 2, answer, request, 1, room_number, lock
                )
                free_lock(room_number, lock)
                return return_value
        else:
            if duel.ask == 2 or duel.ask == 3:
                return_value = multiple_answer_det(
                    duelobj, duel, 2, answer, request, 2, room_number, lock
                )
                free_lock(room_number, lock)
                return return_value
    free_lock(room_number, lock)
    return HttpResponse("error")


def answerorder(request):
    room_number = int(request.POST["room_number"])
    lock = Lock.objects.get()
    lock_flag = lock_lock(room_number, lock,request)
    if lock_flag != "OK":
        return HttpResponse("waiting")
    duelobj = DuelObj(room_number)
    duel = Duel.objects.filter(id=room_number).get()
    if "ID" in request.COOKIES :
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    ID1 = duel.guest_id
    ID2 = duel.guest_id2
    if duel.user_1 != request.user and duel.user_2 != request.user:
        if (ID1 == ID and duel.guest_flag) or (ID2 == ID and duel.guest_flag2):
            pass
        else:
            free_lock(room_number, lock)
            return HttpResponseRedirect(reverse("tcgcreator:watch_battle"))
    duelobj.duel = duel
    duelobj.room_number = room_number
    if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag == True):
        user = 1
        other_user = 2
        duelobj.user = 1
    else:
        duelobj.user = 2
        user = 2
        other_user = 1
    if duel.user_turn == 1:
        if user == 1 and duel.ask != 1:
            free_lock(room_number, lock)
            return HttpResponse("error")
        elif user == 2 and duel.ask != 2:
            free_lock(room_number, lock)
            return HttpResponse("error")
    else:
        if user == 2 and duel.ask != 1:
            free_lock(room_number, lock)
            return HttpResponse("error")
        elif user == 1 and duel.ask != 2:
            free_lock(room_number, lock)
            return HttpResponse("error")
    duelobj.init_all(user, other_user, room_number)
    duelobj.in_execute = False
    acc = duelobj.acc_global
    order = request.POST["order"].split("_")
    if len(acc) != len(order):
        free_lock(room_number, lock)
        return HttpResponse("error")
    for tmp in order:
        if int(tmp) >= len(order):
            free_lock(room_number, lock)
            return HttpResponse("error")
        if order.count(tmp) > 1:
            free_lock(room_number, lock)
            return HttpResponse("error")
    dummy_list = []
    for tmp in order:
        dummy_list.append(acc[int(tmp)])
    duel.ask = 0
    if duel.ask == 0:
        chain_det = json.loads(duel.chain_det)
        current_chain = chain_det[str(duel.chain - 1)]
        effect = MonsterEffectWrapper.objects.get(id=current_chain)
        if effect.pac:
            next_effect = duelobj._pac(effect.pac)
        else:
            next_effect = effect.monster_effect_next
        if next_effect != 0 and next_effect is not None:
            chain_det[str(duel.chain - 1)] = next_effect.id
        else:
            pac = json.loads(duel.in_pac)
            if str(duel.chain - 1) in pac and pac[str(duel.chain - 1)] != []:
                pac_id = pac[str(duel.chain - 1)].pop()
                pac = PacWrapper.objects.get(id=pac_id)
                next_effect = pac.monster_effect_next
                if next_effect is None:
                    Trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
                    if trigger.chain_flag is True:
                        duel.virtual_chain -= 1
                    duel.chain -= 1
                else:
                    chain_det[str(duel.chain - 1)] = next_effect.id
            else:
                Trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
                if trigger.chain_flag is True:
                    duel.virtual_chain -= 1
                duel.chain -= 1
        duelobj.duel.chain_det = json.dumps(chain_det)
    duelobj.acc_global = dummy_list
    duelobj.save_all(user, other_user, room_number)
    free_lock(room_number, lock)
    return battle_det(request, duelobj)


def answer(request):
    global check_array
    room_number = int(request.POST["room_number"])
    lock = Lock.objects.get()
    lock_flag = lock_lock(room_number, lock,request)
    if lock_flag != "OK":
        return HttpResponse("waiting")
    duelobj = DuelObj(room_number)
    check_array = []
    duel = Duel.objects.filter(id=room_number).get()
    if "ID" in request.COOKIES :
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    ID1 = duel.guest_id
    ID2 = duel.guest_id2
    if duel.user_1 != request.user and duel.user_2 != request.user:
        if (ID1 == ID and duel.guest_flag) or (ID2 == ID and duel.guest_flag2):
            pass
        else:
            free_lock(room_number, lock)
            return HttpResponseRedirect(reverse("tcgcreator:watch_battle"))
    duelobj.duel = duel
    duelobj.room_number = room_number
    if duel.user_1 == request.user or (ID == ID1 and duel.guest_flag):
        user = 1
        other_user = 2
        duelobj.user = 1
    else:
        duelobj.user = 2
        user = 2
        other_user = 1
    duelobj.init_all(user, other_user, room_number)
    duelobj.in_execute = False
    decks = Deck.objects.all()
    graves = Grave.objects.all()
    hands = Hand.objects.all()
    duelobj.check_eternal_effect(
        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
    if duel.in_cost:
        return answer_cost(duelobj, duel, request, room_number, lock)
    answer = request.POST["answer"]

    if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag is True):
        if duel.user_turn == 1:
            if duel.ask == 1 or duel.ask == 3:
                return_value = answer_det(duelobj, duel, 1, answer, request, 1, lock,ID1,ID2)
                free_lock(room_number, lock)
                return return_value
        else:
            if duel.ask == 2 or duel.ask == 3:
                return_value = answer_det(duelobj, duel, 1, answer, request, 2, lock,ID1,ID2)
                free_lock(room_number, lock)
                return return_value
    elif duel.user_2 == request.user or (ID2 == ID and duel.guest_flag2 is True):
        if duel.user_turn == 2:
            if duel.ask == 1 or duel.ask == 3:
                return_value = answer_det(duelobj, duel, 2, answer, request, 1, lock,ID1,ID2)
                free_lock(room_number, lock)
                return return_value
        else:
            if duel.ask == 2 or duel.ask == 3:
                return_value = answer_det(duelobj, duel, 2, answer, request, 2, lock,ID1,ID2)
                free_lock(room_number, lock)
                return return_value
    free_lock(room_number, lock)
    return HttpResponse("error")


def chain_variable(request):
    room_number = int(request.POST["room_number"])
    lock = Lock.objects.get()
    lock_flag = lock_lock(room_number, lock,request)
    if lock_flag != "OK":
        return HttpResponse("waiting")
    duel = Duel.objects.filter(id=room_number).get()
    if "ID" in request.COOKIES :
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    ID1 = duel.guest_id
    ID2 = duel.guest_id2
    duelobj = DuelObj(room_number)
    duelobj.duel = duel
    duelobj.in_execute = False
    if duel.user_1 != request.user and duel.user_2 != request.user:
        if (ID1 == ID and duel.guest_flag) or (ID2 == ID and duel.guest_flag2):
            pass
        else:
            free_lock(room_number, lock)
            return HttpResponseRedirect(reverse("tcgcreator:watch_battle"))
    duelobj.duel = duel
    duelobj.room_number = room_number
    if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag is True):
        user = 1
        other_user = 2
        duelobj.user = 1
    else:
        duelobj.user = 2
        user = 2
        other_user = 1
    duelobj.init_all(user, other_user, room_number)
    str_chain = str(duel.chain)
    chain_det = json.loads(duel.chain_det)
    chain_variable_det = json.loads(duel.chain_variable)
    decks = Deck.objects.all()
    graves = Grave.objects.all()
    hands = Hand.objects.all()
    duelobj.check_eternal_effect(
        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
    if duel.in_cost is True:
        if duel.in_copying is True:
            duelobj.tmp_chain = duel.chain - 1
        else:
            duelobj.tmp_chain = duel.chain
        cost_det = duel.cost_det
        cost = CostWrapper.objects.get(id=cost_det).cost
        cost_val = cost.cost_val
        if(cost_val == 63 or cost_val == 64):
                chain_variablle_det = json.loads(duel.global_variable)
        cost = json.loads(cost.cost)
        if(cost_val == 63 or cost_val == 64):
            tmp = cost["chain_variable"].split("_")
            mine_or_other = int(tmp[2])
            chain_variable_name = tmp[1]
        else:
            chain_variable_name = cost["chain_variable"]
        min_equation_number = duelobj.calculate_boland(cost["min_equation_number"])
        max_equation_number = duelobj.calculate_boland(cost["max_equation_number"])
        chain_variable = int(request.POST["chain_variable"])
        if chain_variable < min_equation_number or chain_variable > max_equation_number:
            free_lock(room_number, lock)
            return HttpResponse("error")
        if(cost_val == 63 or cost_val == 64):
            pass
        elif str_chain not in chain_variable_det:
            chain_variable_det[str_chain] = {}

        if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag is True):
            if duel.user_turn == 1:
                if duel.ask == 1 or duel.ask == 3:
                    duel.ask -= 1
                    if(cost_val == 63 or cost_val == 64):
                        if mine_or_other == 1:
                            chain_variable_det[chain_variable_name]["1_value"]= chain_variable
                        elif mine_or_other == 2:
                            chain_variable_det[chain_variable_name]["2_value"]= chain_variable
                        else:    
                            chain_variable_det[chain_variable_name]["value"]= chain_variable
                        duel.global_variable = json.dumps(chain_variable_det)
                    else:
                        chain_variable_det[str_chain][chain_variable_name] = chain_variable
                        duel.chain_variable = json.dumps(chain_variable_det)
                    duelobj.in_execute = False
            else:
                if duel.ask == 2 or duel.ask == 3:
                    duel.ask -= 2
                    if(cost_val == 63 or cost_val == 64):
                        if mine_or_other == 1:
                            chain_variable_det[chain_variable_name]["2_value"]= chain_variable
                        elif mine_or_other == 2:
                            chain_variable_det[chain_variable_name]["1_value"]= chain_variable
                        else:
                            chain_variable_det[chain_variable_name]["value"]= chain_variable
                        duel.global_variable = json.dumps(chain_variable_det)
                    else:
                        chain_variable_det[str_chain][chain_variable_name] = chain_variable
                        duel.chain_variable = json.dumps(chain_variable_det)
                    duelobj.in_execute = False
        elif duel.user_2 == request.user:
            if duel.user_turn == 2:
                if duel.ask == 1 or duel.ask == 3:
                    duel.ask -= 1
                    if(cost_val == 63 or cost_val == 64):
                        if mine_or_other == 1:
                            chain_variable_det[chain_variable_name]["2_value"]= chain_variable
                        elif mine_or_other == 2:
                            chain_variable_det[chain_variable_name]["1_value"]= chain_variable
                        else:
                            chain_variable_det[chain_variable_name]["value"]= chain_variable

                        duel.global_variable = json.dumps(chain_variable_det)
                    else:    
                        chain_variable_det[str_chain][chain_variable_name] = chain_variable
                        duel.chain_variable = json.dumps(chain_variable_det)
                    duelobj.in_execute = False
            else:
                if duel.ask == 2 or duel.ask == 3:
                    duel.ask -= 2
                    if(cost_val == 63 or cost_val == 64):
                        if mine_or_other == 1:
                            chain_variable_det[chain_variable_name]["1_value"]= chain_variable
                        elif mine_or_other == 2:    
                            chain_variable_det[chain_variable_name]["2_value"]= chain_variable
                        else:    
                            chain_variable_det[chain_variable_name]["value"]= chain_variable
                        duel.global_variable = json.dumps(chain_variable_det)
                    else:    
                        chain_variable_det[str_chain][chain_variable_name] = chain_variable
                        duel.chain_variable = json.dumps(chain_variable_det)
                    duelobj.in_execute = False
        if duel.ask == 0:
            duelobj.check_eternal_effect(
                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
            )
            cost_det = duel.cost_det
            effect = CostWrapper.objects.get(id=cost_det)
            next_effect = effect.cost_next
            trigger = Trigger.objects.get(id=duel.current_trigger)
            tmp = duelobj.pay_cost(next_effect, user,duel.chain,trigger)
            if next_effect == 0 or tmp is True:
                duelobj.end_cost(duel.cost_user,duel.chain,trigger)
            duelobj.save_all(user, other_user, room_number)
    else:
        duelobj.tmp_chain = duel.chain
        chain_det = json.loads(duel.chain_det)
        monster_effect_wrapper = MonsterEffectWrapper.objects.get(
            id=int(chain_det[str(duel.chain - 1)])
        )
        monster_effect = monster_effect_wrapper.monster_effect
        monster_effect_val = monster_effect.monster_effect_val
        if(monster_effect_val == 63 or monster_effect_val == 64):
            chain_variable_det = json.loads(duel.global_variable)
        chain_user = json.loads(duel.chain_user)
        effect_user = chain_user[str(duel.chain - 1)]
        monster_effect = json.loads(monster_effect.monster_effect)
        chain_variable_name = monster_effect["chain_variable"]
        if(monster_effect_val == 63 or monster_effect_val == 64):
            tmp = chain_variable_name.split("_")
            chain_variable_name = tmp[1]
            mine_or_other = int(tmp[2])

        min_equation_number = duelobj.calculate_boland(
            monster_effect["min_equation_number"]
        )
        max_equation_number = duelobj.calculate_boland(
            monster_effect["max_equation_number"]
        )
        chain_variable = int(request.POST["chain_variable"])
        if chain_variable < min_equation_number or chain_variable > max_equation_number:
            free_lock(room_number, lock)
            return HttpResponse("error")
        if(monster_effect_val == 63 or monster_effect_val == 64):
            pass
        elif duel.chain - 1 not in chain_variable_det:
            chain_variable_det[str(duel.chain - 1)] = {}
            
        if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag is True):
            if duel.user_turn == 1:
                if duel.ask == 1 or duel.ask == 3:
                    duel.ask -= 1
                    if(monster_effect_val == 63 or monster_effect_val == 64):
                        if mine_or_other == 1:
                            chain_variable_det[chain_variable_name]["1_value"]= chain_variable
                        elif mine_or_other == 2:
                            chain_variable_det[chain_variable_name]["2_value"]= chain_variable
                        else:
                            chain_variable_det[chain_variable_name]["value"]= chain_variable
                        duel.global_variable = json.dumps(chain_variable_det)
                    else:
                        chain_variable_det[str(duel.chain - 1)][
                            chain_variable_name
                        ] = chain_variable
                        duel.chain_variable = json.dumps(chain_variable_det)
            else:
                if duel.ask == 2 or duel.ask == 3:
                    duel.ask -= 2
                    if(monster_effect_val == 63 or monster_effect_val == 64):
                        if mine_or_other == 1:
                            chain_variable_det[chain_variable_name]["2_value"]= chain_variable
                        elif mine_or_other == 2:
                            chain_variable_det[chain_variable_name]["1_value"]= chain_variable
                        else:
                            chain_variable_det[chain_variable_name]["value"]= chain_variable
                        duel.global_variable = json.dumps(chain_variable_det)
                    else:
                        chain_variable_det[str(duel.chain - 1)][
                            chain_variable_name
                        ] = chain_variable
                        duel.chain_variable = json.dumps(chain_variable_det)
        elif duel.user_2 == request.user:
            if duel.user_turn == 2:
                if duel.ask == 1 or duel.ask == 3:
                    duel.ask -= 1
                    if(monster_effect_val == 63 or monster_effect_val == 64):
                        if mine_or_other == 1:
                            chain_variable_det[chain_variable_name]["2_value"]= chain_variable
                        elif mine_or_other == 2:
                            chain_variable_det[chain_variable_name]["1_value"]= chain_variable
                        else:
                            chain_variable_det[chain_variable_name]["value"]= chain_variable
                        duel.global_variable = json.dumps(chain_variable_det)
                    else:
                        chain_variable_det[str(duel.chain - 1)][
                            chain_variable_name
                        ] = chain_variable
                        duel.chain_variable = json.dumps(chain_variable_det)
            else:
                if duel.ask == 2 or duel.ask == 3:
                    duel.ask -= 2
                    if(monster_effect_val == 63 or monster_effect_val == 64):
                        if mine_or_other == 1:
                            chain_variable_det[chain_variable_name]["1_value"]= chain_variable
                        elif mine_or_other == 2:
                            chain_variable_det[chain_variable_name]["2_value"]= chain_variable
                        else:
                            chain_variable_det[chain_variable_name]["value"]= chain_variable
                        duel.global_variable = json.dumps(chain_variable_det)
                    else:
                        chain_variable_det[str(duel.chain - 1)][
                            chain_variable_name
                        ] = chain_variable
                        duel.chain_variable = json.dumps(chain_variable_det)
        if duel.ask == 0:
            if monster_effect_wrapper.pac:
                next_effect = duelobj._pac(monster_effect_wrapper.pac)
            else:
                next_effect = monster_effect_wrapper.monster_effect_next
            if next_effect != 0 and next_effect is not None:
                chain_det[str(duel.chain - 1)] = next_effect.id
            duel.chain_det = json.dumps(chain_det)
    duelobj.check_eternal_effect(
        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
    '''if duel.in_cost is False and duel.in_trigger_waiting is False:
        duelobj.retrieve_chain(
            decks, graves, hands, duel.phase, duel.user_turn, user, other_user
        )
    '''
    if duel.chain == 0:
        duel.appoint = duel.user_turn
        tmp = {}
        duel.mess = json.dumps(tmp)
        duel.cost_result = json.dumps(tmp)
        duel.cost = json.dumps(tmp)
        duelobj.invoke_trigger_waiting(duel.trigger_waiting)
        duel.current_priority = 10000
        choices = duelobj.check_trigger(
            decks, graves, hands, duel.phase, duel.user_turn, user, other_user
        )
    else:
        choices = None
    duelobj.save_all(user, other_user, room_number)
    free_lock(room_number, lock)
    return battle_det(request, duelobj, choices)


def yes_or_no_cost(request, duelobj, user, other_user, room_number, lock):
    duel = duelobj.duel
    if "ID" in request.COOKIES :
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    ID1 = duel.guest_id
    ID2 = duel.guest_id2
    cost_det = duel.cost_det
    cost_user = duel.cost_user
    duelobj.tmp_chain = str(duel.chain)
    if cost_user == 0:
        if request.user == duel.user_1 or (ID1 == ID and duel.guest_flag is True):
            cost_user = 1
        else:
            cost_user = 2
    cost = CostWrapper.objects.get(id=cost_det).cost
    cost_effect_val = cost.cost_val
    if cost_effect_val != 48 and cost_effect_val != 16 and cost_effect_val != 26:
        free_lock(room_number, lock)
        return HttpResponse("error")
    answer = request.POST["answer"]
    if cost_user == duel.user_turn:
        if duel.ask != 1:
            free_lock(room_number, lock)
            return HttpResponse("error")
    if cost_user != duel.user_turn:
        if duel.ask != 2:
            free_lock(room_number, lock)
            return HttpResponse("error")
    decks = Deck.objects.all()
    graves = Grave.objects.all()
    hands = Hand.objects.all()
    duelobj.check_eternal_effect(
        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
    if answer == "yes":
        duel.ask = 0
        effect = CostWrapper.objects.get(id=cost_det)
        # 効果コピー
        if(cost_effect_val == 48):
            next_effect = duelobj.copy_special_effect(effect.cost,effect.cost_kind,True)
        tmp = False
        if next_effect is not None and isinstance(next_effect,int) is False and next_effect[0] is not None:
            duel.cost_det = next_effect[0].id
            trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
            tmp = duelobj.pay_cost(next_effect[0], user,duel.chain,trigger)
        else:
            duel.cost_det = 0
        if duel.cost_det == 0 and tmp is False:
            if duel.in_copying is False:
                duelobj.end_cost(duel.cost_user,duel.chain,trigger)
                trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
                if trigger.chain_flag is True:
                    duel.virtual_chain += 1
                duel.chain += 1
            else:
                duelobj.end_cost(duel.cost_user,duel.chain,trigger)
        choices = None
    else:
        duel.ask = 0
        effect = CostWrapper.objects.get(id=cost_det)
        if cost_effect_val == 48:
            if effect.pac:
                next_effect = duelobj._pac_cost(effect.pac)
            elif effect.cost_next:
                next_effect = effect.cost_next
            else:
                next_effect = duelobj.pop_pac_cost(user)
            tmp = False
            if next_effect is not None and next_effect != -2:
                duel.cost_det = next_effect.id
                trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
                tmp = duelobj.pay_cost(next_effect, user,duel.chain,trigger)
            else:
                duel.cost_det = 0
            if duel.cost_det == 0 and tmp is False:
                if duel.in_copying is False:
                    duelobj.end_cost(duel.cost_user,duel.chain,trigger)
                    #効果をコピーしない場合はchainを増やさない
                    #duel.chain += 1
                else:
                    duelobj.end_cost(duel.cost_user,duel.chain,trigger)
            choices = None
            if effect.pac2:
                next_effect = duelobj._pac_cost(effect.pac2)
            elif effect.cost_next2:
                next_effect = effect.cost_next
            else:
                next_effect = duelobj.pop_pac_cost(user)
            tmp = False
            if next_effect is not None and next_effect != -2:
                duel.cost_det = next_effect.id
                trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
                tmp = duelobj.pay_cost(next_effect, user,duel.chain,trigger)
            else:
                duel.cost_det = 0
            if duel.cost_det == 0 and tmp is False:
                if duel.in_copying is False :
                    duelobj.end_cost(duel.cost_user,duel.chain,trigger)
                    #効果をコピーしない場合はchainを増やさない
                    #duel.chain += 1
                else:
                    duelobj.end_cost(duel.cost_user,duel.chain,trigger)
            choices = None
    duelobj.save_all(user, other_user, room_number)
    free_lock(room_number, lock)
    return battle_det(request, duelobj, choices)


def multiple_choice(request):
    room_number = int(request.POST["room_number"])
    lock = Lock.objects.get()
    lock_flag = lock_lock(room_number, lock,request)
    if lock_flag != "OK":
        return HttpResponse("waiting")
    duel = Duel.objects.filter(id=room_number).get()
    if "ID" in request.COOKIES :
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    ID1 = duel.guest_id
    ID2 = duel.guest_id2
    duelobj = DuelObj(room_number)
    duelobj.duel = duel
    if duel.user_1 != request.user and duel.user_2 != request.user:
        if (ID1 == ID and duel.guest_flag) or (ID2 == ID and duel.guest_flag2):
            pass
        else:
            free_lock(room_number, lock)
            return HttpResponseRedirect(reverse("tcgcreator:watch_battle"))
    duelobj.duel = duel
    duelobj.room_number = room_number
    if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag is True):
        user = 1
        other_user = 2
        duelobj.user = 1
    else:
        duelobj.user = 2
        user = 2
        other_user = 1
    duelobj.init_all(user, other_user, room_number)
    if user == duel.user_turn:
        if duel.ask != 1:
            free_lock(room_number, lock)
            return HttpResponse("error")
    if duel.user_turn != user:
        if duel.ask != 2:
            free_lock(room_number, lock)
            return HttpResponse("error")
    chain_det = json.loads(duel.chain_det)

    monster_effect = MonsterEffectWrapper.objects.get(
        id=int(chain_det[str(duel.chain - 1)])
    ).monster_effect
    monster_effect_val = monster_effect.monster_effect_val
    if monster_effect_val != 66 and monster_effect_val != 67:
        free_lock(room_number, lock)
        return HttpResponse("error")
    answer = request.POST["answer"]
    multiple_json = json.loads(monster_effect.monster_effect)
    if answer not in multiple_json["monster_effect_wrapper"]:
        free_lock(room_number, lock)
        return HttpResponse("error")
    duel.ask = 0
    next_effect = MonsterEffectWrapper(id = int(answer))
    chain_det[str(duel.chain - 1)] = next_effect.id
    duel.chain_det = json.dumps(chain_det)
    decks = Deck.objects.all()
    graves = Grave.objects.all()
    hands = Hand.objects.all()
    duelobj.check_eternal_effect(
        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
    duelobj.retrieve_chain(
        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
    if duel.chain == 0:
        duelobj.invoke_after_chain_effect(
           decks, graves, hands, duel.phase, duel.user_turn, user, other_user
        )
        duel.appoint = duel.user_turn
        tmp = {}
        duel.mess = json.dumps(tmp)
        duel.cost_result = json.dumps(tmp)
        duel.cost = json.dumps(tmp)
        duelobj.invoke_trigger_waiting(duel.trigger_waiting)
        duel.current_priority = 10000
        choices = duelobj.check_trigger(
            decks, graves, hands, duel.phase, duel.user_turn, user, other_user
        )
    else:
        choices = None
    duelobj.save_all(user, other_user, room_number)

    free_lock(room_number, lock)
    return battle_det(request, duelobj, choices)

def yes_or_no(request):
    room_number = int(request.POST["room_number"])
    lock = Lock.objects.get()
    lock_flag = lock_lock(room_number, lock,request)
    if lock_flag != "OK":
        return HttpResponse("waiting")
    duel = Duel.objects.filter(id=room_number).get()
    if "ID" in request.COOKIES :
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    ID1 = duel.guest_id
    ID2 = duel.guest_id2
    duelobj = DuelObj(room_number)
    duelobj.duel = duel
    if duel.user_1 != request.user and duel.user_2 != request.user:
        if (ID1 == ID and duel.guest_flag) or (ID2 == ID and duel.guest_flag2):
            pass
        else:
            free_lock(room_number, lock)
            return HttpResponseRedirect(reverse("tcgcreator:watch_battle"))
    duelobj.duel = duel
    duelobj.room_number = room_number
    if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag is True):
        user = 1
        other_user = 2
        duelobj.user = 1
    else:
        duelobj.user = 2
        user = 2
        other_user = 1
    duelobj.init_all(user, other_user, room_number)
    if user == duel.user_turn:
        if duel.ask != 1:
            free_lock(room_number, lock)
            return HttpResponse("error")
    if duel.user_turn != user:
        if duel.ask != 2:
            free_lock(room_number, lock)
            return HttpResponse("error")
    if duel.in_cost is True:
        return yes_or_no_cost(request, duelobj, user, other_user, room_number, lock)
    if duel.in_trigger_waiting is True and duel.force == 0:
        answer = request.POST["answer"]
        if answer == "yes":
            duel.force = 2
        else:
            duel.force = 1
        duel.ask = 0
        duelobj.save_all(user, other_user, room_number)
        free_lock(room_number, lock)
        return battle_det(request, duelobj, None)

    chain_det = json.loads(duel.chain_det)

    monster_effect = MonsterEffectWrapper.objects.get(
        id=int(chain_det[str(duel.chain - 1)])
    ).monster_effect
    monster_effect_val = monster_effect.monster_effect_val
    if monster_effect_val != 16 and monster_effect_val != 26:
        free_lock(room_number, lock)
        return HttpResponse("error")
    answer = request.POST["answer"]
    if answer == "yes":
        duel.ask = 0
        chain_det = json.loads(duel.chain_det)
        current_chain = chain_det[str(duel.chain - 1)]
        effect = MonsterEffectWrapper.objects.get(id=current_chain)
        if effect.pac:
            next_effect = duelobj._pac(effect.pac)
        else:
            next_effect = effect.monster_effect_next
        if next_effect != 0 and next_effect is not None:
            chain_det[str(duel.chain - 1)] = next_effect.id
        else:
            pac = json.loads(duel.in_pac)
            if str(duel.chain - 1) in pac and pac[str(duel.chain - 1)] != []:
                pac_id = pac[str(duel.chain - 1)].pop()
                duel.in_pac = json.dumps(pac)
                pac = PacWrapper.objects.get(id=pac_id)
                next_effect = pac.monster_effect_next
                if next_effect is None:
                    Trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
                    if trigger.chain_flag is True:
                        duel.virtual_chain -= 1
                    duel.chain -= 1
                else:
                    chain_det[str(duel.chain - 1)] = next_effect.id
            else:
                Trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
                if trigger.chain_flag is True:
                    duel.virtual_chain -= 1
                duel.chain -= 1
        duel.chain_det = json.dumps(chain_det)
    else:
        duel.ask = 0
        chain_det = json.loads(duel.chain_det)
        current_chain = chain_det[str(duel.chain - 1)]
        effect = MonsterEffectWrapper.objects.get(id=current_chain)
        next_effect = effect.monster_effect_next2
        if effect.pac2:
            next_effect = duelobj._pac(effect.pac2)
        else:
            next_effect = effect.monster_effect_next2
        if next_effect is not None and next_effect != 0:
            chain_det[str(duel.chain - 1)] = next_effect.id
        else:
            pac = json.loads(duel.in_pac)
            if str(duel.chain - 1) in pac and pac[str(duel.chain - 1)] != []:
                pac_id = pac[str(duel.chain - 1)].pop()
                duel.in_pac = json.dumps(pac)
                pac = PacWrapper.objects.get(id=pac_id)
                next_effect = pac.monster_effect_next
                if next_effect is None:
                    Trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
                    if trigger.chain_flag is True:
                        duel.virtual_chain -= 1
                    duel.chain -= 1
                else:
                    chain_det[str(duel.chain - 1)] = next_effect.id
            else:
                Trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
                if trigger.chain_flag is True:
                    duel.virtual_chain -= 1
                duel.chain -= 1
        duel.chain_det = json.dumps(chain_det)
    decks = Deck.objects.all()
    graves = Grave.objects.all()
    hands = Hand.objects.all()
    duelobj.check_eternal_effect(
        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
    duelobj.retrieve_chain(
        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
    if duel.chain == 0:
        duelobj.invoke_after_chain_effect(
           decks, graves, hands, duel.phase, duel.user_turn, user, other_user
        )
        duel.appoint = duel.user_turn
        tmp = {}
        duel.mess = json.dumps(tmp)
        duel.cost_result = json.dumps(tmp)
        duel.cost = json.dumps(tmp)
        duelobj.invoke_trigger_waiting(duel.trigger_waiting)
        duel.current_priority = 10000
        choices = duelobj.check_trigger(
            decks, graves, hands, duel.phase, duel.user_turn, user, other_user
        )
    else:
        choices = None
        if(duel.ask == 1 ):
            duel.appoint = duel.user_turn
        elif(duel.ask == 2 ):
            if duel.user_turn == 1:
                duel.appoint = 2
            else:
                duel.appoint = 1
    duelobj.save_all(user, other_user, room_number)

    free_lock(room_number, lock)
    return battle_det(request, duelobj, choices)


def answer_under_det(
    duelobj,
    duel,
    user,
    answer,
    exclude,
    whether_monster,
    monster_effect_text,
    monster_effect_val,
    request,
    cost_flag=0,
    log=None,
    lock=None,
    effect_kind="",
):
    global check_array
    if "ID" in request.COOKIES :
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    ID1 = duel.guest_id
    ID2 = duel.guest_id2
    room_number = int(request.POST["room_number"])
    if user == 1:
        other_user = 2
    else:
        other_user = 1
    chain_det = json.loads(duel.chain_det)
    chain_user = json.loads(duel.chain_user)
    if cost_flag == 0:
        chain_user = int(chain_user[str(duel.chain - 1)])
    else:
        chain_user = int(chain_user[duelobj.tmp_chain])
    mess = duelobj.mess
    cost = duelobj.cost
    return_value = []
    for answer_val in answer:
        x = int(answer_val["x"])
        y = int(answer_val["y"])
        under_id = answer_val["under_id"]
        tmp_count = 0
        for monster_effect_det in monster_effect_text:
            as_monster_effect = monster_effect_det["as_monster_condition"]
            if monster_effect_val == 44:
                if as_monster_effect[0] == "~":
                    cost = duelobj.cost
                    #if str(int(duel.chain-2)) not in cost:
                    cost[str(int(duel.chain - 2))] = {}
                    cost[str(int(duel.chain - 2))]["choose"] = []
                    effect_cost_flag = 1
                else:
                    mess = duelobj.mess
                    #if str(int(duel.chain-2)) not in mess:
                    mess[str(int(duel.chain - 2))] = {}
                    mess[str(int(duel.chain - 2))]["choose"] = []
                    effect_cost_flag == 0
            tmp_count += 1
            if (user == 1 and chain_user == 1) or (user == 2 and chain_user == 2):
                if (
                    (monster_effect_val == 3)
                    or (monster_effect_val == 44)
                    or (monster_effect_val == 5 and tmp_count == 1)
                ):
                    monster_effect_det_monster = monster_effect_det["monster"]
                    for place in monster_effect_det_monster["place"]:
                        place_tmp = place["det"].split("_")
                        if place_tmp[2] == "4":
                            mine_or_other = user
                        elif place_tmp[2] == "5":
                            mine_or_other = other_user
                        else:
                            mine_or_other = 0

                        if place_tmp[0] == "field":
                            fields = duelobj.field
                        field = fields[x][y]
                        if field["kind"].find(place_tmp[1]) == -1:
                            continue
                        if field["mine_or_other"] != mine_or_other:
                            continue

                        if field["det"] is None:
                            return HttpResponse("error")
                        else:
                            if "under" not in field["det"]:
                                return HttpResponse("error")
                            under_flag = False
                            for under in field["det"]["under"]:
                                if under["place_unique_id"] == under_id:
                                    under_flag = True
                                    break
                            if under_flag is False:
                                return HttpResponse("error")
                            tmp2 = {}
                            tmp2["det"] = field["det"]
                            tmp2["mine_or_other"] = field["mine_or_other"]
                            tmp2["user"] = chain_user
                            tmp2["place"] = "under"
                            tmp2["deck_id"] = 0
                            tmp2["x"] = x
                            tmp2["y"] = y
                            tmp2["place_unique_id"] = field["det"]["place_unique_id"]
                            tmp2["under_id"] = under_id
                            return_value.append(tmp2)
                            if not duelobj.validate_answer(
                                tmp2,
                                monster_effect_det_monster,
                                exclude,
                                duel,
                                1,
                                0,
                                effect_kind,
                                user,
                            ):
                                return HttpResponse("error")
                            check_array.append(field["det"])
                            if cost_flag == 0:
                                if monster_effect_val == 44:
                                    if effect_cost_flag == 0:
                                        if str(duel.chain - 2) not in mess:
                                           mess[str(duel.chain - 2)] = {}
                                        if "choose" not in mess[str(duel.chain - 1)]:
                                            mess[str(duel.chain - 2)]["choose"] = []
                                    else:
                                        if str(duel.chain - 2) not in cost:
                                            cost[str(duel.chain - 2)] = {}
                                        if "choose" not in cost[str(duel.chain - 1)]:
                                            cost[str(duel.chain - 2)]["choose"] = []
                                else:
                                    if str(duel.chain - 1) not in mess:
                                        mess[str(duel.chain - 1)] = {}
                                    if "choose" not in mess[str(duel.chain - 1)]:
                                        mess[str(duel.chain - 1)]["choose"] = []
                                tmp2 = {}
                                tmp2["det"] = field["det"]
                                tmp2["hide"] = (
                                    field["hide"] if ("hide" in field) else False
                                )
                                tmp2["mine_or_other"] = field["mine_or_other"]
                                tmp2["x"] = x
                                tmp2["y"] = y
                                tmp2["deck_id"] = 0
                                tmp2["place_unique_id"] = field["det"][
                                    "place_unique_id"
                                ]
                                tmp2["user"] = user
                                tmp2["place"] = "under"
                                tmp2["under_id"] = under_id
                                return_value.append(tmp2)
                                if monster_effect_val == 44:
                                    if effect_cost_flag == 0:
                                        if (
                                            as_monster_effect
                                            not in mess[str(duel.chain - 2)]
                                        ):
                                            mess[str(duel.chain - 2)][
                                                as_monster_effect
                                            ] = []
                                        mess[str(duel.chain - 2)][
                                            as_monster_effect
                                        ].append(tmp2)
                                    else:
                                        if (
                                            as_monster_effect
                                            not in cost[str(duel.chain - 2)]
                                        ):
                                            cost[str(duel.chain - 2)][
                                                as_monster_effect
                                            ] = []
                                        cost[str(duel.chain - 2)][
                                            as_monster_effect
                                        ].append(tmp2)
                                else:
                                    if (
                                        as_monster_effect
                                        not in mess[str(duel.chain - 1)]
                                    ):
                                        mess[str(duel.chain - 1)][
                                            as_monster_effect
                                        ] = []
                                    mess[str(duel.chain - 1)][as_monster_effect].append(
                                        tmp2
                                    )
                            else:
                                if str(duelobj.tmp_chain) not in cost:
                                    cost[str(duelobj.tmp_chain)] = {}
                                if "choose" not in cost[str(duelobj.tmp_chain)]:
                                    cost[str(duelobj.tmp_chain)]["choose"] = []
                                tmp2 = {}
                                tmp2["det"] = field["det"]
                                tmp2["hide"] = (
                                    field["hide"] if ("hide" in field) else False
                                )
                                tmp2["x"] = x
                                tmp2["y"] = y
                                tmp2["deck_id"] = 0
                                tmp2["place_unique_id"] = field["det"][
                                    "place_unique_id"
                                ]
                                tmp2["user"] = user
                                tmp2["place"] = "under"
                                tmp2["mine_or_other"] = field["mine_or_other"]
                                tmp2["under_id"] = under_id
                                return_value.append(tmp2)
                                if (
                                    as_monster_effect
                                    not in cost[str(duelobj.tmp_chain)]
                                ):
                                    cost[str(duelobj.tmp_chain)][as_monster_effect] = []
                                cost[str(duelobj.tmp_chain)][as_monster_effect].append(
                                    tmp2
                                )

            elif (user == 2 and chain_user == 1) or (user == 1 and chain_user == 2):
                if (monster_effect_val == 4) or (
                    monster_effect_val == 5 and tmp_count == 2
                ):
                    monster_effect_det_monster = monster_effect_det["monster"]
                    for place in monster_effect_det_monster["place"]:
                        place_tmp = place["det"].split("_")
                        if place_tmp[2] == "4":
                            mine_or_other = user
                        elif place_tmp[2] == "5":
                            mine_or_other = other_user
                        else:
                            mine_or_other = 0
                        if place_tmp[0] == "field":
                            fields = duelobj.field
                        field = fields[x][y]
                        if field["kind"].find(place_tmp[1]) == -1:
                            continue
                        if field["mine_or_other"] != mine_or_other:
                            continue
                        if field["det"] is None:
                            return HttpResponse("error")
                        else:
                            if "under" not in field["det"]:
                                return HttpResponse("error")
                            under_flag = False
                            for under in field["det"]["under"]:
                                if under["place_unique_id"] == under_id:
                                    under_flag = True
                                    break
                            if under_flag is False:
                                return HttpResponse("error")
                            tmp2 = {}
                            tmp2["det"] = field["det"]
                            tmp2["mine_or_other"] = field["mine_or_other"]
                            tmp2["user"] = chain_user
                            tmp2["place"] = "under"
                            tmp2["deck_id"] = 0
                            tmp2["x"] = x
                            tmp2["y"] = y
                            tmp2["place_unique_id"] = field["det"]["place_unique_id"]
                            tmp2["under_id"] = under_id
                            return_value.append(tmp2)
                            if not duelobj.validate_answer(
                                tmp2,
                                monster_effect_det_monster,
                                exclude,
                                duel,
                                1,
                                0,
                                effect_kind,
                                user,
                            ):
                                return HttpResponse("error")
                            check_array.append(field["det"])
                            if cost_flag == 0:
                                if monster_effect_val == 44:
                                    if effect_cost_flag == 0:
                                        if str(duel.chain - 2) not in mess:
                                            mess[str(duel.chain - 2)] = {}
                                        if "choose" not in mess[str(duel.chain - 2)]:
                                            mess[str(duel.chain - 2)]["choose"] = []
                                    else:
                                        if str(duel.chain - 2) not in cost:
                                            cost[str(duel.chain - 2)] = {}
                                        if "choose" not in cost[str(duel.chain - 2)]:
                                            cost[str(duel.chain - 2)]["choose"] = []
                                else:
                                    if str(duel.chain - 1) not in mess:
                                        mess[str(duel.chain - 1)] = {}
                                    if "choose" not in mess[str(duel.chain - 1)]:
                                        mess[str(duel.chain - 1)]["choose"] = []
                                tmp2 = {}
                                tmp2["det"] = field["det"]
                                tmp2["hide"] = (
                                    field["hide"] if ("hide" in field) else False
                                )
                                tmp2["x"] = x
                                tmp2["y"] = y
                                tmp2["deck_id"] = 0
                                tmp2["place_unique_id"] = field["det"][
                                    "place_unique_id"
                                ]
                                tmp2["user"] = other_user
                                tmp2["place"] = "under"
                                tmp2["mine_or_other"] = field["mine_or_other"]
                                tmp2["under_id"] = under_id
                                if monster_effect_val == 44:
                                    if effect_cost_flag == 0:
                                        if (
                                            as_monster_effect
                                            not in mess[str(duel.chain - 2)]
                                        ):
                                            mess[str(duel.chain - 2)][
                                                as_monster_effect
                                            ] = []
                                        mess[str(duel.chain - 2)][
                                            as_monster_effect
                                        ].append(tmp2)
                                    else:
                                        if (
                                            as_monster_effect
                                            not in cost[str(duel.chain - 2)]
                                        ):
                                            cost[str(duel.chain - 2)][
                                                as_monster_effect
                                            ] = []
                                        cost[str(duel.chain - 2)][
                                            as_monster_effect
                                        ].append(tmp2)
                                else:
                                    if (
                                        as_monster_effect
                                        not in mess[str(duel.chain - 1)]
                                    ):
                                        mess[str(duel.chain - 1)][
                                            as_monster_effect
                                        ] = []
                                    mess[str(duel.chain - 1)][as_monster_effect].append(
                                        tmp2
                                    )
                            else:
                                if str(duelobj.tmp_chain) not in cost:
                                    cost[str(duelobj.tmp_chain)] = {}
                                if "choose" not in cost[str(duelobj.tmp_chain)]:
                                    cost[str(duelobj.tmp_chain)]["choose"] = []
                                tmp2 = {}
                                tmp2["det"] = field["det"]
                                tmp2["hide"] = (
                                    field["hide"] if ("hide" in field) else False
                                )
                                tmp2["x"] = x
                                tmp2["y"] = y
                                tmp2["deck_id"] = 0
                                tmp2["place_unique_id"] = field["det"][
                                    "place_unique_id"
                                ]
                                tmp2["user"] = other_user
                                tmp2["place"] = "under"
                                tmp2["mine_or_other"] = field["mine_or_other"]
                                tmp2["under_id"] = under_id
                                return_value.append(tmp2)
                                if (
                                    as_monster_effect
                                    not in cost[str(duelobj.tmp_chain)]
                                ):
                                    cost[str(duelobj.tmp_chain)][as_monster_effect] = []
                                cost[str(duelobj.tmp_chain)][as_monster_effect].append(
                                    tmp2
                                )
            else:
                for place in monster_effect_det_monster["place"]:
                    place_tmp = place["det"].split("_")
                    if place_tmp[0] == "field":
                        fields = duelobj.field
                    field = fields[x][y]
                    if field["kind"].find(place_tmp[1]) == -1:
                        continue
                    if int(field["mine_or_other"]) != 0:
                        continue

                    if field["det"] is None:
                        return HttpResponse("error")
                    else:
                        if "under" not in field["det"]:
                            return HttpResponse("error")
                        under_flag = False
                        for under in field["det"]["under"]:
                            if under["place_unique_id"] == under_id:
                                under_flag = True
                                break
                        if under_flag is False:
                            return HttpResponse("error")
                        tmp2 = {}
                        tmp2["det"] = field[x][y]["det"]
                        tmp2["mine_or_other"] = field[x][y]["mine_or_other"]
                        tmp2["user"] = chain_user
                        tmp2["place"] = "under"
                        tmp2["deck_id"] = 0
                        tmp2["x"] = x
                        tmp2["y"] = y
                        tmp2["place_unique_id"] = field[x][y]["det"]["place_unique_id"]
                        tmp2["under_id"] = under_id
                        return_value.append(tmp2)
                        if not duelobj.validate_answer(
                            tmp2,
                            monster_effect_det_monster,
                            exclude,
                            duel,
                            1,
                            0,
                            effect_kind,
                            user,
                        ):
                            return HttpResponse("error")
                        check_array.append(field["det"])
                        if cost_flag == 0:
                            if monster_effect_val != 44:
                                if str(duel.chain - 1) not in mess:
                                    mess[str(duel.chain - 1)] = {}
                                if "choose" not in mess[str(duel.chain - 1)]:
                                    mess[str(duel.chain - 1)]["choose"] = []
                            tmp2 = {}
                            tmp2["det"] = field["det"]
                            tmp2["hide"] = field["hide"] if ("hide" in field) else False
                            tmp2["x"] = x
                            tmp2["y"] = y
                            tmp2["deck_id"] = 0
                            tmp2["place_unique_id"] = field["det"]["place_unique_id"]
                            tmp2["user"] = user
                            tmp2["place"] = "under"
                            tmp2["under_id"] = under_id
                            tmp2["mine_or_other"] = field["mine_or_other"]
                            return_value.append(tmp2)
                            if monster_effect_val != 44:
                                if as_monster_effect not in mess[str(duel.chain - 1)]:
                                    mess[str(duel.chain - 1)][as_monster_effect] = []
                                mess[str(duel.chain - 1)][as_monster_effect].append(
                                    tmp2
                                )
                            else:
                                if effect_cost_flag == 0:
                                    if (
                                        as_monster_effect
                                        not in mess[str(duel.chain - 2)]
                                    ):
                                        mess[str(duel.chain - 2)][
                                            as_monster_effect
                                        ] = []
                                    mess[str(duel.chain - 2)][as_monster_effect].append(
                                        tmp2
                                    )
                                else:
                                    if (
                                        as_monster_effect
                                        not in cost[str(duel.chain - 2)]
                                    ):
                                        cost[str(duel.chain - 2)][
                                            as_monster_effect
                                        ] = []
                                    cost[str(duel.chain - 2)][as_monster_effect].append(
                                        tmp2
                                    )
                        else:
                            if str(duelobj.tmp_chain) not in cost:
                                cost[str(duelobj.tmp_chain)] = {}
                            if "choose" not in cost[str(duelobj.tmp_chain)]:
                                cost[str(duelobj.tmp_chain)]["choose"] = []
                            tmp2 = {}
                            tmp2["det"] = field["det"]
                            tmp2["hide"] = field["hide"] if ("hide" in field) else False
                            tmp2["x"] = x
                            tmp2["y"] = y
                            tmp2["deck_id"] = 0
                            tmp2["place_unique_id"] = field["det"]["place_unique_id"]
                            tmp2["user"] = user
                            tmp2["place"] = "under"
                            tmp2["under_id"] = under_id
                        tmp2["mine_or_other"] = field["mine_or_other"]
                        return_value.append(tmp2)
                        if as_monster_effect not in cost[str(duelobj.tmp_chain)]:
                            cost[str(duelobj.tmp_chain)][as_monster_effect] = []
                        cost[str(duelobj.tmp_chain)][as_monster_effect].append(tmp2)
    duelobj.mess = mess
    duelobj.cost = cost
    choices = None
    if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag is True):
        if duel.user_turn == 1:
            if duel.ask == 1 or duel.ask == 3:
                duel.ask -= 1
        else:
            if duel.ask == 2 or duel.ask == 3:
                duel.ask -= 2
    elif duel.user_2 == request.user:
        if duel.user_turn == 2:
            if duel.ask == 1 or duel.ask == 3:
                duel.ask -= 1
        else:
            if duel.ask == 2 or duel.ask == 3:
                duel.ask -= 2
    if duel.ask == 0 and duel.in_cost is False:
        chain_det = json.loads(duel.chain_det)
        current_chain = chain_det[str(duel.chain - 1)]
        effect = MonsterEffectWrapper.objects.get(id=current_chain)
        if effect.pac:
            next_effect = duelobj._pac(effect.pac)
        else:
            next_effect = effect.monster_effect_next
        if next_effect != 0 and next_effect is not None:
            chain_det[str(duel.chain - 1)] = next_effect.id
        else:
            pac = json.loads(duel.in_pac)
            if str(duel.chain - 1) in pac and pac[str(duel.chain - 1)] != []:
                pac_id = pac[str(duel.chain - 1)].pop()
                duel.in_pac = json.dumps(pac)
                pac = PacWrapper.objects.get(id=pac_id)
                next_effect = pac.monster_effect_next
                if next_effect is None:
                    Trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
                    if trigger.chain_flag is True:
                        duel.virtual_chain -= 1
                    duel.chain -= 1
                else:
                    chain_det[str(duel.chain - 1)] = next_effect.id
            else:
                Trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
                if trigger.chain_flag is True:
                   duel.virtual_chain -= 1
                duel.chain -= 1
        duelobj.duel.chain_det = json.dumps(chain_det)
        decks = Deck.objects.all()
        graves = Grave.objects.all()
        hands = Hand.objects.all()
        duelobj.check_eternal_effect(
            decks, graves, hands, duel.phase, duel.user_turn, user, other_user
        )
        if duel.in_trigger_waiting is False:
            duelobj.retrieve_chain(
                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
            )
        if duel.chain == 0:
            duelobj.invoke_after_chain_effect(
                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
            )
            duel.appoint = duel.user_turn
            tmp = {}
            duel.mess = json.dumps(tmp)
            duel.cost_result = json.dumps(tmp)
            duel.cost = json.dumps(tmp)
            duelobj.invoke_trigger_waiting(duel.trigger_waiting)
            duel.current_priority = 10000
            choices = duelobj.check_trigger(
                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
            )
        else:
            choices = None
    elif duel.ask == 0:
        cost_det = duel.cost_det
        effect = CostWrapper.objects.get(id=cost_det)
        if effect.pac:
            next_effect = duelobj._pac_cost(cost.pac)
        elif effect.cost_next:
            next_effect = effect.cost_next
        else:
            next_effect = duelobj.pop_pac_cost(user)
        tmp = False
        if next_effect is not None and next_effect != -2:
            duel.cost_det = next_effect.id
            trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
            tmp = duelobj.pay_cost(next_effect, user,duel.chain,trigger)
        else:
            duel.cost_det = 0
        if duel.cost_det == 0 and tmp is False:
            if duel.in_copying is False:
                duelobj.end_cost(duel.cost_user,duel.chain,trigger)
                trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
                if trigger.chain_flag is True:
                    duel.virtual_chain += 1
                duel.chain += 1
            else:
                duelobj.end_cost(duel.cost_user,duel.chain,trigger)
        choices = None
    if duel.in_cost is False:
        data = {}
        data["monsters"] = return_value
        if log is None:
            log = ""
        duel.log_turn += duelobj.write_log(log, user, data)
        duel.log += duelobj.write_log(log, user, data)
    duelobj.save_all(user, other_user, room_number)
    free_lock(room_number, lock)
    return battle_det(request, duelobj, choices)


def answer_as_under(
        duelobj,
        duel,
        user,
        answer,
        exclude,
        whether_monster,
        monster_effect_text,
        monster_effect_val,
        request,
        cost_flag=0,
        log=None,
        lock=None,
        room_number=None,
):
    if user == 1:
        other_user = 2
    else:
        other_user = 1
    decks = Deck.objects.all()
    graves = Grave.objects.all()
    hands = Hand.objects.all()
    return_value = []
    chain_det = json.loads(duel.chain_det)
    chain_user = json.loads(duel.chain_user)
    chain_user = int(chain_user[str(duel.chain - 1)])
    monster_effect_wrapper = MonsterEffectWrapper.objects.get(
        id=int(chain_det[str(duel.chain - 1)])
    )
    monster_effect = monster_effect_wrapper.monster_effect
    effect_kind = monster_effect_wrapper.monster_effect_kind
    monster_effect_text = json.loads(monster_effect.monster_effect)
    as_monster = monster_effect_text["monster"][0]["as_monster_condition"]
    field = duelobj.field
    monster_effect_det = monster_effect_text["monster"][0]
    as_monster_to = monster_effect_text["as_monster_condition_to"]
    mess = duelobj.mess
    as_monsters = mess[str(int(duel.chain - 1))][as_monster]
    flag = False
    if as_monster_to not in mess[str(int(duel.chain - 1))]:
        mess[str(int(duel.chain - 1))][as_monster_to] = []
    for answer_val in answer:
        if answer_val["place"] == "under":
            x = int(answer_val["x"])
            y = int(answer_val["y"])
            place_unique_id = answer_val["under_id"]
        flag = False
        for as_monster in as_monsters:
            x = as_monster["x"]
            y = as_monster["y"]
            if duelobj.check_monster_condition_det(
                    monster_effect_det,
                    as_monster["det"],
                    user,
                    effect_kind,
                    1,
                    "field",
                    0,
                    x,
                    y,
            ):
                if "under" in field[x][y]["det"]:
                    for under in field[x][y]["det"]["under"]:
                        if under["place_unique_id"] == place_unique_id:
                            tmp2 = {}
                            tmp2["det"] = under
                            tmp2["x"] = x
                            tmp2["y"] = y
                            tmp2["deck_id"] = 0
                            tmp2["user"] = user
                            tmp2["place"] = "under"
                            tmp2["mine_or_other"] = field[x][y]["mine_or_other"]
                            tmp2["place_unique_id"] = field[x][y]["det"]["place_unique_id"]
                            tmp2["under_id"] = under["place_unique_id"]
                            flag = True
                            return_value.append(tmp2)
                            mess[str(int(duel.chain - 1))][as_monster_to].append(tmp2)
    if flag is False:
        return HttpResponse("error")
    duelobj.mess = mess
    duel.ask -= 1
    if duel.ask == 0 and duel.in_cost is False:
        chain_det = json.loads(duel.chain_det)
        current_chain = chain_det[str(duel.chain - 1)]
        effect = MonsterEffectWrapper.objects.get(id=current_chain)
        if effect.pac:
            next_effect = duelobj._pac(effect.pac)
        else:
            next_effect = effect.monster_effect_next
        if next_effect != 0 and next_effect is not None:
            chain_det[str(duel.chain - 1)] = next_effect.id
        else:
            pac = json.loads(duel.in_pac)
            if str(duel.chain - 1) in pac and pac[str(duel.chain - 1)] != []:
                pac_id = pac[str(duel.chain - 1)].pop()
                duel.in_pac = json.dumps(pac)
                pac = PacWrapper.objects.get(id=pac_id)
                next_effect = pac.monster_effect_next
                if next_effect is None:
                    Trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
                    if trigger.chain_flag is True:
                        duel.virtual_chain -= 1
                    duel.chain -= 1
                else:
                    chain_det[str(duel.chain - 1)] = next_effect.id
            else:
                Trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
                if trigger.chain_flag is True:
                   duel.virtual_chain -= 1
                duel.chain -= 1
        duelobj.duel.chain_det = json.dumps(chain_det)
        decks = Deck.objects.all()
        graves = Grave.objects.all()
        hands = Hand.objects.all()
        duelobj.check_eternal_effect(
            decks, graves, hands, duel.phase, duel.user_turn, user, other_user
        )
        if duel.in_trigger_waiting is False:
            duelobj.retrieve_chain(
                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
            )
        if duel.chain == 0:
            duelobj.invoke_after_chain_effect(
                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
            )
            duel.appoint = duel.user_turn
            tmp = {}
            duel.mess = json.dumps(tmp)
            duel.cost_result = json.dumps(tmp)
            duel.cost = json.dumps(tmp)
            duelobj.invoke_trigger_waiting(duel.trigger_waiting)
            duel.current_priority = 10000
            choices = duelobj.check_trigger(
                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
            )
        else:
            choices = None
    if duel.in_cost is False:
        data = {}
        data["monsters"] = return_value
        if log is None:
            log = ""
        duel.log_turn += duelobj.write_log(log, user, data)
        duel.log += duelobj.write_log(log, user, data)
    duelobj.save_all(user, other_user, room_number)
    free_lock(room_number, lock)
    return battle_det(request, duelobj, choices)

def answer_as(
    duelobj,
    duel,
    user,
    answer,
    exclude,
    whether_monster,
    monster_effect_text,
    monster_effect_val,
    request,
    cost_flag=0,
    log=None,
    lock=None,
    room_number=None,
):
    if user == 1:
        other_user = 2
    else:
        other_user = 1
    decks = Deck.objects.all()
    graves = Grave.objects.all()
    hands = Hand.objects.all()
    return_value = []
    chain_det = json.loads(duel.chain_det)
    chain_user = json.loads(duel.chain_user)
    chain_user = int(chain_user[str(duel.chain - 1)])
    monster_effect_wrapper = MonsterEffectWrapper.objects.get(
        id=int(chain_det[str(duel.chain - 1)])
    )
    monster_effect = monster_effect_wrapper.monster_effect
    effect_kind = monster_effect_wrapper.monster_effect_kind
    monster_effect_text = json.loads(monster_effect.monster_effect)
    as_monster = monster_effect_text["monster"][0]["as_monster_condition"]
    monster_effect_det = monster_effect_text["monster"][0]
    as_monster_to = monster_effect_text["as_monster_condition_to"]
    mess = duelobj.mess
    as_monsters = mess[str(int(duel.chain - 1))][as_monster]
    if as_monster_to not in mess[str(int(duel.chain - 1))]:
        mess[str(int(duel.chain - 1))][as_monster_to] = []
    for answer_val in answer:
        if answer_val["place"] == "field":
            x = int(answer_val["x"])
            y = int(answer_val["y"])
            place_unique_id = duelobj.field[x][y]["det"]["place_unique_id"]
        flag = False
        for as_monster in as_monsters:
            if as_monster["det"]["place_unique_id"] == place_unique_id:
                if duelobj.check_monster_condition_det(
                    monster_effect_det,
                    as_monster["det"],
                    user,
                    effect_kind,
                    1,
                    "field",
                    0,
                    x,
                    y,
                ):
                    flag = True
                    return_value.append(as_monster)
                    mess[str(int(duel.chain - 1))][as_monster_to].append(as_monster)
        if flag is False:
            return HttpResponse("error")
    duelobj.mess = mess
    duel.ask -= 1
    if duel.ask == 0 and duel.in_cost is False:
        chain_det = json.loads(duel.chain_det)
        current_chain = chain_det[str(duel.chain - 1)]
        effect = MonsterEffectWrapper.objects.get(id=current_chain)
        if effect.pac:
            next_effect = duelobj._pac(effect.pac)
        else:
            next_effect = effect.monster_effect_next
        if next_effect != 0 and next_effect is not None:
            chain_det[str(duel.chain - 1)] = next_effect.id
        else:
            pac = json.loads(duel.in_pac)
            if str(duel.chain - 1) in pac and pac[str(duel.chain - 1)] != []:
                pac_id = pac[str(duel.chain - 1)].pop()
                duel.in_pac = json.dumps(pac)
                pac = PacWrapper.objects.get(id=pac_id)
                next_effect = pac.monster_effect_next
                if next_effect is None:
                    Trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
                    if trigger.chain_flag is True:
                        duel.virtual_chain -= 1
                    duel.chain -= 1
                else:
                    chain_det[str(duel.chain - 1)] = next_effect.id
            else:
                Trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
                if trigger.chain_flag is True:
                   duel.virtual_chain -= 1
                duel.chain -= 1
        duelobj.duel.chain_det = json.dumps(chain_det)
        decks = Deck.objects.all()
        graves = Grave.objects.all()
        hands = Hand.objects.all()
        duelobj.check_eternal_effect(
            decks, graves, hands, duel.phase, duel.user_turn, user, other_user
        )
        if duel.in_trigger_waiting is False:
            duelobj.retrieve_chain(
                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
            )
        if duel.chain == 0:
            duelobj.invoke_after_chain_effect(
                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
            )
            duel.appoint = duel.user_turn
            tmp = {}
            duel.mess = json.dumps(tmp)
            duel.cost_result = json.dumps(tmp)
            duel.cost = json.dumps(tmp)
            duelobj.invoke_trigger_waiting(duel.trigger_waiting)
            duel.current_priority = 10000
            choices = duelobj.check_trigger(
                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
            )
        else:
            choices = None
    if duel.in_cost is False:
        data = {}
        data["monsters"] = return_value
        if log is None:
            log = ""
        duel.log_turn += duelobj.write_log(log, user, data)
        duel.log += duelobj.write_log(log, user, data)
    duelobj.save_all(user, other_user, room_number)
    free_lock(room_number, lock)
    return battle_det(request, duelobj, choices)


def answer_field_det(
    duelobj,
    duel,
    user,
    answer_org,
    exclude,
    whether_monster,
    monster_effect_text,
    monster_effect_val,
    request,
    cost_flag=0,
    log=None,
    lock=None,
    effect_kind="",
):
    global check_array
    if "ID" in request.COOKIES :
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    ID1 = duel.guest_id
    ID2 = duel.guest_id2
    room_number = int(request.POST["room_number"])
    if user == 1:
        other_user = 2
    else:
        other_user = 1
    chain_det = json.loads(duel.chain_det)
    chain_user = json.loads(duel.chain_user)
    if cost_flag == 0:
        chain_user = int(chain_user[str(duel.chain - 1)])
    else:
        chain_user = int(chain_user[duelobj.tmp_chain])
    mess = duelobj.mess
    timing_mess = duelobj.timing_mess
    cost = duelobj.cost
    return_value = []
    answer = sorted(answer_org,key=lambda x:x["x"])
    for answer_val in answer:
        x = int(answer_val["x"])
        y = int(answer_val["y"])
        tmp_count = 0
        for monster_effect_det in monster_effect_text:
            as_monster_effect = monster_effect_det["as_monster_condition"]
            if monster_effect_val == 44:
                if as_monster_effect[0] == "~":
                    #if str(int(duel.chain-2)) not in cost:
                    cost[str(int(duel.chain - 2))] = {}
                    if "choose" not in cost[str(int(duel.chain - 2))]:
                        cost[str(int(duel.chain - 2))]["choose"] = []
                    effect_cost_flag = 1
                else:
                    #if str(int(duel.chain-2)) not in mess:
                    mess[str(int(duel.chain - 2))] = {}
                    if "choose" not in mess[str(int(duel.chain - 2))]:
                       mess[str(int(duel.chain - 2))]["choose"] = []
                    effect_cost_flag == 0
            tmp_count += 1
            if (user == 1 and chain_user == 1) or (user == 2 and chain_user == 2):
                if (
                    (monster_effect_val == 3)
                    or (monster_effect_val == 44)
                    or (monster_effect_val == 5 and tmp_count == 1)
                ):
                    monster_effect_det_monster = monster_effect_det["monster"]
                    for place in monster_effect_det_monster["place"]:
                        place_tmp = place["det"].split("_")
                        if place_tmp[2] == "1":
                            mine_or_other = user
                        elif place_tmp[2] == "2":
                            mine_or_other = other_user
                        else:
                            mine_or_other = 0

                        if place_tmp[0] == "field":
                            fields = duelobj.field
                        field = fields[x][y]
                        if field["kind"].find(place_tmp[1]) == -1:
                            continue
                        if field["mine_or_other"] != mine_or_other:
                            continue

                        if whether_monster == 0:
                            if field["det"] is not None:
                                return HttpResponse("error")
                            else:
                                if cost_flag == 0:
                                    if monster_effect_val != 44:
                                        if not str(duel.chain - 1) in mess:
                                            mess[str(duel.chain - 1)] = {}
                                        if "choose" in mess[str(duel.chain - 1)]:
                                            mess[str(duel.chain - 1)]["choose"] = []
                                    tmp2 = {}
                                    tmp2["det"] = field["det"]
                                    tmp2["hide"] = (
                                        field["hide"] if ("hide" in field) else False
                                    )
                                    tmp2["x"] = x
                                    tmp2["y"] = y
                                    tmp2["deck_id"] = 0
                                    tmp2["user"] = user
                                    tmp2["place"] = "field"
                                    tmp2["mine_or_other"] = field["mine_or_other"]
                                    return_value.append(tmp2)
                                    if monster_effect_val == 44:
                                        if effect_cost_flag == 1:
                                            if (
                                                as_monster_effect
                                                not in cost[str(duel.chain - 2)]
                                            ):
                                                cost[str(duel.chain - 2)][
                                                    as_monster_effect
                                                ] = []
                                            cost[str(duel.chain - 2)][
                                                as_monster_effect
                                            ].append(tmp2)
                                        else:
                                            if as_monster_effect[0] == "%":
                                                if as_monster_effect not in timing_mess:
                                                    timing_mess[as_monster_effect]=[]
                                                timing_mess[as_monster_effect].append(tmp2)
                                            else:
                                                if (
                                                    as_monster_effect
                                                    not in mess[str(duel.chain - 2)]
                                                ):
                                                    mess[str(duel.chain - 2)][
                                                        as_monster_effect
                                                    ] = []
                                                mess[str(duel.chain - 2)][
                                                    as_monster_effect
                                                ].append(tmp2)
                                    else:
                                        if as_monster_effect[0] == "%":
                                            if as_monster_effect not in timing_mess:
                                                timing_mess[as_monster_effect]=[]
                                            timing_mess[as_monster_effect].append(tmp2)
                                        else:
                                           if (
                                               as_monster_effect
                                               not in mess[str(duel.chain - 1)]
                                           ):
                                               mess[str(duel.chain - 1)][
                                                   as_monster_effect
                                               ] = []
                                           mess[str(duel.chain - 1)][
                                               as_monster_effect
                                           ].append(tmp2)
                                else:
                                    if str(duelobj.tmp_chain) not in cost:
                                        cost[str(duelobj.tmp_chain)] = {}
                                    if "choose" not in cost[str(duelobj.tmp_chain)]:
                                        cost[str(duelobj.tmp_chain)]["choose"] = []
                                    tmp2 = {}
                                    tmp2["det"] = field["det"]
                                    tmp2["mine_or_other"] = field["mine_or_other"]
                                    tmp2["hide"] = (
                                        field["hide"] if ("hide" in field) else False
                                    )
                                    tmp2["x"] = x
                                    tmp2["y"] = y
                                    tmp2["deck_id"] = 0
                                    tmp2["user"] = user
                                    tmp2["place"] = "field"
                                    return_value.append(tmp2)
                                    if (
                                        as_monster_effect
                                        not in cost[str(duelobj.tmp_chain)]
                                    ):
                                        cost[str(duelobj.tmp_chain)][
                                            as_monster_effect
                                        ] = []
                                    cost[str(duelobj.tmp_chain)][
                                        as_monster_effect
                                    ].append(tmp2)
                        else:
                            if field["det"] is None:
                                return HttpResponse("error")
                            else:
                                tmp2 = {}
                                tmp2["det"] = field["det"]
                                tmp2["mine_or_other"] = field["mine_or_other"]
                                tmp2["user"] = chain_user
                                tmp2["place"] = "field"
                                tmp2["deck_id"] = 0
                                tmp2["x"] = x
                                tmp2["y"] = y
                                tmp2["place_unique_id"] = field["det"][
                                    "place_unique_id"
                                ]
                                return_value.append(tmp2)
                                if not duelobj.validate_answer(
                                    tmp2,
                                    monster_effect_det_monster,
                                    exclude,
                                    duel,
                                    1,
                                    cost_flag,
                                    effect_kind,
                                    user,
                                ):
                                    return HttpResponse("error")
                                check_array.append(field["det"])
                                if cost_flag == 0:
                                    if monster_effect_val == 44:
                                        if effect_cost_flag == 0:
                                            if str(duel.chain - 2) not in mess:
                                                mess[str(duel.chain - 2)] = {}
                                            if (
                                                "choose"
                                                not in mess[str(duel.chain - 1)]
                                            ):
                                                mess[str(duel.chain - 2)]["choose"] = []
                                        else:
                                            if str(duel.chain - 2) not in cost:
                                                cost[str(duel.chain - 2)] = {}
                                            if (
                                                "choose"
                                                not in cost[str(duel.chain - 1)]
                                            ):
                                                cost[str(duel.chain - 2)]["choose"] = []
                                    else:
                                        if str(duel.chain - 1) not in mess:
                                            mess[str(duel.chain - 1)] = {}
                                        if "choose" not in mess[str(duel.chain - 1)]:
                                            mess[str(duel.chain - 1)]["choose"] = []
                                    tmp2 = {}
                                    tmp2["det"] = field["det"]
                                    tmp2["hide"] = (
                                        field["hide"] if ("hide" in field) else False
                                    )
                                    tmp2["mine_or_other"] = field["mine_or_other"]
                                    tmp2["x"] = x
                                    tmp2["y"] = y
                                    tmp2["deck_id"] = 0
                                    tmp2["place_unique_id"] = field["det"][
                                        "place_unique_id"
                                    ]
                                    tmp2["user"] = user
                                    tmp2["place"] = "field"
                                    return_value.append(tmp2)
                                    if monster_effect_val == 44:
                                        if effect_cost_flag == 0:
                                            if as_monster_effect[0] == "%":
                                                if as_monster_effect not in timing_mess:
                                                    timing_mess[as_monster_effect]=[]
                                                timing_mess[as_monster_effect].append(tmp2)
                                            else:
                                               if (
                                                   as_monster_effect
                                                   not in mess[str(duel.chain - 2)]
                                               ):
                                                   mess[str(duel.chain - 2)][
                                                       as_monster_effect
                                                   ] = []
                                               mess[str(duel.chain - 2)][
                                                   as_monster_effect
                                               ].append(tmp2)
                                        else:
                                            if (
                                                as_monster_effect
                                                not in cost[str(duel.chain - 2)]
                                            ):
                                                cost[str(duel.chain - 2)][
                                                    as_monster_effect
                                                ] = []
                                            cost[str(duel.chain - 2)][
                                                as_monster_effect
                                            ].append(tmp2)
                                    else:
                                        if as_monster_effect[0] == "%":
                                            if as_monster_effect not in timing_mess:
                                                timing_mess[as_monster_effect]=[]
                                            timing_mess[as_monster_effect].append(tmp2)
                                        else:
                                           if (
                                               as_monster_effect
                                               not in mess[str(duel.chain - 1)]
                                           ):
                                               mess[str(duel.chain - 1)][
                                                   as_monster_effect
                                               ] = []
                                           mess[str(duel.chain - 1)][
                                               as_monster_effect
                                           ].append(tmp2)
                                else:
                                    if str(duelobj.tmp_chain) not in cost:
                                        cost[str(duelobj.tmp_chain)] = {}
                                    if "choose" not in cost[str(duelobj.tmp_chain)]:
                                        cost[str(duelobj.tmp_chain)]["choose"] = []
                                    tmp2 = {}
                                    tmp2["det"] = field["det"]
                                    tmp2["hide"] = (
                                        field["hide"] if ("hide" in field) else False
                                    )
                                    tmp2["x"] = x
                                    tmp2["y"] = y
                                    tmp2["deck_id"] = 0
                                    tmp2["place_unique_id"] = field["det"][
                                        "place_unique_id"
                                    ]
                                    tmp2["user"] = user
                                    tmp2["place"] = "field"
                                    tmp2["mine_or_other"] = field["mine_or_other"]
                                    return_value.append(tmp2)
                                    if (
                                        as_monster_effect
                                        not in cost[str(duelobj.tmp_chain)]
                                    ):
                                        cost[str(duelobj.tmp_chain)][
                                            as_monster_effect
                                        ] = []
                                    cost[str(duelobj.tmp_chain)][
                                        as_monster_effect
                                    ].append(tmp2)

            elif (user == 2 and chain_user == 1) or (user == 1 and chain_user == 2):
                if (monster_effect_val == 4) or (
                    monster_effect_val == 5 and tmp_count == 2
                ):
                    monster_effect_det_monster = monster_effect_det["monster"]
                    for place in monster_effect_det_monster["place"]:
                        place_tmp = place["det"].split("_")
                        if place_tmp[2] == "1":
                            mine_or_other = user
                        elif place_tmp[2] == "2":
                            mine_or_other = other_user
                        else:
                            mine_or_other = 0
                        if place_tmp[0] == "field":
                            fields = duelobj.field
                        field = fields[x][y]
                        if field["kind"].find(place_tmp[1]) == -1:
                            continue
                        if field["mine_or_other"] != mine_or_other:
                            continue
                        if whether_monster == 0:
                            if field["det"] is not None:
                                return HttpResponse("error")
                            else:
                                if cost_flag == 0:
                                    if monster_effect_val == 44:
                                        if effect_cost_flag == 0:
                                            if str(duel.chain - 2) not in mess:
                                                mess[str(duel.chain - 2)] = {}
                                            if (
                                                "choose"
                                                not in mess[str(duel.chain - 2)]
                                            ):
                                                mess[str(duel.chain - 2)]["choose"] = []
                                        elif effect_cost_flag == 1:
                                            if str(duel.chain - 2) not in cost:
                                                cost[str(duel.chain - 2)] = {}
                                            if (
                                                "choose"
                                                not in cost[str(duel.chain - 2)]
                                            ):
                                                cost[str(duel.chain - 2)]["choose"] = []
                                    else:
                                        if str(duel.chain - 1) not in mess:
                                            mess[str(duel.chain - 1)] = {}
                                        if "choose" not in mess[str(duel.chain - 1)]:
                                            mess[str(duel.chain - 1)]["choose"] = []
                                    tmp2 = {}
                                    tmp2["det"] = field["det"]
                                    tmp2["hide"] = (
                                        field["hide"] if ("hide" in field) else False
                                    )
                                    tmp2["x"] = x
                                    tmp2["y"] = y
                                    tmp2["deck_id"] = 0
                                    tmp2["user"] = other_user
                                    tmp2["place"] = "field"
                                    tmp2["mine_or_other"] = field["mine_or_other"]
                                    return_value.append(tmp2)
                                    if monster_effect_val == 44:
                                        if effect_cost_flag == 0:
                                            if as_monster_effect[0] == "%":
                                                if as_monster_effect not in timing_mess:
                                                    timing_mess[as_monster_effect]=[]
                                                timing_mess[as_monster_effect].append(tmp2)
                                            else:
                                               if (
                                                   as_monster_effect
                                                   not in mess[str(duel.chain - 2)]
                                               ):
                                                   mess[str(duel.chain - 2)][
                                                       as_monster_effect
                                                   ] = []
                                               mess[str(duel.chain - 2)][
                                                   as_monster_effect
                                               ].append(tmp2)
                                        else:
                                            if (
                                                as_monster_effect
                                                not in cost[str(duel.chain - 2)]
                                            ):
                                                cost[str(duel.chain - 2)][
                                                    as_monster_effect
                                                ] = []
                                            cost[str(duel.chain - 2)][
                                                as_monster_effect
                                            ].append(tmp2)
                                    else:
                                        if as_monster_effect[0] == "%":
                                            if as_monster_effect not in timing_mess:
                                                timing_mess[as_monster_effect]=[]
                                            timing_mess[as_monster_effect].append(tmp2)
                                        else:
                                            if (
                                                as_monster_effect
                                                not in mess[str(duel.chain - 1)]
                                            ):
                                                mess[str(duel.chain - 1)][
                                                    as_monster_effect
                                                ] = []
                                            mess[str(duel.chain - 1)][
                                                as_monster_effect
                                            ].append(tmp2)
                                else:
                                    if str(duelobj.tmp_chain) not in cost:
                                        cost[str(duelobj.tmp_chain)] = {}
                                    if "choose" not in cost[str(duelobj.tmp_chain)]:
                                        cost[str(duelobj.tmp_chain)]["choose"] = []
                                    tmp2 = {}
                                    tmp2["det"] = field["det"]
                                    tmp2["hide"] = (
                                        field["hide"] if ("hide" in field) else False
                                    )
                                    tmp2["x"] = x
                                    tmp2["y"] = y
                                    tmp2["deck_id"] = 0
                                    tmp2["user"] = other_user
                                    tmp2["place"] = "field"
                                    tmp2["mine_or_other"] = field["mine_or_other"]
                                    return_value.append(tmp2)
                                    if (
                                        as_monster_effect
                                        not in cost[str(duelobj.tmp_chain)]
                                    ):
                                        cost[str(duelobj.tmp_chain)][
                                            as_monster_effect
                                        ] = []
                                    cost[str(duelobj.tmp_chain)][
                                        as_monster_effect
                                    ].append(tmp2)
                        else:
                            if field["det"] is None:
                                return HttpResponse("error")
                            else:
                                tmp2 = {}
                                tmp2["det"] = field["det"]
                                tmp2["mine_or_other"] = field["mine_or_other"]
                                tmp2["user"] = chain_user
                                tmp2["place"] = "field"
                                tmp2["deck_id"] = 0
                                tmp2["x"] = x
                                tmp2["y"] = y
                                tmp2["place_unique_id"] = field["det"][
                                    "place_unique_id"
                                ]
                                return_value.append(tmp2)
                                if not duelobj.validate_answer(
                                    tmp2,
                                    monster_effect_det_monster,
                                    exclude,
                                    duel,
                                    1,
                                    cost_flag,
                                    effect_kind,
                                    user,
                                ):
                                    return HttpResponse("error")
                                check_array.append(field["det"])
                                if cost_flag == 0:
                                    if monster_effect_val == 44:
                                        if effect_cost_flag == 0:
                                            if str(duel.chain - 2) not in mess:
                                                mess[str(duel.chain - 2)] = {}
                                            if (
                                                "choose"
                                                not in mess[str(duel.chain - 2)]
                                            ):
                                                mess[str(duel.chain - 2)]["choose"] = []
                                        else:
                                            if str(duel.chain - 2) not in cost:
                                                cost[str(duel.chain - 2)] = {}
                                            if (
                                                "choose"
                                                not in cost[str(duel.chain - 2)]
                                            ):
                                                cost[str(duel.chain - 2)]["choose"] = []
                                    else:
                                        if str(duel.chain - 1) not in mess:
                                            mess[str(duel.chain - 1)] = {}
                                        if "choose" not in mess[str(duel.chain - 1)]:
                                            mess[str(duel.chain - 1)]["choose"] = []
                                    tmp2 = {}
                                    tmp2["det"] = field["det"]
                                    tmp2["hide"] = (
                                        field["hide"] if ("hide" in field) else False
                                    )
                                    tmp2["x"] = x
                                    tmp2["y"] = y
                                    tmp2["deck_id"] = 0
                                    tmp2["place_unique_id"] = field["det"][
                                        "place_unique_id"
                                    ]
                                    tmp2["user"] = other_user
                                    tmp2["place"] = "field"
                                    tmp2["mine_or_other"] = field["mine_or_other"]
                                    if monster_effect_val == 44:
                                        if effect_cost_flag == 0:
                                            if as_monster_effect[0] == "%":
                                                if as_monster_effect not in timing_mess:
                                                    timing_mess[as_monster_effect]=[]
                                                timing_mess[as_monster_effect].append(tmp2)
                                            else:
                                                if (
                                                    as_monster_effect
                                                    not in mess[str(duel.chain - 2)]
                                                ):
                                                    mess[str(duel.chain - 2)][
                                                        as_monster_effect
                                                    ] = []
                                                mess[str(duel.chain - 2)][
                                                    as_monster_effect
                                                ].append(tmp2)
                                        else:
                                            if (
                                                as_monster_effect
                                                not in cost[str(duel.chain - 2)]
                                            ):
                                                cost[str(duel.chain - 2)][
                                                    as_monster_effect
                                                ] = []
                                            cost[str(duel.chain - 2)][
                                                as_monster_effect
                                            ].append(tmp2)
                                    else:
                                        if as_monster_effect[0] == "%":
                                            if as_monster_effect not in timign_mess:
                                                timing_mess[as_monster_effect]=[]
                                            timing_mess[as_monster_effect].append(tmp2)
                                        else:
                                            if (
                                                as_monster_effect
                                                not in mess[str(duel.chain - 1)]
                                            ):
                                                mess[str(duel.chain - 1)][
                                                    as_monster_effect
                                                ] = []
                                            mess[str(duel.chain - 1)][
                                                as_monster_effect
                                            ].append(tmp2)
                                else:
                                    if str(duelobj.tmp_chain) not in cost:
                                        cost[str(duelobj.tmp_chain)] = {}
                                    if "choose" not in cost[str(duelobj.tmp_chain)]:
                                        cost[str(duelobj.tmp_chain)]["choose"] = []
                                    tmp2 = {}
                                    tmp2["det"] = field["det"]
                                    tmp2["hide"] = (
                                        field["hide"] if ("hide" in field) else False
                                    )
                                    tmp2["x"] = x
                                    tmp2["y"] = y
                                    tmp2["deck_id"] = 0
                                    tmp2["place_unique_id"] = field["det"][
                                        "place_unique_id"
                                    ]
                                    tmp2["user"] = other_user
                                    tmp2["place"] = "field"
                                    tmp2["mine_or_other"] = field["mine_or_other"]
                                    return_value.append(tmp2)
                                    if (
                                        as_monster_effect
                                        not in cost[str(duelobj.tmp_chain)]
                                    ):
                                        cost[str(duelobj.tmp_chain)][
                                            as_monster_effect
                                        ] = []
                                    cost[str(duelobj.tmp_chain)][
                                        as_monster_effect
                                    ].append(tmp2)
            else:
                for place in monster_effect_det_monster["place"]:
                    place_tmp = place["det"].split("_")
                    if place_tmp[0] == "field":
                        fields = duelobj.field
                    field = fields[x][y]
                    if field["kind"].find(place_tmp[1]) == -1:
                        continue
                    if int(field["mine_or_other"]) != 0:
                        continue

                    if whether_monster == 0:
                        if field["det"] is not None:
                            return HttpResponse("error")
                        else:
                            if cost_flag == 0:
                                if monster_effect_val == 44:
                                    if effect_cost_flag == 0:
                                        if str(duel.chain - 2) not in mess:
                                            mess[str(duel.chain - 2)] = {}
                                        if "choose" not in mess[str(duel.chain - 2)]:
                                            mess[str(duel.chain - 2)]["choose"] = []
                                    else:
                                        if str(duel.chain - 2) not in cost:
                                            cost[str(duel.chain - 2)] = {}
                                        if "choose" not in cost[str(duel.chain - 2)]:
                                            cost[str(duel.chain - 1)]["choose"] = []
                                else:
                                    if str(duel.chain - 1) not in mess:
                                        mess[str(duel.chain - 1)] = {}
                                    if "choose" not in mess[str(duel.chain - 1)]:
                                        mess[str(duel.chain - 1)]["choose"] = []
                                tmp2 = {}
                                tmp2["mine_or_other"] = field["mine_or_other"]
                                tmp2["det"] = field["det"]
                                tmp2["hide"] = (
                                    field["hide"] if ("hide" in field) else False
                                )
                                tmp2["x"] = x
                                tmp2["y"] = y
                                tmp2["deck_id"] = 0
                                tmp2["user"] = user
                                tmp2["place"] = "field"
                                return_value.append(tmp2)
                                if monster_effect_val == 44:
                                    if effect_cost_flag == 0:
                                        if as_monster_effect[0] == "%":
                                            if as_monster_effect not in timing_mess:
                                                timing_mess[as_monster_effect]=[]
                                            timing_mess[as_monster_effect].append(tmp2)
                                        else:
                                            if (
                                                as_monster_effect
                                                not in mess[str(duel.chain - 2)]
                                            ):
                                                mess[str(duel.chain - 2)][
                                                    as_monster_effect
                                                ] = []
                                            mess[str(duel.chain - 2)][
                                                as_monster_effect
                                            ].append(tmp2)
                                    else:
                                        if (
                                            as_monster_effect
                                            not in cost[str(duel.chain - 2)]
                                        ):
                                            cost[str(duel.chain - 2)][
                                                as_monster_effect
                                            ] = []
                                        cost[str(duel.chain - 2)][
                                            as_monster_effect
                                        ].append(tmp2)
                                else:
                                    if as_monster_effect[0] == "%":
                                        if as_monster_effect not in timing_mess:
                                            timing_mess[as_monster_effect]=[]
                                        timing_mess[as_monster_effect].append(tmp2)
                                    else:
                                       if (
                                           as_monster_effect
                                           not in mess[str(duel.chain - 1)]
                                       ):
                                           mess[str(duel.chain - 1)][
                                               as_monster_effect
                                           ] = []
                                       mess[str(duel.chain - 1)][as_monster_effect].append(
                                           tmp2
                                       )
                            else:
                                if str(duelobj.tmp_chain) not in cost:
                                    cost[str(duelobj.tmp_chain)] = {}
                                if "choose" not in cost[str(duelobj.tmp_chain)]:
                                    cost[str(duelobj.tmp_chain)]["choose"] = []
                                tmp2 = {}
                                tmp2["det"] = field["det"]
                                tmp2["hide"] = (
                                    field["hide"] if ("hide" in field) else False
                                )
                                tmp2["x"] = x
                                tmp2["y"] = y
                                tmp2["deck_id"] = 0
                                tmp2["user"] = user
                                tmp2["place"] = "field"
                                tmp2["mine_or_other"] = field["mine_or_other"]
                                return_value.append(tmp2)
                                if (
                                    as_monster_effect
                                    not in cost[str(duelobj.tmp_chain)]
                                ):
                                    cost[str(duelobj.tmp_chain)][as_monster_effect] = []
                                cost[str(duelobj.tmp_chain)][as_monster_effect].append(
                                    tmp2
                                )
                    else:
                        if field["det"] is None:
                            return HttpResponse("error")
                        else:
                            tmp2 = {}
                            tmp2["det"] = field[x][y]["det"]
                            tmp2["mine_or_other"] = field[x][y]["mine_or_other"]
                            tmp2["user"] = chain_user
                            tmp2["place"] = "field"
                            tmp2["deck_id"] = 0
                            tmp2["x"] = x
                            tmp2["y"] = y
                            tmp2["place_unique_id"] = field[x][y]["det"][
                                "place_unique_id"
                            ]
                            return_value.append(tmp2)
                            if not duelobj.validate_answer(
                                tmp2,
                                monster_effect_det_monster,
                                exclude,
                                duel,
                                1,
                                cost_flag,
                                effect_kind,
                                user,
                            ):
                                return HttpResponse("error")
                            check_array.append(field["det"])
                            if cost_flag == 0:
                                if monster_effect_val != 44:
                                    if str(duel.chain - 1) not in mess:
                                        mess[str(duel.chain - 1)] = {}
                                    if "choose" not in mess[str(duel.chain - 1)]:
                                        mess[str(duel.chain - 1)]["choose"] = []
                                tmp2 = {}
                                tmp2["det"] = field["det"]
                                tmp2["hide"] = (
                                    field["hide"] if ("hide" in field) else False
                                )
                                tmp2["x"] = x
                                tmp2["y"] = y
                                tmp2["deck_id"] = 0
                                tmp2["place_unique_id"] = field["det"][
                                    "place_unique_id"
                                ]
                                tmp2["user"] = user
                                tmp2["place"] = "field"
                                tmp2["mine_or_other"] = field["mine_or_other"]
                                return_value.append(tmp2)
                                if monster_effect_val != 44:
                                    if (
                                        as_monster_effect
                                        not in mess[str(duel.chain - 1)]
                                    ):
                                        mess[str(duel.chain - 1)][
                                            as_monster_effect
                                        ] = []
                                    mess[str(duel.chain - 1)][as_monster_effect].append(
                                        tmp2
                                    )
                                else:
                                    if effect_cost_flag == 0:
                                        if as_monster_effect[0] == "%":
                                            if as_monster_effect not in timing_mess:
                                                timing_mess[as_monster_effect]=[]
                                            timing_mess[as_monster_effect].append(tmp2)
                                        else:
                                            if (
                                                as_monster_effect
                                                not in mess[str(duel.chain - 2)]
                                            ):
                                                mess[str(duel.chain - 2)][
                                                    as_monster_effect
                                                ] = []
                                            mess[str(duel.chain - 2)][
                                                as_monster_effect
                                            ].append(tmp2)
                                    else:
                                        if (
                                            as_monster_effect
                                            not in cost[str(duel.chain - 2)]
                                        ):
                                            cost[str(duel.chain - 2)][
                                                as_monster_effect
                                            ] = []
                                        cost[str(duel.chain - 2)][
                                            as_monster_effect
                                        ].append(tmp2)
                            else:
                                if str(duelobj.tmp_chain) not in cost:
                                    cost[str(duelobj.tmp_chain)] = {}
                                if "choose" not in cost[str(duelobj.tmp_chain)]:
                                    cost[str(duelobj.tmp_chain)]["choose"] = []
                                tmp2 = {}
                                tmp2["det"] = field["det"]
                                tmp2["hide"] = (
                                    field["hide"] if ("hide" in field) else False
                                )
                                tmp2["x"] = x
                                tmp2["y"] = y
                                tmp2["deck_id"] = 0
                                tmp2["place_unique_id"] = field["det"][
                                    "place_unique_id"
                                ]
                                tmp2["user"] = user
                                tmp2["place"] = "field"
                            tmp2["mine_or_other"] = field["mine_or_other"]
                            return_value.append(tmp2)
                            if as_monster_effect not in cost[str(duelobj.tmp_chain)]:
                                cost[str(duelobj.tmp_chain)][as_monster_effect] = []
                            cost[str(duelobj.tmp_chain)][as_monster_effect].append(tmp2)
    duelobj.mess = mess
    duelobj.timing_mess = timing_mess
    duelobj.cost = cost
    choices = None
    if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag is True):
        if duel.user_turn == 1:
            if duel.ask == 1 or duel.ask == 3:
                duel.ask -= 1
        else:
            if duel.ask == 2 or duel.ask == 3:
                duel.ask -= 2
    elif duel.user_2 == request.user or (ID2 == ID and duel.guest_flag2 is True):
        if duel.user_turn == 2:
            if duel.ask == 1 or duel.ask == 3:
                duel.ask -= 1
        else:
            if duel.ask == 2 or duel.ask == 3:
                duel.ask -= 2
    if duel.ask == 0 and duel.in_cost is False:
        chain_det = json.loads(duel.chain_det)
        current_chain = chain_det[str(duel.chain - 1)]
        effect = MonsterEffectWrapper.objects.get(id=current_chain)
        if effect.pac:
            next_effect = duelobj._pac(effect.pac)
        else:
            next_effect = effect.monster_effect_next
        if next_effect != 0 and next_effect is not None:
            chain_det[str(duel.chain - 1)] = next_effect.id
        else:
            pac = json.loads(duel.in_pac)
            if str(duel.chain - 1) in pac and pac[str(duel.chain - 1)] != []:
                pac_id = pac[str(duel.chain - 1)].pop()
                duel.in_pac = json.dumps(pac)
                pac = PacWrapper.objects.get(id=pac_id)
                next_effect = pac.monster_effect_next
                if next_effect is None:
                    trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
                    if trigger.chain_flag is True:
                        duel.virtual_chain -= 1
                    duel.chain -= 1
                else:
                    chain_det[str(duel.chain - 1)] = next_effect.id
            else:
                trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
                if trigger.chain_flag is True:
                    duel.virtual_chain -= 1
                duel.chain -= 1
        duelobj.duel.chain_det = json.dumps(chain_det)
        decks = Deck.objects.all()
        graves = Grave.objects.all()
        hands = Hand.objects.all()
        duelobj.check_eternal_effect(
            decks, graves, hands, duel.phase, duel.user_turn, user, other_user
        )
        if duel.in_trigger_waiting is False:
            duelobj.retrieve_chain(
                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
            )
        if duel.chain == 0:
            duelobj.invoke_after_chain_effect(
                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
            )
            #duelobj.invoke_trigger_waiting(duel.trigger_waiting)
            #duelobj.retrieve_chain(
            #    decks, graves, hands, duel.phase, duel.user_turn, user, other_user
            #)
            duel.appoint = duel.user_turn
            tmp = {}
            duel.mess = json.dumps(tmp)
            duel.cost_result = json.dumps(tmp)
            duel.cost = json.dumps(tmp)
            duelobj.invoke_trigger_waiting(duel.trigger_waiting)
            duel.current_priority = 10000
            choices = duelobj.check_trigger(
                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
            )
        else:
            choices = None
    elif duel.ask == 0:
        cost_det = duel.cost_det
        effect = CostWrapper.objects.get(id=cost_det)
        if effect.pac:
            next_effect = duelobj._pac_cost(cost.pac)
        elif effect.cost_next:
            next_effect = effect.cost_next
        else:
            next_effect = duelobj.pop_pac_cost(user)
        tmp = False
        if next_effect is not None and next_effect != -2:
            duel.cost_det = next_effect.id
            trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
            tmp = duelobj.pay_cost(next_effect, user,duel.chain,trigger)
        else:
            duel.cost_det = 0
        if duel.cost_det == 0 and tmp is False:
            if duel.in_copying is False:
                trigger = Trigger.objects.get(id=duel.current_trigger)
                duelobj.end_cost(duel.cost_user,duel.chain,trigger)
                if trigger.chain_flag is True:
                    duel.virtual_chain += 1
                duel.chain += 1
            else:
                duelobj.end_cost(duel.cost_user,duel.chain,trigger)
        if duel.in_cost is False and duel.chain == 0 and duel.in_copying is False:
            chain_det = json.loads(duel.chain_det)
            current_chain = chain_det[str(0)]
            if current_chain == 0:
                duelobj.cost = {}
        choices = None
    if duel.in_cost is False:
        data = {}
        data["monsters"] = return_value
        if log is None:
            log = ""
        duel.log_turn += duelobj.write_log(log, user, data)
        duel.log += duelobj.write_log(log, user, data)
    duelobj.save_all(user, other_user, room_number)
    free_lock(room_number, lock)
    return battle_det(request, duelobj, choices)


def answer_det(duelobj, duel, user, answer_json, request, del_ask, lock,ID1,ID2):
    global check_array
    if "ID" in request.COOKIES :
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    room_number = int(request.POST["room_number"])
    answer = json.loads(answer_json)
    chain_det = json.loads(duel.chain_det)
    chain_user = json.loads(duel.chain_user)
    chain_user = int(chain_user[str(duel.chain - 1)])
    if duel.in_copying is True:
        duelobj.tmp_chain = str(duel.chain - 1)
    else:
        duelobj.tmp_chain = str(duel.chain)
    if chain_user == 0:
        if request.user == duel.user_1 or (ID1 == ID or duel.guest_flag is True):
            chain_user = 1
        else:
            chain_user = 2
    if user == 1:
        other_user = 2
    else:
        other_user = 1
    monster_effect_wrapper = MonsterEffectWrapper.objects.get(
        id=int(chain_det[str(duel.chain - 1)])
    )
    duelobj.retrieve = 1
    effect_kind = monster_effect_wrapper.monster_effect_kind
    monster_effect = monster_effect_wrapper.monster_effect
    other_user_flag = False
    if monster_effect.monster_effect_val == 4:
        other_user_flag = True
    if monster_effect.monster_effect_val == 5:
        if duelobj.user != chain_user:
            other_user_flag = True

    log = monster_effect_wrapper.log
    monster_effect_text = json.loads(monster_effect.monster_effect)
    monster_effect_val = monster_effect.monster_effect_val
    exclude = monster_effect_text["exclude"]
    if "whether_monster" in monster_effect_text:
        whether_monster = monster_effect_text["whether_monster"]
    else:
        whether_monster = 0
    monster_effect_text = monster_effect_text["monster"]
    if len(answer) < duelobj.calculate_boland(
        monster_effect_text[0]["min_equation_number"], None, other_user_flag
    ) or len(answer) > duelobj.calculate_boland(
        monster_effect_text[0]["max_equation_number"], None, other_user_flag
    ):
        return HttpResponse("error")
    return_val = []
    if monster_effect.monster_effect_val == 65:
        return answer_as_under(
            duelobj,
            duel,
            user,
            answer,
            exclude,
            whether_monster,
            monster_effect_text,
            monster_effect_val,
            request,
            0,
            log,
            lock,
            room_number,
        )
    if monster_effect.monster_effect_val == 57:
        return answer_as(
            duelobj,
            duel,
            user,
            answer,
            exclude,
            whether_monster,
            monster_effect_text,
            monster_effect_val,
            request,
            0,
            log,
            lock,
            room_number,
        )
    for answer_val in answer:
        place_for_answer = answer_val["place"]
        if place_for_answer == "player":
            effect_det_monster = effect_det["monster"]
            as_effect = effect_det["as_monster_condition"]
            for place in effect_det_monster["place"]:
                place_tmp = place["det"].split("_")
                mine_or_other = int(answer_val["mine_or_other"])
                if(place_tmp[0] == "player" and place_tmp[1] == mine_or_other):
                    tmp2 = {}
                    tmp2["kind"] =  "player"
                    tmp2["mine_or_other"] =  mine_or_other
                    tmp[as_effect].append(tmp2)

        elif place_for_answer == "under":
            if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag is True):
                if duel.user_turn == 1:
                    if duel.ask == 1 or duel.ask == 3:
                        return answer_under_det(
                            duelobj,
                            duel,
                            1,
                            answer,
                            exclude,
                            whether_monster,
                            monster_effect_text,
                            monster_effect_val,
                            request,
                            0,
                            log,
                            lock,
                            effect_kind,
                        )
                else:
                    if duel.ask == 2 or duel.ask == 3:
                        return answer_under_det(
                            duelobj,
                            duel,
                            1,
                            answer,
                            exclude,
                            whether_monster,
                            monster_effect_text,
                            monster_effect_val,
                            request,
                            0,
                            log,
                            lock,
                            effect_kind,
                        )
            elif duel.user_2 == request.user or (ID2 == ID and duel.guest_flag2 is True):
                if duel.user_turn == 2:
                    if duel.ask == 1 or duel.ask == 3:
                        return answer_under_det(
                            duelobj,
                            duel,
                            2,
                            answer,
                            exclude,
                            whether_monster,
                            monster_effect_text,
                            monster_effect_val,
                            request,
                            0,
                            log,
                            lock,
                            effect_kind,
                        )
                else:
                    if duel.ask == 2 or duel.ask == 3:
                        return answer_under_det(
                            duelobj,
                            duel,
                            2,
                            answer,
                            exclude,
                            whether_monster,
                            monster_effect_text,
                            monster_effect_val,
                            request,
                            0,
                            log,
                            lock,
                            effect_kind,
                        )
        elif place_for_answer == "field":
            if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag is True):
                if duel.user_turn == 1:
                    if duel.ask == 1 or duel.ask == 3:
                        return answer_field_det(
                            duelobj,
                            duel,
                            1,
                            answer,
                            exclude,
                            whether_monster,
                            monster_effect_text,
                            monster_effect_val,
                            request,
                            0,
                            log,
                            lock,
                            effect_kind,
                        )
                else:
                    if duel.ask == 2 or duel.ask == 3:
                        return answer_field_det(
                            duelobj,
                            duel,
                            1,
                            answer,
                            exclude,
                            whether_monster,
                            monster_effect_text,
                            monster_effect_val,
                            request,
                            0,
                            log,
                            lock,
                            effect_kind,
                        )
            elif duel.user_2 == request.user or (ID2 == ID and duel.guest_flag2 is True):
                if duel.user_turn == 2:
                    if duel.ask == 1 or duel.ask == 3:
                        return answer_field_det(
                            duelobj,
                            duel,
                            2,
                            answer,
                            exclude,
                            whether_monster,
                            monster_effect_text,
                            monster_effect_val,
                            request,
                            0,
                            log,
                            lock,
                            effect_kind,
                        )
                else:
                    if duel.ask == 2 or duel.ask == 3:
                        return answer_field_det(
                            duelobj,
                            duel,
                            2,
                            answer,
                            exclude,
                            whether_monster,
                            monster_effect_text,
                            monster_effect_val,
                            request,
                            0,
                            log,
                            lock,
                            effect_kind,
                        )
        else:
            tmp_count = 0
            place_unique_id = answer_val["place_unique_id"]
            mine_or_other = int(answer_val["mine_or_other"])

            if user == 1:
                if mine_or_other == 1:
                    mine_or_other = 1
                    mine_or_other_org = 1
                elif mine_or_other == 2:
                    mine_or_other = 2
                    mine_or_other_org = 2
                else:
                    mine_or_other = 3
                    mine_or_other_org = 3
            else:
                if mine_or_other == 1:
                    mine_or_other = 2
                    mine_or_other_org = 1
                elif mine_or_other == 2:
                    mine_or_other = 1
                    mine_or_other_org = 2
                else:
                    mine_or_other = 3
                    mine_or_other_org = 3
            for monster_effect_det in monster_effect_text:
                tmp_count += 1
                as_monster_effect = monster_effect_det["as_monster_condition"]
                if monster_effect_val == 44:
                    if as_monster_effect[0] == "%":
                        timing_mess = duelobj.timing_mess
                        #cost_flagが２はtiming_mess
                        cost_flag = 2
                    elif as_monster_effect[0] == "~":
                        cost = duelobj.cost
                        #if str(int(duel.chain-2)) not in cost:
                        cost[str(int(duel.chain - 2))] = {}
                        cost[str(int(duel.chain - 2))]["choose"] = []
                        cost_flag = 1
                    else:
                        mess = duelobj.mess
                        mess[str(int(duel.chain - 2))] = {}
                        mess[str(int(duel.chain - 2))]["choose"] = []
                        cost_flag = 0

                if (user == 1 and chain_user == 1) or (user == 2 and chain_user == 2):
                    if (monster_effect_val == 3) or (
                        monster_effect_val == 5 and tmp_count == 1
                    ):
                        monster_effect_det_monster = monster_effect_det["monster"]
                        for place in monster_effect_det_monster["place"]:
                            current_place_and_or = place["and_or"]
                            place_tmp = place["det"].split("_")
                            deck_id = -1
                            if place_tmp[0] == "deck" and "deck_id" in answer_val:
                                deck_id = int(answer_val["deck_id"])

                            elif place_tmp[0] == "grave" and "grave_id" in answer_val:
                                deck_id = int(answer_val["grave_id"])
                            elif place_tmp[0] == "hand" and "hand_id" in answer_val:
                                deck_id = int(answer_val["hand_id"])
                            if deck_id == -1:
                                continue
                            if place_tmp[0] == place_for_answer:
                                if place_tmp[0] == "deck" and deck_id == int(
                                    place_tmp[1]
                                ):
                                    if mine_or_other_org == 1:
                                        tmp = duelobj.decks[deck_id]["mydeck"]
                                    elif mine_or_other_org == 2:
                                        tmp = duelobj.decks[deck_id]["otherdeck"]
                                    else:
                                        tmp = duelobj.decks[deck_id]["commondeck"]
                                    user_decks = tmp
                                    for user_deck in user_decks:
                                        if (
                                            place_unique_id
                                            == user_deck["place_unique_id"]
                                        ):
                                            tmp2 = {}
                                            tmp2["det"] = user_deck
                                            tmp2["mine_or_other"] = mine_or_other
                                            tmp2["user"] = chain_user
                                            tmp2["place"] = "deck"
                                            tmp2["deck_id"] = deck_id
                                            tmp2["x"] = 0
                                            tmp2["y"] = 0
                                            tmp2["place_unique_id"] = user_deck[
                                                "place_unique_id"
                                            ]
                                            if not duelobj.validate_answer(
                                                tmp2,
                                                monster_effect_det_monster,
                                                exclude,
                                                duel,
                                                1,
                                                0,
                                                effect_kind,
                                                user,
                                            ):
                                                return HttpResponse("error")

                                            check_array.append(user_deck)
                                            tmp = duelobj.mess
                                            if monster_effect_val != 44:
                                                if str(duel.chain - 1) not in tmp:
                                                    tmp[str(duel.chain - 1)] = {}
                                                if (
                                                    "choose"
                                                    not in tmp[str(duel.chain - 1)]
                                                ):
                                                    tmp[str(duel.chain - 1)][
                                                        "choose"
                                                    ] = []
                                            tmp2 = {}
                                            tmp2["det"] = user_deck
                                            tmp2["mine_or_other"] = mine_or_other
                                            tmp2["user"] = user
                                            tmp2["place"] = "deck"
                                            tmp2["deck_id"] = deck_id
                                            tmp2["x"] = 0
                                            tmp2["y"] = 0
                                            tmp2["place_unique_id"] = place_unique_id
                                            return_val.append(tmp2)
                                            if monster_effect_val != 44:
                                                if (
                                                    as_monster_effect
                                                    not in tmp[str(duel.chain - 1)]
                                                ):
                                                    tmp[str(duel.chain - 1)][
                                                        as_monster_effect
                                                    ] = []
                                                tmp[str(duel.chain - 1)][
                                                    as_monster_effect
                                                ].append(tmp2)
                                                duelobj.mess = tmp
                                            else:
                                                if cost_flag == 2:
                                                    timing_mess[
                                                        as_monster_effect
                                                    ].append(tmp2)
                                                    duelobj.timing_mess = timing_mess

                                                elif cost_flag == 0:
                                                    mess[str(duel.chain - 2)][
                                                        as_monster_effect
                                                    ].append(tmp2)
                                                    duelobj.mess = mess
                                                else:
                                                    cost[str(duel.chain - 2)][
                                                        as_monster_effect
                                                    ].append(tmp2)
                                                    duelobj.cost = cost

                                if place_tmp[0] == "grave" and deck_id == int(
                                    place_tmp[1]
                                ):
                                    if mine_or_other_org == 1:
                                        tmp = duelobj.graves[deck_id]["mygrave"]
                                    elif mine_or_other_org == 2:
                                        tmp = duelobj.graves[deck_id]["othergrave"]
                                    else:
                                        tmp = duelobj.graves[deck_id]["commongrave"]
                                    user_graves = tmp
                                    for user_grave in user_graves:
                                        if (
                                            place_unique_id
                                            == user_grave["place_unique_id"]
                                        ):
                                            tmp2 = {}
                                            tmp2["det"] = user_grave
                                            tmp2["mine_or_other"] = mine_or_other
                                            tmp2["user"] = chain_user
                                            tmp2["place"] = "grave1"
                                            tmp2["deck_id"] = deck_id
                                            tmp2["x"] = 0
                                            tmp2["y"] = 0
                                            tmp2["place_unique_id"] = user_grave[
                                                "place_unique_id"
                                            ]
                                            return_val.append(tmp2)
                                            if not duelobj.validate_answer(
                                                tmp2,
                                                monster_effect_det_monster,
                                                exclude,
                                                duel,
                                                1,
                                                0,
                                                effect_kind,
                                                user,
                                            ):
                                                return HttpResponse("error")
                                            check_array.append(user_grave)
                                            tmp = duelobj.mess
                                            if monster_effect_val != 44:
                                                if str(duel.chain - 1) not in tmp:
                                                    tmp[str(duel.chain - 1)] = {}
                                                if (
                                                    "choose"
                                                    not in tmp[str(duel.chain - 1)]
                                                ):
                                                    tmp[str(duel.chain - 1)][
                                                        "choose"
                                                    ] = []
                                            tmp2 = {}
                                            tmp2["x"] = 0
                                            tmp2["y"] = 0
                                            tmp2["det"] = user_grave
                                            tmp2["mine_or_other"] = mine_or_other
                                            tmp2["user"] = user
                                            tmp2["place"] = "grave"
                                            tmp2["deck_id"] = deck_id
                                            tmp2["place_unique_id"] = place_unique_id
                                            return_val.append(tmp2)
                                            if monster_effect_val != 44:
                                                if (
                                                    as_monster_effect
                                                    not in tmp[str(duel.chain - 1)]
                                                ):
                                                    tmp[str(duel.chain - 1)][
                                                        as_monster_effect
                                                    ] = []
                                                tmp[str(duel.chain - 1)][
                                                    as_monster_effect
                                                ].append(tmp2)
                                                duelobj.mess = tmp
                                            else:
                                                if cost_flag == 2:
                                                    timing_mess[
                                                        as_monster_effect
                                                    ].append(tmp2)
                                                    duelobj.timing_mess = timing_mess
                                                elif cost_flag == 0:
                                                    mess[str(duel.chain - 2)][
                                                        as_monster_effect
                                                    ].append(tmp2)
                                                    duelobj.mess = mess
                                                else:
                                                    cost[str(duel.chain - 2)][
                                                        as_monster_effect
                                                    ].append(tmp2)
                                                    duelobj.cost = cost

                                if place_tmp[0] == "hand" and deck_id == int(
                                    place_tmp[1]
                                ):
                                    deck_id = answer_val["hand_id"]
                                    if mine_or_other_org == 1:
                                        tmp = duelobj.hands[deck_id]["myhand"]
                                    elif mine_or_other_org == 2:
                                        tmp = duelobj.hands[deck_id]["otherhand"]
                                    else:
                                        tmp = duelobj.hands[deck_id]["commonhand"]
                                    user_hands = tmp
                                    for user_hand in user_hands:
                                        if (
                                            place_unique_id
                                            == user_hand["place_unique_id"]
                                        ):
                                            tmp2 = {}
                                            tmp2["det"] = user_hand
                                            tmp2["mine_or_other"] = mine_or_other
                                            tmp2["user"] = chain_user
                                            tmp2["place"] = "hand"
                                            tmp2["deck_id"] = deck_id
                                            tmp2["x"] = 0
                                            tmp2["y"] = 0
                                            tmp2["place_unique_id"] = user_hand[
                                                "place_unique_id"
                                            ]
                                            return_val.append(tmp2)
                                            if not duelobj.validate_answer(
                                                tmp2,
                                                monster_effect_det_monster,
                                                exclude,
                                                duel,
                                                1,
                                                0,
                                                effect_kind,
                                                user,
                                            ):
                                                return HttpResponse("error")
                                            check_array.append(user_hand)
                                            tmp = duelobj.mess
                                            if monster_effect_val != 44:
                                                if str(duel.chain - 1) not in tmp:
                                                    tmp[str(duel.chain - 1)] = {}
                                                if (
                                                    "choose"
                                                    not in tmp[str(duel.chain - 1)]
                                                ):
                                                    tmp[str(duel.chain - 1)][
                                                        "choose"
                                                    ] = []
                                            tmp2 = {}
                                            tmp2["x"] = 0
                                            tmp2["y"] = 0
                                            tmp2["det"] = user_hand
                                            tmp2["mine_or_other"] = mine_or_other
                                            tmp2["user"] = user
                                            tmp2["place"] = "hand"
                                            tmp2["deck_id"] = deck_id
                                            tmp2["place_unique_id"] = place_unique_id
                                            return_val.append(tmp2)
                                            if monster_effect_val != 44:
                                                if (
                                                    as_monster_effect
                                                    not in tmp[str(duel.chain - 1)]
                                                ):
                                                    tmp[str(duel.chain - 1)][
                                                        as_monster_effect
                                                    ] = []
                                                tmp[str(duel.chain - 1)][
                                                    as_monster_effect
                                                ].append(tmp2)
                                                duelobj.mess = tmp
                                            else:
                                                if cost_flag == 2:
                                                    timing_mess[
                                                        as_monster_effect
                                                    ].append(tmp2)
                                                    duelobj.timing_mess = timing_mess
                                                elif cost_flag == 0:
                                                    mess[str(duel.chain - 2)][
                                                        as_monster_effect
                                                    ].append(tmp2)
                                                    duelobj.mess = mess
                                                else:
                                                    cost[str(duel.chain - 2)][
                                                        as_monster_effect
                                                    ].append(tmp2)
                                                    duelobj.cost = cost

                if (user == 2 and chain_user == 1) or (user == 1 and chain_user == 2):
                    if (monster_effect_val == 4) or (
                        monster_effect_val == 5 and tmp_count == 2
                    ):
                        monster_effect_det_monster = monster_effect_det["monster"]
                        for place in monster_effect_det_monster["place"]:
                            place_tmp = place["det"].split("_")

                            if place_tmp[0] == "deck":
                                deck_id = answer_val["deck_id"]
                            elif place_tmp[0] == "grave":
                                deck_id = answer_val["grave_id"]
                            elif place_tmp[0] == "hand":
                                deck_id = answer_val["hand_id"]

                            if place_tmp[0] == place_for_answer:
                                if (
                                    place_tmp[0] == "deck"
                                    and int(place_tmp[1]) == deck_id
                                ):
                                    if mine_or_other_org == 1:
                                        tmp = duelobj.decks[deck_id]["mydeck"]
                                    elif mine_or_other_org == 2:
                                        tmp = duelobj.decks[deck_id]["otherdeck"]
                                    else:
                                        tmp = duelobj.decks[deck_id]["commondeck"]
                                    user_decks = tmp
                                    tmp_flag = False
                                    for user_deck in user_decks:
                                        if (
                                            place_unique_id
                                            == user_deck["place_unique_id"]
                                        ):
                                            tmp_flag = True
                                            tmp2 = {}
                                            tmp2["det"] = user_deck
                                            tmp2["mine_or_other"] = mine_or_other
                                            tmp2["user"] = chain_user
                                            tmp2["place"] = "deck"
                                            tmp2["deck_id"] = deck_id
                                            tmp2["x"] = 0
                                            tmp2["y"] = 0
                                            tmp2["place_unique_id"] = user_deck[
                                                "place_unique_id"
                                            ]
                                            return_val.append(tmp2)
                                            if not duelobj.validate_answer(
                                                tmp2,
                                                monster_effect_det_monster,
                                                exclude,
                                                duel,
                                                1,
                                                0,
                                                effect_kind,
                                                user,
                                            ):
                                                return HttpResponse("error")
                                            check_array.append(user_deck)
                                            tmp = duelobj.mess
                                            if monster_effect_val != 44:
                                                if str(duel.chain - 1) not in tmp:
                                                    tmp[str(duel.chain - 1)] = {}
                                                if (
                                                    "choose"
                                                    not in tmp[str(duel.chain - 1)]
                                                ):
                                                    tmp[str(duel.chain - 1)][
                                                        "choose"
                                                    ] = []
                                            tmp2 = {}
                                            tmp2["x"] = 0
                                            tmp2["y"] = 0
                                            tmp2["det"] = user_deck
                                            tmp2["mine_or_other"] = mine_or_other
                                            tmp2["user"] = user
                                            tmp2["place"] = "deck"
                                            tmp2["deck_id"] = deck_id
                                            tmp2["place_unique_id"] = place_unique_id
                                            return_val.append(tmp2)
                                            if monster_effect_val != 44:
                                                if (
                                                    as_monster_effect
                                                    not in tmp[str(duel.chain - 1)]
                                                ):
                                                    tmp[str(duel.chain - 1)][
                                                        as_monster_effect
                                                    ] = []
                                                tmp[str(duel.chain - 1)][
                                                    as_monster_effect
                                                ].append(tmp2)
                                                duelobj.mess = tmp
                                            else:
                                                if cost_flag == 2:
                                                    timing_mess[
                                                        as_monster_effect
                                                    ].append(tmp2)
                                                    duelobj.timing_mess = timing_mess
                                                elif cost_flag == 0:
                                                    mess[str(duel.chain - 2)][
                                                        as_monster_effect
                                                    ].append(tmp2)
                                                    duelobj.mess = mess
                                                else:
                                                    cost[str(duel.chain - 2)][
                                                        as_monster_effect
                                                    ].append(tmp2)
                                                    duelobj.cost = cost
                                    if tmp_flag is False:
                                        return HttpResponse("error")

                                if (
                                    place_tmp[0] == "grave"
                                    and int(place_tmp[1]) == deck_id
                                ):

                                    if mine_or_other_org == 1:
                                        tmp = duelobj.graves[deck_id]["mygrave"]
                                    elif mine_or_other_org == 2:
                                        tmp = duelobj.graves[deck_id]["othergrave"]
                                    else:
                                        tmp = duelobj.graves[deck_id]["commongrave"]
                                    user_graves = tmp
                                    tmp_flag = False

                                    for user_grave in user_graves:
                                        if (
                                            place_unique_id
                                            == user_grave["place_unique_id"]
                                        ):
                                            tmp_flag = True
                                            tmp2 = {}
                                            tmp2["det"] = user_grave
                                            tmp2["mine_or_other"] = mine_or_other
                                            tmp2["user"] = chain_user
                                            tmp2["place"] = "grave"
                                            tmp2["deck_id"] = deck_id
                                            tmp2["x"] = 0
                                            tmp2["y"] = 0
                                            tmp2["place_unique_id"] = user_grave[
                                                "place_unique_id"
                                            ]
                                            return_val.append(tmp2)
                                            if not duelobj.validate_answer(
                                                tmp2,
                                                monster_effect_det_monster,
                                                exclude,
                                                duel,
                                                1,
                                                0,
                                                effect_kind,
                                                user,
                                            ):
                                                return HttpResponse("error")
                                            check_array.append(user_grave)
                                            tmp = duelobj.mess
                                            if monster_effect_val != 44:
                                                if str(duel.chain - 1) not in tmp:
                                                    tmp[str(duel.chain - 1)] = {}
                                                if (
                                                    "choose"
                                                    not in tmp[str(duel.chain - 1)]
                                                ):
                                                    tmp[str(duel.chain - 1)][
                                                        "choose"
                                                    ] = []
                                            tmp2 = {}
                                            tmp2["x"] = 0
                                            tmp2["y"] = 0
                                            tmp2["det"] = user_grave
                                            tmp2["mine_or_other"] = mine_or_other
                                            tmp2["user"] = user
                                            tmp2["place"] = "grave"
                                            tmp2["deck_id"] = deck_id
                                            tmp2["place_unique_id"] = place_unique_id
                                            return_val.append(tmp2)
                                            if monster_effect_val != 44:
                                                if (
                                                    as_monster_effect
                                                    not in tmp[str(duel.chain - 1)]
                                                ):
                                                    tmp[str(duel.chain - 1)][
                                                        as_monster_effect
                                                    ] = []
                                                tmp[str(duel.chain - 1)][
                                                    as_monster_effect
                                                ].append(tmp2)
                                                duelobj.mess = tmp
                                            else:
                                                if cost_flag == 2:
                                                    timing_mess[
                                                        as_monster_effect
                                                    ].append(tmp2)
                                                    duelobj.timing_mess = timing_mess
                                                elif cost_flag == 0:
                                                    mess[str(duel.chain - 2)][
                                                        as_monster_effect
                                                    ].append(tmp2)
                                                    duelobj.mess = mess
                                                else:
                                                    cost[str(duel.chain - 2)][
                                                        as_monster_effect
                                                    ].append(tmp2)
                                                    duelobj.cost = cost
                                    if tmp_flag is False:
                                        return HttpResponse("error")
                                if (
                                    place_tmp[0] == "hand"
                                    and int(place_tmp[1]) == deck_id
                                ):
                                    deck_id = answer_val["hand_id"]
                                    if mine_or_other_org == 1:
                                        tmp = duelobj.hands[deck_id]["myhand"]
                                    elif mine_or_other_org == 2:
                                        tmp = duelobj.hands[deck_id]["otherhand"]
                                    else:
                                        tmp = duelobj.hands[deck_id]["commonhand"]
                                    user_hands = tmp
                                    tmp_flag = False
                                    for user_hand in user_hands:
                                        if (
                                            place_unique_id
                                            == user_hand["place_unique_id"]
                                        ):
                                            tmp_flag = True
                                            tmp2 = {}
                                            tmp2["det"] = user_hand
                                            tmp2["mine_or_other"] = mine_or_other
                                            tmp2["user"] = chain_user
                                            tmp2["place"] = "hand"
                                            tmp2["deck_id"] = deck_id
                                            tmp2["x"] = 0
                                            tmp2["y"] = 0
                                            tmp2["place_unique_id"] = user_hand[
                                                "place_unique_id"
                                            ]
                                            return_val.append(tmp2)
                                            if not duelobj.validate_answer(
                                                tmp2,
                                                monster_effect_det_monster,
                                                exclude,
                                                duel,
                                                1,
                                                0,
                                                effect_kind,
                                                user,
                                            ):
                                                return HttpResponse("error")
                                            check_array.append(user_hand)
                                            tmp = duelobj.mess
                                            if monster_effect_val != 44:
                                                if str(duel.chain - 1) not in tmp:
                                                    tmp[str(duel.chain - 1)] = {}
                                                if (
                                                    "choose"
                                                    not in tmp[str(duel.chain - 1)]
                                                ):
                                                    tmp[str(duel.chain - 1)][
                                                        "choose"
                                                    ] = []
                                            tmp2 = {}
                                            tmp2["det"] = user_hand
                                            tmp2["x"] = 0
                                            tmp2["y"] = 0
                                            tmp2["mine_or_other"] = mine_or_other
                                            tmp2["user"] = user
                                            tmp2["place"] = "hand"
                                            tmp2["deck_id"] = deck_id
                                            tmp2["place_unique_id"] = place_unique_id
                                            return_val.append(tmp2)
                                            if monster_effect_val != 44:
                                                if (
                                                    as_monster_effect
                                                    not in tmp[str(duel.chain - 1)]
                                                ):
                                                    tmp[str(duel.chain - 1)][
                                                        as_monster_effect
                                                    ] = []
                                                tmp[str(duel.chain - 1)][
                                                    as_monster_effect
                                                ].append(tmp2)
                                                duelobj.mess = tmp
                                            else:
                                                if cost_flag == 2:
                                                    timing_mess[
                                                        as_monster_effect
                                                    ].append(tmp2)
                                                    duelobj.timing_mess = timing_mess
                                                elif cost_flag == 0:
                                                    mess[str(duel.chain - 2)][
                                                        as_monster_effect
                                                    ].append(tmp2)
                                                    duelobj.mess = mess
                                                else:
                                                    cost[str(duel.chain - 2)][
                                                        as_monster_effect
                                                    ].append(tmp2)
                                                    duelobj.cost = cost
                                    if tmp_flag is False:
                                        return HttpResponse("error")
    choices = None
    duel.ask -= del_ask
    if monster_effect.monster_condition != "":
        if not check_condition(duel, monster_effect.monster_condition, duelobj):
            return HttpResponse("error")
    if duel.ask == 0:
        chain_det = json.loads(duel.chain_det)
        current_chain = chain_det[str(duel.chain - 1)]
        effect = MonsterEffectWrapper.objects.get(id=current_chain)
        if effect.pac:
            next_effect = duelobj._pac(effect.pac)
        else:
            next_effect = effect.monster_effect_next
        if next_effect != 0:
            chain_det[str(duel.chain - 1)] = next_effect.id
        else:
            pac = json.loads(duel.in_pac)
            if str(duel.chain - 1) in pac and pac[str(duel.chain - 1)] != []:
                pac_id = pac[str(duel.chain - 1)].pop()
                pac = PacWrapper.objects.get(id=pac_id)
                next_effect = pac.monster_effect_next
                if next_effect is None:
                    trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
                    if trigger.chain_flag is True:
                        duel.virtual_chain -= 1
                    duel.chain -= 1
                else:
                    chain_det[str(duel.chain - 1)] = next_effect.id
            else:
                trigger = Triggtrigger = Trigger.objects.get(id=duel.current_trigger)
                if trigger.chain_flag is True:
                   duel.virtual_chain -= 1
                duel.chain -= 1
        duelobj.duel.chain_det = json.dumps(chain_det)
        decks = Deck.objects.all()
        graves = Grave.objects.all()
        hands = Hand.objects.all()
        duelobj.check_eternal_effect(
            decks, graves, hands, duel.phase, duel.user_turn, user, other_user
        )
        if duel.in_trigger_waiting is False :
            duelobj.retrieve_chain(
                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
            )
        if duel.chain == 0:
            duelobj.invoke_after_chain_effect(
                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
            )
            #duelobj.nvoke_trigger_waiting(duel.trigger_waiting)
            #duelobj.retrieve_chain(
            #    decks, graves, hands, duel.phase, duel.user_turn, user, other_user
            #)
            duel.appoint = duel.user_turn
            tmp = {}
            duel.mess = json.dumps(tmp)
            duel.cost_result = json.dumps(tmp)
            duel.cost = json.dumps(tmp)
            duelobj.invoke_trigger_waiting(duel.trigger_waiting)
            duel.current_priority = 10000
            choices = duelobj.check_trigger(
                decks, graves, hands, duel.phase, duel.user_turn, user, other_user
            )
    if duel.in_cost is False:
        data = {}
        data["monsters"] = return_val
        if log is None:
            log = ""
        duel.log_turn += duelobj.write_log(log, user, data)
        duel.log += duelobj.write_log(log, user, data)
    duelobj.save_all(user, other_user, room_number)
    free_lock(room_number, lock)
    return battle_det(request, duelobj, choices)


def answer_field_det_cost(
    duelobj,
    duel,
    user,
    answer,
    exclude,
    whether_monster,
    cost_text,
    cost_effect_val,
    request,
    room_number,
    lock,
    effect_kind,
):
    return answer_field_det(
        duelobj,
        duel,
        user,
        answer,
        exclude,
        whether_monster,
        cost_text,
        cost_effect_val,
        request,
        room_number,
        None,
        lock,
        effect_kind,
    )


def answer_det_cost(duelobj, duel, user, answer, request, del_ask, room_number, lock,ID1,ID2):
    if "ID" in request.COOKIES :
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    if user == 1:
        other_user = 2
    else:
        other_user = 1
    global check_array
    room_number = int(request.POST["room_number"])

    cost_det = duel.cost_det
    cost_user = duel.cost_user
    if cost_user == 0:
        if request.user == duel.user_1 or (ID1 == ID and duel.guest_flag is True):
            cost_user = 1
        else:
            cost_user = 2
    cost_wrapper = CostWrapper.objects.get(id=cost_det)
    cost = cost_wrapper.cost
    other_user_flag = False
    if cost.cost_val == 4:
        other_user_flag = True
    if cost.cost_val == 5:
        if duelobj.user != cost_user:
            other_user_flag = True
    effect_kind = cost_wrapper.cost_kind
    cost_text = json.loads(cost.cost)
    cost_effect_val = cost.cost_val
    exclude = cost_text["exclude"]
    if duel.in_copying is True:
        duelobj.tmp_chain = str(duel.chain - 1)
    else:
        duelobj.tmp_chain = str(duel.chain)
    if "whether_monster" in cost_text:
        whether_monster = cost_text["whether_monster"]
    else:
        whether_monster = 0
    cost_text = cost_text["monster"]
    if len(answer) < duelobj.calculate_boland(
        cost_text[0]["min_equation_number"], None, other_user_flag
    ) or len(answer) > duelobj.calculate_boland(
        cost_text[0]["max_equation_number"], None, other_user_flag
    ):
        free_lock(room_number, lock)
        return HttpResponse("error")
    own_player_flag = False
    other_player_flag = True
    for answer_val in answer:
        place_for_answer = answer_val["place"]
        if place_for_answer == "player":
            cost_det_monster = cost_det["monster"]
            as_cost = cost_det["as_monster_condition"]
            for place in cost_det_monster["place"]:
                place_tmp = place["det"].split("_")
                mine_or_other = int(answer_val["mine_or_other"])
                if(place_tmp[0] == "player" and place_tmp[1] == mine_or_other):
                    if place_tmp[1] == "1":
                        if own_player_flag == True:
                            free_lock(room_number, lock)
                            return HttpResponse("error")
                        else:
                            own_player_flag = True
                    if place_tmp[1] == "2":
                        if other_player_flag == True:
                            free_lock(room_number, lock)
                            return HttpResponse("error")
                        else:
                            other_player_flag = True
                    tmp2 = {}
                    tmp2["place"] =  "player"
                    tmp2["mine_or_other"] =  mine_or_other
                    tmp[as_cost].append(tmp2)

        elif place_for_answer == "field":
            if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag is True):
                if duel.user_turn == 1:
                    if duel.ask == 1 or duel.ask == 3:
                        return_value = answer_field_det_cost(
                            duelobj,
                            duel,
                            1,
                            answer,
                            exclude,
                            whether_monster,
                            cost_text,
                            cost_effect_val,
                            request,
                            room_number,
                            lock,
                            effect_kind,
                        )
                        free_lock(room_number, lock)
                        return return_value

                else:
                    if duel.ask == 2 or duel.ask == 3:
                        return_value = answer_field_det_cost(
                            duelobj,
                            duel,
                            1,
                            answer,
                            exclude,
                            whether_monster,
                            cost_text,
                            cost_effect_val,
                            request,
                            room_number,
                            lock,
                            effect_kind,
                        )
                        free_lock(room_number, lock)
                        return return_value
            elif duel.user_2 == request.user or (ID2 == ID and duel.guest_flag2 is True):
                if duel.user_turn == 2:
                    if duel.ask == 1 or duel.ask == 3:
                        return_value = answer_field_det_cost(
                            duelobj,
                            duel,
                            2,
                            answer,
                            exclude,
                            whether_monster,
                            cost_text,
                            cost_effect_val,
                            request,
                            room_number,
                            lock,
                            effect_kind,
                        )
                        free_lock(room_number, lock)
                        return return_value
                else:
                    if duel.ask == 2 or duel.ask == 3:
                        return_value = answer_field_det_cost(
                            duelobj,
                            duel,
                            2,
                            answer,
                            exclude,
                            whether_monster,
                            cost_text,
                            cost_effect_val,
                            request,
                            room_number,
                            lock,
                            effect_kind,
                        )
                        free_lock(room_number, lock)
                        return return_value
        else:
            place_unique_id = answer_val["place_unique_id"]
            mine_or_other = int(answer_val["mine_or_other"])
            if user == 2:
                if mine_or_other == 1:
                    mine_or_other_absolute = 2
                elif mine_or_other == 2:
                    mine_or_other_absolute = 1
            else:
                mine_or_other_absolute = mine_or_other

            for cost_det in cost_text:
                as_cost = cost_det["as_monster_condition"]
                if (user == 1 and cost_user == 1) or (user == 2 and cost_user == 2):
                    cost_det_monster = cost_det["monster"]
                    for place in cost_det_monster["place"]:
                        place_tmp = place["det"].split("_")

                        if place_tmp[0] == place_for_answer:
                            if place_tmp[0] == "deck":
                                deck_id = answer_val["deck_id"]
                                if mine_or_other == 1:
                                    tmp = duelobj.decks[deck_id]["mydeck"]
                                elif mine_or_other == 2:
                                    tmp = duelobj.decks[deck_id]["otherdeck"]
                                else:
                                    tmp = duelobj.decks[deck_id]["commondeck"]
                                user_decks = tmp
                                for user_deck in user_decks:
                                    if place_unique_id == user_deck["place_unique_id"]:
                                        tmp2 = {}
                                        tmp2["det"] = user_deck
                                        tmp2["mine_or_other"] = mine_or_other
                                        tmp2["user"] = user
                                        tmp2["place"] = "deck"
                                        tmp2["deck_id"] = deck_id
                                        tmp2["x"] = 0
                                        tmp2["y"] = 0
                                        tmp2["place_unique_id"] = user_deck[
                                            "place_unique_id"
                                        ]
                                        if not duelobj.validate_answer(
                                            tmp2,
                                            cost_det_monster,
                                            exclude,
                                            duel,
                                            1,
                                            1,
                                            effect_kind,
                                            user,
                                        ):
                                            free_lock(room_number, lock)
                                            return HttpResponse("error")
                                        check_array.append(user_deck)
                                        tmp3 = duelobj.cost
                                        tmp = tmp3[str(duelobj.tmp_chain)]
                                        if "choose" not in tmp:
                                            tmp["choose"] = []
                                        tmp2 = {}
                                        tmp2["x"] = 0
                                        tmp2["y"] = 0
                                        tmp2["det"] = user_deck
                                        tmp2["mine_or_other"] = mine_or_other_absolute
                                        tmp2["user"] = user
                                        tmp2["place"] = "deck"
                                        tmp2["deck_id"] = deck_id
                                        tmp2["place_unique_id"] = place_unique_id
                                        if as_cost not in tmp:
                                            tmp[as_cost] = []
                                        tmp[as_cost].append(tmp2)
                                        tmp3[str(duel.chain)] = tmp
                                        duelobj.cost = tmp3

                            if place_tmp[0] == "grave":
                                deck_id = answer_val["grave_id"]
                                if mine_or_other == 1:
                                    tmp = duelobj.graves[deck_id]["mygrave"]
                                elif mine_or_other == 2:
                                    tmp = duelobj.graves[deck_id]["othergrave"]
                                else:
                                    tmp = duelobj.graves[deck_id]["commongrave"]
                                user_graves = tmp
                                for user_grave in user_graves:
                                    if place_unique_id == user_grave["place_unique_id"]:
                                        tmp2 = {}
                                        tmp2["det"] = user_grave
                                        tmp2["mine_or_other"] = mine_or_other
                                        tmp2["user"] = user
                                        tmp2["place"] = "grave"
                                        tmp2["deck_id"] = deck_id
                                        tmp2["x"] = 0
                                        tmp2["y"] = 0
                                        tmp2["place_unique_id"] = user_grave[
                                            "place_unique_id"
                                        ]
                                        if not duelobj.validate_answer(
                                            tmp2,
                                            cost_det_monster,
                                            exclude,
                                            duel,
                                            1,
                                            0,
                                            effect_kind,
                                            user,
                                        ):
                                            free_lock(room_number, lock)
                                            return HttpResponse("error")
                                        check_array.append(user_grave)
                                        tmp3 = duelobj.cost
                                        tmp = tmp3[str(duelobj.tmp_chain)]
                                        if "choose" not in tmp:
                                            tmp["choose"] = []
                                        tmp2 = {}
                                        tmp2["x"] = 0
                                        tmp2["y"] = 0
                                        tmp2["det"] = user_grave
                                        tmp2["mine_or_other"] = mine_or_other_absolute
                                        tmp2["user"] = user
                                        tmp2["place"] = "grave"
                                        tmp2["deck_id"] = deck_id
                                        tmp2["place_unique_id"] = place_unique_id
                                        if as_cost not in tmp:
                                            tmp[as_cost] = []
                                        tmp[as_cost].append(tmp2)
                                        tmp3[str(duel.chain)] = tmp
                                        duelobj.cost = tmp3

                            if place_tmp[0] == "hand":
                                deck_id = answer_val["hand_id"]
                                if mine_or_other == 1:
                                    tmp = duelobj.hands[deck_id]["myhand"]
                                elif mine_or_other == 2:
                                    tmp = duelobj.hands[deck_id]["otherhand"]
                                else:
                                    tmp = duelobj.hands[deck_id]["commonhand"]
                                user_hands = tmp
                                for user_hand in user_hands:
                                    if place_unique_id == user_hand["place_unique_id"]:
                                        tmp2 = {}
                                        tmp2["det"] = user_hand
                                        tmp2["mine_or_other"] = mine_or_other
                                        tmp2["user"] = user
                                        tmp2["place"] = "hand"
                                        tmp2["deck_id"] = deck_id
                                        tmp2["x"] = 0
                                        tmp2["y"] = 0
                                        tmp2["place_unique_id"] = user_hand[
                                            "place_unique_id"
                                        ]
                                        if not duelobj.validate_answer(
                                            tmp2,
                                            cost_det_monster,
                                            exclude,
                                            duel,
                                            1,
                                            0,
                                            effect_kind,
                                            user,
                                        ):
                                            free_lock(room_number, lock)
                                            return HttpResponse("error")
                                        check_array.append(user_hand)
                                        tmp3 = duelobj.cost
                                        tmp = tmp3[str(duelobj.tmp_chain)]
                                        if "choose" not in tmp:
                                            tmp["choose"] = []
                                        tmp2 = {}
                                        tmp2["x"] = 0
                                        tmp2["y"] = 0
                                        tmp2["det"] = user_hand
                                        tmp2["mine_or_other"] = mine_or_other_absolute
                                        tmp2["user"] = user
                                        tmp2["place"] = "hand"
                                        tmp2["deck_id"] = deck_id
                                        tmp2["place_unique_id"] = place_unique_id
                                        if as_cost not in tmp:
                                            tmp[as_cost] = []
                                        tmp[as_cost].append(tmp2)
                                        tmp3[str(duel.chain)] = tmp
                                        duelobj.cost = tmp3

                if (user == 2 and cost_user == 1) or (user == 1 and cost_user == 2):
                    for place in cost_det["place"].values():
                        place_tmp = place["det"].split("_")

                        if place_tmp[0] == place_for_answer:
                            if place_tmp[0] == "deck":
                                deck_id = answer_val["deck_id"]
                                if mine_or_other == 1:
                                    tmp = duelobj.decks[deck_id]["mydeck"]
                                elif mine_or_other == 2:
                                    tmp = duelobj.decks[deck_id]["otherdeck"]
                                else:
                                    tmp = duelobj.decks[deck_id]["commondeck"]
                                user_decks = tmp
                                for user_deck in user_decks:
                                    if place_unique_id == user_deck["place_unique_id"]:
                                        tmp2 = {}
                                        tmp2["det"] = user_deck
                                        tmp2["mine_or_other"] = mine_or_other
                                        tmp2["user"] = user
                                        tmp2["place"] = "deck"
                                        tmp2["deck_id"] = deck_id
                                        tmp2["x"] = 0
                                        tmp2["y"] = 0
                                        tmp2["place_unique_id"] = user_deck[
                                            "place_unique_id"
                                        ]
                                        if not duelobj.validate_answer(
                                            tmp2,
                                            cost_det_monster,
                                            exclude,
                                            duel,
                                            1,
                                            0,
                                            effect_kind,
                                            user,
                                        ):
                                            free_lock(room_number, lock)
                                            return HttpResponse("error")
                                        check_array.append(user_deck)
                                        tmp3 = duelobj.cost
                                        tmp = tmp3[str(duelobj.tmp_chain)]
                                        if "choose" not in tmp:
                                            tmp["choose"] = []
                                        tmp2 = {}
                                        tmp2["x"] = 0
                                        tmp2["y"] = 0
                                        tmp2["det"] = user_deck
                                        tmp2["mine_or_other"] = mine_or_other_absolute
                                        tmp2["user"] = user
                                        tmp2["place"] = "deck"
                                        tmp2["deck_id"] = deck_id
                                        tmp2["place_unique_id"] = place_unique_id
                                        if as_cost not in tmp:
                                            tmp[as_cost] = []
                                        tmp[as_cost].append(tmp2)
                                        tmp3[str(duel.chain)] = tmp
                                        duelobj.cost = tmp3

                            if place_tmp[0] == "grave":
                                deck_id = answer_val["grave_id"]
                                if mine_or_other == 1:
                                    tmp = duelobj.graves[deck_id]["mygrave"]
                                elif mine_or_other == 2:
                                    tmp = duelobj.graves[deck_id]["othergrave"]
                                else:
                                    tmp = duelobj.graves[deck_id]["commongrave"]
                                user_graves = tmp
                                for user_grave in user_graves:
                                    if place_unique_id == user_grave["place_unique_id"]:
                                        tmp2 = {}
                                        tmp2["det"] = user_grave
                                        tmp2["mine_or_other"] = mine_or_other
                                        tmp2["user"] = user
                                        tmp2["place"] = "grave"
                                        tmp2["deck_id"] = deck_id
                                        tmp2["x"] = 0
                                        tmp2["y"] = 0
                                        tmp2["place_unique_id"] = user_grave[
                                            "place_unique_id"
                                        ]
                                        if not duelobj.validate_answer(
                                            tmp2,
                                            cost_det_monster,
                                            exclude,
                                            duel,
                                            1,
                                            0,
                                            effect_kind,
                                            user,
                                        ):
                                            free_lock(room_number, lock)
                                            return HttpResponse("error")
                                        check_array.append(user_grave)
                                        tmp3 = duelobj.cost
                                        tmp = tmp3[str(duelobj.tmp_chain)]
                                        if "choose" not in tmp:
                                            tmp["choose"] = []
                                        tmp2 = {}
                                        tmp2["x"] = 0
                                        tmp2["y"] = 0
                                        tmp2["det"] = user_grave
                                        tmp2["mine_or_other"] = mine_or_other_absolute
                                        tmp2["user"] = user
                                        tmp2["place"] = "grave"
                                        tmp2["deck_id"] = deck_id
                                        tmp2["place_unique_id"] = place_unique_id
                                        if as_cost not in tmp:
                                            tmp[as_cost] = []
                                        tmp[as_cost].append(tmp2)
                                        tmp3[str(duel.chain)] = tmp
                                        duelobj.cost = tmp3
                            if place_tmp[0] == "hand":
                                deck_id = answer_val["hand_id"]
                                if mine_or_other == 1:
                                    tmp = duelobj.hands[deck_id]["myhand"]
                                elif mine_or_other == 2:
                                    tmp = duelobj.hands[deck_id]["otherhand"]
                                else:
                                    tmp = duelobj.hands[deck_id]["commonhand"]
                                user_hands = tmp
                                for user_hand in user_hands:
                                    if place_unique_id == user_hand["place_unique_id"]:
                                        tmp2 = {}
                                        tmp2["det"] = user_hand
                                        tmp2["mine_or_other"] = mine_or_other
                                        tmp2["user"] = user
                                        tmp2["place"] = "hand"
                                        tmp2["deck_id"] = deck_id
                                        tmp2["x"] = 0
                                        tmp2["y"] = 0
                                        tmp2["place_unique_id"] = user_hand[
                                            "place_unique_id"
                                        ]
                                        if not duelobj.validate_answer(
                                            tmp2,
                                            cost_det_monster,
                                            exclude,
                                            duel,
                                            1,
                                            1,
                                            effect_kind,
                                            user,
                                        ):
                                            free_lock(room_number, lock)
                                            return HttpResponse("error")
                                        check_array.append(user_hand)
                                        tmp3 = duelobj.cost
                                        tmp = tmp3[str(duelobj.tmp_chain)]
                                        if "choose" not in tmp:
                                            tmp["choose"] = []
                                        tmp2 = {}
                                        tmp2["x"] = 0
                                        tmp2["y"] = 0
                                        tmp2["det"] = user_hand
                                        tmp2["mine_or_other"] = mine_or_other_absolute
                                        tmp2["user"] = user
                                        tmp2["place"] = "hand"
                                        tmp2["deck_id"] = deck_id
                                        tmp2["place_unique_id"] = place_unique_id
                                        if as_cost not in tmp:
                                            tmp[as_cost] = []
                                        tmp[as_cost].append(tmp2)
                                        tmp3[str(duel.chain)] = tmp
                                        duelobj.cost = tmp3

    if cost.cost_condition != "":
        if not check_condition(cost.cost_condition, duelobj):
            free_lock(room_number, lock)
            return HttpResponse("error")
    if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag is True):
        if duel.user_turn == 1:
            if duel.ask == 1 or duel.ask == 3:
                duel.ask -= 1
        else:
            if duel.ask == 2 or duel.ask == 3:
                duel.ask -= 2
    elif duel.user_2 == request.user or (ID2 == ID and duel.guest_flag2 is True):
        if duel.user_turn == 2:
            if duel.ask == 1 or duel.ask == 3:
                duel.ask -= 1
        else:
            if duel.ask == 2 or duel.ask == 3:
                duel.ask -= 2
    if duel.ask == 0:
        cost_det = duel.cost_det
        effect = CostWrapper.objects.get(id=cost_det)
        if effect.pac:
            next_effect = duelobj._pac_cost(cost.pac)
        elif effect.cost_next:
            next_effect = effect.cost_next
        else:
            next_effect = duelobj.pop_pac_cost(user)
        if next_effect is not None and next_effect != -2:
            duel.cost_det = next_effect.id
        else:
            duel.cost_det = 0
            next_effect = None
        trigger = Trigger.objects.get(id=duel.current_trigger)
        tmp = duelobj.pay_cost(next_effect, user,duel.chain,trigger)
        if next_effect == 0 or tmp is True:
            duelobj.end_cost(duel.cost_user,duel.chain,trigger)
        duelobj.save_all(user, other_user, room_number)
    free_lock(room_number, lock)
    return battle_det(request, duelobj)


def check_condition(duel, monster_condition, duelobj):
    monster = None
    duelobj.duel = duel
    global check_array
    effect_det_org = json.loads(monster_condition)
    if "different_flag" in effect_det_org:
        different_flag = effect_det_org["different_flag"]
    else:
        different_flag = False
    effect_det = effect_det_org["monster"][0]["monster"]

    monster_name_kind = effect_det["monster_name_kind"]
    equation_kind = effect_det_org["monster"][0]["equation"]["equation_kind"]
    current_and_or = "and"
    count = 0
    variety = []
    same_name = {}
    variable_variety = []
    variable_counter = 0
    counter = -1
    x_counter = 0
    y_counter = 0
    if (
        equation_kind != "number"
        and equation_kind != "kind"
        and equation_kind != "same_name"
    ):
        counter = equation_kind
    different_array = []
    for monster in check_array:
        if different_flag ==True:
            if monster["monster_name"] in different_array:
                return False
            else:
                different_array.append(monster["monster_name"])
        name_flag = True
        for name_kind in monster_name_kind:
            if name_kind != "":
                if name_kind["operator"] == "=":
                    if monster["monster_name"] != duelobj.get_name(
                        name_kind["monster_name"]
                    ):
                        if current_and_or == "and":
                            name_flag = False
                    else:
                        if current_and_or == "or":
                            name_flag = True
                    current_and_or = name_kind["and_or"]

                elif name_kind["operator"] == "like":
                    if (
                        monster["monster_name"].find(
                            duelobj.get_name(name_kind["monster_name"])
                        )
                        > -1
                    ):
                        if current_and_or == "and":
                            name_flag = False
                    else:
                        if current_and_or == "or":
                            name_flag = True
                    current_and_or = name_kind["and_or"]
        if name_flag is False:
            continue

        monster_condition_val = effect_det["monster_condition"]
        cond_flag = True
        for cond_det in monster_condition_val:
            current_and_or = "and"
            tmp_flag = True

            for cond_val in cond_det:
                if len(cond_val) == 0:
                    continue

                tmp = monster["variables"][cond_val["name"]]
                if cond_val["init"] == 0:
                    value = tmp["value"]
                elif cond_val["init"] == 1:
                    value = tmp["i_val"]
                elif cond_val["init"] == 2:
                    value = tmp["i_i_val"]
                if cond_val["operator"] == "=" or cond_val["operator"] == "":
                    if int(value) != duelobj.calculate_boland(cond_val["num"]):
                        tmp_flag = False
                elif cond_val["operator"] == "<=":
                    if int(value) > duelobj.calculate_boland(cond_val["num"]):
                        tmp_flag = False
                elif cond_val["operator"] == ">=":
                    if int(value) < duelobj.calculate_boland(cond_val["num"]):
                        tmp_flag = False
                elif cond_val["operator"] == "!=":
                    if int(value) == duelobj.calculate_boland(cond_val["num"]):
                        tmp_flag = False
                if current_and_or == "and":
                    if cond_flag is True:
                        cond_flag = tmp_flag
                else:
                    if cond_flag is False:
                        cond_flag = tmp_flag
            if cond_flag is False:
                break
        if cond_flag is False:
            continue
        custom_monster_condition = effect_det["custom_monster_condition"]
        cond_flag = True
        for cond_det in custom_monster_condition:
            current_and_or = "and"
            tmp_flag = True
            for cond_val in cond_det:
                if not cond_val:
                    continue
                tmp = monster["custom_variables"][cond_val["name"]]
                if cond_val["init"] == 0:
                    value = tmp["value"]
                elif cond_val["init"] == 1:
                    value = tmp["i_val"]
                elif cond_val["init"] == 2:
                    value = tmp["i_i_val"]
                if cond_val["operator"] == "=" or cond_val["operator"] == "":
                    if int(value) != duelobj.calculate_boland(cond_val["num"]):
                        tmp_flag = False
                elif cond_val["operator"] == "<=":
                    if int(value) > duelobj.calculate_boland(cond_val["num"]):
                        tmp_flag = False
                elif cond_val["operator"] == ">=":
                    if int(value) < duelobj.calculate_boland(cond_val["num"]):
                        tmp_flag = False
                elif cond_val["operator"] == "!=":
                    if int(value) == duelobj.calculate_boland(cond_val["num"]):
                        tmp_flag = False
                if current_and_or == "and":
                    if cond_flag is True:
                        cond_flag = tmp_flag

                else:
                    if cond_flag is False:
                        cond_flag = tmp_flag
            if cond_flag is False:
                break
        if cond_flag is False:
            continue
        if counter != -1:
            variable = monster["variables"][counter]["value"]
            tmp_varieties = variable.split("_")
            for tmp_variety in tmp_varieties:
                variable_variety.append(tmp_variety)
            variable_counter += int(variable)
        if monster["id"] not in variety:
            variety.append(monster["id"])
        if monster["monster_name"] not in same_name:
            same_name[monster["monster_name"]] = 0
        same_name[monster["monster_name"]] += 1
        count += 1
    min_equation_number = effect_det_org["monster"][0]["min_equation_number"]
    max_equation_number = effect_det_org["monster"][0]["max_equation_number"]
    if equation_kind == "number":
        if count >= duelobj.calculate_boland(
            min_equation_number, monster
        ) and count <= duelobj.calculate_boland(max_equation_number, monster):
            return True
        else:
            return False

    elif equation_kind == "kind":
        if len(variety) >= duelobj.calculate_boland(
            min_equation_number, monster
        ) and len(variety) <= duelobj.calculate_boland(max_equation_number, monster):
            return True
        else:
            return False
    elif equation_kind == "same_name":
        same_name_max = max(same_name.values())
        if (
            same_name
            and same_name_max >= duelobj.calculate_boland(min_equation_number, monster)
            and same_name_max <= duelobj.calculate_boland(max_equation_number, monster)
        ):
            return True
        else:
            return False
    elif counter == "x":
        if x_counter >= duelobj.calculate_boland(
            min_equation_number, monster
        ) and x_counter <= duelobj.calculate_boland(max_equation_number, monster):
            return True
        else:
            return False
    elif counter == "y":
        if y_counter >= duelobj.calculate_boland(
            min_equation_number, monster
        ) and y_counter <= duelobj.calculate_boland(max_equation_number, monster):
            return True
        else:
            return False
    else:
        if variable_counter >= duelobj.calculate_boland(
                min_equation_number, monster
        ) and variable_counter <= duelobj.calculate_boland(max_equation_number, monster):
            return True
        else:
            return False


def free_lock(room_number, lock):
    if room_number == 1:
        lock.lock_1 = False
        lock.save()
    elif room_number == 2:
        lock.lock_2 = False
        lock.save()
    elif room_number == 3:
        lock.lock_3 = False
        lock.save()

def force_trigger(request):
    global check_array
    room_number = int(request.POST["room_number"])
    lock = Lock.objects.get()
    lock_flag = lock_lock(room_number, lock,request)
    if lock_flag != "OK":
        return HttpResponse("waiting")
    duelobj = DuelObj(room_number)
    check_array = []
    duel = Duel.objects.filter(id=room_number).get()
    if "ID" in request.COOKIES :
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    ID1 = duel.guest_id
    ID2 = duel.guest_id2
    if duel.user_1 != request.user and duel.user_2 != request.user:
        if (ID1 == ID and duel.guest_flag) or (ID2 == ID and duel.guest_flag2):
            pass
        else:
            free_lock(room_number, lock)
            return HttpResponseRedirect(reverse("tcgcreator:watch_battle"))
    duelobj.duel = duel
    duelobj.room_number = room_number
    if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag):
        user = 1
        other_user = 2
        duelobj.user = 1
    else:
        duelobj.user = 2
        user = 2
        other_user = 1
    duelobj.init_all(user, other_user, room_number)
    duelobj.in_execute = False
    decks = Deck.objects.all()
    graves = Grave.objects.all()
    hands = Hand.objects.all()
    duelobj.check_eternal_effect(
        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
    chain_det = json.loads(duel.chain_det)
    monster_effect_wrapper = MonsterEffectWrapper.objects.get(
        id=int(chain_det[str(duel.chain - 1)])
    )
    monster_effect = monster_effect_wrapper.monster_effect
    if monster_effect.monster_effect_val != 59:
        free_lock(room_number, lock)
        return HttpResponse("error")
    det = json.loads(monster_effect.monster_effect)
    deck_id = det["deck_id"]
    ignore_timing = det["ignore_timing"]
    if duel.user_turn == 1:
        if duel.ask == 1:
            if user == 2:
                return HttpResponse("error")
        elif duel.ask == 2:
            if user == 1:
                return HttpResponse("error")
    elif duel.user_turn == 2:
        if duel.ask == 2:
            if user == 2:
                return HttpResponse("error")
        elif duel.ask == 1:
            if user == 1:
                return HttpResponse("error")
    place_unique_id = request.POST["place_unique_id"]
    hand = duelobj.hands[deck_id]["otherhand"]
    user_hands = hand
    i=0
    mine_or_other = other_user
    for user_hand in user_hands:
        if user_hand["place_unique_id"] != place_unique_id:
            continue
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
                duelobj.invoke_force_trigger(
                    trigger,
                    "hand",
                    user_hand,
                    mine_or_other,
                    other_user,
                    deck_id,
                    0,
                    0,
                    None,
                    None,
                    None,
                    None,
                    None,
                )
                duelobj.save_all(user, other_user, room_number)
                free_lock(room_number, lock)
                return battle_det(request, duelobj, None)
    free_lock(room_number, lock)
    return HttpResponse("error")

def change_wait(request):
    room_number = int(request.POST["room_number"])
    lock = Lock.objects.get()
    lock_flag = lock_lock(room_number, lock,request)
    if lock_flag != "OK":
        return HttpResponse("waiting")
    duel = Duel.objects.filter(id=room_number).get()
    if "ID" in request.COOKIES :
        ID = request.COOKIES["ID"]
    else:
        ID = ""
    ID1 = duel.guest_id
    ID2 = duel.guest_id2
    duelobj = DuelObj(room_number)
    duelobj.duel = duel
    duelobj.room_number = room_number
    if not request.user.is_authenticated:
        if (ID1 == ID and duel.guest_flag) or (ID2 == ID and duel.guest_flag2):
            pass
        else:
            free_lock(room_number, lock)
            return HttpResponse("Please Login")
    if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag is True):
        user = 1
        duelobj.user = 1
        other_user = 2
    else:
        duelobj.user = 2
        user = 2
        other_user = 1
    duelobj.init_all(user, other_user, room_number)
    if user == 1:
        whether_my_phase = duel.phase_whether_1_1.split("_")
        whether_my_kind = duel.kind_whether_1_1.split("_")
        whether_my_timing = duel.timing_whether_1_1.split("_")
        whether_other_phase = duel.phase_whether_1_2.split("_")
        whether_other_kind = duel.kind_whether_1_2.split("_")
        whether_other_timing = duel.timing_whether_1_2.split("_")
    else:
        whether_my_phase = duel.phase_whether_2_1.split("_")
        whether_my_kind = duel.kind_whether_2_1.split("_")
        whether_my_timing = duel.timing_whether_2_1.split("_")
        whether_other_phase = duel.phase_whether_2_2.split("_")
        whether_other_kind = duel.kind_whether_2_2.split("_")
        whether_other_timing = duel.timing_whether_2_2.split("_")
    checks = request.POST["check"].split("_")
    for check in checks:
        check_det = check.split("-")
        if check_det[0] == "phase":
            if check_det[1] == "my":
                if check_det[3] == "check":
                    if check_det[2] in whether_my_phase:
                        pass
                    else:
                        whether_my_phase.append(check_det[2])
                else:
                    if check_det[2] not in whether_my_phase:
                        pass
                    else:
                        whether_my_phase.remove(check_det[2])
            elif check_det[1] == "other":
                if check_det[3] == "check":
                    if check_det[2] in whether_other_phase:
                        pass
                    else:
                        whether_other_phase.append(check_det[2])
                else:
                    if check_det[2] not in whether_other_phase:
                        pass
                    else:
                        whether_other_phase.remove(check_det[2])
        elif check_det[0] == "kind":
            if check_det[1] == "my":
                if check_det[3] == "check":
                    if check_det[2] in whether_my_kind:
                        pass
                    else:
                        whether_my_kind.append(check_det[2])
                else:
                    if check_det[2] not in whether_my_kind:
                        pass
                    else:
                        whether_my_kind.remove(check_det[2])
            elif check_det[1] == "other":
                if check_det[3] == "check":
                    if check_det[2] in whether_other_kind:
                        pass
                    else:
                        whether_other_kind.append(check_det[2])
                else:
                    if check_det[2] not in whether_other_kind:
                        pass
                    else:
                        whether_other_kind.remove(check_det[2])
        elif check_det[0] == "timing":
            if check_det[1] == "my":
                if check_det[3] == "check":
                    if check_det[2] in whether_my_timing:
                        pass
                    else:
                        whether_my_timing.append(check_det[2])
                else:
                    if check_det[2] not in whether_my_timing:
                        pass
                    else:
                        whether_my_timing.remove(check_det[2])
            elif check_det[1] == "other":
                if check_det[3] == "check":
                    if check_det[2] in whether_other_timing:
                        pass
                    else:
                        whether_other_timing.append(check_det[2])
                else:
                    if check_det[2] not in whether_other_timing:
                        pass
                    else:
                        whether_other_timing.remove(check_det[2])
    if user == 1:
        duel.phase_whether_1_1 = "_".join(whether_my_phase)
        duel.kind_whether_1_1 = "_".join(whether_my_kind)
        duel.timing_whether_1_1 = "_".join(whether_my_timing)
        duel.phase_whether_1_2 = "_".join(whether_other_phase)
        duel.kind_whether_1_2 = "_".join(whether_other_kind)
        duel.timing_whether_1_2 = "_".join(whether_other_timing)
    else:
        duel.phase_whether_1_1 = "_".join(whether_my_phase)
        duel.kind_whether_2_1 = "_".join(whether_my_kind)
        duel.timing_whether_2_1 = "_".join(whether_my_timing)
        duel.phase_whether_2_2 = "_".join(whether_other_phase)
        duel.kind_whether_2_2 = "_".join(whether_other_kind)
        duel.timing_whether_2_2 = "_".join(whether_other_timing)
    duelobj.save_all(user, other_user, room_number)
    free_lock(room_number, lock)
    return HttpResponse("OK")
