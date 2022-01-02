from .models import (
    Deck,
    Duel,
    DuelDeck,
)
from .battle_functions import(
    modify_show,
    modify_show2,
)

from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render
import json
from pprint import pprint


def explain_deck(request):
    room_number = int(request.GET["room_number"])
    deck_number = int(request.GET["deck"])
    duel = Duel.objects.all().get(id=room_number)
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
    user_1 = duel.user_1
    user_2 = duel.user_2
    if request.user != user_1 and request.user != user_2:
        if (ID1 == ID and duel.guest_flag) or (ID2 == ID and duel.guest_flag2):
            pass
        else:
            return HttpResponse("error")
    if request.user == user_1 or (ID1 == ID and duel.guest_flag is True):
        user = 1
        other_user = 2
    if request.user == user_2 or (ID2 == ID and duel.guest_flag2 is True):
        user = 2
        other_user = 1
    i = 0
    decks = Deck.objects.all()
    for deck in decks:
        if deck_number == deck.id:
            if deck.mine_or_other == 1:
                if deck.show >= 1:
                    tmp = DuelDeck.objects.filter(
                        room_number=room_number, mine_or_other=3, deck_id=(i + 1)
                    ).first()
                    tmp = json.loads(tmp.deck_content)
                    if deck.show == 3:
                        tmp = modify_show(tmp,room_number,user,other_user,3,"deck",(i+1))
                else:
                    return HttpResponse("error")
            else:
                if deck.show == 3 :
                    if int(request.GET["user_number"]) == user:
                        tmp = DuelDeck.objects.filter(
                            room_number=room_number, mine_or_other=user, deck_id=(i + 1)
                        ).first()
                        tmp = json.loads(tmp.deck_content)
                        tmp = modify_show(tmp,room_number,user,other_user,1,"deck",(i+1))
                    else:
                        tmp = DuelDeck.objects.filter(
                            room_number=room_number, mine_or_other=other_user, deck_id=(i + 1)
                        ).first()
                        tmp = json.loads(tmp.deck_content)
                        tmp = modify_show(tmp,room_number,user,other_user,2,"deck",(i+1))
                elif deck.show >= 1 and int(request.GET["user_number"]) == user:
                    tmp = DuelDeck.objects.filter(
                        room_number=room_number, mine_or_other=user, deck_id=(i + 1)
                    ).first()
                    tmp = json.loads(tmp.deck_content)
                    tmp = modify_show2(tmp,room_number,user,other_user,2,"deck",(i+1))
                elif deck.show == 4:
                    tmp = DuelDeck.objects.filter(
                        room_number=room_number, mine_or_other=other_user, deck_id=(i + 1)
                    ).first()
                    tmp = json.loads(tmp.deck_content)
                    tmp = modify_show(tmp,room_number,user,other_user,2,"deck",(i+1))
                elif deck.show >= 2:
                    tmp = DuelDeck.objects.filter(
                        room_number=room_number,
                        mine_or_other=other_user,
                        deck_id=(i + 1),
                    ).first()
                    tmp = json.loads(tmp.deck_content)
                    tmp = modify_show2(tmp,room_number,user,other_user,2,"deck",(i+1))
                else:
                    return HttpResponse("error")
        i += 1

    return render(request, "cell/explain_deck.html", {"decks_obj": tmp})
