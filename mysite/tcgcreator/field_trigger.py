from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import (
    Monster,
    Deck,
    Grave,
    Hand,
    Duel,
    Lock,
)
from pprint import pprint
from .battle_det import battle_det
from .duel import DuelObj


from time import time
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


def field_trigger(request):
    room_number = int(request.POST["room_number"])
    place_unique_id = request.POST["place_unique_id"]
    place = "field"
    x = int(request.POST["x"])
    y = int(request.POST["y"])
    trigger_id = int(request.POST["trigger_id"])
    mine_or_other = request.POST["mine_or_other"]
    lock = Lock.objects.get()
    lock_flag = lock_lock(room_number, lock)
    if lock_flag != "OK":
        return HttpResponse("waiting")
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
    duelobj = DuelObj(room_number)

    duelobj.duel = duel
    duelobj.room_number = room_number
    if duel.user_1 == request.user or (ID1 == ID and duel.guest_flag is True):
        duelobj.user = 1
        user = 1
        other_user = 2
    elif duel.user_2 == request.user or (ID2 == ID and duel.guest_flag2 is True):
        duelobj.user = 2
        user = 2
        other_user = 1
    else:
        return HttpResponse("error")
    duelobj.init_all(user, other_user, room_number)
    decks = Deck.objects.all()
    graves = Grave.objects.all()
    hands = Hand.objects.all()
    duelobj.check_eternal_effect(
        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
    if duel.user_1 != request.user and duel.user_2 != request.user:
        if (ID1 == ID and duel.guest_flag) or (ID2 == ID and duel.guest_flag2):
            pass
        else:
            free_lock(room_number, lock)
            return HttpResponseRedirect(reverse("tcgcreator:watch_battle"))

    if duel.user_1 == request.user or(ID1 == ID and duel.guest_flag is True):
        if (
            field_trigger_det(
                duelobj,
                place_unique_id,
                place,
                mine_or_other,
                x,
                y,
                trigger_id,
                request,
            )
            is True
        ):
            duelobj.save_all(user, other_user, room_number)
            free_lock(room_number, lock)
            return battle_det(request, duelobj)
        else:
            free_lock(room_number, lock)
            return HttpResponse("error")
    elif duel.user_2 == request.user or (ID2 == ID and duel.guest_flag2 is True):
        if (
            field_trigger_det(
                duelobj,
                place_unique_id,
                place,
                mine_or_other,
                x,
                y,
                trigger_id,
                request,
            )
            is True
        ):
            duelobj.save_all(user, other_user, room_number)
            free_lock(room_number, lock)
            return battle_det(request, duelobj)
        else:
            free_lock(room_number, lock)
            return HttpResponse("error")
    free_lock(room_number, lock)
    return HttpResponse("error")


def field_trigger_det(
    duelobj, place_unique_id, place_for_answer, mine_or_other, x, y, trigger_id, request
):
    duel = duelobj.duel
    if duelobj.user == 1:
        user = 1
        other_user = 2
    else:
        user = 2
        other_user = 1

    field = duelobj.field
    if field[x][y]["det"]["place_unique_id"] == place_unique_id:
        mine_or_other = field[x][y]["mine_or_other"]
        monster_id = duelobj.get_monster_id_easy(field[x][y]["det"])
        monster = Monster.objects.get(id=monster_id)
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
            mine_or_other,
            "field",
            place_unique_id,
            0,
            x,
            y,
            fusion=1
        ):
            duelobj.invoke_trigger(
                result_trigger,
                "field",
                field[x][y]["det"],
                mine_or_other,
                duelobj.user,
                0,
                x,
                y,
            )
            return True
    return False
