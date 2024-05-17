from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    content = forms.CharField(min_length=5)

    class Meta:
        model = Post
        fields = ['title', 'content', 'categories', 'author']

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        title = cleaned_data.get("title")

        if title == content:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data