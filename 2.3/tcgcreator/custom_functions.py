from .models import (
    MonsterItem,
    Monster,
    Field,
    EternalEffect,
    Trigger,
    UserDeck,
    UserDeckGroup,
    UserDeckChoice,
    Deck,
    Grave,
    Hand,
    FieldKind,
    EnemyDeckGroup,
    EnemyDeckChoice,
    EnemyDeck,
    DefaultDeckGroup,
    DefaultDeckChoice,
    DefaultDeck,
    Constraint,
    SpecialCard
)
from django.http import HttpResponse, HttpResponseRedirect
import json
import uuid
import numpy as np
from pprint import pprint


def init_monster_item(monster_variable):
    monster = Monster.objects.all()
    for tmp in monster:
        monster_item = MonsterItem(
            monster_id=tmp,
            monster_variables_id=monster_variable,
            monster_item_text=monster_variable.default_value,
        )

        monster_item.save()


def init_field(x, y):
    Field.objects.all().delete()
    for tmp_x in range(0, int(x)):
        for tmp_y in range(0, int(y)):
            field = Field(x=tmp_x, y=tmp_y, kind="", mine_or_other=0)
            field.save()


def create_user_deck(user_id, deck_id, deck_group, default_deck_group_id):
    if default_deck_group_id != "0":
        default_deck_group_id = int(default_deck_group_id)
        default_deck = DefaultDeckGroup.objects.all().get(
            default_deck_id=default_deck_group_id
        )
        default_deck = DefaultDeck.objects.all().get(
            deck_type=deck_id, deck_group=default_deck
        )

        user_deck = UserDeck(
            user=user_id, deck_type=deck_id, deck=default_deck.deck, deck_group=deck_group
        )
    else:
        user_deck = UserDeck(
            user=user_id, deck_type=deck_id, deck="", deck_group=deck_group
        )
    user_deck.save()


def create_user_deck_group(deck_group, user_id, deck_name):
    user_deck = UserDeckGroup(
        user_deck_id=deck_group, user=user_id, deck_name=deck_name
    )
    user_deck.save()


def create_user_deck_choice(deck_group, user_id):
    user_deck = UserDeckChoice(user=user_id, user_deck=deck_group)
    user_deck.save()


def create_default_deck(deck_id, deck_group):
    default_deck = DefaultDeck(deck_type=deck_id, deck="", deck_group=deck_group)
    default_deck.save()


def create_default_deck_group(deck_group, deck_name):
    default_deck = DefaultDeckGroup(default_deck_id=deck_group, deck_name=deck_name)
    default_deck.save()


def create_enemy_deck(deck_id, deck_group):
    enemy_deck = EnemyDeck(deck_type=deck_id, deck="", deck_group=deck_group)
    enemy_deck.save()


def create_enemy_deck_group(deck_group, deck_name):
    enemy_deck = EnemyDeckGroup(enemy_deck_id=deck_group, deck_name=deck_name)
    enemy_deck.save()


def create_enemy_deck_choice(deck_group):
    enemy_deck = EnemyDeckChoice(enemy_deck=deck_group)
    enemy_deck.save()

def create_default_deck_choice(deck_group):
    default_deck = DefaultDeckChoice(default_deck=deck_group)
    default_deck.save()


def copy_to_enemy_deck(post, deck_group):
    decks = Deck.objects.all()
    all_decks = []
    result_decks = []
    enemy_decks = EnemyDeck.objects.filter(deck_group=deck_group)
    for deck in decks:
        result_deck = []
        enemy_deck = enemy_decks.filter(deck_type_id=deck.id).first()
        exclude_deck = post.getlist("exclude_monster_deck_" + str(deck.id))
        enemy_deck_array = enemy_deck.deck.split("_")
        for exclude_deck_det in exclude_deck:
            try:
                enemy_deck_array.remove(exclude_deck_det)
            except ValueError:
                pass
        if len(enemy_deck_array) != 0 and enemy_deck_array[0] != "":
            result_deck.extend(enemy_deck_array)
            all_decks.extend(enemy_deck_array)
        add_deck = post.getlist("monster_deck_" + str(deck.id))
        for monster_id in add_deck:
            monster = Monster.objects.filter(id=monster_id).first()
            in_decks =  monster.monster_deck.split("_")
            if(str(deck.id) not in in_decks):
                return HttpResponse("error")
        if len(add_deck) != 0:
            all_decks.extend(add_deck)
            result_deck.extend(add_deck)
        result_deck = sorted(result_deck)
        if enemy_deck.deck == "":

            enemy_deck_size = 0
        else:
            enemy_deck_size = len(enemy_deck_array)
        add_deck_size = len(add_deck)
        if deck.max_deck_size < add_deck_size + enemy_deck_size:
            return "デッキ枚数が多すぎます"
        result_decks.append(result_deck)

    all_decks = sorted(all_decks)
    tmp = 0
    for all_deck in all_decks:
        if all_deck != tmp:
            tmp = all_deck
            monster = Monster.objects.filter(id=int(all_deck)).first()
            if all_decks.count(all_deck) > monster.monster_limit:
                return monster.monster_name + "の制限を違反しています"

    i = 0
    for deck in decks:
        enemy_deck = enemy_decks.filter(deck_type_id=deck.id).first()
        enemy_deck.deck = "_".join(result_decks[i])
        enemy_deck.save()
        i += 1
    return ""

def copy_to_default_deck(post, deck_group):
    decks = Deck.objects.all()
    all_decks = []
    result_decks = []
    default_decks = DefaultDeck.objects.filter(deck_group=deck_group)
    for deck in decks:
        result_deck = []
        default_deck = default_decks.filter(deck_type_id=deck.id).first()
        exclude_deck = post.getlist("exclude_monster_deck_" + str(deck.id))
        default_deck_array = default_deck.deck.split("_")
        for exclude_deck_det in exclude_deck:
            try:
                default_deck_array.remove(exclude_deck_det)
            except ValueError:
                pass
        if len(default_deck_array) != 0 and default_deck_array[0] != "":
            result_deck.extend(default_deck_array)
            all_decks.extend(default_deck_array)
        add_deck = post.getlist("monster_deck_" + str(deck.id))
        for monster_id in add_deck:
            monster = Monster.objects.filter(id=monster_id).first()
            in_decks =  monster.monster_deck.split("_")
            if(str(deck.id) not in in_decks):
                return HttpResponse("error")
        if len(add_deck) != 0:
            all_decks.extend(add_deck)
            result_deck.extend(add_deck)
        result_deck = sorted(result_deck)
        if default_deck.deck == "":

            default_deck_size = 0
        else:
            default_deck_size = len(default_deck_array)
        add_deck_size = len(add_deck)
        if deck.max_deck_size < add_deck_size + default_deck_size:
            return "デッキ枚数が多すぎます"
        result_decks.append(result_deck)

    all_decks = sorted(all_decks)
    tmp = 0
    for all_deck in all_decks:
        if all_deck != tmp:
            tmp = all_deck
            monster = Monster.objects.filter(id=int(all_deck)).first()
            if all_decks.count(all_deck) > monster.monster_limit:
                return monster.monster_name + "の制限を違反しています"

    i = 0
    for deck in decks:
        default_deck = default_decks.filter(deck_type_id=deck.id).first()
        default_deck.deck = "_".join(result_decks[i])
        default_deck.save()
        i += 1
    return ""


def copy_to_deck_text(user_id, post, deck_group):
    decks = Deck.objects.all()
    all_decks = []
    result_decks = []
    user_decks = UserDeck.objects.filter(user=user_id, deck_group=deck_group)
    for deck in decks:
        result_deck = []
        user_deck = user_decks.filter(deck_type_id=deck.id).first()
        add_decks = post["user_deck_text_"+str(deck.id)].split("\r\n")
        tmp = []
        if len(add_decks) != 0:
            for add_deck in add_decks:
                if add_deck == "":
                    continue
                monster = Monster.objects.filter(monster_name=add_deck).get()
                
                if monster.token_flag is True:
                    return HttpResponse("error")
                monster_id = monster.id
                monster_places = monster.monster_deck.split("_")
                if str(deck.id) not in  monster_places:
                        break
                all_decks.append(str(monster_id))
                result_deck.append(str(monster_id))
        else:
            continue
        result_deck = sorted(result_deck)
        result_deck_size = len(result_deck)
        if deck.max_deck_size < result_deck_size:
            return "デッキ枚数が多すぎます"
        result_decks.append(result_deck)

    all_decks = sorted(all_decks)
    tmp = 0
    if Constraint.objects.exists():
        constraint = Constraint.objects.get()
        constraint_variable = constraint.monster_variable.id
    else:
        constraint_variable = -1
    constraint_variety = []
    special_cards = check_special_cards(all_decks)
    max_deck_size = deck.max_deck_size 
    for special_card in special_cards:
        if deck in special_card.deck.all():
           special_first = special_card.first()
           min_deck_size = special_first.min_deck_size
           max_deck_size = special_first.max_deck_size
    for all_deck in all_decks:
        if all_deck != tmp:
            tmp = all_deck
            monster = Monster.objects.filter(id=int(all_deck)).first()
            if constraint_variable != -1:
                monsteritem = (
                MonsterItem.objects
                    .filter(monster_id__id=int(all_deck) , monster_variables_id__id = constraint_variable)
            ).get()
            if all_decks.count(all_deck) > monster.monster_limit:
                return monster.monster_name + "の制限を違反しています"
            if not constraint_variable:
                continue
            if constraint_variable == -1 or monsteritem.monster_item_text == constraint.except_val:
                continue
            elif monsteritem.monster_item_text not in constraint_variety and int(monsteritem.monster_item_text) != int(constraint.except_val):
                constraint_variety.append(monsteritem.monster_item_text)
    if constraint_variable != -1 and (len(constraint_variety) > constraint.limit):
        return "制約に違反しています。"

    i = 0
    for deck in decks:
        user_deck = user_decks.filter(deck_type_id=deck.id).first()
        user_deck.deck = "_".join(result_decks[i])
        user_deck.save()
        i += 1
    return ""


def copy_to_deck(user_id, post, deck_group):
    decks = Deck.objects.filter( makedeckshow=True)
    all_decks = []
    result_decks = []
    user_decks = UserDeck.objects.filter(user=user_id, deck_group=deck_group)
    special_first = None
    for deck in decks:
        result_deck = []
        user_deck = user_decks.filter(deck_type_id=deck.id).first()
        exclude_deck = post.getlist("exclude_monster_deck_" + str(deck.id))
        user_deck_array = user_deck.deck.split("_")
        for exclude_deck_det in exclude_deck:
            try:
                user_deck_array.remove(exclude_deck_det)
            except ValueError:
                pass
        if len(user_deck_array) != 0 and user_deck_array[0] != "":
            result_deck.extend(user_deck_array)
            all_decks.extend(user_deck_array)
        add_deck = post.getlist("monster_deck_" + str(deck.id))
        for monster_id in add_deck:
            monster = Monster.objects.filter(id=monster_id).first()
            if monster.token_flag is True:
                return HttpResponse("error")
            in_decks =  monster.monster_deck.split("_")
            if(str(deck.id) not in in_decks):
                return HttpResponse("error")
        if len(add_deck) != 0:
            all_decks.extend(add_deck)
            result_deck.extend(add_deck)
        special_cards = check_special_cards(all_decks)
        max_deck_size = deck.max_deck_size 
        for special_card in special_cards:
            if deck in special_card.deck.all():
               special_first = special_card.first()
               min_deck_size = special_first.min_deck_size
               max_deck_size = special_first.max_deck_size
        result_deck = sorted(result_deck)
        if user_deck.deck == "":

            user_deck_size = 0
        else:
            user_deck_size = len(user_deck_array)
        add_deck_size = len(add_deck)
        if deck.max_deck_size < add_deck_size + user_deck_size:
            return "デッキ枚数が多すぎます"
        result_decks.append(result_deck)

    all_decks = sorted(all_decks)
    tmp = 0
    if Constraint.objects.exists() :
        constraint = Constraint.objects.get()
        if special_first and special_first.constraint == constraint:
            constraint_variable = -1
        else:
            constraint_variable = constraint.monster_variable.id
    else:
        constraint_variable = -1
    constraint_variety = []
    for all_deck in all_decks:
        if all_deck != tmp:
            tmp = all_deck
            monster = Monster.objects.filter(id=int(all_deck)).first()
            if constraint_variable != -1:
                monsteritem = (
                MonsterItem.objects
                .filter(monster_id__id=int(all_deck) , monster_variables_id__id = constraint_variable)
                ).get()

            if all_decks.count(all_deck) > monster.monster_limit:
                return monster.monster_name + "の制限を違反しています"
            if not constraint_variable:
                continue
            if constraint_variable == -1 or monsteritem.monster_item_text == constraint.except_val:
                continue
            elif monsteritem.monster_item_text not in constraint_variety and int(monsteritem.monster_item_text) != int(constraint.except_val):
                constraint_variety.append(monsteritem.monster_item_text)
    if constraint_variable != -1 and (len(constraint_variety) > constraint.limit):
        return "制約に違反しています。"
    i = 0
    for deck in decks:
        user_deck = user_decks.filter(deck_type_id=deck.id).first()
        user_deck.deck = "_".join(result_decks[i])
        user_deck.save()
        i += 1
    return ""


def cheat_get(id, deck_id, owner, place):
    monster = Monster.objects.filter(id=int(id)).first()
    tmp = {}
    tmp6 = {}
    tmp["flag"] = 0
    tmp["monster_name"] = monster.monster_name
    tmp["id"] = monster.id
    tmp["token"] = monster.token_flag
    tmp["org_id"] = monster.id
    tmp["monster_sentence"] = monster.monster_sentence
    tmp["img"] = monster.img
    tmp["user"]= owner
    tmp["mine_or_other"]= owner
    monsteritems = (
        MonsterItem.objects.all()
        .filter(monster_id__id=id)
        .order_by("-monster_variables_id__priority")
        .select_related("monster_variables_id")
        .select_related("monster_variables_id__monster_variable_kind_id")
    )

    for monsteritem in monsteritems:
        tmp5 = {}
        monster_variable = monsteritem.monster_variables_id
        tmp5["name"] = monster_variable.monster_variable_name
        tmp5["minus"] = monster_variable.monster_variable_minus
        tmp5["value"] = monsteritem.monster_item_text
        tmp5["i_val"] = monsteritem.monster_item_text
        tmp5["i_i_val"] = monsteritem.monster_item_text
        tmp5["show"] = monster_variable.monster_variable_show_battle
        tmp5["kind"] = monster_variable.monster_variable_kind_id.monster_variable_sentence 
        tmp5["kind_id"] = monster_variable.monster_variable_kind_id.id
        tmp2 = monsteritem.monster_item_text.split("_")
        if monster_variable.monster_variable_kind_id.monster_variable_name == "数値":
            tmp5["str"] = tmp5["value"]
        else:
            tmp5["str"] = "deck_"
            for tmp3 in tmp2:
                tmp4 = monster_variable.monster_variable_kind_id.monster_variable_sentence.split(
                    "|"
                )
                tmp5["str"] += tmp4[int(tmp3) - 1]
        tmp6[monster_variable.monster_variable_name] = tmp5
    tmp["variables"] = tmp6
    tmp["place"] = place
    tmp["from"] = None
    tmp["noeffect"] = ""
    tmp["nochoose"] = ""
    tmp["owner"] = owner
    tmp["user"] = owner
    tmp["deck_id"] = deck_id
    tmp["card_unique_id"] = str(uuid.uuid4())
    tmp["place_unique_id"] = str(uuid.uuid4())
    decks = Deck.objects.all()
    graves = Grave.objects.all()
    hands = Hand.objects.all()
    fields = FieldKind.objects.all()
    tmp["deck_eternal"] = {}
    tmp["deck_trigger"] = {}
    tmp["grave_eternal"] = {}
    tmp["grave_trigger"] = {}
    tmp["hand_eternal"] = {}
    tmp["hand_trigger"] = {}
    tmp["field_eternal"] = {}
    tmp["field_trigger"] = {}
    for deck in decks:
        eternals = monster.eternal_effect.filter(eternal_deck__id=deck.id).all()
        tmp["deck_eternal"][str(deck.id)] = []
        for eternal in eternals:
            tmp["deck_eternal"][str(deck.id)].append(eternal.id) 
        triggers = monster.trigger.filter(trigger_deck__id=deck.id,trigger_timing = False).all()
        tmp["deck_trigger"][str(deck.id)] = []
        for trigger in triggers:
            tmp["deck_trigger"][str(deck.id)].append(trigger.id) 
    for grave in graves:
        eternals = monster.eternal_effect.filter(eternal_grave__id=grave.id).all()
        tmp["grave_eternal"][str(grave.id)] = []
        for eternal in eternals:
            tmp["grave_eternal"][str(grave.id)].append(eternal.id) 
        triggers = monster.trigger.filter(trigger_grave__id=grave.id,trigger_timing = False).all()
        tmp["grave_trigger"][str(grave.id)] = []
        for trigger in triggers:
            tmp["grave_trigger"][str(grave.id)].append(trigger.id) 
    for hand in hands:
        eternals = monster.eternal_effect.filter(eternal_hand__id=hand.id).all()
        tmp["hand_eternal"][str(hand.id)] = []
        for eternal in eternals:
            tmp["hand_eternal"][str(hand.id)].append(eternal.id) 
        triggers = monster.trigger.filter(trigger_hand__id=hand.id,trigger_timing = False).all()
        tmp["hand_trigger"][str(hand.id)] = []
        for trigger in triggers:
            tmp["hand_trigger"][str(hand.id)].append(trigger.id) 
    for field in fields:
        eternals = monster.eternal_effect.filter(eternal_field__id=field.id).all()
        tmp["field_eternal"][str(field.id)] = []
        for eternal in eternals:
            tmp["field_eternal"][str(field.id)].append(eternal.id) 
        triggers = monster.trigger.filter(trigger_field__id=field.id,trigger_timing = False).all()
        tmp["field_trigger"][str(field.id)] = []
        for trigger in triggers:
            tmp["field_trigger"][str(field.id)].append(trigger.id) 
    return tmp


def create_user_deck_det(user_deck, deck_id, owner):
    ids = user_deck.split("_")
    return_value = []
    if user_deck == "":
        return return_value
    for id in ids:
        tmp = {}
        tmp6 = {}

        monster = Monster.objects.filter(id=int(id)).first()
        tmp["flag"] = 0
        tmp["token"] = monster.token_flag
        tmp["monster_name"] = monster.monster_name
        tmp["id"] = monster.id
        tmp["org_id"] = monster.id
        tmp["monster_sentence"] = monster.monster_sentence
        tmp["img"] = monster.img
        decks = Deck.objects.all()
        graves = Grave.objects.all()
        hands = Hand.objects.all()
        fields = FieldKind.objects.all()
        tmp["deck_eternal"] = {}
        tmp["deck_trigger"] = {}
        tmp["grave_eternal"] = {}
        tmp["grave_trigger"] = {}
        tmp["hand_eternal"] = {}
        tmp["hand_trigger"] = {}
        tmp["field_eternal"] = {}
        tmp["field_trigger"] = {}
        for deck in decks:
            eternals = monster.eternal_effect.filter(eternal_deck__id=deck.id).all()
            tmp["deck_eternal"][str(deck.id)] = []
            for eternal in eternals:
                tmp["deck_eternal"][str(deck.id)].append(eternal.id) 
            triggers = monster.trigger.filter(trigger_deck__id=deck.id,trigger_timing = False).all()
            tmp["deck_trigger"][str(deck.id)] = []
            for trigger in triggers:
                tmp["deck_trigger"][str(deck.id)].append(trigger.id) 
        for grave in graves:
            eternals = monster.eternal_effect.filter(eternal_grave__id=grave.id).all()
            tmp["grave_eternal"][str(grave.id)] = []
            for eternal in eternals:
                tmp["grave_eternal"][str(grave.id)].append(eternal.id) 
            triggers = monster.trigger.filter(trigger_grave__id=grave.id,trigger_timing = False).all()
            tmp["grave_trigger"][str(grave.id)] = []
            for trigger in triggers:
                tmp["grave_trigger"][str(grave.id)].append(trigger.id) 
        for hand in hands:
            eternals = monster.eternal_effect.filter(eternal_hand__id=hand.id).all()
            tmp["hand_eternal"][str(hand.id)] = []
            for eternal in eternals:
                tmp["hand_eternal"][str(hand.id)].append(eternal.id) 
            triggers = monster.trigger.filter(trigger_hand__id=hand.id,trigger_timing = False).all()
            tmp["hand_trigger"][str(hand.id)] = []
            for trigger in triggers:
                tmp["hand_trigger"][str(hand.id)].append(trigger.id) 
        for field in fields:
            eternals = monster.eternal_effect.filter(eternal_field__id=field.id).all()
            tmp["field_eternal"][str(field.id)] = []
            for eternal in eternals:
                tmp["field_eternal"][str(field.id)].append(eternal.id) 
            triggers = monster.trigger.filter(trigger_field__id=field.id,trigger_timing = False).all()
            tmp["field_trigger"][str(field.id)] = []
            for trigger in triggers:
                tmp["field_trigger"][str(field.id)].append(trigger.id) 
        monsteritems = (
            MonsterItem.objects.all()
            .filter(monster_id__id=id)
            .order_by("-monster_variables_id__priority")
            .select_related("monster_variables_id")
            .select_related("monster_variables_id__monster_variable_kind_id")
        )

        for monsteritem in monsteritems:
            tmp5 = {}
            monster_variable = monsteritem.monster_variables_id
            tmp5["name"] = monster_variable.monster_variable_name
            tmp5["minus"] = monster_variable.monster_variable_minus
            tmp5["value"] = monsteritem.monster_item_text
            tmp5["i_val"] = monsteritem.monster_item_text
            tmp5["i_i_val"] = monsteritem.monster_item_text
            tmp5["show"] = monster_variable.monster_variable_show_battle
            tmp5["kind"] = monster_variable.monster_variable_kind_id.monster_variable_sentence 
            tmp5["kind_id"] = monster_variable.monster_variable_kind_id.id
            tmp2 = monsteritem.monster_item_text.split("_")
            if monster_variable.monster_variable_kind_id.monster_variable_name == "数値":
                tmp5["str"] = tmp5["value"]
            else:
                tmp5["str"] = ""
                for tmp3 in tmp2:
                    tmp4 = monster_variable.monster_variable_kind_id.monster_variable_sentence.split(
                        "|"
                    )
                    tmp5["str"] += tmp4[int(tmp3) - 1]
            tmp6[monster_variable.monster_variable_name] = tmp5
        tmp["variables"] = tmp6
        tmp["place"] = "deck"
        tmp["from"] = None
        tmp["noeffect"] = ""
        tmp["nochoose"] = ""
        tmp["owner"] = owner
        tmp["user"] = owner
        tmp["mine_or_other"] = owner
        tmp["deck_id"] = deck_id
        tmp["card_unique_id"] = str(uuid.uuid4())
        tmp["place_unique_id"] = str(uuid.uuid4())

        return_value.append(tmp)
    np.random.shuffle(return_value)
    return json.dumps(return_value)
def get_field_y_range(fields,field_size):
    ary = [0] *field_size
    ary2 = [0] *field_size
    for y in range(field_size):
        field =  fields.filter(y=y,x=0).get()
        if field.no_clear is True and field.mine_or_other == 1:
            ary2.append(y)
        else:
            ary[y]=y
    for y in range(field_size):
        if ary[y] == 0 and y != 0:
            ary[y] = ary2[-1]
            del ary2[-1]
    return ary
def check_special_cards(user_decks):
    special_cards = SpecialCard.objects.all()
    result_special_card = []
    for user_deck in user_decks:
        if user_deck == "":
            return []
        result_special_card.extend(special_cards.filter(special_card__id = int(user_deck)))
    return result_special_card
