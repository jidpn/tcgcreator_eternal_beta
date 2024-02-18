from django.db import models
from django.contrib.auth.models import (
    User,
)
SHOW_IMG = (
        (0,"画像不使用"),
        (1,"画像使用"),
        )
WIN_OR_LOSE = (
        (0,"なし"),
        (1,"勝利"),
        (2,"敗北")
        )
CSV_ENCODING = (
        (0,"SJIS"),
        (1,"EUC-JP"),
        (2,"UTF-8")
        )
ORDER = ((0,"起きた順"),(1,"ターンプレイヤーが選ぶ"),(2,"ターンプレイヤーが優先され、ターンプレイヤー、非ターンプレイヤーが選ぶ"),(3,"プレイヤーが交互に選ぶ"))
UP_OR_DOWN = ((0,"大きい"),(1,"小さい"))
SHORI = ((0,"順方向"),(1,"逆方向"))
WHO = ((0, "trigger"), (1, "triggerexist"), (2, "triggerrelate"))
ENEMY = ((0, "human"), (1, "human and ai"), (2, "ai"))
TRIGGER_WHO2 = ((0, "元々の持ち主"), (1, "行使者"), (2, "非行使者"), (3, "場所"), (4, "リレーション"))
TRIGGER_WHO3 = ((0, "元々の持ち主"), (1, "行使者"), (2, "非行使者"), (3, "場所"), (4, "リレーション"),(5, "リレーションのリレーション"))
ETERNAL_IGNORE = (
    (1, "チェイン"),
    (2, "チェインを相手のみまたは自分のみ無視"),
    (3, "チェイン種類無視"),
    (4, "同一チェインOK"),
    (5, "同一モンスターチェインOK"),
    (6, "同一モンスター存在チェインOK"),
    (7, "フェイズ無視"),
    (8, "モンスター自分または相手無視"),
    (9, "発動できない無視"),
    (10, "タイミング無視"),
    (11, "モンスター場所無視"),
    (12, "モンスター場所条件無視"),
    (13, "ターン無視"),
    (14, "条件無視"),
    (15, "変数条件無視"),
)
TRIGGER_WHO = (
    (0, "元々の持ち主"),
    (1, "行使者"),
    (2, "非行使者"),
    (3, "移動元"),
    (4, "移動先"),
    (5, "リレーション"),
)

MINE_OR_OTHER4 = ((1, "自分"), (2, "相手"), (3, "共通"), (4, "元々"))
MINE_OR_OTHER3 = ((0, "全て"), (1, "自分"), (2, "相手"), (3, "共通"))
MINE_OR_OTHER = ((0, "共通"), (1, "自分"), (2, "相手"),(3,"共通２"))
PLACE_KIND_WITHOUT_ALL = ((1, "デッキ"), (2, "墓地"), (3, "手札"), (4, "フィールド"), (5, "重ねられた"))
PLACE_KIND = ((0, "全て"), (1, "デッキ"), (2, "墓地"), (3, "手札"), (4, "フィールド"), (5, "重ねられた"))
COST_OR_EFFECT = ((0, "両方"), (1, "コスト"), (2, "効果"))
CHAIN = ((0, "以上"), (1, "以下"), (2, "ちょうど"))
CONFIG_TEMPLATE_CHOICE = ((1,"普通"),(2,"並列"),(3,"並列２"))
EQUATION = ((0,"="),(1,"<="),(2,">="),(3,"!="))
LEFT_OR_CENTER = (
        (0,"左"),
        (1,"中央"),
        (2,"右")
)
class UnderDirection(models.Model):
    to_place_kind = models.IntegerField(choices=PLACE_KIND, default=0)
    to_deck = models.ForeignKey(
        "Deck",
        default=None,
        null=True,
        related_name="to_deck_under",
        blank=True,
        on_delete=models.SET_NULL,
    )
    to_grave = models.ForeignKey(
        "Grave",
        default=None,
        null=True,
        related_name="to_grave_under",
        blank=True,
        on_delete=models.SET_NULL,
    )
    to_hand = models.ForeignKey(
        "Hand",
        default=None,
        null=True,
        related_name="to_hand_under",
        blank=True,
        on_delete=models.SET_NULL,
    )
    to_field = models.ForeignKey(
        "FieldKind",
        default=None,
        null=True,
        related_name="to_field_kind_under",
        blank=True,
        on_delete=models.SET_NULL,
    )
    to_mine_or_other = models.IntegerField(choices=MINE_OR_OTHER3, default=0)
    dest_place_kind = models.IntegerField(choices=PLACE_KIND_WITHOUT_ALL, default=0)
    dest_deck = models.ForeignKey(
        "Deck",
        default=None,
        null=True,
        related_name="dest_deck",
        blank=True,
        on_delete=models.SET_NULL,
    )
    dest_grave = models.ForeignKey(
        "Grave",
        default=None,
        null=True,
        related_name="dest_grave",
        blank=True,
        on_delete=models.SET_NULL,
    )
    dest_hand = models.ForeignKey(
        "Hand",
        default=None,
        null=True,
        related_name="dest_hand",
        blank=True,
        on_delete=models.SET_NULL,
    )
    dest_field = models.ForeignKey(
        "FieldKind",
        default=None,
        null=True,
        related_name="dest_field_kind",
        blank=True,
        on_delete=models.SET_NULL,
    )
    dest_mine_or_other = models.IntegerField(choices=MINE_OR_OTHER4, default=0)
    shuffle = models.BooleanField(default=False, null=True)


class Timing(models.Model):
    next_timing = models.ForeignKey(
        "Timing", default=None, blank=True, null=True, on_delete=models.SET_NULL
    )
    timing_name = models.CharField(max_length=32, blank=True)
    timing_auto = models.BooleanField(default=False)
    timing_whether_show = models.BooleanField(default=False)
    pri = models.BooleanField(default=True)

    def __str__(self):
        return self.timing_name

    class Meta:
        db_table = "tcgcreator_timing"


class TriggerTimingRelation(models.Model):
    def __str__(self):
        return self.trigger_timing_name

    trigger = models.ForeignKey(
        "Trigger", default=None, null=True, blank=True, on_delete=models.SET_NULL
    )
    kinds = models.CharField(max_length=32, blank=True)
    monster = models.ManyToManyField("Monster", blank=True)
    who = models.IntegerField(choices=TRIGGER_WHO2, default=0)
    chain_user = models.IntegerField(choices=MINE_OR_OTHER3, default=0)
    cost_or_effect = models.IntegerField(choices=COST_OR_EFFECT)
    trigger_timing_name = models.CharField(max_length=32)
    relation_kind = models.CharField(max_length=32, blank=True)
    relation_name = models.CharField(max_length=32, blank=True)
    relation_to = models.BooleanField(default=False, blank=True)
    clear_flag = models.BooleanField(default=False, blank=True)
    leave_flag_self = models.BooleanField(default=False, blank=True)
    leave_flag_null_relate = models.BooleanField(default=True, blank=True)
    which_monster_effect = models.IntegerField(choices = WHO,default = 0)
    once_per_turn_relate = models.BooleanField(default=False,blank=True)
    once_per_turn_exist = models.BooleanField(default=False,blank=True)
    enemy = models.IntegerField(choices = ENEMY,default =1)
    enemy_own = models.IntegerField(choices = ENEMY,default =1)
    chain = models.IntegerField(default=0, blank=True)
    chain_kind = models.IntegerField(default=0, blank=True, choices=CHAIN)
    class Meta:
        db_table = "tcgcreator_triggertimingrelation"


class TriggerTimingNotEffected(models.Model):
    def __str__(self):
        return self.trigger_timing_name

    trigger = models.ForeignKey(
        "Trigger", default=None, null=True, blank=True, on_delete=models.SET_NULL
    )
    kinds = models.CharField(max_length=32, blank=True)
    monster = models.ManyToManyField("Monster", blank=True)
    monster_specify_flag = models.BooleanField(blank=True, default=True)
    monster_relate = models.ManyToManyField(
        "Monster", related_name="monster_relate_not_effected_exist", blank=True
    )
    monster_relate_specify_flag = models.BooleanField(blank=True, default=False)
    who = models.IntegerField(choices=TRIGGER_WHO3, default=0)
    chain_user = models.IntegerField(choices=MINE_OR_OTHER3, default=0)
    cost_or_effect = models.IntegerField(choices=COST_OR_EFFECT, blank=True)
    trigger_timing_name = models.CharField(max_length=32)
    change_val = models.IntegerField(default=0)
    change_val_operator = models.CharField(max_length=32, blank=True)
    org = models.BooleanField(default=True)
    relation = models.BooleanField(default=False)
    relation_kind = models.CharField(max_length=32, blank=True)
    relation_name = models.CharField(max_length=32, blank=True)
    relation_to = models.BooleanField(default=False, blank=True)
    relation2 = models.BooleanField(default=False)
    relation_kind2 = models.CharField(max_length=32, blank=True)
    relation_name2 = models.CharField(max_length=32, blank=True)
    relation_to2 = models.BooleanField(default=False, blank=True)
    org_flag = models.BooleanField(default=False, blank=True)
    monster_exist = models.ManyToManyField(
        "Monster", related_name="monster_exist_trigger_not_effected_timing_change_val", blank=True
    )
    monster_exist_specify_flag = models.BooleanField(blank=True, default=False)
    exist_place_kind = models.IntegerField(choices=PLACE_KIND, default=0)
    exist_deck = models.ForeignKey(
        "Deck",
        default=None,
        null=True,
        related_name="exist_deck_not_effected",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exist_grave = models.ForeignKey(
        "Grave",
        default=None,
        null=True,
        related_name="exist_grave_not_effected",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exist_hand = models.ForeignKey(
        "Hand",
        default=None,
        null=True,
        related_name="exist_hand_not_effected",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exist_field = models.ForeignKey(
        "FieldKind",
        default=None,
        null=True,
        related_name="exist_field_kind_not_effected",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exist_kinds = models.CharField(max_length=32, blank=True)
    exist_mine_or_other = models.IntegerField(choices=MINE_OR_OTHER3, default=0)
    which_monster_effect = models.IntegerField(choices = WHO,default = 0)
    variable_name = models.CharField(max_length=32, blank=True)
    once_per_turn_relate = models.BooleanField(default=False,blank=True)
    once_per_turn_exist = models.BooleanField(default=False,blank=True)
    enemy = models.IntegerField(choices = ENEMY,default =1)
    enemy_own = models.IntegerField(choices = ENEMY,default =1)
    chain = models.IntegerField(default=0, blank=True)
    chain_kind = models.IntegerField(default=0, blank=True, choices=CHAIN)

    class Meta:
        db_table = "tcgcreator_triggertimingnoteffected"

class TriggerTimingMonsterChangeVal(models.Model):
    def __str__(self):
        return self.trigger_timing_name

    trigger = models.ForeignKey(
        "Trigger", default=None, null=True, blank=True, on_delete=models.SET_NULL
    )
    kinds = models.CharField(max_length=32, blank=True)
    monster = models.ManyToManyField("Monster", blank=True)
    monster_specify_flag = models.BooleanField(blank=True, default=True)
    monster_relate = models.ManyToManyField(
        "Monster", related_name="monster_relate_monster_change_val_exist", blank=True
    )
    monster_relate_specify_flag = models.BooleanField(blank=True, default=False)
    who = models.IntegerField(choices=TRIGGER_WHO3, default=0)
    chain_user = models.IntegerField(choices=MINE_OR_OTHER3, default=0)
    cost_or_effect = models.IntegerField(choices=COST_OR_EFFECT, blank=True)
    trigger_timing_name = models.CharField(max_length=32)
    change_val = models.IntegerField(default=0)
    change_val_operator = models.CharField(max_length=32, blank=True)
    org = models.BooleanField(default=True)
    relation = models.BooleanField(default=False)
    relation_kind = models.CharField(max_length=32, blank=True)
    relation_name = models.CharField(max_length=32, blank=True)
    relation_to = models.BooleanField(default=False, blank=True)
    relation2 = models.BooleanField(default=False)
    relation_kind2 = models.CharField(max_length=32, blank=True)
    relation_name2 = models.CharField(max_length=32, blank=True)
    relation_to2 = models.BooleanField(default=False, blank=True)
    org_flag = models.BooleanField(default=False, blank=True)
    monster_exist = models.ManyToManyField(
        "Monster", related_name="monster_exist_trigger_monster_timing_change_val", blank=True
    )
    monster_exist_specify_flag = models.BooleanField(blank=True, default=False)
    exist_place_kind = models.IntegerField(choices=PLACE_KIND, default=0)
    exist_deck = models.ForeignKey(
        "Deck",
        default=None,
        null=True,
        related_name="exist_deck_monster_change_val",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exist_grave = models.ForeignKey(
        "Grave",
        default=None,
        null=True,
        related_name="exist_grave_monster_change_val",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exist_hand = models.ForeignKey(
        "Hand",
        default=None,
        null=True,
        related_name="exist_hand_monster_change_val",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exist_field = models.ForeignKey(
        "FieldKind",
        default=None,
        null=True,
        related_name="exist_field_kind_monster_change_val",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exist_kinds = models.CharField(max_length=32, blank=True)
    exist_mine_or_other = models.IntegerField(choices=MINE_OR_OTHER3, default=0)
    which_monster_effect = models.IntegerField(choices = WHO,default = 0)
    variable_name = models.CharField(max_length=32, blank=False)
    once_per_turn_relate = models.BooleanField(default=False,blank=True)
    once_per_turn_exist = models.BooleanField(default=False,blank=True)
    enemy = models.IntegerField(choices = ENEMY,default =1)
    enemy_own = models.IntegerField(choices = ENEMY,default =1)
    chain = models.IntegerField(default=0, blank=True)
    chain_kind = models.IntegerField(default=0, blank=True, choices=CHAIN)

    class Meta:
        db_table = "tcgcreator_triggertimingmonsterchangeval"

class TriggerTimingChangeVal(models.Model):
    def __str__(self):
        return self.trigger_timing_name

    trigger = models.ForeignKey(
        "Trigger", default=None, null=True, blank=True, on_delete=models.SET_NULL
    )
    kinds = models.CharField(max_length=32, blank=True)
    monster = models.ManyToManyField("Monster", blank=True)
    monster_specify_flag = models.BooleanField(blank=True, default=True)
    who = models.IntegerField(choices=TRIGGER_WHO2, default=0)
    chain_user = models.IntegerField(choices=MINE_OR_OTHER3, default=0)
    cost_or_effect = models.IntegerField(choices=COST_OR_EFFECT, blank=True)
    trigger_timing_name = models.CharField(max_length=32)
    change_val = models.IntegerField(default=0)
    change_val_operator = models.CharField(max_length=32, blank=True)
    org = models.BooleanField(default=True)
    relation = models.BooleanField(default=False)
    relation_kind = models.CharField(max_length=32, blank=True)
    relation_name = models.CharField(max_length=32, blank=True)
    relation_to = models.BooleanField(default=False, blank=True)
    org_flag = models.BooleanField(default=False, blank=True)
    monster_exist = models.ManyToManyField(
        "Monster", related_name="monster_exist_trigger_timing_monster_change_val", blank=True
    )
    monster_exist_specify_flag = models.BooleanField(blank=True, default=False)
    exist_place_kind = models.IntegerField(choices=PLACE_KIND, default=0)
    exist_deck = models.ForeignKey(
        "Deck",
        default=None,
        null=True,
        related_name="exist_deck_change_val",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exist_grave = models.ForeignKey(
        "Grave",
        default=None,
        null=True,
        related_name="exist_grave_change_val",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exist_hand = models.ForeignKey(
        "Hand",
        default=None,
        null=True,
        related_name="exist_hand_change_val",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exist_field = models.ForeignKey(
        "FieldKind",
        default=None,
        null=True,
        related_name="exist_field_kind_change_val",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exist_kinds = models.CharField(max_length=32, blank=True)
    exist_mine_or_other = models.IntegerField(choices=MINE_OR_OTHER3, default=0)
    which_monster_effect = models.IntegerField(choices = WHO,default = 0)
    once_per_turn_relate = models.BooleanField(default=False,blank=True)
    once_per_turn_exist = models.BooleanField(default=False,blank=True)
    enemy = models.IntegerField(choices = ENEMY,default =1)
    enemy_own = models.IntegerField(choices = ENEMY,default =1)
    chain = models.IntegerField(default=0, blank=True)
    chain_kind = models.IntegerField(default=0, blank=True, choices=CHAIN)

    class Meta:
        db_table = "tcgcreator_triggertimingchangeval"


class TriggerTiming(models.Model):
    def __str__(self):
        return self.trigger_timing_name

    trigger = models.ForeignKey(
        "Trigger", default=None, null=True, blank=True, on_delete=models.SET_NULL
    )
    win_or_lose = models.IntegerField(default=0, choices=WIN_OR_LOSE)
    kinds = models.CharField(max_length=32, blank=True)
    from_place_kind = models.IntegerField(choices=PLACE_KIND, default=0)
    from_deck = models.ForeignKey(
        "Deck",
        default=None,
        null=True,
        related_name="from_deck",
        blank=True,
        on_delete=models.SET_NULL,
    )
    from_grave = models.ForeignKey(
        "Grave",
        default=None,
        null=True,
        related_name="from_grave",
        blank=True,
        on_delete=models.SET_NULL,
    )
    from_hand = models.ForeignKey(
        "Hand",
        default=None,
        null=True,
        related_name="from_hand",
        blank=True,
        on_delete=models.SET_NULL,
    )
    from_field = models.ForeignKey(
        "FieldKind",
        default=None,
        null=True,
        related_name="from_field_kind",
        blank=True,
        on_delete=models.SET_NULL,
    )
    from_mine_or_other = models.IntegerField(choices=MINE_OR_OTHER3)
    exclude_from_place_kind = models.IntegerField(choices=PLACE_KIND, default=0)
    exclude_from_deck = models.ForeignKey(
        "Deck",
        default=None,
        null=True,
        related_name="exclude_from_deck",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exclude_from_grave = models.ForeignKey(
        "Grave",
        default=None,
        null=True,
        related_name="exclude_from_grave",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exclude_from_hand = models.ForeignKey(
        "Hand",
        default=None,
        null=True,
        related_name="exclude_from_hand",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exclude_from_field = models.ForeignKey(
        "FieldKind",
        default=None,
        null=True,
        related_name="exclude_from_field_kind",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exclude_from_mine_or_other = models.IntegerField(choices=MINE_OR_OTHER3, default=0)
    to_place_kind = models.IntegerField(choices=PLACE_KIND, default=0)
    to_deck = models.ForeignKey(
        "Deck",
        default=None,
        null=True,
        related_name="to_deck",
        blank=True,
        on_delete=models.SET_NULL,
    )
    to_grave = models.ForeignKey(
        "Grave",
        default=None,
        null=True,
        related_name="to_grave",
        blank=True,
        on_delete=models.SET_NULL,
    )
    to_hand = models.ForeignKey(
        "Hand",
        default=None,
        null=True,
        related_name="to_hand",
        blank=True,
        on_delete=models.SET_NULL,
    )
    to_field = models.ForeignKey(
        "FieldKind",
        default=None,
        null=True,
        related_name="to_field_kind",
        blank=True,
        on_delete=models.SET_NULL,
    )
    to_mine_or_other = models.IntegerField(choices=MINE_OR_OTHER3)
    exclude_to_place_kind = models.IntegerField(choices=PLACE_KIND, default=0)
    exclude_to_deck = models.ForeignKey(
        "Deck",
        default=None,
        null=True,
        related_name="exclude_to_deck",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exclude_to_grave = models.ForeignKey(
        "Grave",
        default=None,
        null=True,
        related_name="exclude_to_grave",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exclude_to_hand = models.ForeignKey(
        "Hand",
        default=None,
        null=True,
        related_name="exclude_to_hand",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exclude_to_field = models.ForeignKey(
        "FieldKind",
        default=None,
        null=True,
        related_name="exclude_to_field_kind",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exclude_to_mine_or_other = models.IntegerField(choices=MINE_OR_OTHER3, default=0)
    monster = models.ManyToManyField("Monster", blank=True)
    monster_specify_flag = models.BooleanField(blank=True, default=True)
    monster_relate = models.ManyToManyField(
        "Monster", related_name="monster_relate_exist", blank=True
    )
    monster_relate_specify_flag = models.BooleanField(blank=True, default=False)
    monster_relate_except = models.ManyToManyField(
        "Monster", related_name="monster_relate_except", blank=True
    )
    monster_relate_except_flag = models.BooleanField(blank=True, default=False)
    monster_exist = models.ManyToManyField(
        "Monster", related_name="monster_exist_trigger_timing", blank=True
    )
    monster_exist_specify_flag = models.BooleanField(blank=True, default=False)
    exist_place_kind = models.IntegerField(choices=PLACE_KIND, default=0)
    exist_deck = models.ForeignKey(
        "Deck",
        default=None,
        null=True,
        related_name="exist_deck",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exist_grave = models.ForeignKey(
        "Grave",
        default=None,
        null=True,
        related_name="exist_grave",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exist_hand = models.ForeignKey(
        "Hand",
        default=None,
        null=True,
        related_name="exist_hand",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exist_field = models.ForeignKey(
        "FieldKind",
        default=None,
        null=True,
        related_name="exist_field_kind",
        blank=True,
        on_delete=models.SET_NULL,
    )
    exist_kinds = models.CharField(max_length=32, blank=True)
    exist_mine_or_other = models.IntegerField(choices=MINE_OR_OTHER3, default=0)
    who = models.IntegerField(choices=TRIGGER_WHO, default=0)
    chain_user = models.IntegerField(choices=MINE_OR_OTHER3, default=0)
    cost_or_effect = models.IntegerField(choices=COST_OR_EFFECT)
    trigger_timing_name = models.CharField(max_length=32)
    relation = models.BooleanField(default=False)
    # relation_monster = models.ManyToManyField("Monster",related_name = "relation_monster_trigger_timing",blank=True)
    # relation_monster_specify_flag = models.BooleanField(blank=True,default=False)
    relation2 = models.BooleanField(default=False)
    relation_kind = models.CharField(max_length=32, blank=True)
    relation_name = models.CharField(max_length=32, blank=True)
    relation_to = models.BooleanField(default=False, blank=True)
    org_flag = models.BooleanField(default=False, blank=True)
    which_monster_effect = models.IntegerField(choices = WHO,default = 0)
    once_per_turn_relate = models.BooleanField(default=False,blank=True)
    once_per_turn_exist = models.BooleanField(default=False,blank=True)
    enemy = models.IntegerField(choices = ENEMY,default =1)
    enemy_own = models.IntegerField(choices = ENEMY,default =1)
    chain = models.IntegerField(default=0, blank=True)
    chain_kind = models.IntegerField(default=0, blank=True, choices=CHAIN)

    class Meta:
        db_table = "tcgcreator_triggertiming"


class Trigger(models.Model):
    mine_or_other = models.IntegerField(choices=MINE_OR_OTHER, default=1)
    priority = models.IntegerField(default="100")
    storategy_priority = models.IntegerField(default="100")
    turn = models.IntegerField(choices=MINE_OR_OTHER)
    phase = models.ManyToManyField(
        "Phase", default=None, blank=True, related_name="phases"
    )
    chain = models.IntegerField(default=0, blank=True)
    chain_kind = models.IntegerField(default=0, blank=True, choices=CHAIN)
    no_chain = models.BooleanField(default=False)
    force = models.BooleanField(default=False)
    pac = models.ForeignKey(
        "PacWrapper", default=None, blank=True, null=True, on_delete=models.SET_NULL
    )
    next_effect = models.ForeignKey(
        "MonsterEffectWrapper",
        default=None,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    trigger_condition = models.TextField(default="", blank=True)
    trigger_timing = models.BooleanField(default=False,blank=True)
    trigger_monster = models.TextField(default=None, null=True, blank=True)
    trigger_deck = models.ManyToManyField("Deck", default=None, blank=True, null=True)
    trigger_grave = models.ManyToManyField("Grave", default=None, blank=True, null=True)
    trigger_hand = models.ManyToManyField("Hand", default=None, blank=True, null=True)
    trigger_field = models.ManyToManyField("FieldKind", default=None, blank=True, null=True)
    trigger_none_monster = models.BooleanField(default=False)
    trigger_name = models.CharField(max_length=32, default=None, null=True)
    trigger_sentence = models.CharField(
        max_length=32, default=None, null=True, blank=True
    )
    trigger_prompt = models.CharField(max_length=256, default="", blank=True)
    trigger_cost = models.ForeignKey(
        "CostWrapper", default=None, null=True, blank=True, on_delete=models.SET_NULL
    )
    trigger_cost_pac = models.ForeignKey(
        "PacCostWrapper", default=None, blank=True, null=True, on_delete=models.SET_NULL
    )
    trigger_kind = models.CharField(max_length=32, default="", blank=True)
    timing = models.ManyToManyField(Timing, default=None, blank=True, null=True)
    timing2 = models.ManyToManyField(Timing, default=None, blank=True, null=True,related_name="trigger_timing2")
    timing3 = models.ManyToManyField(Timing, default=None, blank=True, null=True,related_name="trigger_timing3")
    timing_trigger = models.BooleanField(default=False)
    none_timing = models.BooleanField(default=True)
    none_timing2 = models.BooleanField(default=True)
    none_timing3 = models.BooleanField(default=True)
    log = models.TextField(default="", blank=True)
    chain_mine_or_other = models.IntegerField(
        default=0, blank=True, choices=MINE_OR_OTHER
    )
    can_chain_kind = models.CharField(default="", blank=True, max_length=32)
    copy = models.BooleanField(default=True)
    copy2 = models.BooleanField(default=False)
    copy3 = models.BooleanField(default=False)
    canbetwice = models.BooleanField(default=True)
    monstercanbetwice = models.BooleanField(default=True)
    existcanbetwice = models.BooleanField(default=True)
    canbechained = models.BooleanField(default=True)
    none_exist = models.BooleanField(default=False,blank=True)
    once_per_turn = models.BooleanField(default=False,blank=True)
    once_per_duel = models.BooleanField(default=False,blank=True)
    once_per_turn_monster = models.BooleanField(default=False,blank=True)
    once_per_turn_group = models.IntegerField(default=0,blank=True)
    once_per_turn_monster_group = models.IntegerField(default=0,blank=True)
    enemy = models.IntegerField(choices = ENEMY,default =1)
    enemy_own = models.IntegerField(choices = ENEMY,default =1)
    strategy = models.CharField(max_length=32,blank=True,default="")
    strategy_up_or_down = models.IntegerField(choices = UP_OR_DOWN,default=0)
    immidiate_flag = models.BooleanField(default=False, blank=True)
    chain_flag = models.BooleanField(default=True, blank=True)
    fusion_monster = models.TextField(blank=True,default="")
    instead_condition = models.TextField(blank=True,default="")
    fusion_flag = models.BooleanField(default=False, null=True)
    fusion1 = models.TextField(blank=True,default="")
    instead1 = models.TextField(blank=True,default="")
    fusion2 = models.TextField(blank=True,default="")
    instead2 = models.TextField(blank=True,default="")
    fusion3 = models.TextField(blank=True,default="")
    instead3 = models.TextField(blank=True,default="")
    def __str__(self):
        return self.trigger_name


    class Meta:
        db_table = "tcgcreator_trigger"


class FieldSize(models.Model):
    field_x = models.IntegerField()
    field_y = models.IntegerField()

    class Meta:
        db_table = "tcgcreator_fieldsize"


# Create your models here.
MINE_OR_OTHER2 = ((0, "特になし"), (1, "共通"))
SHOW = ((0, "表示しない"), (1, "自分のみ"), (2, "両方"),(3,"表のみ"),(4,"自分または表のみ"),(5,"全く表示しない"))
MONSTER_VARIABLE_SHOn = ((0, "表示しない"), (1, "表示"), (2, "0以外表示"))
SHOW2 = ((0, "表示しない"), (1, "表示"))
ETERNAL_EFFECT_VAL = (
    (0, "無効化 効果を受けない"),
    (1, "数値変動"),
    (3, "選択できない"),
    (2, "発動できない"),
    (4, "行き先変更"),
    (5, "逆転"),
    (8, "逆転元々"),
    (6, "条件無視"),
    (7, "代わりに受ける"),
    (8, "名前変更"),
    (9, "名前追加"),
)
ETERNAL_EFFECT_VAL2 = (
    (0, "永続無効化"),
    (1, "発動効果無効化"),
    (2, "無効化"),
    (3, "効果を受けない"),
    (4, "無効化　発動できない"),
)
MONSTER_EFFECT_VAL = (
    (0, "条件"),
    (53, "軽減変数条件"),
    (43, "チェーン条件"),
    (41, "タイミングフェイズ条件"),
    (39, "無効"),
    (1, "移動"),
    (82, "選択移動"),
    (76, "融合選択"),
    (77, "融合素材"),
    (78, "融合固有効果"),
    (83, "融合条件"),
    (51, "移動under"),
    # リレーション先を移動させる
    (40, "移動リレーション"),
    (36, "下に重ねる"),
    (50, "上に重ねる"),
    (17, "シンプル移動"),
    (72, "トークン生成"),
    (73, "カード消去"),
    (2, "変数変動"),
    (54, "変数変動順番"),
    (55, "変数変動順番相手"),
    (49, "変数軽減"),
    (52, "変数変動flush"),
    (34, "変数変動byモンスター"),
    (29, "変数変動複数"),
    (80, "変数表示変更"),
    (9, "モンスター変数変動"),
    (32, "モンスター変数変動リレーション"),
    (25, "モンスターリレーション"),
    (70, "モンスターリレーション付け替え"),
    (38, "モンスターリレーションクリア"),
    (33, "モンスターリレーション全部クリア"),
    (35, "モンスターコピー"),
    (71, "モンスターコピーモンスター指定"),
    (37, "効果コピー"),
    (46, "効果コピー2"),
    (48, "効果コピー(コスト)"),
    (3, "選択自分"),
    (57, "選択自分as"),
    (65, "選択自分as_under"),
    (44, "選択リライト自分"),
    (4, "選択相手"),
    (5, "選択両者"),
    (56, "選択クリア"),
    (58, "選択リロード(非推奨)"),
    (69, "選択リロードnew"),
    (81, "選択割り振り"),
    (7, "フェイズ移動"),
    (8, "ターンエンド"),
    (10, "シャッフル"),
    (11, "フラグクリア"),
    (12, "レイズ"),
    (13, "優先権移行"),
    (14, "タイミング移行"),
    (19, "タイミング次に移行"),
    (24, "永続レイズ"),
    (45, "コイントス"),
    (79, "ランダム分岐"),
    (16, "Yes Or No"),
    (26, "Yes Or No相手"),
    (66, "分岐複数"),
    (67, "分岐複数相手"),
    (18, "タイミング 変数移動"),
    (27, "チェーン変数設定"),
    (28, "チェーン変数設定相手"),
    (63, "グローバル変数設定"),
    (64, "グローバル変数設定相手"),
    (30, "多対多"),
    (31, "多対多相手"),
    (61, "優先権操作"),
    (59, "強制発現"),
    (42, "ミュート"),
    (21, "音楽鳴らす"),
    (60, "効果音鳴らす"),
    (20, "キャンセル"),
    (22, "勝利"),
    (23, "敗北"),
    (47, "引き分け`"),
    (62, "each"),
    (68, "コスト実行"),
    (74, "永続リセット"),
    (6, "コメント"),
)
ASK = ((0, "なし"), (1, "ターンプレイヤー"), (2, "非ターンプレイヤー"), (3, "両者"))


class Phase(models.Model):
    priority = models.IntegerField(unique=True)
    phase_name = models.CharField(max_length=32, default="")
    show = models.IntegerField(default=1, choices=SHOW2)
    phase_whether_show = models.BooleanField(default=False)
    pri = models.BooleanField(default=True)

    def __str__(self):
        return self.phase_name

    class Meta:
        db_table = "tcgcreator_phase"


class Background(models.Model):

    background_name = models.CharField(max_length=32, default="")
    file_name = models.CharField(max_length=32, default="")
    font_color=models.CharField(max_length=32,default="black",blank=True);
    def __str__(self):
        return self.background_name
    class Meta:
        db_table = "tcgcreator_background"
class DuelDeck(models.Model):
    room_number = models.IntegerField()
    mine_or_other = models.IntegerField(choices=MINE_OR_OTHER)
    deck_id = models.IntegerField()
    deck_name = models.CharField(max_length=32, default="")
    deck_content = models.TextField(blank=True)

    class Meta:
        db_table = "tcgcreator_dueldeck"


class DuelGrave(models.Model):
    room_number = models.IntegerField()
    mine_or_other = models.IntegerField(choices=MINE_OR_OTHER)
    grave_id = models.IntegerField()
    grave_name = models.CharField(max_length=32, default="")
    deck_content = models.TextField(blank=True)
    grave_content = models.TextField(blank=True)

    class Meta:
        db_table = "tcgcreator_duelgrave"


class DuelHand(models.Model):
    room_number = models.IntegerField()
    mine_or_other = models.IntegerField(choices=MINE_OR_OTHER)
    hand_id = models.IntegerField()
    hand_name = models.CharField(max_length=32, default="")
    hand_content = models.TextField(blank=True)

    class Meta:
        db_table = "tcgcreator_duelhand"


class Deck(models.Model):
    mine_or_other = models.IntegerField(choices=MINE_OR_OTHER2)
    min_deck_size = models.IntegerField()
    max_deck_size = models.IntegerField()
    deck_name = models.CharField(max_length=32, default="")
    show = models.IntegerField(choices=SHOW)
    makedeckshow = models.BooleanField(default=True)
    persist = models.BooleanField(default = True)
    token = models.BooleanField(default = True)
    priority = models.IntegerField(default=100)
    invoke = models.BooleanField(default=True)
    eternal = models.BooleanField(default=True)

    def __str__(self):
        return self.deck_name

    class Meta:
        db_table = "tcgcreator_deck"


class UserPoint(models.Model):
    user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="tcgcreatoruserpoint"
    )
    win = models.IntegerField( default = 0)
    win_ai = models.IntegerField( default = 0)
    lose = models.IntegerField(default = 0)
    point = models.IntegerField(default = 0)
    draw = models.IntegerField(default = 0)
    class Meta:
        db_table = "tcgcreator_userpoint"
class UserDeckGroup(models.Model):
    user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="tcgcreatorusergroup"
    )
    deck_name = models.TextField(default="デッキ")
    user_deck_id = models.IntegerField()

    class Meta:
        db_table = "tcgcreator_userdeckgroup"


class EnemyDeckChoice(models.Model):
    enemy_deck = models.ForeignKey(
        "EnemyDeckGroup", default="1", null=True, on_delete=models.SET_NULL
    )

    class Meta:
        db_table = "tcgcreator_enemydeckchoice"

class EnemyDeckGroup(models.Model):
    deck_name = models.TextField(default="デッキ")
    enemy_deck_id = models.IntegerField()

    class Meta:
        db_table = "tcgcreator_enemydeckgroup"

class DefaultDeckGroup(models.Model):
    deck_name = models.TextField(default="デッキ")
    default_deck_id = models.IntegerField()

    class Meta:
        db_table = "tcgcreator_defaultdeckgroup"


class UserDeck(models.Model):
    user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="tcgcreatoruserdeck"
    )
    deck_type = models.ForeignKey(Deck, null=True, on_delete=models.SET_NULL)
    deck_group = models.ForeignKey(UserDeckGroup, null=True, on_delete=models.SET_NULL)
    deck = models.TextField(blank=True)

    class Meta:
        db_table = "tcgcreator_userdeck"


class EnemyDeck(models.Model):
    deck = models.TextField( blank=True)
    deck_type = models.ForeignKey(Deck, null=True, on_delete=models.SET_NULL)
    deck_group = models.ForeignKey(
        EnemyDeckGroup, default="1", null=True, on_delete=models.SET_NULL
    )

    class Meta:
        db_table = "tcgcreator_enemydeck"

class DefaultDeck(models.Model):
    deck = models.TextField(blank=True)
    deck_type = models.ForeignKey(Deck, null=True, on_delete=models.SET_NULL)
    deck_group = models.ForeignKey(
        DefaultDeckGroup, default="1", null=True, on_delete=models.SET_NULL
    )

    class Meta:
        db_table = "tcgcreator_defaultdeck"


class DefaultDeckChoice(models.Model):
    default_deck = models.ForeignKey(
        DefaultDeckGroup, default="1", null=True, on_delete=models.SET_NULL
    )

    class Meta:
        db_table = "tcgcreator_defaultdeckchoice"


class UserDeckChoice(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, related_name="tcgcreatoruserdeckchoice"
    )
    user_deck = models.ForeignKey(UserDeckGroup, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "tcgcreator_userdeckchoice"


class Grave(models.Model):
    mine_or_other = models.IntegerField(choices=MINE_OR_OTHER2)
    show = models.IntegerField(default=0, choices=SHOW)
    grave_name = models.CharField(max_length=32, default="")
    persist = models.BooleanField(default = True)
    token = models.BooleanField(default = True)
    priority = models.IntegerField(default=100)
    invoke = models.BooleanField(default=True)
    eternal = models.BooleanField(default=True)

    def __str__(self):
        return self.grave_name

    class Meta:
        db_table = "tcgcreator_usergrave"


class Hand(models.Model):
    mine_or_other = models.IntegerField(choices=MINE_OR_OTHER2)
    show = models.IntegerField(default=0, choices=SHOW)
    hand_name = models.CharField(max_length=32, default="")
    persist = models.BooleanField(default = True)
    token = models.BooleanField(default = True)
    invoke = models.BooleanField(default=True)
    eternal = models.BooleanField(default=True)

    def __str__(self):
        return self.hand_name

    class Meta:
        db_table = "tcgcreator_userhand"


class Field(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    no_clear = models.BooleanField(default=False)
    box = models.BooleanField(default=True)
    color = models.CharField(max_length=32, blank=True,default="")
    kind = models.CharField(max_length=32, blank=True)
    sentence = models.CharField(max_length=32, blank=True,default="")
    mine_or_other = models.IntegerField(choices=MINE_OR_OTHER)

    class Meta:
        db_table = "tcgcreator_field"


class MonsterVariablesKind(models.Model):
    monster_variable_sentence = models.TextField(null=True)
    monster_variable_name = models.CharField(max_length=32, null=True)

    def __str__(self):
        return self.monster_variable_name

    class Meta:
        db_table = "tcgcreator_monstervariablekind"


class MonsterVariables(models.Model):
    monster_variable_name = models.CharField(max_length=32)
    monster_variable_label = models.CharField(max_length=32)
    monster_variable_kind_id = models.ForeignKey(
        MonsterVariablesKind,
        related_name="monster_variable_kind_id",
        on_delete=models.CASCADE,
    )
    monster_variable_minus = models.BooleanField(default=False)
    monster_variable_show = models.IntegerField(default=0)
    monster_variable_show2 = models.IntegerField(default=0)
    monster_variable_show_battle = models.IntegerField(default=1)
    priority = models.IntegerField()
    default_value = models.CharField(max_length=32)

    def __str__(self):
        return self.monster_variable_name

    class Meta:
        db_table = "tcgcreator_monstervariables"




class Monster(models.Model):
    monster_name = models.CharField(max_length=32)
    monster_sentence = models.TextField(default="", blank=True)
    monster_limit = models.IntegerField(default=2)
    monster_deck = models.CharField(max_length=32, default="1")
    monster_variable = models.ManyToManyField(MonsterVariables, through="MonsterItem")
    trigger = models.ManyToManyField(Trigger, blank=True)
    eternal_effect = models.ManyToManyField("EternalEffect", blank=True)
    img = models.CharField(max_length=32, default="", blank=True)
    instead_img = models.CharField(max_length=32, default="", blank=True)
    token_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.monster_name

    class Meta:
        db_table = "tcgcreator_monster"


class MonsterItem(models.Model):
    monster_id = models.ForeignKey(
        Monster, related_name="monster_item", on_delete=models.CASCADE
    )
    monster_variables_id = models.ForeignKey(MonsterVariables, on_delete=models.CASCADE)
    monster_item_text = models.CharField(max_length=32, null=True)

    class Meta:
        db_table = "tcgcreator_monsteritem"


class FieldKind(models.Model):
    field_kind_name = models.CharField(max_length=32)
    mine_or_other = models.IntegerField(default=0, choices=MINE_OR_OTHER2)

    def __str__(self):
        return self.field_kind_name

    class Meta:
        db_table = "tcgcreator_fieldkind"


class GlobalVariable(models.Model):
    variable_name = models.CharField(max_length=32)
    priority = models.IntegerField(default=100)
    show = models.IntegerField(default=1, choices=SHOW2)
    initial_value = models.IntegerField(default=0)
    mine_or_other = models.IntegerField(default=0, choices=MINE_OR_OTHER2)
    center = models.BooleanField(default=False)
    font_size=models.CharField(max_length=32,default="16",blank=True);

    def __str__(self):
        return self.variable_name

    class Meta:
        db_table = "tcgcreator_globalvariable"


class VirtualVariable(models.Model):
    variable_name = models.CharField(max_length=32)
    priority = models.IntegerField(default=100)
    show = models.IntegerField(default=1, choices=SHOW2)
    value = models.TextField(default="")
    mine_or_other = models.IntegerField(default=0, choices=MINE_OR_OTHER2)
    center = models.BooleanField(default=False)
    font_size=models.CharField(max_length=32,default="16",blank=True);

    def __str__(self):
        return self.variable_name

    class Meta:
        db_table = "tcgcreator_virtualvariable"


class SpecialCard(models.Model):
    special_card_name = models.CharField(max_length=32)
    special_card = models.ManyToManyField(Monster,blank=True)
    constraint = models.ManyToManyField("Constraint",blank = True)
    deck = models.ManyToManyField(Deck,blank=True,related_name="special_deck")
    min_deck_size = models.IntegerField(blank=True)
    max_deck_size = models.IntegerField(blank=True)
    

    def __str__(self):
        return self.special_card_name

    class Meta:
        db_table = "tcgcreator_specialcard"
class MonsterEffectKind(models.Model):
    monster_effect_name = models.CharField(max_length=32)
    monster_effect_show=models.BooleanField(default=False,blank=True);

    def __str__(self):
        return self.monster_effect_name

    class Meta:
        db_table = "tcgcreator_monstereffectkind"


class MonsterEffect(models.Model):
    monster_effect_val = models.IntegerField(choices=MONSTER_EFFECT_VAL)
    monster_effect = models.TextField(blank=True)
    monster_condition = models.TextField(blank=True)
    prompt = models.TextField(blank=True)
    sentence = models.CharField(max_length=32, blank=True, default="")
    monster_effect_name = models.CharField(default="", max_length=32)
    eternal_flag = models.BooleanField(default=False)
    change_val_monster_flag = models.BooleanField(default=False)
    accumulate_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.monster_effect_name

    class Meta:
        db_table = "tcgcreator_monstereffect"


class PacCostWrapper(models.Model):
    cost_next = models.ForeignKey(
        "CostWrapper",
        related_name="%(class)s_cost_next",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    cost_next2 = models.ForeignKey(
        "CostWrapper",
        related_name="%(class)s_cost_next2",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    pac_next = models.ForeignKey(
        "PacCostWrapper",
        related_name="%(class)s_pac_cost_next",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
    )
    pac_next2 = models.ForeignKey(
        "PacCostWrapper",
        related_name="%(class)s_pac_cost_next2",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
    )
    monster_effect_kind = models.CharField(max_length=32, blank=True)
    monster_effect_kind_rel = models.CharField(max_length=32, blank=True)
    pac_cost = models.ForeignKey(
        "PacCost", related_name="PacCost", on_delete=models.CASCADE
    )
    pac_cost_name = models.CharField(default="", max_length=32)
    log = models.TextField(default="", blank=True)

    def __str__(self):
        return self.pac_cost_name

    class Meta:
        db_table = "tcgcreator_paccostwrapper"


class PacCost(models.Model):
    pac_cost_next = models.ForeignKey(
        "CostWrapper",
        null=True,
        blank=True,
        related_name="%(class)s_pac_cost_next",
        on_delete=models.SET_NULL,
    )
    pac_cost_name = models.CharField(default="", max_length=32)

    def __str__(self):
        return self.pac_cost_name

    class Meta:
        db_table = "tcgcreator_paccost"


class PacWrapper(models.Model):
    monster_effect_next = models.ForeignKey(
        "MonsterEffectWrapper",
        related_name="%(class)s_monster_effect_next",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    monster_effect_next2 = models.ForeignKey(
        "MonsterEffectWrapper",
        related_name="%(class)s_monster_effect_next2",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    pac_next = models.ForeignKey(
        "PacWrapper",
        related_name="%(class)s_pac_cost_next",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
    )
    pac_next2 = models.ForeignKey(
        "PacWrapper",
        related_name="%(class)s_pac_cost_next2",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
    )
    monster_effect_kind = models.CharField(max_length=32, blank=True)
    monster_effect_kind_rel = models.CharField(max_length=32, blank=True)
    pac = models.ForeignKey("Pac", related_name="Pac", on_delete=models.CASCADE)
    pac_name = models.CharField(default="", max_length=32)
    log = models.TextField(default="", blank=True)

    def __str__(self):
        return self.pac_name

    class Meta:
        db_table = "tcgcreator_pacwrapper"


class Pac(models.Model):
    pac_next = models.ForeignKey(
        "MonsterEffectWrapper",
        null=True,
        blank=True,
        related_name="%(class)s_pac_next",
        on_delete=models.SET_NULL,
    )
    pac_name = models.CharField(default="", max_length=32)

    def __str__(self):
        return self.pac_name

    class Meta:
        db_table = "tcgcreator_pac"


class EndChainEffect(models.Model):
    priority = models.IntegerField(default="100")
    monster_effect = models.ForeignKey(
        MonsterEffect, related_name="endchain_wrapper", on_delete=models.CASCADE
    )
    monster_effect_kind = models.CharField(max_length=32, blank=True)
    monster_effect_next = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL
    )
    monster_effect_next2 = models.ForeignKey(
        "self",
        related_name="%(class)s_monster_effect_next2",
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    monster_effect_name = models.CharField(default="", max_length=32)
    log = models.TextField(default="", blank=True)
    none_timing = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.monster_effect_name

    class Meta:
        db_table = "tcgcreator_endchainwrapper"

class EternalWrapper(models.Model):
    priority = models.IntegerField(default="100")
    monster_effect = models.ForeignKey(
        MonsterEffect, related_name="eternal_wrapper", on_delete=models.CASCADE
    )
    monster_effect_kind = models.CharField(max_length=32, blank=True)
    monster_effect_next = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL
    )
    monster_effect_next2 = models.ForeignKey(
        "self",
        related_name="%(class)s_monster_effect_next2",
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    monster_effect_name = models.CharField(default="", max_length=32)
    log = models.TextField(default="", blank=True)
    none_timing = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.monster_effect_name

    class Meta:
        db_table = "tcgcreator_eternalwrapper"


class MonsterEffectWrapper(models.Model):
    monster_effect = models.ForeignKey(
        MonsterEffect, related_name="monster_effect_wrapper", on_delete=models.CASCADE
    )
    monster_effect_kind = models.CharField(max_length=32, blank=True)
    monster_effect_kind_rel = models.CharField(max_length=32, blank=True)
    monster_effect_next = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL
    )
    monster_effect_next2 = models.ForeignKey(
        "self",
        related_name="%(class)s_monster_effect_next2",
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    pac = models.ForeignKey(
        PacWrapper,
        null=True,
        blank=True,
        related_name="%(class)s_pac",
        on_delete=models.SET_NULL,
    )
    pac2 = models.ForeignKey(
        PacWrapper,
        related_name="%(class)s_pac2",
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    monster_effect_name = models.CharField(default="", max_length=32)
    log = models.TextField(default="", blank=True)
    prompt = models.TextField(blank=True)
    sentence = models.CharField(max_length=32, blank=True, default="")
    if_not_to_2 = models.BooleanField(blank=True,default=False)
    strategy = models.CharField(max_length=32,blank=True,default="")
    strategy_up_or_down = models.IntegerField(choices = UP_OR_DOWN,default=0)
    effect = models.TextField(blank=True,default="")
    fusion_flag = models.BooleanField(blank=True,default=False)

    def __str__(self):
        return self.monster_effect_name

    class Meta:
        db_table = "tcgcreator_monstereffectwrapper"


class EternalTrigger(models.Model):
    priority = models.IntegerField(default="100")
    turn = models.IntegerField(choices=MINE_OR_OTHER)
    chain = models.IntegerField(default=0, blank=True, null=True)
    chain_kind = models.IntegerField(default=0, blank=True, choices=CHAIN)
    phase = models.ForeignKey(
        "Phase", default=None, blank=True, null=True, on_delete=models.SET_NULL
    )
    timing = models.ManyToManyField(Timing, default=None, blank=True, null=True)
    timing2 = models.ManyToManyField(Timing, default=None, blank=True, null=True,related_name="eternal_timing2")
    timing3 = models.ManyToManyField(Timing, default=None, blank=True, null=True,related_name="eternal_timing3")
    none_timing = models.BooleanField(default=True)
    none_timing2 = models.BooleanField(default=True)
    none_timing3 = models.BooleanField(default=True)
    eternal_effect_next = models.ForeignKey(
        EternalWrapper, default=None, blank=True, null=True, on_delete=models.SET_NULL
    )
    eternal_name = models.CharField(max_length=32, default=None, null=True)
    enemy = models.IntegerField(choices = ENEMY,default =0)
    enemy_own = models.IntegerField(choices = ENEMY,default =1)

    def __str__(self):
        return self.eternal_name

    class Meta:
        db_table = "tcgcreator_eternaltrigger"


class EternalEffect(models.Model):
    eternal_effect_val = models.IntegerField(choices=ETERNAL_EFFECT_VAL, default=0)
    eternal_effect_val2 = models.IntegerField(choices=ETERNAL_EFFECT_VAL2, default=0)
    priority = models.IntegerField(default="100")
    turn = models.IntegerField(choices=MINE_OR_OTHER)
    chain = models.IntegerField(default=0, blank=True, null=True)
    chain_kind = models.IntegerField(default=0, blank=True, choices=CHAIN)
    phase = models.ManyToManyField(
        "Phase", default=None, blank=True, null=True
    )
    mine_or_other = models.IntegerField(choices=MINE_OR_OTHER, default=0)
    mine_or_other_effect = models.IntegerField(choices=MINE_OR_OTHER, default=0)
    eternal_effect_condition = models.TextField(default="", blank=True)
    eternal_monster = models.TextField(default=None, null=True, blank=True)
    eternal_deck = models.ManyToManyField("Deck", default=None, blank=True, null=True)
    eternal_grave = models.ManyToManyField("Grave", default=None, blank=True, null=True)
    eternal_hand = models.ManyToManyField("Hand", default=None, blank=True, null=True)
    eternal_field = models.ManyToManyField("FieldKind", default=None, blank=True, null=True)
    eternal_global_variable = models.TextField(default=None, null=True, blank=True)
    eternal_global_variable_val = models.CharField(
        max_length=32, default=None, null=True, blank=True
    )
    eternal_variable = models.CharField(max_length=32, default="", blank=True)
    eternal_variable_val = models.IntegerField(default=0, null=True, blank=True)
    eternal_variable_equation = models.IntegerField(default=0, null=True, blank=True,choices=EQUATION)
    eternal_name = models.CharField(max_length=32, default=None, null=True, blank=False)
    eternal_kind = models.CharField(max_length=32, default="", blank=True)
    invalid_eternal_kind = models.CharField(max_length=32, default="-1", blank=True)
    invalid_monster = models.TextField(default="", blank=True)
    timing = models.ManyToManyField(Timing, default=None, blank=True, null=True)
    none_timing = models.BooleanField(default=True)
    timing2 = models.ManyToManyField(Timing, default=None, blank=True, null=True,related_name = "eternal_effect_timing2")
    none_timing2 = models.BooleanField(default=True)
    timing3 = models.ManyToManyField(Timing, default=None, blank=True, null=True,related_name = "eternal_effect_timing3")
    none_timing3 = models.BooleanField(default=True)
    none_monster = models.BooleanField(default=False)
    # 変数による永続効果
    # effect_val_eternal = models.BooleanField(default=False)
    invalid_none_monster = models.BooleanField(default=False)
    persist = models.BooleanField(default=False)
    relation = models.BooleanField(default=False)
    relation_kind = models.CharField(max_length=32, blank=True)
    relation_to = models.BooleanField(default=False)
    eternal_tmp_val = models.CharField(max_length=256, blank=True, default="")
    val_name = models.CharField(max_length=256, blank=True, default="")
    value = models.CharField(max_length=255, blank=True, default=0)
    cost_or_effect = models.IntegerField(choices=COST_OR_EFFECT, default=0)
    ignore = models.IntegerField(default=0, choices=ETERNAL_IGNORE)
    ignore_phase = models.ManyToManyField(
        Phase, default=None, blank=True, related_name="ignore_phase"
    )
    ignore_effect_kind = models.TextField(default="", blank=True)
    ignore_timing = models.ManyToManyField(
        Timing, default=None, blank=True, related_name="ignore_timing"
    )
    ignore_none_timing = models.BooleanField(default=False, blank=True)
    ignore_variable = models.ForeignKey(
        "GlobalVariable", default=None, blank=True, on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return self.eternal_name

    class Meta:
        db_table = "tcgcreator_eternaleffect"


class Cost(models.Model):
    cost_val = models.IntegerField(choices=MONSTER_EFFECT_VAL)
    cost = models.TextField(blank=True)
    cost_condition = models.TextField(default="", blank=True)
    cost_name = models.CharField(default="", max_length=32)
    # 対象を取るなど
    change_val_monster_flag = models.BooleanField(default=False)
    effect_flag = models.BooleanField(default=False, blank=True)
    prompt = models.TextField(blank=True)
    sentence = models.CharField(max_length=32, blank=True, default="")
    accumulate_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.cost_name

    class Meta:
        db_table = "tcgcreator_cost"


class CostWrapper(models.Model):
    cost = models.ForeignKey(
        Cost, related_name="cost_wrapper", on_delete=models.CASCADE
    )
    cost_kind = models.CharField(max_length=32, blank=True, default="")
    cost_kind_rel = models.CharField(max_length=32, blank=True, default="")
    cost_next = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL
    )
    cost_next2 = models.ForeignKey(
        "self",
        related_name="%(class)s_cost_next2",
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    pac = models.ForeignKey(
        "PacCostWrapper",
        null=True,
        blank=True,
        related_name="%(class)s_pac",
        on_delete=models.SET_NULL,
    )
    pac2 = models.ForeignKey(
        "PacCostWrapper",
        related_name="%(class)s_pac2",
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    cost_name = models.CharField(default="", max_length=32)
    log = models.TextField(default="", blank=True)
    prompt = models.TextField(blank=True)
    sentence = models.CharField(max_length=32, blank=True, default="")
    strategy = models.CharField(max_length=32,blank=True,default="")
    strategy_up_or_down = models.IntegerField(choices = UP_OR_DOWN,default=0)
    if_not_to_2 = models.BooleanField(blank=True,default=False)

    def __str__(self):
        return self.cost_name

    class Meta:
        db_table = "tcgcreator_costwrapper"


class Battle(models.Model):
    battle_number = models.IntegerField()
    attaker = models.CharField(max_length=32)

    class Meta:
        db_table = "tcgcreator_battle"


class Duel(models.Model):
    id = models.IntegerField(primary_key=True)
    user_deck1 = models.ForeignKey(
        UserDeckChoice, default=None, blank=True, null=True, on_delete=models.SET_NULL,related_name = "user_deck1"
    )
    user_deck2 = models.ForeignKey(
        UserDeckChoice, default=None, blank=True, null=True, on_delete=models.SET_NULL,related_name = "user_deck2"

    )
    default_deck1 = models.ForeignKey(
        DefaultDeckGroup, default=None, blank=True, null=True, on_delete=models.SET_NULL,related_name = "default_deck1"
    )
    default_deck2 = models.ForeignKey(
        DefaultDeckGroup, default=None, blank=True, null=True, on_delete=models.SET_NULL,related_name = "default_deck2"
    )
    ai_deck2 = models.ForeignKey(
        EnemyDeckChoice, default=None, blank=True, null=True, on_delete=models.SET_NULL,related_name = "enemy_deck2"

    )
    deck_choose_flag1 = models.BooleanField(default = False)
    deck_choose_flag2 = models.BooleanField(default = False)
    field = models.TextField(blank=True)
    turn_count = models.IntegerField(default=0)
    ask = models.IntegerField(default=0, choices=ASK)
    ask2 = models.IntegerField(default=0, choices=ASK)
    retrieve = models.IntegerField(default=0, choices=ASK)
    ask_kind = models.CharField(max_length=32, blank=True, default="")
    asked = models.IntegerField(blank=True, default=0)
    ask_det = models.TextField(default="", blank=True)
    answer = models.TextField(default="", blank=True)
    user_turn = models.IntegerField(default=0)
    phase = models.ForeignKey(
        Phase, default=None, blank=True, null=True, on_delete=models.SET_NULL
    )
    phase_whether_1_1 = models.CharField(max_length=256, blank=True, default="")
    phase_whether_1_2 = models.CharField(max_length=256, blank=True, default="")
    phase_whether_2_1 = models.CharField(max_length=256, blank=True, default="")
    phase_whether_2_2 = models.CharField(max_length=256, blank=True, default="")
    timing_whether_1_1 = models.CharField(max_length=256, blank=True, default="")
    timing_whether_1_2 = models.CharField(max_length=256, blank=True, default="")
    timing_whether_2_1 = models.CharField(max_length=256, blank=True, default="")
    timing_whether_2_2 = models.CharField(max_length=256, blank=True, default="")
    kind_whether_1_1 = models.CharField(max_length=256, blank=True, default="")
    kind_whether_1_2 = models.CharField(max_length=256, blank=True, default="")
    kind_whether_2_1 = models.CharField(max_length=256, blank=True, default="")
    kind_whether_2_2 = models.CharField(max_length=256, blank=True, default="")

    audio = models.CharField(max_length=32, default="", blank=True)
    global_variable = models.TextField(default="", blank=True)
    user_1 = models.ForeignKey(
        User,
        blank=True,
        related_name="tcgcreator%(class)s_requests_user_1",
        default=None,
        null=True,
        on_delete=models.SET_NULL,
    )
    user_2 = models.ForeignKey(
        User,
        default=None,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="tcgcreatorduel",
    )
    each = models.IntegerField(default=0, blank=True, null=False)
    chain = models.IntegerField(default=0, blank=True, null=False)
    virtual_chain = models.IntegerField(default=0, blank=True, null=False)
    chain_det = models.TextField(default="", blank=True)
    chain_det_trigger = models.TextField(default="", blank=True)
    chain_user = models.TextField(default="", blank=True)
    chain_variable = models.TextField(default="", blank=True)
    mess = models.TextField(blank=True, default="")
    variable_mess = models.TextField(blank=True, default="")
    # 多々多のためのmess
    multiple_mess = models.TextField(blank=True, default="")
    in_cost = models.BooleanField(default=False)
    in_cost_cancel = models.BooleanField(default=False)
    in_trigger_waiting = models.BooleanField(default=False)
    in_cost_force = models.BooleanField(default=False)
    cost_result = models.TextField(blank=True, default="")
    cost = models.TextField(blank=True, default="")
    cost_det = models.IntegerField(default=0, blank=True)
    cost_user = models.IntegerField(default=0, blank=True)
    trigger_waiting = models.TextField(default="", blank=True)
    trigger_force = models.TextField(default="", blank=True)
    appoint = models.IntegerField(default=0, blank=True)
    change_appoint_flag = models.IntegerField(default=0, blank=True)
    timing = models.ForeignKey(
        Timing, default=None, blank=True, null=True, on_delete=models.SET_NULL
    )
    timing2 = models.ForeignKey(
        Timing, default=None, blank=True, null=True, on_delete=models.SET_NULL,related_name = "duel_timing2"
    )
    timing3 = models.ForeignKey(
        Timing, default=None, blank=True, null=True, on_delete=models.SET_NULL,related_name="duel_timing3"
    )
    timing_fresh = models.BooleanField(default=False)
    none = models.BooleanField(default=False)
    timing_waiting = models.ForeignKey(
        Trigger, default=None, blank=True, null=True, on_delete=models.SET_NULL
    )
    timing_mess = models.TextField(default="", blank=True)
    current_priority = models.IntegerField(default=10000)
    pac = models.IntegerField(default=0, blank=True, null=False)
    in_pac = models.TextField(default="", blank=True)
    in_pac_cost = models.TextField(default="", blank=True)
    no_invoke_eternal_effect = models.TextField(default="", blank=True)
    invoke_invalid_eternal_effect = models.TextField(default="", blank=True)
    no_choose_eternal_effect = models.TextField(default="", blank=True)
    no_eternal_eternal_effect = models.TextField(default="", blank=True)
    not_effected_eternal_effect = models.TextField(default="", blank=True)
    change_val_eternal_effect = models.TextField(default="", blank=True)
    sound_effect_1 = models.TextField(default="", blank=True)
    sound_effect_2 = models.TextField(default="", blank=True)
    trigger_log = models.TextField(default="", blank=True)
    log = models.TextField(default="", blank=True)
    current_log = models.TextField(default="", blank=True)
    message_log = models.TextField(default="", blank=True)
    log_turn = models.TextField(default="", blank=True)
    cost_log = models.TextField(default="", blank=True)
    duel_id = models.TextField(default="", blank=True)
    winner = models.IntegerField(default=0, blank=True)
    winner_ai = models.IntegerField(default=0, blank=True)
    in_eternal = models.BooleanField(default=False)
    in_copying = models.BooleanField(default=False)
    eternal_det = models.TextField(default="", blank=True)
    in_pac_eternal = models.TextField(default="", blank=True)
    eternal_mess = models.TextField(default="", blank=True)
    eternal_user = models.TextField(default="", blank=True)
    time_1 = models.FloatField(default=0.0)
    time_2 = models.FloatField(default=0.0)
    waiting = models.BooleanField(default=False)
    end_time = models.FloatField(default=0.0)
    canbechained = models.BooleanField(default=True)
    mute = models.IntegerField(default=0)
    force = models.IntegerField(default=0)
    trigger_name = models.CharField(max_length=256, blank=True)
    in_execute = models.BooleanField(default=False)
    # 広域変数を軽減する変数
    alt_global = models.TextField(blank=True, default="")
    accumulate_global = models.TextField(blank=True, default="")
    wait_time = models.FloatField(default=0.0)
    once_per_duel1 = models.TextField(blank=True, default="")
    once_per_duel2 = models.TextField(blank=True, default="")
    once_per_turn1 = models.TextField(blank=True, default="")
    once_per_turn_monster1 = models.TextField(blank=True, default="")
    once_per_turn2 = models.TextField(blank=True, default="")
    once_per_turn_monster2 = models.TextField(blank=True, default="")
    once_per_turn_group1 = models.TextField(blank=True, default="")
    once_per_turn_monster_group1 = models.TextField(blank=True, default="")
    once_per_turn_group2 = models.TextField(blank=True, default="")
    once_per_turn_monster_group2 = models.TextField(blank=True, default="")
    once_per_turn_exist1 = models.TextField(blank=True, default="")
    once_per_turn_exist1 = models.TextField(blank=True, default="")
    once_per_turn_exist2 = models.TextField(blank=True, default="")
    once_per_turn_relate1 = models.TextField(blank=True, default="")
    once_per_turn_relate2 = models.TextField(blank=True, default="")
    tmponce_per_turn1 = models.CharField(blank=True, max_length = 100,default="")
    tmponce_per_turn_monster1 = models.CharField(blank=True, max_length=100,default="")
    tmponce_per_turn2 = models.CharField(max_length=100,blank=True, default="")
    tmponce_per_turn_monster2 = models.CharField(max_length=100,blank=True, default="")
    tmponce_per_turn_group1 = models.CharField(blank=True, max_length = 100,default="")
    tmponce_per_turn_group2 = models.CharField(max_length=100,blank=True, default="")
    tmponce_per_turn_monster_group1 = models.CharField(blank=True, max_length = 100,default="")
    tmponce_per_turn_monster_group2 = models.CharField(max_length=100,blank=True, default="")
    tmponce_per_turn_exist1 = models.CharField(max_length=100,blank=True, default="")
    tmponce_per_turn_exist1 = models.CharField(max_length=100,blank=True, default="")
    tmponce_per_turn_exist2 = models.CharField(max_length=100,blank=True, default="")
    tmponce_per_turn_relate1 = models.CharField(max_length=100,blank=True, default="")
    tmponce_per_turn_relate2 = models.CharField(max_length=100,blank=True, default="")
    is_ai = models.BooleanField(default=False)
    guest_flag = models.BooleanField(default=False)
    guest_id = models.TextField(default="",blank=True)
    guest_name = models.CharField(default="",blank=True,max_length=32)
    guest_flag2 = models.BooleanField(default=False)
    guest_id2 = models.TextField(default="",blank=True)
    guest_name2 = models.CharField(default="",blank=True,max_length=32)
    ai_choosing = models.BooleanField(default=False)
    current_trigger = models.IntegerField(default=0)

    effect = models.TextField(default="", blank=True)
    effect2 = models.TextField(default="", blank=True)
    effect_flag = models.IntegerField(default=False,blank = True)
    background_image=models.CharField(max_length=32,default="",blank=True);
    change_turn_flag = models.BooleanField(default=False)
    already_choosed = models.IntegerField(default=0)
    class Meta:
        db_table = "tcgcreator_duel"


class Config(models.Model):
    cancel_name = models.CharField(max_length=32,default="キャンセル")
    sort = models.BooleanField(default=False,blank=True)
    auto_max = models.CharField(max_length=32,default="の高いものを選択")
    surrender_name = models.CharField(max_length=32,default="降参")
    turn_name = models.CharField(max_length=32,default="ターン")
    time_name = models.CharField(max_length=32,default="残り時間")
    reload_name = models.CharField(max_length=32,default="更新")
    tomessage_name = models.CharField(max_length=32,default="メッセージ送信")
    log_name = models.CharField(max_length=32, default="これまでのデュエル内容を確認")
    game_name = models.CharField(max_length=32, default="")
    hide_name = models.CharField(max_length=32, default="")
    limit_time = models.IntegerField(default=300)
    room_time = models.IntegerField(default=180)
    time_win = models.CharField(default="", blank=True, max_length=32)
    deck_side = models.BooleanField(default=False)
    common_name = models.CharField(default="共有", max_length=32)
    gray_out = models.ForeignKey(
        MonsterVariables, default=None, blank=True, null=True, on_delete=models.SET_NULL
    )
    default_sort = models.ForeignKey(
        MonsterVariables,
        default=None,
        blank=True,
        null=True,
        related_name="default_sort",
        on_delete=models.SET_NULL,
    )
    field_free = models.BooleanField(default=False)
    initial_turn_log = models.BooleanField(default=True)
    initial_turn_start_log = models.BooleanField(default=True)
    detail_log = models.BooleanField(default=False)
    cheat = models.BooleanField(default=False)
    choose_multiple_cancel = models.CharField(max_length=32,default="迎撃しない")
    message_position = models.IntegerField(choices=LEFT_OR_CENTER, default=1)
    templates = models.IntegerField(choices=CONFIG_TEMPLATE_CHOICE, default=3)
    explain_height=models.IntegerField(default=50) 
    chain_string=models.CharField(max_length=32,default="", blank=True)
    mine_color=models.CharField(max_length=32,default="#FFFFFF");
    other_color=models.CharField(max_length=32,default="#FFFFFF");
    background_image=models.CharField(max_length=32,default="",blank=True);
    font_color=models.CharField(max_length=32,default="black",blank=True);
    link_color=models.CharField(max_length=32,default="purple",blank=True);
    phase_color=models.CharField(max_length=32,default="green",blank=True);
    log_background_color=models.CharField(max_length=32,default="white",blank=True);
    turn_font_size=models.CharField(max_length=32,default="16",blank=True);
    life_font_size=models.CharField(max_length=32,default="16",blank=True);
    time_font_size=models.CharField(max_length=32,default="16",blank=True);
    deck_font_size=models.CharField(max_length=32,default="16",blank=True);
    phase_font_size=models.CharField(max_length=32,default="16",blank=True);
    hand_name_show_flag=models.BooleanField(default=False,blank=True);
    ask_audio=models.CharField(max_length=32,default="",blank=True);
    win_audio=models.CharField(max_length=32,default="",blank=True);
    lose_audio=models.CharField(max_length=32,default="",blank=True);
    chat_audio=models.CharField(max_length=32,default="",blank=True);
    audio_volume = models.FloatField( default="0.5")
    card_width = models.IntegerField(default=150)
    card_height = models.IntegerField(default=210)
    card_href = models.BooleanField(default = False)
    show_wait_chain = models.BooleanField(default=False)
    up_reverse = models.BooleanField(default = False)
    from_left = models.BooleanField(default=False)
    add_variables_show = models.CharField(default="",blank=True,max_length=32)
    show_message = models.BooleanField(default=True)
    ai = models.BooleanField(default = False,blank = True)
    return_url = models.CharField(default="../choose/",max_length = 128,blank=True)
    shori = models.IntegerField(choices=SHORI, default=1)
    order = models.IntegerField(choices=ORDER, default=0)
    show_img = models.IntegerField(choices=SHOW_IMG,default = 1,blank = True)
    csv_encoding = models.IntegerField(choices= CSV_ENCODING,default=0,blank=True)
    back_side_of_card = models.CharField(default="",max_length = 128,blank=True)
    class Meta:
        db_table = "tcgcreator_config"


class Lock(models.Model):
    lock_1 = models.BooleanField(default=False)
    time_1 = models.FloatField(default=0.0)
    lock_2 = models.BooleanField(default=False)
    time_2 = models.FloatField(default=0.0)
    lock_3 = models.BooleanField(default=False)
    time_3 = models.FloatField(default=0.0)
    db_table = "tcgcreator_lock"
class Constraint(models.Model):
    monster_variable = models.ForeignKey(MonsterVariables,blank=True,on_delete=models.SET_NULL,null=True)
    except_val = models.TextField(default = "")
    limit = models.IntegerField(default=100)
    db_table = "tcgcreator_constraint"
class Fusion(models.Model):
    def __str__(self):
        return self.fusion_name
    fusion_name = models.CharField(max_length=32,default="", blank=True)
    fusion_sentence = models.CharField(default="", blank=True,max_length=32)
    fusion1 = models.TextField(default="", blank=True)
    fusion2 = models.TextField(default="", blank=True)
    fusion3 = models.TextField(default="", blank=True)
    monster = models.ManyToManyField("Monster", blank=True)
    unique_effect = models.ForeignKey(
        "MonsterEffectWrapper",
        default=None,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    class Meta:
        db_table = "tcgcreator_fusion"
