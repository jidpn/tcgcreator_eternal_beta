from django.forms import ModelForm
from django import forms
from django.forms import ModelChoiceField
import json
import re
from django.contrib.auth.models import (
    User,
)
from .models import MonsterVariables, MonsterVariablesKind, Monster, MonsterItem, Field
from django.contrib.auth.forms import UserCreationForm
from pprint import pprint

class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        exclude = ["x", "y"]


class CustomChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.monster_variable_name


class EditMonsterVariablesForm(ModelForm):
    monster_variable_kind_id = CustomChoiceField(
        queryset=MonsterVariablesKind.objects.all()
    )

    class Meta:
        model = MonsterVariables
        fields = [
            "id",
            "monster_variable_kind_id",
            "monster_variable_name",
            "monster_variable_label",
            "monster_variable_show",
            "priority",
            "default_value",
        ]


class EditMonsterVariablesKindForm(ModelForm):
    class Meta:
        model = MonsterVariablesKind
        fields = ["monster_variable_name", "monster_variable_sentence"]


class EditMonsterForm(ModelForm):
    class Meta:
        model = Monster
        fields = ["monster_name", "monster_sentence"]


class EditMonsterItemForm(ModelForm):
    class Meta:
        model = MonsterItem
        fields = ["monster_item_text", "monster_variables_id", "monster_id"]


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2", "first_name"]


class profileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name"]

class PacWrapperForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        val = cleaned_data.get("pac_name")


        if re.search('[!-/:-@[-`{-~]',val):
            raise forms.ValidationError("名前に記号は入れないでください")
            return
class MonsterEffectWrapperForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        val = cleaned_data.get("monster_effect_name")


        #if re.search(r'[()%!"#\$&\'=-^~|{}\[\@:;+*<>]',val):
        if re.search('[!-/:-@[-`{-~]',val):
            raise forms.ValidationError("名前に記号は入れないでください")
            return
class MonsterEffectForm(forms.ModelForm):
    '''
    def clean_monster_effect(self):
        value = self.cleaned_data["monster_effect"]
        return value
        '''
    def clean(self):
        cleaned_data = super().clean()
        val = cleaned_data.get("monster_effect_val")
        if val != 21 and val != 56 and val != 58 and val != 60:
            value = cleaned_data.get("monster_effect")
        return cleaned_data
    def clean_monster_condition(self):
        value = self.cleaned_data["monster_condition"]
        return value
class CostForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        val = cleaned_data.get("cost_val")
        if val != 21 and val != 56 and val != 58 and val != 60:
            value = cleaned_data.get("cost")
        return cleaned_data
    def clean_cost_condition(self):
        value = self.cleaned_data["cost_condition"]
        return value
def isJsonFormat(line):
    try:
        json.loads(line)
    except json.JSONDecodeError as e:
        return False
    # 以下の例外でも捕まえるので注意
    except ValueError as e:
        return False
    except Exception as e:
        return False
    return True
