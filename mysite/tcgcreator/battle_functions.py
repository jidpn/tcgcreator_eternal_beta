from time import time
from .duel import DuelObj
import copy
from django.db.models import Prefetch, Max
from .models import (
    MonsterEffectKind,
    DefaultDeckGroup,
    UserDeckGroup,
    UserDeckChoice,
    UserDeck,
    Config,
    FieldSize,
    Field,
    Deck,
    Duel,
    Phase,
    GlobalVariable,
    Grave,
    Hand,
    DuelDeck,
    DuelGrave,
    DuelHand,
    Lock,
    Timing,
    EnemyDeck,
    EnemyDeckGroup,
    EnemyDeckChoice,
    DefaultDeck
)
from django.http import HttpResponse, HttpResponseRedirect
from .custom_functions import (
    check_special_cards,
    create_user_deck_det,
    create_user_deck_group,
    create_user_deck,
    create_user_deck_choice,
)
import json
import uuid
import random
from pprint import pprint

def init_ai_choosing(room_number,user):
    pass
def init_duel(room_number, user,default_deck = None,enemy_deck=None,user1_choosing=False,user2_choosing = True,ai_choosing=False,user_deck=None,which_user=None):
    '''
    if default_deck:
        default_deck = int(default_deck)
    if user_deck:
        user_deck = int(user_deck)
        '''
    if enemy_deck:
        enemy_deck = int(enemy_deck)
    duel = Duel.objects.all().filter(id=room_number).first()
    duel_deck = DuelDeck.objects.all().filter(room_number=room_number)
    duel_deck.delete()
    duel_grave = DuelGrave.objects.all().filter(room_number=room_number)
    duel_grave.delete()
    duel_hand = DuelHand.objects.all().filter(room_number=room_number)
    duel_hand.delete()
    decks = Deck.objects.all()
    graves = Grave.objects.all()
    hands = Hand.objects.all()
    if user1_choosing == True:
        #duel.deck_choose_flag1 = True
        duel.deck_choose_flag1 = False
    if duel.deck_choose_flag1 is False:
        deck_group = duel.user_deck1
        if duel.default_deck1:
            default_deck2 = duel.default_deck1.id
        else:
            default_deck2 = None
        if deck_group is None and duel.guest_flag is False:
            deck_group = UserDeckChoice.objects.filter(user=duel.user_1).first()
            if not deck_group:
                initial_flag = True
                default_decks = DefaultDeckGroup.objects.all()
                default_deck_id = -1
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
                    create_user_deck_group(deck_group2, duel.user_1, default_deck.deck_name)
                    user_deck_group = (
                        UserDeckGroup.objects.all().filter(user_deck_id=deck_group2, user=dueoluser_1).first()
                    )
                    if initial_flag is True:
                        create_user_deck_choice(user_deck_group, duel.user_1)
                        initial_flag = False
                    deck_group = UserDeckChoice.objects.all().filter(user=duel.user_1).first()
                    for deck in decks:
                        create_user_deck(duel.user_1, deck, user_deck_group, default_deck_id)
            else:
                user_deck_group = deck_group.user_deck
            duel.user_deck1 = deck_group
    lock = Lock.objects.get()
    if room_number == 1:
        lock.lock_1 = False
    elif room_number == 2:
        lock.save()
        lock.lock_2 = False
        lock.save()
    elif room_number == 3:
        lock.lock_3 = False
        lock.save()
    if deck_group:
        user_deck = int(deck_group.user_deck.id)
    else:
        user_deck = None
    if user_deck :
       user_decks = UserDeck.objects.filter(deck_group__id = user_deck)
    elif default_deck2:
        user_decks = DefaultDeck.objects.filter(deck_group__id=default_deck2)
    else:
        if duel.guest_flag is False:
            if duel.deck_choose_flag1 is False:
                user_deck_group = deck_group.user_deck
                if not user_deck_group:
                    return "エラーが発生しました"
                elif user_deck_group.user != duel.user_1:
                    resetduel(duel)
                    duel.save()
                    return "エラーが発生しました"
                else:
                    user_decks = UserDeck.objects.filter(user=duel.user_1, deck_group=user_deck_group)
                    if not user_decks:
                        return False
        else:
            if user_deck:
                user_decks = UserDeck.objects.filter(deck_group__id=user_deck)
            elif default_deck:
                user_decks = DefaultDeck.objects.filter(deck_group__id=default_deck)
            else:
                duel.deck_choose_flag1 = True
    i = 1
    for grave in graves:
        if grave.mine_or_other == 1:
            DuelGrave(
                grave_name = grave.grave_name,room_number=room_number, mine_or_other=3, grave_id=i, grave_content="[]",
                id=i*100+room_number*10+3
            ).save()
        else:
            DuelGrave(
                grave_name = grave.grave_name,room_number=room_number, mine_or_other=1, grave_id=i, grave_content="[]",
            id=i*100+room_number*10+1
            ).save()
            DuelGrave(
                grave_name = grave.grave_name,room_number=room_number, mine_or_other=2, grave_id=i, grave_content="[]",
                id=i*100+room_number*10+2
            ).save()
        i += 1
    i = 1
    for hand in hands:
        if hand.mine_or_other == 1:
            DuelHand(
                hand_name = hand.hand_name,room_number=room_number, mine_or_other=3, hand_id=i, hand_content="[]",
                id=i*100+room_number*10+3
            ).save()
        else:
            DuelHand(
                hand_name = hand.hand_name,room_number=room_number, mine_or_other=1, hand_id=i, hand_content="[]",
                id=i*100+room_number*10+1
            ).save()
            DuelHand(
                hand_name = hand.hand_name,room_number=room_number, mine_or_other=2, hand_id=i, hand_content="[]",
                id=i*100+room_number*10+2
            ).save()
        i += 1
    i = 1
    duel.deck_choose_flag1 = False
    #if which_user == 1 and duel.deck_choose_flag1 is False:
    special_cards = []
    if duel.deck_choose_flag1 is False:
        for deck in decks:
            user_deck = user_decks.filter(deck_type=deck).first()
            user_deck_det = user_deck.deck.split("_")
            special_cards.extend( check_special_cards(user_deck_det))
        for deck in decks:
            user_deck = user_decks.filter(deck_type=deck).first()
            user_deck_det = user_deck.deck.split("_")
            min_deck_size = deck.min_deck_size
            max_deck_size = deck.max_deck_size
            for special_card in special_cards:
                if deck in special_card.deck.all():
                    special_first = special_card
                    min_deck_size = special_first.min_deck_size
                    max_deck_size = special_first.max_deck_size
            if len(user_deck_det) < min_deck_size:
                resetduel(duel)
                duel.save()
                return HttpResponse("エラーが発生しました")
            elif len(user_deck_det) > max_deck_size:
                resetduel(duel)
                duel.save()
                return HttpResponse("エラーが発生しました")
            user_deck_det = create_user_deck_det(user_deck.deck, i, 1)
            if deck.mine_or_other == 1:
                DuelDeck.objects.filter(
                    room_number=room_number, mine_or_other=3, deck_id=i
                ).delete()
                DuelDeck(
                    deck_name = deck.deck_name,
                    room_number=room_number,
                    mine_or_other=3,
                    deck_id=i,
                    deck_content=user_deck_det,
                    id=i*100+room_number*10+3

                ).save()
            else:
                DuelDeck.objects.filter(
                    room_number=room_number, mine_or_other=1, deck_id=i
                ).delete()
                DuelDeck(
                    deck_name = deck.deck_name,
                    room_number=room_number,
                    mine_or_other=1,
                    deck_id=i,
                    deck_content=user_deck_det,
                    id=i*100+room_number*10+1
                ).save()
            i += 1
    if duel.is_ai is False or ai_choosing is False:
        duel.ai_choosing = False
    if duel.is_ai is False and duel.guest_flag2 is False:
        user_2 = user
        decks = Deck.objects.all()
        if duel.deck_choose_flag2 == False:
            deck_group = duel.user_deck2
            if not deck_group:
                return HttpResponse("エラーが発生しました")
            else:
                user_deck_group = deck_group.user_deck
                if not user_deck_group:
                    resetduel(duel)
                    duel.save()
                    return HttpResponse("エラーが発生しました")
                if user_deck_group.user != user_2:
                    resetduel(duel)
                    duel.save()
                    return HttpResponse("エラーが発生しました")
                user_decks = UserDeck.objects.filter(user=user_2, deck_group=user_deck_group)
                if not user_decks:
                    resetduel(duel)
                    duel.save()
                    return HttpResponse("エラーが発生しました")
    elif duel.is_ai is True:
        decks = Deck.objects.all()
        deck_group = duel.ai_deck2
        if not deck_group:
            return HttpResponse("デッキを構築してください")
        enemy_deck_group = deck_group.enemy_deck
        if enemy_deck:
            user_decks = EnemyDeck.objects.filter(deck_group__id=enemy_deck)
        else:
            user_decks = EnemyDeck.objects.filter(deck_group=enemy_deck_group)
        if not user_deck:
            resetduel(duel)
            duel.save()
            return HttpResponse("エラーが発生しました")
    else:
        user_decks = DefaultDeck.objects.filter(deck_group=duel.default_deck2)
        if not user_decks:
            duel.deck_choose_flag2 = True
    i = 1
    if duel.deck_choose_flag2 is False:
        special_cards = []
        for deck in decks:
            if not user_deck:
                return HttpResponse("エラーが発生しました")
            user_deck = user_decks.filter(deck_type=deck).first()
            user_deck_det = user_deck.deck.split("_")
            special_cards.extend( check_special_cards(user_deck_det))
        for deck in decks:
            user_deck = user_decks.filter(deck_type=deck).first()
            if not user_deck:
                return HttpResponse("エラーが発生しました")
            else:
                user_deck_det = user_deck.deck.split("_")
                min_deck_size = deck.min_deck_size
                max_deck_size = deck.max_deck_size
                for special_card in special_cards:
                    if special_card.filter(deck = deck):
                        special_first = special_card
                        min_deck_size = special_first.min_deck_size
                        max_deck_size = special_first.max_deck_size
                if len(user_deck_det) < deck.min_deck_size and duel.is_ai == False:
                    resetduel(duel)
                    duel.save()
                    return HttpResponse("エラーが発生しました")
                elif len(user_deck_det) > max_deck_size and duel.is_ai == False:
                    resetduel(duel)
                    duel.save()
                    return HttpResponse("エラーが発生しました")
                user_deck_det = create_user_deck_det(user_deck.deck, i, 2)
                if deck.mine_or_other == 0:
                    DuelDeck.objects.filter(
                        room_number=room_number, mine_or_other=2, deck_id=i
                    ).delete()
                    DuelDeck(
                        room_number=room_number,
                        deck_name = deck.deck_name,
                        mine_or_other=2,
                        deck_id=i,
                        deck_content=user_deck_det,
                        id=i*100+room_number*10+2
                    ).save()
            i += 1
    start_phase = Phase.objects.order_by("-priority").first()
    config = Config.objects.get()
    effect_kinds =  MonsterEffectKind.objects.filter(monster_effect_show = False)
    kind_whether_1_1 = ""
    kind_whether_2_1 = ""
    kind_whether_1_2 = ""
    kind_whether_2_2 = ""
    '''
    for effect_kind in effect_kinds:
        kind_whether_1_1 += str(effect_kind.id) + "_"
        kind_whether_1_2 += str(effect_kind.id) + "_"
        kind_whether_2_1 += str(effect_kind.id) + "_"
        kind_whether_2_2 += str(effect_kind.id) + "_"
    kind_whether_1_1 = kind_whether_1_1[:-1]
    kind_whether_1_2 = kind_whether_1_2[:-1]
    kind_whether_2_1 = kind_whether_2_1[:-1]
    kind_whether_2_2 = kind_whether_2_2[:-1]
    '''
    duel.kind_whether_1_1 = kind_whether_1_1
    duel.kind_whether_1_2 = kind_whether_1_2
    duel.kind_whether_2_1 = kind_whether_2_1
    duel.kind_whether_2_2 = kind_whether_2_2
    duel.sound_effect_1 = ""
    duel.sound_effect_2 = ""
    duel.once_per_turn1 = ""
    duel.once_per_turn_monster1 = ""
    duel.once_per_turn_monster_group1 = ""
    duel.once_per_turn_group1 = ""
    duel.once_per_turn_exist1 = ""
    duel.once_per_turn_relate1 = ""
    duel.once_per_turn2 = ""
    duel.once_per_turn_monster2 = ""
    duel.once_per_turn_monster_group2 = ""
    duel.once_per_turn_group2 = ""
    duel.once_per_turn_exist2 = ""
    duel.once_per_turn_relate2 = ""
    duel.tmponce_per_turn1 = ""
    duel.tmponce_per_turn_monster1 = ""
    duel.tmponce_per_turn2 = ""
    duel.tmponce_per_turn_monster2 = ""
    duel.tmponce_per_turn_group1 = ""
    duel.tmponce_per_turn_group2 = ""
    duel.tmponce_per_turn_exist1 = ""
    duel.tmponce_per_turn_exist2 = ""
    duel.tmponce_per_turn_relate1 = ""
    duel.tmponce_per_turn_relate2 = ""
    duel.effect_flag = 0
    effect_timings =  Timing.objects.filter(timing_whether_show = False)
    timing_whether_1_1 = ""
    timing_whether_1_2 = ""
    timing_whether_2_1 = ""
    timing_whether_2_2 = ""
    for effect_timing in effect_timings:
        timing_whether_1_1 += str(effect_timing.id) + "_"
        timing_whether_1_2 += str(effect_timing.id) + "_"
        timing_whether_2_1 += str(effect_timing.id) + "_"
        timing_whether_2_2 += str(effect_timing.id) + "_"
    timing_whether_1_1 = timing_whether_1_1[:-1]
    timing_whether_1_2 = timing_whether_1_2[:-1]
    timing_whether_2_1 = timing_whether_2_1[:-1]
    timing_whether_2_2 = timing_whether_2_2[:-1]
    duel.timing_whether_1_1 = timing_whether_1_1
    duel.timing_whether_1_2 = timing_whether_1_2
    duel.timing_whether_2_1 = timing_whether_2_1
    duel.timing_whether_2_2 = timing_whether_2_2
    effect_phases =  Phase.objects.filter(phase_whether_show = False)
    phase_whether_1_1 = ""
    phase_whether_1_2 = ""
    phase_whether_2_1 = ""
    phase_whether_2_2 = ""
    for effect_phase in effect_phases:
        phase_whether_1_1 += str(effect_phase.id) + "_"
        phase_whether_1_2 += str(effect_phase.id) + "_"
        phase_whether_2_1 += str(effect_phase.id) + "_"
        phase_whether_2_2 += str(effect_phase.id) + "_"
    phase_whether_1_1 = phase_whether_1_1[:-1]
    phase_whether_1_2 = phase_whether_1_2[:-1]
    phase_whether_2_1 = phase_whether_2_1[:-1]
    phase_whether_2_2 = phase_whether_2_2[:-1]
    duel.phase_whether_1_1= phase_whether_1_1
    duel.phase_whether_1_2 = phase_whether_1_2
    duel.phase_whether_2_1= phase_whether_2_1
    duel.phase_whether_2_2 = phase_whether_2_2
    duel.field = init_field(config)
    duel.winner = 0
    duel.winner_ai = 0
    duel.duel_id = str(uuid.uuid4())
    duel.cost_log = ""
    duel.current_log = ""
    duel.message_log = ""
    duel.log = "デュエルID " + duel.duel_id + "\n"
    duel.log_turn = duel.log
    duel.phase = start_phase
    duel.audio = ""
    duel.chain = 0
    duel.virtual_chain = 0
    duel.alt_global = ""
    duel.accumulate_global = []
    duel.chain_det = ""
    duel.chain_det_trigger = "{}"
    duel.chain_user = ""
    duel.chain_variable = "{}"
    if duel.is_ai is False and duel.guest_flag2 is False:
        duel.user_2 = user
    else:
        duel.user_2 = None
    duel.global_variable = init_global_variable()
    duel.mess = init_mess()
    duel.variable_mess = init_mess()
    duel.timing_mess = "{}"
    duel.timing = None
    duel.timing2 = None
    duel.timing3 = None
    duel.time_1 = time()
    duel.time_2 = time()
    duel.cost_result = init_cost_result()
    duel.waiting = False
    tmp = {}
    t_tmp = []
    duel.in_pac = json.dumps(tmp)
    duel.in_pac_cost = json.dumps(t_tmp)
    duel.trigger_waiting = json.dumps(t_tmp)
    duel.eternal_det = json.dumps(t_tmp)
    duel.in_trigger_waiting = False
    duel.cost = json.dumps(tmp)
    duel.cost_det = 0
    duel.chain = 0
    duel.virtual_chain = 0
    duel.in_cost = False
    duel.in_cost_cancel = True
    duel.canbechained = True
    if duel.is_ai == False:
        duel.user_turn = random.randrange(1, 3)
    else:
        duel.user_turn = 1
    duel.turn_count = 0
    if config.initial_turn_start_log is True:
        if duel.user_turn == 1:
            if duel.guest_flag is False:
                duel.log_turn += duel.user_1.first_name + "のターンからスタート\n"
            else:   
                duel.log_turn += duel.guest_name + "のターンからスタート\n"
        elif duel.user_turn == 2:
            if duel.guest_flag2 is False:
                duel.log_turn += duel.user_2.first_name + "のターンからスタート\n"
            else:   
                duel.log_turn += duel.guest_name2 + "のターンからスタート\n"
    duel.appoint = duel.user_turn
    duel.current_priority = 10000
    duel.ask = 0
    duel.timing_fresh = False
    duel.background_image = config.background_image
    duel.save()
    return False


def init_field(config):
    field_size = FieldSize.objects.first()
    fields = Field.objects.all()
    field_x = field_size.field_x
    field_y = field_size.field_y
    result_field = []
    if config.field_free is False:
        for x in range(field_x):
            tmp = []
            for y in range(field_y):
                tmp_field = {}
                field = fields.get(x=x, y=y)
                tmp_field["kind"] = field.kind
                tmp_field["mine_or_other"] = field.mine_or_other
                tmp_field["color"] = field.color
                tmp_field["sentence"] = field.sentence
                tmp_field["det"] = None
                tmp.append(tmp_field)
            result_field.append(tmp)
    else:
        for x in range(100):
            tmp = []
            for y in range(field_y):
                tmp_field = {}
                field = fields.get(x=0, y=y)
                tmp_field["kind"] = field.kind
                tmp_field["mine_or_other"] = field.mine_or_other
                tmp_field["color"] = field.color
                tmp_field["sentence"] = field.sentence
                tmp_field["det"] = None
                tmp.append(tmp_field)
            result_field.append(tmp)
    return json.dumps(result_field)


def init_mess():
    return_value = {}
    return json.dumps(return_value)


def init_cost_result():
    return_value = {}
    return json.dumps(return_value)


def init_global_variable():
    return_value = {}
    global_variables = GlobalVariable.objects.order_by("-priority").all()
    for global_variable in global_variables:
        tmp = {}
        if global_variable.mine_or_other == 1:
            tmp["mine_or_other"] = 1
            tmp["value"] = global_variable.initial_value
            tmp["show"] = global_variable.show
        else:
            tmp["mine_or_other"] = 0
            tmp["1_value"] = global_variable.initial_value
            tmp["1_show"] = global_variable.show
            tmp["2_value"] = global_variable.initial_value
            tmp["2_show"] = global_variable.show
        return_value[global_variable.variable_name] = tmp
    return json.dumps(return_value)


def check_enemy_deck(user,ai_id):
    decks = Deck.objects.all()
    enemy_deck_group = EnemyDeckGroup.objects.filter(enemy_deck_id=ai_id).first()
    enemy_decks = EnemyDeck.objects.filter(deck_group=enemy_deck_group)
    if not enemy_decks:
        return "error"
    for deck in decks:
        enemy_deck = enemy_decks.filter(deck_type=deck).first()
        if not enemy_deck:
            return "NPCデッキが不正です"
        enemy_deck_det = enemy_deck.deck.split("_")
    return False
def check_user_deck(user,deck_id):
    decks = Deck.objects.all()
    special_cards = []
    for deck in decks:
        user_deck_group = UserDeckGroup.objects.filter(user = user,user_deck_id=deck_id).first()
        user_decks = UserDeck.objects.filter(user=user, deck_group=user_deck_group)
        user_deck = user_decks.filter(deck_type=deck).first()
        if not user_deck:
            return HttpResponse("エラーが発生しました")
        user_deck = user_decks.filter(deck_type=deck).first()
        user_deck_det = user_deck.deck.split("_")
        special_cards.extend( check_special_cards(user_deck_det))
    user_deck_group = UserDeckGroup.objects.filter(user = user,user_deck_id=deck_id).first()
    if user_deck_group.user != user:
        return "デッキを構築してください"
    user_decks = UserDeck.objects.filter(user=user, deck_group=user_deck_group)
    if not user_decks:
        return "error"
    for deck in decks:
        min_deck_size = deck.min_deck_size
        max_deck_size = deck.max_deck_size
        for special_card in special_cards:
           if deck in special_card.deck.all():
               min_deck_size = special_card.min_deck_size
               max_deck_size = special_card.max_deck_size
               break
        user_deck = user_decks.filter(deck_type=deck).first()
        if not user_deck:
            return "デッキを構築してください"
        user_deck_det = user_deck.deck.split("_")
        if len(user_deck_det) < min_deck_size:
            return deck.deck_name + "のデッキ枚数が足りません"
        elif len(user_deck_det) > max_deck_size:
            return deck.deck_name + "のデッキ枚数が多すぎます"
    return False


def check_in_other_room_num(user,ID):
    for i in range(1, 4):
        duel = Duel.objects.filter(id=i).first()
        if (
                duel.waiting == 0
                and duel.winner == 0
                and user is None
                and ((duel.guest_flag is True and ID == duel.guest_id) or (duel.guest_flag2 is True and  ID == duel.guest_id2))
        ):
            return i
        if (
                duel.waiting == 0
                and duel.winner == 0
                and ((duel.user_1 == user and duel.guest_flag is False) or (duel.guest_flag2 is False and duel.user_2 == user and duel.is_ai is False))
        ):
            return i
        elif duel.waiting == 1 and (((user is not None and duel.user_1 == user) or (duel.guest_flag is True and duel.guest_id == ID)) and duel.user_2 is None and duel.guest_flag2 is False and duel.is_ai == False):
            return i
    return False
def check_in_other_room(user, room_number,ID):
    for i in range(1, 4):
        if i == room_number:
            continue
        duel = Duel.objects.filter(id=i).first()
        if (
            duel.waiting == 0
            and duel.winner == 0
            and user.is_anonymous
            and ((duel.guest_flag is True and ID == duel.guest_id) or (duel.guest_flag2 is True and  ID == duel.guest_id2))
        ):
            return True
        if (
            duel.waiting == 0
            and duel.winner == 0
            and ((duel.user_1 == user and duel.user_1 is not None and duel.guest_flag is False) or (duel.guest_flag2 is False and duel.user_2 == user and duel.user_2 is not None  and duel.is_ai is False))
        ):
            return True
        elif duel.waiting == 1 and (((user is not None and duel.user_1 == user) or (duel.guest_flag is True and duel.guest_id == ID)) and duel.user_2 is None and duel.guest_flag2 is False and duel.is_ai == False):
            return True
    return False
def modify_show(tmp,room_number,user,other_user,mine_or_other,place,deck_id):
    duelobj = DuelObj(room_number)
    duel = Duel.objects.filter(id=room_number).get()
    duelobj.duel = duel
    duelobj.room_number = room_number
    duelobj.user = user
    duelobj.other_user = other_user
    duelobj.init_all(user, other_user, room_number)
    decks = Deck.objects.all()
    graves = Grave.objects.all()
    hands = Hand.objects.all()
    duelobj.check_eternal_effect(
        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
    result = []
    for card in tmp:
         show = int(card["variables"]["show"]["value"])
         show = duelobj.check_change_val(
             card,
             mine_or_other,
             place,
             deck_id,
             0,
             0,
             "show",
             mine_or_other,
             show
         )
         if show >= 1:
             result.append(card)
         else:
             result.append(-1)
    return result
def modify_show2(tmp,room_number,user,other_user,mine_or_other,place,deck_id):
    duelobj = DuelObj(room_number)
    duel = Duel.objects.filter(id=room_number).get()
    duelobj.duel = duel
    duelobj.room_number = room_number
    duelobj.user = user
    duelobj.other_user = other_user
    duelobj.init_all(user, other_user, room_number)
    decks = Deck.objects.all()
    graves = Grave.objects.all()
    hands = Hand.objects.all()
    duelobj.check_eternal_effect(
        decks, graves, hands, duel.phase, duel.user_turn, user, other_user
    )
    result = []
    for card in tmp:
         show = int(card["variables"]["show"]["value"])
         show = duelobj.check_change_val(
             card,
             mine_or_other,
             place,
             deck_id,
             0,
             0,
             "show",
             mine_or_other,
             show
         )
         if show >= 1:
             result.append(card)
         else:
             card["monster_name"] = "*"+card["monster_name"]
             result.append(card)
    return result

def resetduel(duel):
        room_number = duel.id
        lock = Lock.objects.get()
        if room_number == 1:
            lock.lock_1 = False
            lock.save()
        elif room_number == 2:
            lock.lock_2 = False
            lock.save()
        elif room_number == 3:
            lock.lock_3 = False
            lock.save()
        duel.user_1 = None
        duel.user_2 = None
        duel.user_deck1 = None
        duel.user_deck2 = None
        duel.default_deck1 = None
        duel.default_deck2 = None
        duel.guest_flag = False
        duel.guest_flag2 = False
        duel.guest_id = "-1"
        duel.guest_id2 = "-1"
        duel.is_ai = False
        duel.waiting = True
        duel.time_1 = time()
        duel.time_2 = time()
        duel.winner = 0
        duel.winner_ai = 0
        duel.save()


