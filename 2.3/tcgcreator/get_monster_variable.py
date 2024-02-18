from django.http import HttpResponse
from .models import (
    MonsterVariables,
)
from pprint import pprint
import json


def get_monster_variable(request):
    result = []
    monster_variables = MonsterVariables.objects.order_by("-priority")
    for monster_variable in monster_variables:
        tmp = {}
        monster_variable_kind = monster_variable.monster_variable_kind_id
        tmp["variable_id"] = monster_variable_kind.id
        tmp["variable_name"] = monster_variable_kind.monster_variable_name
        if monster_variable_kind.id != 1:
            variable_sentence = monster_variable_kind.monster_variable_sentence
            tmp["sentence"] = variable_sentence.split("_")
        result.append(tmp)

    return HttpResponse(json.dumps(result))
