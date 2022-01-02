from .models import (
    Duel,
    Grave,
    DuelGrave,
)
from .battle_functions import(
    modify_show,
    modify_show2,
)
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render
from pprint import pprint
import json


def explain_grave(request):
    room_number = int(request.GET["room_number"])
    grave_number = int(request.GET["grave"])
    duel = Duel.objects.all().get(id=room_number)
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
    user_1 = duel.user_1
    user_2 = duel.user_2
    if request.user != user_1 and request.user != user_2:
        if (ID1 == ID and duel.guest_flag) or (ID2 == ID and duel.guest_flag2):
            pass
        else:
            return HttpResponse("error")
    if request.user == user_1 or (ID1 == ID and duel.guest_flag):
        user = 1
        other_user = 2
    if request.user == user_2 or (ID2 == ID and duel.guest_flag2):
        user = 2
        other_user = 1
    i = 0
    graves = Grave.objects.all()
    for grave in graves:
        pprint(grave.id)
        if grave_number == grave.id:
            if grave.mine_or_other == 1:
                if grave.show >= 1:
                    tmp = DuelGrave.objects.filter(
                        room_number=room_number, mine_or_other=3, grave_id=(i + 1)
                    ).first()
                    tmp = json.loads(tmp.grave_content)
                    if grave.show == 3:
                        tmp = modify_show(tmp,room_number,user,other_user,3,"grave",(i+1))
                else:
                    return HttpResponse("error")
            else:
                if grave.show == 3 :
                    if int(request.GET["user_number"]) == user:
                        tmp = DuelGrave.objects.filter(
                            room_number=room_number, mine_or_other=user, grave_id=(i + 1)

                        ).first()
                        tmp = json.loads(tmp.grave_content)
                        tmp = modify_show(tmp,room_number,user,other_user,1,"grave",(i+1))
                    else:
                        tmp = DuelGrave.objects.filter(
                            room_number=room_number, mine_or_other=other_user, grave_id=(i + 1)

                        ).first()
                        tmp = json.loads(tmp.grave_content)
                        tmp = modify_show(tmp,room_number,user,other_user,2,"grave",(i+1))
                elif grave.show >= 1 and int(request.GET["user_number"]) == user:
                    tmp = DuelGrave.objects.filter(
                        room_number=room_number, mine_or_other=user, grave_id=(i + 1)
                    ).first()
                    tmp = json.loads(tmp.grave_content)
                    tmp = modify_show2(tmp,room_number,user,other_user,3,"grave",(i+1))
                elif grave.show == 4:
                    tmp = DuelGrave.objects.filter(
                        room_number=room_number, mine_or_other=other_user, grave_id=(i + 1)
                    ).first()
                    tmp = json.loads(tmp.grave_content)
                    tmp = modify_show(tmp,room_number,user,other_user,2,"grave",(i+1))
                elif grave.show >= 2:
                    tmp = DuelGrave.objects.filter(
                        room_number=room_number,
                        mine_or_other=other_user,
                        grave_id=(i + 1),
                    ).first()
                    tmp = json.loads(tmp.grave_content)
                    tmp = modify_show2(tmp,room_number,user,other_user,3,"grave",(i+1))
                else:
                    return HttpResponse("error")
        i += 1

    return render(request, "tcgcreator/explain_grave.html", {"graves_obj": tmp})
