from django import forms
from .models import *


class PostForm(forms.ModelForm):
    main_image = forms.ImageField(
        label="메인 사진 :",
    )

    field_order = [
        "main_image",
    ]

    class Meta:
        model = Post
        fields = ["main_image"]


class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        label="사진 추가 :",
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
    )

    class Meta:
        model = Image
        fields = ["image"]


class PostingCommentForm(forms.ModelForm):
    text = forms.CharField(
        max_length=100,
        label="내용 :",
        required=False,
    )

    class Meta:
        model = Comment
        fields = ["text"]


class UserImageForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
    )

    class Meta:
        model = Image
        fields = ["image"]
