from .models import (
    FieldSize,
    MonsterVariables,
    MonsterVariablesKind,
    MonsterItem,
    Monster,
    Field,
    UserDeck,
    UserDeckGroup,
    Deck,
    UserDeck,
    UserDeckGroup,
    UserDeckChoice,
    Duel,
    Phase,
    Trigger,
    Grave,
    Hand,
    DuelGrave,
    CostWrapper,
    Config,
    GlobalVariable,
    VirtualVariable,
)
from django.http import HttpResponse, HttpResponseRedirect
from .custom_functions import (
    init_monster_item,
    create_user_deck,
    create_user_deck_group,
    copy_to_deck,
    create_user_deck_choice,
    create_user_deck_det,
)
from django.db.models import Q
from django.shortcuts import render
from .duel import DuelObj
import json
import copy
from pprint import pprint


def watch_det(request, duelobj=None):
    room_number = int(request.POST["room_number"])
    duel = Duel.objects.get(id=room_number)
    duelobj = DuelObj(room_number)
    duelobj.duel = duel
    duelobj.room_number = room_number
    duelobj.in_execute = False
    duelobj.user = 1
    if not request.user.is_authenticated:
        user_flag = False
        if "ID" in request.COOKIES:
            ID = request.COOKIES["ID"]
    no_user = False
    if duel.user_1 == request.user or (duel.guest_id == ID and duel.guest_flag is True):
        user = 1
        other_user = 2
    elif duel.user_2 == request.user or (duel.guest_id2 == ID and duel.guest_flag2 is True):
        user = 2
        other_user = 1
    else:
        user == 1
        other_user == 1
        no_user = True
    duelobj.init_all(user, other_user, room_number)
    decks = Deck.objects.all()
    graves = Grave.objects.all()
    hands = Hand.objects.all()
    turn = duel.user_turn
    duelobj.check_eternal_effect(
        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
    return watch_return(duelobj, decks, graves, hands, user, other_user, room_number,no_user)


def watch_return(duelobj, decks, graves, hands, user, other_user, room_number,no_user):
    if no_user:
        user = 0
        other_user = 0
    duel = duelobj.duel
    return_value = {}
    return_value["variable"] = duelobj.get_variables()
    return_value["phase"] = duel.phase.id
    return_value["turn"] = duel.user_turn
    return_value["log"] = duel.log
    if duel.ask > 0:
        return_value["ask_org"] = True
    else:
        return_value["ask_org"] = False
    if duel.user_turn == 1:
        if duel.guest_flag == False:
            return_value["user_name1"] = duel.user_1.first_name
        else:    
            return_value["user_name1"] = duel.guest_name
        if duel.is_ai == False:
            if duel.guest_flag2 == False:
                return_value["user_name2"] = duel.user_2.first_name
            else:
                return_value["user_name2"] = duel.guest_name2
        else:    
            return_value["user_name2"] = "NPC"
        if duel.ask == 1 or duel.ask == 3:
            return_value["ask"] = True
        else:
            return_value["ask"] = False

    else:
        if duel.is_ai == False:
            if duel.guest_flag2 is False:
                return_value["user_name1"] = duel.user_2.first_name
            else:
                return_value["user_name1"] = duel.guest_name2
        else:
            return_value["user_name1"] = "AI"
        if duel.guest_flag is False:
            return_value["user_name2"] = duel.user_1.first_name
        else:    
            return_value["user_name2"] = duel.guest_name
        if duel.ask == 2 or duel.ask == 3:
            return_value["ask"] = True
        else:
            return_value["ask"] = False
    return_value["ask_det"] = duel.ask_det
    return_value["user"] = user
    return_value["other_user"] = other_user
    if duel.appoint == user:
        return_value["appoint"] = True
    elif duel.appoint == other_user:
        return_value["appoint"] = False
    deck_info = duelobj.get_deck_info(decks, user, other_user, 1)
    return_value["deck_info"] = deck_info
    return_value["grave_info"] = duelobj.get_grave_info(graves, user, other_user, 1)
    return_value["hand_info"] = duelobj.watch_hand(hands,user,other_user)
    pprint("ABC")
    pprint(return_value["hand_info"])
    field = json.loads(duelobj.duel.field)
    return_value["field_info"] = duelobj.watch_field(field)
    if (
        ((duel.timing3 != None  or duel.timing2 != None  or duel.timing != None) and duel.appoint == user and duel.ask == 0)
        or duel.chain > 0
        and duel.ask == 0
    ):
        return_value["pri"] = True
    else:
        return_value["pri"] = False

    return HttpResponse(json.dumps(return_value))


def watch1(request):
    return watch(request, 1)


def watch2(request):
    return watch(request, 2)


def watch3(request):
    return watch(request, 3)


def watch(request, room_number):
    config = Config.objects.first()
    gray_out = config.gray_out
    duel = Duel.objects.filter(id=room_number).get()
    phases = Phase.objects.order_by("-priority").filter(show=1)
    variables = GlobalVariable.objects.order_by("-priority").filter(show=1)
    virtual_variables = VirtualVariable.objects.order_by("-priority").filter(show=1)
    fields = Field.objects.all()
    field_size = FieldSize.objects.first()
    x = range(field_size.field_x)
    y = range(field_size.field_y)
    ID = ""
    user_flag = True
    if not request.user.is_authenticated:
        user_flag = False
        if "ID" in request.COOKIES:
            ID = request.COOKIES["ID"]
    if duel.user_1 == request.user or (duel.guest_id == ID and duel.guest_flag is True):
        user = 1
    elif duel.user_2 == request.user or (duel.guest_id2 == ID and duel.guest_flag2 is True):
        user = 2
    else:
        user = 0
    return render(
        request,
        "tcgcreator/watch.html",
        {
            "room_number": room_number,
            "user":user,
            "Duel": duel,
            "Fields": fields,
            "range_x": x,
            "range_y": y,
            "Config": config,
            "Phases": phases,
            "Variable": variables,
            "VirtualVariable": virtual_variables,
            "gray_out": gray_out,
        },
    )
