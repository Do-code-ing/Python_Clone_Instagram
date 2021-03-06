from django import forms
from .models import *
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class PostForm(forms.ModelForm):
    main_image = forms.ImageField(
        label="",
    )

    field_order = [
        "main_image",
    ]

    class Meta:
        model = Post
        fields = ["main_image"]


class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        label="",
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
    )

    class Meta:
        model = Image
        fields = ["image"]


class PostCommentForm(forms.ModelForm):
    text = forms.CharField(
        max_length=200,
        label="",
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': '내용을 입력하세요.',
            'spellcheck': 'false',
        })
    )

    class Meta:
        model = PostComment
        fields = ["text"]


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        label="",
        max_length=200,
        widget=forms.Textarea(attrs={
            'placeholder': '댓글 달기',
            'spellcheck': 'false',
        })
    )

    class Meta:
        model = Comment
        fields = ["text"]


class UserImageForm(forms.ModelForm):
    user_image = forms.ImageField(
        required=False,
        label="프로필 사진 선택",
        label_suffix="",
    )

    class Meta:
        model = Profile
        fields = ["user_image"]


class ProfileForm(forms.ModelForm):
    name = forms.CharField(
        label="이름",
        label_suffix="",
        max_length=50,
        widget=forms.TextInput(attrs={
            'spellcheck': 'false',
        })
    )
    website = forms.CharField(
        label="웹사이트",
        label_suffix="",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '웹사이트',
            'spellcheck': 'false',
        })
    )
    introduction = forms.CharField(
        label="소개",
        label_suffix="",
        max_length=200,
        required=False,
        widget=forms.Textarea(attrs={
            'spellcheck': 'false',
        })
    )

    class Meta:
        model = Profile
        fields = ["name", "website", "introduction"]


# for customizing


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    new_password1 = forms.CharField(
        label=_("새 비밀번호 "),
        label_suffix="",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("새 비밀번호 확인 "),
        label_suffix="",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = {
        **SetPasswordForm.error_messages,
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    }
    old_password = forms.CharField(
        label=_("이전 비밀번호"),
        label_suffix="",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password
