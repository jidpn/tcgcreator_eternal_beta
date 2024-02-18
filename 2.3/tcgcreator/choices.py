from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from .models import (
    Deck,
    Grave,
    Hand,
    Duel,
    Trigger,
    Lock,
)
from pprint import pprint
from .battle_det import battle_det,battle_det_return_org_ai
from .duel import DuelObj
from time import time

def lock_lock(room_number, lock,request):
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
    if room_number == 1:
        if lock.lock_1 is True and time() - lock.time_1 < 20:
            if duel.is_ai is False:
                return HttpResponse("waiting")
            duelobj = DuelObj(room_number)
            duelobj.duel = duel
            duelobj.room_number = room_number
            duelobj.in_execute = False
            decks = Deck.objects.all()
            graves = Grave.objects.all()
            hands = Hand.objects.all()
            user_1 = duel.user_1
            user_2 = duel.user_2
            if request.user != user_1 and request.user != user_2:
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
            lock.time_1 = time()
            lock.save()
    elif room_number == 2:
        if lock.lock_2 is True and time() - lock.time_2 < 20:
            if duel.is_ai is False:
                return HttpResponse("waiting")
            duelobj = DuelObj(room_number)
            duelobj.duel = duel
            duelobj.room_number = room_number
            duelobj.in_execute = False
            decks = Deck.objects.all()
            graves = Grave.objects.all()
            hands = Hand.objects.all()
            user_1 = duel.user_1
            user_2 = duel.user_2
            if request.user != user_1 and request.user != user_2:
                return HttpResponse("error")
            if request.user == user_1:
                duelobj.user = 1
                user = 1
                other_user = 2
            if request.user == user_2:
                duelobj.user = 2
                user = 2
                other_user = 1
            duelobj.init_all(user, other_user, room_number)
            return battle_det_return_org_ai(
                duelobj, decks, graves, hands, user, other_user, choices, room_number
            )
        else:
            lock.lock_2 = True
            lock.time_2 = time()
            lock.save()
    elif room_number == 3:
        if lock.lock_3 is True and time() - lock.time_3 < 20:
            if duel.is_ai is False:
                return HttpResponse("waiting")
            duelobj = DuelObj(room_number)
            duelobj.duel = duel
            duelobj.room_number = room_number
            duelobj.in_execute = False
            decks = Deck.objects.all()
            graves = Grave.objects.all()
            hands = Hand.objects.all()
            user_1 = duel.user_1
            user_2 = duel.user_2
            if request.user != user_1 and request.user != user_2:
                return HttpResponse("error")
            if request.user == user_1:
                duelobj.user = 1
                user = 1
                other_user = 2
            if request.user == user_2:
                duelobj.user = 2
                user = 2
                other_user = 1
            duelobj.init_all(user, other_user, room_number)
            return battle_det_return_org_ai(
                duelobj, decks, graves, hands, user, other_user, choices, room_number
            )
        else:
            lock.lock_3 = True
            lock.time_3 = time()
            lock.save()
    return "OK"


def choices(request):
    room_number = int(request.POST["room_number"])
    trigger_id = request.POST["trigger_id"]
    lock = Lock.objects.get()
    lock_flag = lock_lock(room_number, lock,request)
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
    if lock_flag != "OK":
        if duel.is_ai == False:
            return HttpResponse("waiting")
        else:
            duelobj = DuelObj(room_number)
            duelobj.duel = duel
            duelobj.room_number = room_number
            duelobj.in_execute = False
            decks = Deck.objects.all()
            graves = Grave.objects.all()
            hands = Hand.objects.all()
            user_1 = duel.user_1
            user_2 = duel.user_2
            if request.user != user_1 and request.user != user_2:
                if (ID1 == ID and duel.guest_flag) or (ID2 == ID and duel.guest_flag2):
                    pass
                else:
                    return HttpResponse("error")
            if request.user == user_1 or(ID1 == ID and duel.guest_flag is True):
                duelobj.user = 1
                user = 1
                other_user = 2
            if request.user == user_2 or(ID2 == ID and duel.guest_flag2 is True):
                duelobj.user = 2
                user = 2
                other_user = 1
            duelobj.init_all(user, other_user, room_number)
            return battle_det_return_org_ai(
                duelobj, decks, graves, hands, user, other_user, choices, room_number
            )

    if duel.user_1 != request.user and duel.user_2 != request.user:
        if (ID1 == ID and duel.guest_flag) or (ID2 == ID and duel.guest_flag2):
            pass
        else:
            free_lock(room_number, lock)
            return HttpResponseRedirect(reverse("tcgcreator:watch_battle"))
    if duel.user_1 == request.user or ( ID1 == ID and duel.guest_flag is True):
        user = 1
        other_user = 2
    elif duel.user_2 == request.user or (ID2 ==  ID and duel.guest_flag2 is True):
        user = 2
        other_user = 1
    duelobj = DuelObj(room_number)
    duelobj.duel = duel
    duelobj.user = user
    duelobj.room_number = room_number
    decks = Deck.objects.all()
    graves = Grave.objects.all()
    hands = Hand.objects.all()
    duelobj.init_all(user, other_user, room_number)
    duelobj.check_eternal_effect(
        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
    if duel.in_cost is True:
        free_lock(room_number, lock)
        return HttpResponse("error")

    if duel.user_1 == request.user or ( ID1 == ID and duel.guest_flag is True):
        if duel.appoint != 1:
            free_lock(room_number, lock)
            return HttpResponse("error")

        duelobj.user = 1
        user = 1
        other_user = 2
        ret = choices_det(duelobj, trigger_id, request, user)
        if ret != -1:
            if ret == "no_fusion":
                free_lock(room_number, lock)
                return HttpResponse("no_fusion")
            duelobj.duel.mute = False
            duelobj.save_all(user, other_user, room_number)
            free_lock(room_number, lock)
            return battle_det(request, duelobj)
        else:
            free_lock(room_number, lock)
            return HttpResponse("error")
    elif duel.user_2 == request.user or (ID2 ==  ID and duel.guest_flag2 is True):
        if duel.appoint != 2:
            free_lock(room_number, lock)
            return HttpResponse("error")
        duelobj.user = 2
        user = 2
        other_user = 1
        ret = choices_det(duelobj, trigger_id, request, user)
        if ret != -1:
            if ret == "no_fusion":
                free_lock(room_number, lock)
                return HttpResponse("no_fusion")
            duelobj.duel.mute = False
            duelobj.save_all(user, other_user, room_number)
            free_lock(room_number, lock)
            return battle_det(request, duelobj)
        else:
            free_lock(room_number, lock)
            return HttpResponse("error")
    free_lock(room_number, lock)
    return HttpResponse("error")


def choices_det(duelobj, trigger_id, request, user):
    if user == 1:
        other_user = 2
    else:
        other_user = 1
    triggers = Trigger.objects.all()
    trigger = triggers.get(id=trigger_id)
    if trigger is not None and duelobj.check_launch_trigger( trigger, duelobj.duel.phase, duelobj.duel.user_turn, user, other_user, user,fusion = 1):
        return duelobj.invoke_trigger(trigger, "", "", "", duelobj.user, "")
    else:
        return -1


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
