from django import forms

class PlotForm(forms.Form):
    start = forms.DateField(widget=forms.DateInput(attrs={'type':'timestamp'}))
    end = forms.DateField(widget=forms.DateInput(attrs={'type':'timestamp'}))
                            