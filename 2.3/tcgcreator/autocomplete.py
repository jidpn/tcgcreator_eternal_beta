import json
from pprint import pprint
from django.http import HttpResponse
from .models import (
    MonsterVariables
)

def monster_variable_autocomplete(request):
    q = request.GET.get('term', '')
    titles = MonsterVariables.objects.filter(monster_variable_name__contains = q )[:10]
    results = []
    for title in titles:
        title_json = {}
        title_json = title.monster_variable_name
        results.append(title_json)
    data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
    
def monster_variable_kind_autocomplete(request):
    mimetype = 'application/json'
    q = request.GET.get('q', '')
    titles = MonsterVariables.objects.filter(monster_variable_name = q ).first()
    if titles is None:
        return HttpResponse([],mimetype)
    MonsterVariableKind = titles.monster_variable_kind_id
    if MonsterVariableKind.id == 1:
        return HttpResponse([],mimetype)
    else:
        results = []
        monster_variables = MonsterVariableKind.monster_variable_sentence.split("|")
        i = 1
        for monster_variable in monster_variables:
            tmp = {}
            tmp["label"]  = monster_variable
            if tmp["label"] == "":
                tmp["label"] = "なし"

            tmp["value"]  = i
            results.append(tmp)
            i+=1
    data = json.dumps(results)
    return HttpResponse(data, mimetype)
    