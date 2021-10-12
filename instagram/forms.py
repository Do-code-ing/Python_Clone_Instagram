from django import forms
from .models import *


class PostForm(forms.ModelForm):
    title = forms.CharField(
        label="제목 :",
    )

    content = forms.CharField(
        label="내용 :",
    )

    main_image = forms.ImageField(
        label="메인 사진 :",
    )

    field_order = [
        "main_image",
        "title",
        "content",
    ]

    class Meta:
        model = Post
        fields = ["title", "content", "main_image"]


class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        label="사진 추가 :",
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
    )

    class Meta:
        model = Image
        fields = ["image"]
