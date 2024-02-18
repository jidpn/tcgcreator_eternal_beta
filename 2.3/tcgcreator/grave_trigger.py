from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import (
    Monster,
    Deck,
    Grave,
    Hand,
    Duel,
    DuelGrave,
    Lock
)
from pprint import pprint
from .battle_det import battle_det
import json
from .duel import DuelObj
from time import time

def grave_trigger(request):
    room_number = int(request.POST["room_number"])
    place_unique_id = request.POST["place_unique_id"]
    place = "grave"
    grave_id = int(request.POST["grave_id"])
    trigger_id = int(request.POST["trigger_id"])
    mine_or_other = request.POST["mine_or_other"]
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
    lock = Lock.objects.get()
    lock_flag = lock_lock(room_number, lock)
    if lock_flag != "OK":
        return HttpResponse("waiting")
    duelobj = DuelObj(room_number)
    duelobj.duel = duel
    duelobj.room_number = room_number
    if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag is True):
        duelobj.user = 1
        user = 1
        other_user = 2
    elif duel.user_2 == request.user or(ID2 == ID and duel.guest_flag2 is True):
        duelobj.user = 2
        user = 2
        other_user = 1
    else:
        return HttpResponse("error")
    duelobj.init_all(user, other_user, room_number,1)
    graves = Grave.objects.all()
    graves = Grave.objects.all()
    hands = Hand.objects.all()
    duelobj.check_eternal_effect(
        graves, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
    if duel.user_1 != request.user and duel.user_2 != request.user:
        if (ID1 == ID and duel.guest_flag) or (ID2 == ID and duel.guest_flag2):
            pass
        else:
            free_lock(room_number, lock)
            return HttpResponseRedirect(reverse("tcgcreator:watch_battle"))

    if duel.user_1 == request.user or (ID1 == ID or duel.guest_flag is True):
        if (
            grave_trigger_det(
                duelobj,
                place_unique_id,
                place,
                mine_or_other,
                grave_id,
                trigger_id,
                request,
            )
            is True
        ):
            free_lock(room_number, lock)
            return battle_det(request, duelobj)
        else:
            free_lock(room_number, lock)
            return HttpResponse("error")
    elif duel.user_2 == request.user or (ID2 == ID or duel.guest_flag2 is True):
        if (
            grave_trigger_det(
                duelobj,
                place_unique_id,
                place,
                mine_or_other,
                grave_id,
                trigger_id,
                request,
            )
            is True
        ):
            free_lock(room_number, lock)
            return battle_det(request, duelobj)
        else:
            free_lock(room_number, lock)
            return HttpResponse("error")
    free_lock(room_number, lock)
    return HttpResponse("error")


def grave_trigger_det(
    duelobj,
    place_unique_id,
    place_for_answer,
    mine_or_other,
    grave_id,
    trigger_id,
    request,
):
    duel = duelobj.duel
    room_number = duelobj.room_number
    if duelobj.user == 1:
        user = 1
        other_user = 2
        if mine_or_other == "1":
            mine_or_other2 = 1
            tmp_user = 1
        else:
            mine_or_other2 = 2
            tmp_user = 2
    else:
        user = 2
        other_user = 1
        if mine_or_other == "1":
            mine_or_other2 = 2
            tmp_user = 2
        else:
            mine_or_other2 = 1
            tmp_user = 1

    if tmp_user == 1:
        tmp = DuelGrave.objects.get(
            room_number=room_number, mine_or_other=1, grave_id=grave_id
        )
        graves = json.loads(tmp.grave_content)

    else:
        tmp = DuelGrave.objects.get(
            room_number=room_number, mine_or_other=2, grave_id=grave_id
        )
        graves = json.loads(tmp.grave_content)
    for grave in graves:
        if grave["place_unique_id"] == place_unique_id:
            monster = Monster.objects.get(id=grave["id"])
            monster_triggers = monster.trigger.all()
            result_trigger = monster_triggers.get(id=trigger_id)
            if result_trigger is None:
                return False
            elif duelobj.check_launch_trigger(
                result_trigger,
                duel.phase,
                duel.user_turn,
                user,
                other_user,
                mine_or_other2,
                "grave",
                place_unique_id,
                grave_id,
                fusion = 1
            ):
                duelobj.invoke_trigger(
                    result_trigger, "grave", grave, mine_or_other2, duelobj.user, grave_id
                )
                duelobj.save_all(user, other_user, room_number)
                return True
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


def lock_lock(room_number, lock):
    if room_number == 1:
        if lock.lock_1 is True and time() - lock.time_1 < 20:
            return HttpResponse("waiting")
        else:
            lock.lock_1 = True
            lock.time_1 = time()
            lock.save()
    elif room_number == 2:
        if lock.lock_2 is True and time() - lock.time_2 < 20:
            return HttpResponse("waiting")
        else:
            lock.lock_2 = True
            lock.time_2 = time()
            lock.save()
    elif room_number == 3:
        if lock.lock_3 is True and time() - lock.time_3 < 20:
            return HttpResponse("waiting")
        else:
            lock.lock_3 = True
            lock.time_3 = time()
            lock.save()
    return "OK"
