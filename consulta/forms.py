from django import forms


class SearchGame(forms.Form):
    name = forms.CharField(label="Nombre", required=False, widget=forms.TextInput(
        attrs={'placeholder': 'cuphead, halo infinite, etc'}))
    url = forms.CharField(label="URL", required=False, widget=forms.TextInput(
        attrs={'placeholder': 'https://store.steampowered.com/app/1708091/Halo_Infinite_Campaa/'}))
