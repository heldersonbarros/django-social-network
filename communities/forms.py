from django import forms
from .models import Community

class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ('title', 'description', 'image',)

        widgets = {
            'title': forms.TextInput(attrs={'class': "form-input"}),
            'description': forms.TextInput(attrs={'class': "form-input"}),
            'image': forms.FileInput(attrs={'class': "form-input"}),
        }