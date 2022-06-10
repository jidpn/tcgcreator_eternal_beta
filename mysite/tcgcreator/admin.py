from django.contrib import admin
from .forms import (
    FieldForm,
    CostForm,
    MonsterEffectForm,
    MonsterEffectWrapperForm,
    PacWrapperForm ,
    CostWrapperForm)
from .models import (
    Background,
    SpecialCard,
    EndChainEffect,
    Constraint,
    UserDeck,
    EnemyDeck,
    EnemyDeckChoice,
    EnemyDeckGroup,
    Fusion,
    MonsterVariablesKind,
    MonsterVariables,
    Monster,
    MonsterItem,
    FieldSize,
    Field,
    FieldKind,
    MonsterEffectKind,
    MonsterEffect,
    Deck,
    Hand,
    Grave,
    Trigger,
    Phase,
    Duel,
    UserDeckGroup,
    UserDeckChoice,
    Config,
    GlobalVariable,
    MonsterEffectWrapper,
    Cost,
    CostWrapper,
    DefaultDeck,
    DefaultDeckChoice,
    DefaultDeckGroup,
    TriggerTiming,
    Timing,
    Pac,
    PacWrapper,
    EternalEffect,
    PacCost,
    PacCostWrapper,
    DuelHand,
    VirtualVariable,
    EternalWrapper,
    DuelDeck,
    DuelGrave,
    EternalTrigger,
    UnderDirection,
    TriggerTimingChangeVal,
    TriggerTimingMonsterChangeVal,
    TriggerTimingNotEffected,
    Lock,
    TriggerTimingRelation,
    MONSTER_EFFECT_VAL,
    UserPoint,
)
from .custom_functions import init_monster_item, init_field

# Register your models here.
# class MyModelAdmin(admin.ModelAdmin):


class DeckAdmin(admin.ModelAdmin):
    save_as = True

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        if Deck.objects.count() >= 10:
            return False
        else:
            return True


admin.site.register(Deck, DeckAdmin)


class HandAdmin(admin.ModelAdmin):
    save_as = True

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        if Hand.objects.count() >= 10:
            return False
        else:
            return True


admin.site.register(Hand, HandAdmin)


class GraveAdmin(admin.ModelAdmin):
    save_as = True

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        if Grave.objects.count() >= 10:
            return False
        else:
            return True


admin.site.register(Grave, GraveAdmin)


class FieldSizeAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if FieldSize.objects.count() != 0:
            return False
        else:
            return True

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.save()
        init_field(request.POST["field_x"], request.POST["field_y"])


admin.site.register(FieldSize, FieldSizeAdmin)


class CostAdmin(admin.ModelAdmin):
    form = CostForm
    save_as = True
    change_form_template = "admin/tcgcreator/monster_effect.html"
    search_fields = ["cost_name"]
    list_display = ("cost_name","cost_val")
    list_filter = ['cost_val']

    class Media:
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "tcgcreator/js/cost_kind.js",
            "tcgcreator/js/field_kind2.js",
            "tcgcreator/js/monster_condition.js",
            "tcgcreator/js/monster_effect_move.js",
            "tcgcreator/js/common.js",
            "tcgcreator/js/monster_variable_change.js",
            "tcgcreator/js/ajax.js",
            "tcgcreator/js/cost.js",
            "tcgcreator/js/monster_effect_kind.js",
            "tcgcreator/js/monster_effect_choose.js",
            "tcgcreator/js/monster_effect_choose_both.js",
        ]


admin.site.register(Cost, CostAdmin)

class FusionAdmin(admin.ModelAdmin):
    change_form_template = "admin/tcgcreator/trigger.html"
    save_as = True
    def has_delete_permission(self, request, obj=None):
        return True
    class Media:
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
  
            "tcgcreator/js/common.js",
            "tcgcreator/js/ajax.js",
            "tcgcreator/js/monster_condition.js",
            "tcgcreator/js/fusion.js",
            "tcgcreator/js/monster_effect_wrapper.js",
        ]
class MonsterEffectAdmin(admin.ModelAdmin):
    save_as = True
    form = MonsterEffectForm

    def has_delete_permission(self, request, obj=None):
        return True

    change_form_template = "admin/tcgcreator/monster_effect.html"
    search_fields = ["monster_effect_name"]
    list_display = ("monster_effect_name","monster_effect_val")
    list_filter = ['monster_effect_val']

    class Media:
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "tcgcreator/js/monster_effect_choose_both.js",
            "tcgcreator/js/monster_effect_choose.js",
            "tcgcreator/js/monster_effect_move.js",
            "tcgcreator/js/monster_variable_change.js",
            "tcgcreator/js/monster_effect_kind.js",
            "tcgcreator/js/field_kind2.js",
            "tcgcreator/js/monster_effect.js",
            "tcgcreator/js/common.js",
            "tcgcreator/js/ajax.js",
            "tcgcreator/js/monster_condition.js",
        ]


admin.site.register(MonsterEffect, MonsterEffectAdmin)


class TriggerTimingRelationAdmin(admin.ModelAdmin):
    save_as = True
    change_form_template = "admin/tcgcreator/trigger.html"
    search_fields = ["trigger_timing_name"]

    class Media:
        css = {"all": ("css/common.css",)}
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "tcgcreator/js/monster_condition.js",
            "tcgcreator/js/field_kind2.js",
            "tcgcreator/js/trigger_timing.js",
            "tcgcreator/js/common.js",
            "tcgcreator/js/ajax.js",
            "tcgcreator/js/trigger_variable.js",
        ]


class TriggerTimingNotEffectedAdmin(admin.ModelAdmin):
    change_form_template = "admin/tcgcreator/trigger.html"
    save_as = True
    search_fields = ["trigger_timing_name"]

    class Media:
        css = {"all": ("css/common.css",)}
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "tcgcreator/js/monster_condition.js",
            "tcgcreator/js/field_kind2.js",
            "tcgcreator/js/trigger_timing.js",
            "tcgcreator/js/common.js",
            "tcgcreator/js/ajax.js",
            "tcgcreator/js/trigger_variable.js",
        ]


admin.site.register(TriggerTimingNotEffected, TriggerTimingNotEffectedAdmin)
class TriggerTimingMonsterChangeValAdmin(admin.ModelAdmin):
    change_form_template = "admin/tcgcreator/trigger.html"
    save_as = True
    search_fields = ["trigger_timing_name"]

    class Media:
        css = {"all": ("css/common.css",)}
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "tcgcreator/js/monster_condition.js",
            "tcgcreator/js/field_kind2.js",
            "tcgcreator/js/trigger_timing.js",
            "tcgcreator/js/common.js",
            "tcgcreator/js/ajax.js",
            "tcgcreator/js/trigger_variable.js",
        ]


admin.site.register(TriggerTimingMonsterChangeVal, TriggerTimingMonsterChangeValAdmin)
class TriggerTimingChangeValAdmin(admin.ModelAdmin):
    change_form_template = "admin/tcgcreator/trigger.html"
    save_as = True
    search_fields = ["trigger_timing_name"]

    class Media:
        css = {"all": ("css/common.css",)}
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "tcgcreator/js/monster_condition.js",
            "tcgcreator/js/field_kind2.js",
            "tcgcreator/js/trigger_timing.js",
            "tcgcreator/js/common.js",
            "tcgcreator/js/ajax.js",
            "tcgcreator/js/trigger_variable.js",
        ]


admin.site.register(TriggerTimingChangeVal, TriggerTimingChangeValAdmin)


class TriggerTimingAdmin(admin.ModelAdmin):
    change_form_template = "admin/tcgcreator/trigger.html"
    save_as = True
    search_fields = ["trigger_timing_name"]

    class Media:
        css = {"all": ("css/common.css",)}
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "tcgcreator/js/monster_condition.js",
            "tcgcreator/js/field_kind2.js",
            "tcgcreator/js/trigger_timing.js",
            "tcgcreator/js/common.js",
            "tcgcreator/js/ajax.js",
            "tcgcreator/js/trigger_variable.js",
        ]


admin.site.register(TriggerTiming, TriggerTimingAdmin)


class TriggerAdmin(admin.ModelAdmin):
    change_form_template = "admin/tcgcreator/trigger.html"
    save_as = True
    search_fields = ["trigger_name","trigger_monster"]

    class Media:
        css = {"all": ("css/common.css",)}
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
              "https://code.jquery.com/jquery-3.6.0.min.js",
            "tcgcreator/js/monster_condition.js",
            "tcgcreator/js/field_kind2.js",
            "tcgcreator/js/trigger.js",
            "tcgcreator/js/cost_wrapper.js",
            "tcgcreator/js/monster_effect_wrapper.js",
            "tcgcreator/js/common.js",
            "tcgcreator/js/ajax.js",
            "tcgcreator/js/trigger_variable.js",
        ]


admin.site.register(Trigger, TriggerAdmin)


class EternalEffectAdmin(admin.ModelAdmin):
    save_as = True
    change_form_template = "admin/tcgcreator/eternal_effect.html"
    search_fields = ["eternal_name"]
    list_filter = ['eternal_effect_val']

    class Media:
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "tcgcreator/js/field_kind2.js",
            "tcgcreator/js/eternal_effect.js",
            "tcgcreator/js/common.js",
            "tcgcreator/js/ajax.js",
            "tcgcreator/js/eternal_effect_variable.js",
            "tcgcreator/js/monster_condition.js",
        ]


admin.site.register(EternalEffect, EternalEffectAdmin)


class FieldAdmin(admin.ModelAdmin):
    form = FieldForm

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    class Media:
        js = [ "tcgcreator/js/field_kind.js", "tcgcreator/js/ajax.js",
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js"]


admin.site.register(Field, FieldAdmin)


class MonsterVariablesAdmin(admin.ModelAdmin):
    search_fields = ["monster_variable_name"]

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.save()
        if change is False:
            init_monster_item(obj)


admin.site.register(MonsterVariablesKind, admin.ModelAdmin)
admin.site.register(FieldKind, admin.ModelAdmin)
admin.site.register(MonsterVariables, MonsterVariablesAdmin)


class MonsterItemInline(admin.StackedInline):
    def has_delete_permission(self, request, obj=None):
        return False

    model = MonsterItem

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        return MonsterVariables.objects.count()


admin.site.register(MonsterEffectKind)


class MonsterAdmin(admin.ModelAdmin):
    save_as = True
    search_fields = ["monster_name"]

    def has_delete_permission(self, request, obj=None):
        return True

    change_form_template = "admin/tcgcreator/monster_form.html"

    def changeform_view(self, request, object_id, form_url, extra_context=None):
        extra_context = {}
        extra_context["monster_item_number"] = MonsterVariables.objects.count()
        return super(MonsterAdmin, self).changeform_view(
            request, object_id, form_url, extra_context=extra_context
        )

    inlines = [MonsterItemInline]

    class Media:
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "tcgcreator/js/monster_deck.js",
            "tcgcreator/js/monster_item.js",
            "tcgcreator/js/ajax.js",
        ]


class PhaseAdmin(admin.ModelAdmin):
    search_fields = ["phase_name"]

    def has_delete_permission(self, request, obj=None):
        return False

    class Media:
        js = [


             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",

                "tcgcreator/js/phase.js", "tcgcreator/js/ajax.js"]


class VirtualVariableAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    change_form_template = "admin/tcgcreator/monster_effect.html"

    class Media:
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "tcgcreator/js/common.js",
            "tcgcreator/js/ajax.js",
            "tcgcreator/js/virtual_variable.js",
        ]


admin.site.register(Monster, MonsterAdmin)


class DuelAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    class Meta:
        fields = []


admin.site.register(Duel)
admin.site.register(Phase, PhaseAdmin)
admin.site.register(UserDeckGroup)
admin.site.register(UserDeckChoice)
admin.site.register(Config)
admin.site.register(GlobalVariable)
admin.site.register(VirtualVariable, VirtualVariableAdmin)


class EternalTriggerAdmin(admin.ModelAdmin):
    save_as = True

    def has_delete_permission(self, request, obj=None):
        return True

    change_form_template = "admin/tcgcreator/monster_effect.html"

    class Media:
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "tcgcreator/js/monster_effect_choose_both.js",
            "tcgcreator/js/monster_effect_choose.js",
            "tcgcreator/js/monster_effect_move.js",
            "tcgcreator/js/monster_variable_change.js",
            "tcgcreator/js/monster_effect_kind.js",
            "tcgcreator/js/field_kind2.js",
            "tcgcreator/js/monster_effect.js",
            "tcgcreator/js/common.js",
            "tcgcreator/js/ajax.js",
            "tcgcreator/js/monster_condition.js",
        ]


admin.site.register(EternalTrigger, EternalTriggerAdmin)


class EternalWrapperAdmin(admin.ModelAdmin):
    save_as = True
    search_fields = ["monster_effect_name"]

    def has_delete_permission(self, request, obj=None):
        return True

    change_form_template = "admin/tcgcreator/monster_effect.html"

    class Media:
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "tcgcreator/js/monster_effect_choose_both.js",
            "tcgcreator/js/monster_effect_choose.js",
            "tcgcreator/js/monster_effect_move.js",
            "tcgcreator/js/monster_variable_change.js",
            "tcgcreator/js/monster_effect_kind.js",
            "tcgcreator/js/field_kind2.js",
            "tcgcreator/js/monster_effect.js",
            "tcgcreator/js/common.js",
            "tcgcreator/js/ajax.js",
            "tcgcreator/js/monster_condition.js",
        ]


admin.site.register(EternalWrapper, EternalWrapperAdmin)


class MonsterEffectWrapperAdmin(admin.ModelAdmin):
    save_as = True
    search_fields = ["monster_effect_name","monster_effect__monster_effect_name","log"]
    list_display = ("monster_effect_name","monster_effect","monster_effect_val")
    list_filter = ['monster_effect__monster_effect_val']
    list_select_related = ('monster_effect',)
    form = MonsterEffectWrapperForm
    def monster_effect_val(self,obj):
        for val in MONSTER_EFFECT_VAL:
            if val[0] == obj.monster_effect.monster_effect_val:
                return val[1]
        return None

    def has_delete_permission(self, request, obj=None):
        return True

    change_form_template = "admin/tcgcreator/monster_effect.html"

    class Media:
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "tcgcreator/js/monster_effect_choose_both.js",
            "tcgcreator/js/monster_effect_choose.js",
            "tcgcreator/js/monster_effect_move.js",
            "tcgcreator/js/monster_variable_change.js",
            "tcgcreator/js/monster_effect_kind.js",
            "tcgcreator/js/field_kind2.js",
            "tcgcreator/js/monster_effect_wrapper.js",
            "tcgcreator/js/common.js",
            "tcgcreator/js/ajax.js",
            "tcgcreator/js/monster_condition.js",
        ]


admin.site.register(MonsterEffectWrapper, MonsterEffectWrapperAdmin)


class CostWrapperAdmin(admin.ModelAdmin):
    save_as = True
    form = CostWrapperForm
    search_fields = ["cost_name","cost__cost_name"]
    list_display = ("cost_name","cost","cost_val")
    list_filter = ['cost__cost_val']
    list_select_related = ('cost',)
    def cost_val(self,obj):
        for val in MONSTER_EFFECT_VAL:
            if val[0] == obj.cost.cost_val:
                return val[1]
        return None
    def has_delete_permission(self, request, obj=None):
        return True

    change_form_template = "admin/tcgcreator/monster_effect.html"

    class Media:
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "tcgcreator/js/cost_kind.js",
            "tcgcreator/js/field_kind2.js",
            "tcgcreator/js/monster_condition.js",
            "tcgcreator/js/monster_effect_move.js",
            "tcgcreator/js/common.js",
            "tcgcreator/js/monster_variable_change.js",
            "tcgcreator/js/ajax.js",
            "tcgcreator/js/cost_wrapper.js",
            "tcgcreator/js/monster_effect_kind.js",
            "tcgcreator/js/monster_effect_choose.js",
            "tcgcreator/js/monster_effect_choose_both.js",
        ]


admin.site.register(CostWrapper, CostWrapperAdmin)


class PacAdmin(admin.ModelAdmin):
    save_as = True

    def has_delete_permission(self, request, obj=None):
        return True

    change_form_template = "admin/tcgcreator/monster_effect.html"

    class Media:
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "tcgcreator/js/monster_effect_choose_both.js",
            "tcgcreator/js/monster_effect_choose.js",
            "tcgcreator/js/monster_effect_move.js",
            "tcgcreator/js/monster_variable_change.js",
            "tcgcreator/js/monster_effect_kind.js",
            "tcgcreator/js/field_kind2.js",
            "tcgcreator/js/monster_effect.js",
            "tcgcreator/js/common.js",
            "tcgcreator/js/ajax.js",
            "tcgcreator/js/monster_condition.js",
            "tcgcreator/js/pac.js",
        ]


class PacCostAdmin(admin.ModelAdmin):
    save_as = True

    def has_delete_permission(self, request, obj=None):
        return True

    change_form_template = "admin/tcgcreator/monster_effect.html"

    class Media:
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "tcgcreator/js/monster_effect_kind.js",
            "tcgcreator/js/field_kind2.js",
            "tcgcreator/js/monster_effect.js",
            "tcgcreator/js/common.js",
            "tcgcreator/js/ajax.js",
            "tcgcreator/js/monster_condition.js",
            "tcgcreator/js/pac_cost.js",
            "tcgcreator/js/cost_wrapper.js",
        ]


class PacCostWrapperAdmin(admin.ModelAdmin):
    save_as = True

    def has_delete_permission(self, request, obj=None):
        return True

    change_form_template = "admin/tcgcreator/monster_effect.html"

    class Media:
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "tcgcreator/js/monster_effect_kind.js",
            "tcgcreator/js/field_kind2.js",
            "tcgcreator/js/monster_effect.js",
            "tcgcreator/js/common.js",
            "tcgcreator/js/ajax.js",
            "tcgcreator/js/monster_condition.js",
            "tcgcreator/js/pac.js",
            "tcgcreator/js/cost_wrapper.js",
            "tcgcreator/js/pac_cost_wrapper.js",
        ]


admin.site.register(Pac, PacAdmin)
admin.site.register(PacCost, PacCostAdmin)
admin.site.register(PacCostWrapper, PacCostWrapperAdmin)


class PacWrapperAdmin(admin.ModelAdmin):
    save_as = True
    form = PacWrapperForm
    def has_delete_permission(self, request, obj=None):
        return True

    change_form_template = "admin/tcgcreator/monster_effect.html"

    class Media:
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "tcgcreator/js/monster_effect_choose_both.js",
            "tcgcreator/js/monster_effect_choose.js",
            "tcgcreator/js/monster_effect_move.js",
            "tcgcreator/js/monster_variable_change.js",
            "tcgcreator/js/monster_effect_kind.js",
            "tcgcreator/js/field_kind2.js",
            "tcgcreator/js/monster_effect.js",
            "tcgcreator/js/common.js",
            "tcgcreator/js/ajax.js",
            "tcgcreator/js/monster_condition.js",
            "tcgcreator/js/pac_wrapper.js",
        ]


admin.site.register(PacWrapper, PacWrapperAdmin)


class SpecialCardAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return True

    class Media:
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
                "tcgcreator/js/phase.js", "tcgcreator/js/ajax.js"]
class BackgroundAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return True

class DefaultDeckAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return True

    class Media:
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
                "tcgcreator/js/phase.js", "tcgcreator/js/ajax.js"]
class EnemyDeckAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return True

    class Media:
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
                "tcgcreator/js/phase.js", "tcgcreator/js/ajax.js"]
class DefaultDeckGroupAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return True

    class Media:
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
                "tcgcreator/js/phase.js", "tcgcreator/js/ajax.js"]
class DefaultDeckChoiceAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    class Media:
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
                "tcgcreator/js/phase.js", "tcgcreator/js/ajax.js"]


class EnemyDeckGroupAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return True

    class Media:
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
                "tcgcreator/js/phase.js", "tcgcreator/js/ajax.js"]
class ConstraintAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return True

    class Media:
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
                "tcgcreator/js/phase.js", "tcgcreator/js/ajax.js"]
class EnemyDeckChoiceAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    class Media:
        js = [
             "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://code.jquery.com/jquery-3.6.0.min.js",
                "tcgcreator/js/phase.js", "tcgcreator/js/ajax.js"]



admin.site.register(DefaultDeck, DefaultDeckAdmin)
admin.site.register(Background, BackgroundAdmin)
admin.site.register(SpecialCard, SpecialCardAdmin)
admin.site.register(EnemyDeck, EnemyDeckAdmin)
admin.site.register(Constraint, ConstraintAdmin)
admin.site.register(DefaultDeckChoice, DefaultDeckChoiceAdmin)
admin.site.register(DefaultDeckGroup, DefaultDeckGroupAdmin)
admin.site.register(EnemyDeckChoice, EnemyDeckChoiceAdmin)
admin.site.register(EnemyDeckGroup, EnemyDeckGroupAdmin)
admin.site.register(Timing)
admin.site.register(UnderDirection)
admin.site.register(DuelHand)
admin.site.register(DuelDeck)
admin.site.register(Lock)
admin.site.register(UserPoint)
admin.site.register(DuelGrave)
admin.site.register(UserDeck)
admin.site.register(Fusion,FusionAdmin)
admin.site.register(EndChainEffect)
admin.site.register(TriggerTimingRelation, TriggerTimingRelationAdmin)
