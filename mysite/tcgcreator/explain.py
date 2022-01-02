from .models import (
    Monster,Config
)
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render
from pprint import pprint


def explain(request):
    config = Config.objects.first()
    if "id" not in request.GET:
        HttpResponse("error")
    monster_id = request.GET["id"]
    monster = Monster.objects.get(id=monster_id)
    img_url = monster.img

    return render(request, "tcgcreator/explain.html", {"img_url": img_url,"config":config})
