from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from . import battle_det
from . import explain_grave
from . import explain
from . import explain_deck
from . import battle
from . import watch
from . import ask
from . import answer
from . import hand_trigger
from . import deck_trigger
from . import grave_trigger
from . import field_trigger
from . import choices
from . import get_monster_variable
from . import api

app_name = "tcgcreator"
urlpatterns = [
    # 	url(r'^$', views.index, name='index'),
    re_path(r"^monster_variables/$", views.monster_variables, name="monster_variables"),
    re_path(
        r"^edit_monster_variables/(?P<monster_variables_id>\d+)/$",
        views.edit_monster_variables,
        name="edit_monster_variables",
    ),
    re_path(
        r"^monster_variables_kind/$",
        views.monster_variables_kind,
        name="monster_variables_kind",
    ),
    re_path(
        r"^edit_monster_variables_kind/(?P<monster_variables_kind_id>\d+)/$",
        views.edit_monster_variables_kind,
        name="edit_monster_variables_kind",
    ),
    re_path(
        r"^new_monster_variables_kind/$",
        views.new_monster_variables_kind,
        name="new_monster_variables_kind",
    ),
    re_path(
        r"^new_monster_variables/$",
        views.new_monster_variables,
        name="new_monster_variables",
    ),
    re_path(r"^new_monster/$", views.new_monster, name="new_monster"),
    re_path(r"^monster/$", views.monster, name="monster"),
    re_path(r"^get_monster/$", views.get_monster, name="get_monster"),
    re_path(r"^choose/$", views.choose, name="choose"),
    re_path(r"^from_out/$", views.from_out, name="from_out"),
    re_path(
        r"^get_monster_kind_type/$",
        views.get_monster_kind_type,
        name="get_monster_kind_type",
    ),
    re_path(
        r"^get_monster_kind_type_for_new_monster/$",
        views.get_monster_kind_type_for_new_monster,
        name="get_monster_kind_type_for_new_monster",
    ),
    re_path(r"^get_field_kind/$", views.get_field_kind, name="get_field_kind"),
    re_path(r"^get_field_kind2/$", views.get_field_kind2, name="get_field_kind2"),
    re_path(r"^get_monster_kind/$", views.get_monster_kind, name="get_monster_kind"),
    re_path(
        r"^get_invalid_monster_kind/$",
        views.get_invalid_monster_kind,
        name="get_invalid_monster_kind",
    ),
    re_path(
        r"^get_monster_condition/$",
        views.get_monster_condition,
        name="get_monster_condition",
    ),
    re_path(r"^get_monster_move/$", views.get_monster_move, name="get_monster_move"),
    re_path(r"^get_equation/$", views.get_equation, name="get_equation"),
    re_path(r"^get_monster_to/$", views.get_monster_to, name="get_monster_to"),
    re_path(r"^get_equation_to/$", views.get_equation_to, name="get_equation_to"),
    re_path(r"^get_trigger/$", views.get_trigger, name="get_trigger"),
    re_path(r"^get_place_kind/$", views.get_place_kind, name="get_place_kind"),
    re_path(r"^get_place_kind_to/$", views.get_place_kind_to, name="get_place_kind_to"),
    re_path(r"^get_variable_kind/$", views.get_variable_kind, name="get_variable_kind"),
    re_path(r"^battle1/$", battle.battle1, name="battle1"),
    re_path(r"^battle2/$", battle.battle2, name="battle2"),
    re_path(r"^battle3/$", battle.battle3, name="battle3"),
    re_path(r"^watch1/$", watch.watch1, name="watch1"),
    re_path(r"^watch2/$", watch.watch2, name="watch2"),
    re_path(r"^watch3/$", watch.watch3, name="watch3"),
    re_path(r"^leave_battle1/$", views.leave_battle1, name="leave_battle1"),
    re_path(r"^leave_battle2/$", views.leave_battle2, name="leave_battle2"),
    re_path(r"^leave_battle3/$", views.leave_battle3, name="leave_battle3"),
    re_path(r"^wait_battle1/$", views.wait_battle1, name="wait_battle1"),
    re_path(r"^wait_battle2/$", views.wait_battle2, name="wait_battle2"),
    re_path(r"^wait_battle3/$", views.wait_battle3, name="wait_battle3"),
    re_path(r"^init_battle1/$", views.init_battle1, name="init_battle1"),
    re_path(r"^init_battle2/$", views.init_battle2, name="init_battle2"),
    re_path(r"^init_battle3/$", views.init_battle3, name="init_battle3"),
    re_path(r"^send_lose/$", views.send_lose, name="send_lose"),
    re_path(r"^exit$", views.exit, name="exit"),
    re_path(r"^get_timing/$", views.get_timing, name="get_timing"),
    re_path(r"^get_hand_id/$", views.get_hand_id, name="get_hand_id"),
    re_path(r"^get_field_x_and_y/$", views.get_field_x_and_y, name="get_field_x_and_y"),
    re_path(r"^makedeck/$", views.makedeck, name="makedeck"),
    re_path(r"^makedecktext/$", views.makedecktext, name="makedecktext"),
    re_path(
        r"^get_monster_deck_type/$",
        views.get_monster_deck_type,
        name="get_monster_deck_type",
    ),
    re_path(r"^battle_det/$", battle_det.battle_det, name="battle_det"),
    re_path(r"^send_message/$", battle_det.send_message, name="send_message"),
    re_path(r"^watch_det/$", watch.watch_det, name="watch_det"),
    re_path(r"^explain_deck/$", explain_deck.explain_deck, name="explain_deck"),
    re_path(r"^explain/$", explain.explain, name="explain"),
    re_path(r"^explain_grave/$", explain_grave.explain_grave, name="explain_grave"),
    re_path(r"^ask_place/$", ask.ask_place, name="ask_place"),
    re_path(r"^answer/$", answer.answer, name="answer"),
    re_path(r"^answer_trigger/$", answer.answer_trigger, name="answer_trigger"),
    re_path(r"^send_fusion_monster/$", answer.send_fusion_monster, name="send_fusion_monster"),
    re_path(r"^send_fusion_monster_field/$", answer.send_fusion_monster_field, name="send_fusion_monster_field"),
    re_path(r"^send_fusion_material/$", answer.send_fusion_material, name="send_fusion_material"),
    re_path(r"^force_trigger/$", answer.force_trigger, name="force_trigger"),
    re_path(r"^answerorder/$", answer.answerorder, name="answerorder"),
    re_path(r"^yes_or_no/$", answer.yes_or_no, name="yes_or_no"),
    re_path(r"^multiple_choice/$", answer.multiple_choice, name="multiple_choice"),
    re_path(r"^multiple_answer/$", answer.multiple_answer, name="multiple_answer"),
    re_path(r"^chain_variable/$", answer.chain_variable, name="chain_variable"),
    re_path(r"^cheat/$", answer.cheat, name="cheat"),
    re_path(r"^cheat2/$", answer.cheat2, name="cheat2"),
    re_path(r"^chooseai/$", answer.chooseai, name="chooseai"),
    re_path(r"^choosedeck/$", answer.choosedeck, name="choosedeck"),
    re_path(r"^chooseuserdeck/$", answer.chooseuserdeck, name="chooseuserdeck"),
    re_path(r"^chooseguestname/$", answer.chooseguestname, name="chooseguestname"),
    re_path(r"^none/$", answer.none, name="none"),
    re_path(r"^cancel/$", answer.cancel, name="cancel"),
    re_path(r"^change_wait/$", answer.change_wait, name="change_wait"),
    re_path(r"^hand_trigger/$", hand_trigger.hand_trigger, name="hand_trigger"),
    re_path(r"^deck_trigger/$", deck_trigger.deck_trigger, name="deck_trigger"),
    re_path(r"^grave_trigger/$", grave_trigger.grave_trigger, name="grave_trigger"),
    re_path(r"^field_trigger/$", field_trigger.field_trigger, name="field_trigger"),
    re_path(r"^choices/$", choices.choices, name="choices"),
    re_path(r"^get_phase/$", views.get_phase, name="get_phase"),
    re_path(r"^get_trigger/$", views.get_trigger, name="get_trigger"),
    re_path(
        r"^get_trigger_with_monster/$",
        views.get_trigger_with_monster,
        name="get_trigger_with_monster",
    ),
    re_path(
        r"^get_monster_effect_wrapper/$",
        views.get_monster_effect_wrapper,
        name="get_monster_effect_wrapper",
    ),
    re_path(r"^get_last_monster_effect/$", views.get_last_monster_effect, name="get_last_monster_effect"),
    re_path(r"^get_monster_effect/$", views.get_monster_effect, name="get_monster_effect"),
                  re_path(
                      r"^get_last_monster_effect_wrapper_specify/$",
                      views.get_last_monster_effect_wrapper_specify,
                      name="get_last_monster_effect_wrapper_specify",
                  ),
    re_path(
        r"^get_monster_effect_wrapper_specify/$",
        views.get_monster_effect_wrapper_specify,
        name="get_monster_effect_wrapper_specify",
    ),
                  re_path(
                      r"^get_pac_specify/$",
                      views.get_pac_specify,
                      name="get_pac_specify",
                  ),
    re_path(
        r"^get_monster_specify/$", views.get_monster_specify, name="get_monster_specify"
    ),
    re_path(r"^get_cost/$", views.get_cost, name="get_cost"),
    re_path(r"^get_last_cost/$", views.get_last_cost, name="get_last_cost"),
    re_path(
        r"^get_trigger_specify/$", views.get_trigger_specify, name="get_trigger_specify"
    ),
    re_path(
         r"^get_last_trigger_specify/$", views.get_last_trigger_specify, name="get_last_trigger_specify"
     ),
    re_path(
        r"^get_cost_wrapper_specify/$",
        views.get_cost_wrapper_specify,
        name="get_cost_wrapper_specify",
    ),
    re_path(
         r"^get_last_cost_wrapper_specify/$",
         views.get_last_cost_wrapper_specify,
         name="get_last_cost_wrapper_specify",
     ),
                  re_path(
                      r"^get_last_pac_cost_wrapper_specify/$",
                      views.get_last_pac_cost_wrapper_specify,
                      name="get_last_pac_cost_wrapper_specify",
                  ),
    re_path(
        r"^get_pac_cost_wrapper_specify/$",
        views.get_pac_cost_wrapper_specify,
        name="get_pac_cost_wrapper_specify",
    ),
    re_path(
        r"^get_pac_wrapper_specify/$",
        views.get_pac_wrapper_specify,
        name="get_pac_wrapper_specify",
    ),
                  re_path(
                      r"^get_last_pac_specify/$",
                      views.get_last_pac_specify,
                      name="get_last_pac_specify",
                  ),
                  re_path(
                      r"^get_last_pac_wrapper_specify/$",
                      views.get_last_pac_wrapper_specify,
                      name="get_last_pac_wrapper_specify",
                  ),
    re_path(r"^get_pac_wrapper/$", views.get_pac_wrapper, name="get_pac_wrapper"),
    re_path(r"^get_tcg_timing/$", views.get_tcg_timing, name="get_tcg_timing"),
    re_path(r"^get_phase_and_turn/$", views.get_phase_and_turn, name="get_phase_and_turn"),
    re_path(
        r"^get_monster_variable/$",
        get_monster_variable.get_monster_variable,
        name="get_monster_variable",
    ),
    re_path(r"^signup/$", views.signup, name="signup"),
    re_path(r"^login/$", views.login_user, name="tcgcreatorlogin"),
    re_path(r"^logout/$", views.logout_user, name="tcgcreatorlogout"),
    re_path(r"^user_info_change/$", views.user_info_change, name="user_info_change"),
    re_path(r"^index$", views.index, name="index"),
    re_path(r"^howto/$", views.howto, name="howto"),
    re_path(r"^save_unit/$", views.save_unit, name="save_unit"),
    re_path(r"^get_effect_kind/$", views.get_effect_kind, name="get_effect_kind"),
    re_path(r"^api/return_highest/$", api.return_highest, name="return_highest"),
    re_path(r"^api/room_data/$", api.room_data, name="room_data"),
    re_path(
        r"^get_variables_condition_for_copy/$",
        views.get_variables_condition_for_copy,
        name="get_variables_condition_for_copy",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
