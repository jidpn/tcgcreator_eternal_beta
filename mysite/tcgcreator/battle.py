from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .custom_functions import (
    get_field_y_range,
    create_user_deck_group,
    create_user_deck_choice,
    create_user_deck,
)
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Prefetch, Max
import copy
from .models import (
    Monster,
    FieldSize,
    Field,
    Duel,
    Phase,
    Config,
    GlobalVariable,
    VirtualVariable,
    Timing,
    MonsterEffectKind,
    EnemyDeckGroup,
    DefaultDeckGroup,
    UserDeckGroup,
    Deck,
    UserDeckChoice,
    UserPoint
)
from pprint import pprint

@ensure_csrf_cookie
def battle1(request):
    return battle(request, 1)


@ensure_csrf_cookie
def battle2(request):
    return battle(request, 2)


@ensure_csrf_cookie
def battle3(request):
    return battle(request, 3)


def battle(request, room_number):
    config = Config.objects.first()
    gray_out = config.gray_out
    field_free = config.field_free
    ID = ""
    user_flag = True
    if not request.user.is_authenticated:
        user_flag = False
        if "ID" in request.COOKIES:
            ID = request.COOKIES["ID"]
    duel = Duel.objects.filter(id=room_number).get()
    if not duel.user_2 and duel.is_ai == False and duel.guest_flag2 is False:
        if room_number == 1:
            return HttpResponseRedirect(reverse("tcgcreator:init_battle1"))
        if room_number == 2:
            return HttpResponseRedirect(reverse("tcgcreator:init_battle2"))
        if room_number == 3:
            return HttpResponseRedirect(reverse("tcgcreator:init_battle3"))

    if duel.waiting is True:
        if room_number == 1:
            return HttpResponseRedirect(reverse("tcgcreator:watch1"))
        if room_number == 2:
            return HttpResponseRedirect(reverse("tcgcreator:watch2"))
        if room_number == 3:
            return HttpResponseRedirect(reverse("tcgcreator:watch3"))
    if duel.winner != 0:
        if room_number == 1:
            return HttpResponseRedirect(reverse("tcgcreator:watch1"))
        if room_number == 2:
            return HttpResponseRedirect(reverse("tcgcreator:watch2"))
        if room_number == 3:
            return HttpResponseRedirect(reverse("tcgcreator:watch3"))
    phases = Phase.objects.order_by("-priority").filter(show=1)
    phase_whether_show = list(Phase.objects.order_by("-priority").filter(phase_whether_show=1).all())

    timing_whether_show = list(Timing.objects.filter(timing_whether_show=1).all())
    kind_whether_show = list(MonsterEffectKind.objects.filter(monster_effect_show=1).all())
    variables = GlobalVariable.objects.order_by("-priority").filter(show=1)
    virtual_variables = VirtualVariable.objects.order_by("-priority").filter(show=1)
    fields = Field.objects.all()
    field_size = FieldSize.objects.first()
    if field_free is False:
        x = range(field_size.field_x)
        field_x = field_size.field_x
    elif field_free is True:
        x = range(100)
        field_x = 100
    if field_free is False:
        y = range(field_size.field_y)
    else:
        y = get_field_y_range(fields,field_size.field_y)
    if config.cheat is True:
        cheat = True
        monsters = Monster.objects.all()
    else:
        cheat = False
        monsters = None
    field_y = field_size.field_y
    if duel.user_1 != request.user and duel.user_2 != request.user and duel.guest_id != ID and duel.guest_id2 != ID:  
        if room_number == 1:
            return HttpResponseRedirect(reverse("tcgcreator:watch1"))
        if room_number == 2:
            return HttpResponseRedirect(reverse("tcgcreator:watch2"))
        if room_number == 3:
            return HttpResponseRedirect(reverse("tcgcreator:watch3"))
    if duel.user_1 == request.user or (duel.guest_id == ID and duel.guest_flag is True):
        user = 1
    else:
        user = 2
    if user == 1:
        phase_my_whether_ary = duel.phase_whether_1_1.split("_")
        phase_other_whether_ary = duel.phase_whether_1_2.split("_")
    else:
        phase_my_whether_ary = duel.phase_whether_2_1.split("_")
        phase_other_whether_ary = duel.phase_whether_2_2.split("_")
    if user == 1:
        timing_my_whether_ary = duel.timing_whether_1_1.split("_")
        timing_other_whether_ary = duel.timing_whether_1_2.split("_")
    else:
        timing_my_whether_ary = duel.timing_whether_2_1.split("_")
        timing_other_whether_ary = duel.timing_whether_2_2.split("_")
    if user == 1:
        kind_my_whether_ary = duel.kind_whether_1_1.split("_")
        kind_other_whether_ary = duel.kind_whether_1_2.split("_")
    else:
        kind_my_whether_ary = duel.kind_whether_2_1.split("_")
        kind_other_whether_ary = duel.kind_whether_2_2.split("_")
    phase_whether_my_show = copy.deepcopy(phase_whether_show)
    phase_whether_other_show = copy.deepcopy(phase_whether_show)
    for index,phase in enumerate(phase_whether_show):
        if str(phase.id) in phase_my_whether_ary:
            phase_whether_my_show[index].checked = True
        else:
            phase_whether_my_show[index].checked = False
        if str(phase.id) in phase_other_whether_ary:
            phase_whether_other_show[index].checked = True
        else:
            phase_whether_other_show[index].checked = False
    timing_whether_my_show = copy.deepcopy(timing_whether_show)
    timing_whether_other_show = copy.deepcopy(timing_whether_show)
    for index,timing in enumerate(timing_whether_show):
        if str(timing.id) in timing_my_whether_ary:
            timing_whether_my_show[index].checked = True
        else:
            timing_whether_my_show[index].checked = False
        if str(timing.id) in timing_other_whether_ary:
            timing_whether_other_show[index].checked = True
        else:
            timing_whether_other_show[index].checked = False
    kind_whether_my_show = copy.deepcopy(kind_whether_show)
    kind_whether_other_show = copy.deepcopy(kind_whether_show)
    for index,kind in enumerate(kind_whether_show):
        if str(kind.id) in kind_my_whether_ary:
            kind_whether_my_show[index].checked = True
        else:
            kind_whether_my_show[index].checked = False
        if str(kind.id) in kind_other_whether_ary:
            kind_whether_other_show[index].checked = True
        else:
            kind_whether_other_show[index].checked = False
    if duel.winner != 0:
        if room_number == 1:
            return HttpResponseRedirect(reverse("tcgcreator:watch1"))
        if room_number == 2:
            return HttpResponseRedirect(reverse("tcgcreator:watch2"))
        if room_number == 3:
            return HttpResponseRedirect(reverse("tcgcreator:watch3"))
    if config.templates == 1:
        html = "battle.html"
    elif config.templates == 2:
        html = "battle_collate.html"
    elif config.templates == 3:
        html = "battle_collate2.html"
    else:
        return HttpResponse("error");
    add_variables = config.add_variables_show.split("_")
    user_deck_groups = None
    if user_flag is True:
        user_deck_groups = UserDeckGroup.objects.filter(user = request.user)
        if not user_deck_groups:
            default_decks = DefaultDeckGroup.objects.all()
            default_deck_id = -1
            initial_flag = True
            decks = Deck.objects.all()
            for default_deck in default_decks:
                if default_deck_id == int(default_deck.default_deck_id):
                    continue
                else:
                    default_deck_id = int(default_deck.default_deck_id)
                user_deck_group_max = UserDeckGroup.objects.all().aggregate(Max("user_deck_id"))
                if(user_deck_group_max["user_deck_id__max"] is None):
                    deck_group2 = 1
                else:
                    deck_group2 = user_deck_group_max["user_deck_id__max"] + 1
                create_user_deck_group(deck_group2, request.user, default_deck.deck_name)
                user_deck_group = (
                    UserDeckGroup.objects.all().filter(user_deck_id=deck_group2, user=request.user).first()
                )
                if initial_flag is True:
                    create_user_deck_choice(user_deck_group, request.user)
                    initial_flag = False
                for deck in decks:
                    create_user_deck(request.user, deck, user_deck_group, default_deck_id)
            user_deck_groups = UserDeckGroup.objects.filter(user = request.user)
    if duel.user_1:
        user_point1 = UserPoint.objects.filter(user = duel.user_1).first()
        user_name1 = duel.user_1.first_name
        if user_point1 is None:
            user_point1 = UserPoint()
            user_point1.user = duel.user_1
            user_point1.win = 0
            user_point1.point = 0
            user_point1.save()
    else:
        user_point1 = None
        user_name1 = None
    if duel.user_2:
        user_point2 = UserPoint.objects.filter(user = duel.user_2).first()
        user_name2 = duel.user_2.first_name
        if user_point2 is None:
            user_point2 = UserPoint()
            user_point2.user = duel.user_2
            user_point2.win = 0
            user_point2.point = 0
            user_point2.save()
    else:
        user_point2 = None
        user_name2 = None
    if user == 2:
        tmp = user_point1
        user_point1 = user_point2
        user_point2 = tmp
        tmp = user_name1
        user_name1 = user_name2
        user_name2 = tmp
    enemy_deck_groups = None
    if user_deck_groups is None:
        default_deck_groups = DefaultDeckGroup.objects.all()
    else:
        default_deck_groups = None
    if duel.is_ai == True:
        enemy_deck_groups = EnemyDeckGroup.objects.all()
    return render(
        request,
        "tcgcreator/"+html,
        {
            "user":user,
            "user_flag":user_flag,
            "room_number": room_number,
            "Duel": duel,
            "Fields": fields,
            "field_x": field_x,
            "field_y": field_y,
            "range_x": x,
            "range_y": y,
            "Config": config,
            "add_variables" :add_variables,
            "Phases": phases,
            "Variable": variables,
            "VirtualVariable": virtual_variables,
            "gray_out": gray_out,
            "user_point1": user_point1,
            "user_point2": user_point2,
            "user_name1": user_name1,
            "user_name2": user_name2,
            "field_free": field_free,
            "monsters": monsters,
            "enemy_deck_groups": enemy_deck_groups,
            "default_deck_groups": default_deck_groups,
            "user_deck_groups": user_deck_groups,
            "cheat": cheat,
            "phase_my_show": phase_whether_my_show,
            "timing_my_show": timing_whether_my_show,
            "kind_my_show": kind_whether_my_show,
            "phase_other_show": phase_whether_other_show,
            "timing_other_show": timing_whether_other_show,
            "kind_other_show": kind_whether_other_show
        },
    )
