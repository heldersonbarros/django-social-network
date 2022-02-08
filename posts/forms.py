from django import forms
from django.forms import ValidationError
from django.core.files.images import get_image_dimensions

from .models import User, Post, Community, Comment
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm

#verificar o nome das classes(ingles incorreto)
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','image',)


        widgets = {
            'title': forms.TextInput(attrs={'class': "form-input"}),
            'image': forms.FileInput(attrs={'class': "form-input"}),
        }

        labels = {
            'title': "Post title",
            'image': "Choose an image",
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise ValidationError("This field is required.")
        else:
            width, height = get_image_dimensions(image)

            if width != 600:
               raise ValidationError("Width should be 600px")
            if height < 300 or height > 600:
               raise ValidationError("Height should be >= 300 and <= 600px")
            
            if image.size > 1024*1024:
                raise ValidationError("Image file too large > 1mb")
        return image

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)