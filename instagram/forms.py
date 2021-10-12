from django import forms
from .models import *


class PostForm(forms.ModelForm):
    title = forms.CharField(
        label="제목 :",
    )

    content = forms.CharField(
        label="내용 :",
    )

    field_order = [
        "title",
        "content",
    ]

    class Meta:
        model = Post
        fields = ["title", "content"]


class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        label="사진: ",
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
    )

    class Meta:
        model = Image
        fields = ["image"]
