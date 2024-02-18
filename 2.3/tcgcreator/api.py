from .models import (
    Config,
    UserPoint,
    Duel,
)
from .battle_functions import resetduel
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import (
    User
)
from time import time
import json
def return_highest(request):
    if "limit" not in request.GET or request.GET["limit"] is None:
        limit = 10
    else:
        limit = int(request.GET["limit"])
    if "method" not in request.GET or request.GET["method"] is None or request.GET["method"] == "point":
        method = "-point"
    elif request.GET["method"] == "win":
        method = "-win"
    elif request.GET["method"] == "win_ai":
        method = "-win_ai"
    user_points = UserPoint.objects.filter(user__isnull = False ).order_by(method).select_related().all()[0:limit]
    result = []
    for user_point in user_points:
        point={}
        point["point"] = user_point.point
        point["win"] = user_point.win
        point["lose"] = user_point.lose
        point["draw"] = user_point.draw
        point["win_ai"] = user_point.win_ai
        point["name"] = user_point.user.first_name
        result.append(point)

    return HttpResponse(json.dumps(result))

def room_data(request):
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
        room_text1 += "対戦中" + user1_1_name + "対" + user1_2_name


        wait_kind1 = 1
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
        room_text2 += "対戦中" + user2_1_name + "対" + user2_2_name
        wait_kind2 = 1
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
        room_text3 += "対戦中" + user3_1_name + "対" + user3_2_name
        wait_kind3 = 1
    if duel_1.winner == 0 and duel_1.waiting == True and (duel_1.user_1 or duel_1.guest_flag):
        if time() - duel_1.wait_time > limit_time:
            duel_1.user_1 = None
            duel_1.guest_id = -1
            duel_1.guest_flag = False
            duel_1.save();
        else:
            room_text1 += "対戦募集中" + user1_1_name
    if duel_2.winner == 0 and duel_2.waiting == True and (duel_2.user_1 or duel_2.guest_flag ):
        if time() - duel_2.wait_time > limit_time:
            duel_2.user_1 = None
            duel_1.guest_id = -1
            duel_2.guest_flag = False
            duel_2.save();
        else:
            room_text2 += "対戦募集中" + user2_1_name
    if duel_3.winner == 0 and duel_3.waiting == True and (duel_3.user_1 or duel_3.guest_flag):
        if time() - duel_3.wait_time > limit_time:
            duel_3.user_1 = None
            duel_1.guest_id = -1
            duel_3.guest_flag = False
            duel_3.save();
        else:
            room_text3 += "対戦募集中" + user3_1_name
    config  = Config.objects.first()
    result = []
    room_data1 = {}
    room_data1["room_num"] = 1
    room_data1["text"] = room_text1
    room_data1["wait_kind"] = wait_kind1
    room_data1["watch"] = watch_1
    result.append(room_data1)
    room_data2 = {}
    room_data2["room_num"] = 2
    room_data2["text"] = room_text2
    room_data2["wait_kind"] = wait_kind2
    room_data2["watch"] = watch_2
    result.append(room_data2)
    room_data3 = {}
    room_data3["room_num"] = 3
    room_data3["text"] = room_text3
    room_data3["wait_kind"] = wait_kind3
    room_data3["watch"] = watch_3
    result.append(room_data3)
    return HttpResponse(json.dumps(result))

