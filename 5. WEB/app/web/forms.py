from django import forms


class UploadFileForm(forms.Form):
    name = forms.CharField()
    external_id = forms.CharField()
    rc = forms.CharField()
    buyed_price = forms.CharField()
    account = forms.IntegerField()
    file = forms.FileField()


class AddressCadastreForm(forms.Form):
    road = forms.IntegerField()
    number = forms.CharField()
    block = forms.CharField(required=False)
    stairs = forms.CharField(required=False)
    floor = forms.CharField(required=False)
    door = forms.FileField(required=False)
