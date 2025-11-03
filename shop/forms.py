from django.contrib.auth.models import User
# Used to be
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
# is
from django.contrib.auth.forms import SetPasswordForm
from django import forms

# Used2B
# from .models import Profile
# is
from .models import User, Profile
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.validators import MinLengthValidator



class UserInfoForm(forms.ModelForm):
    # Used2B
    # phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}), required=False)

    address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'آدرس اول'}), required=False)
    address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'آدرس دوم'}), required=False)
    city = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شهر'}), required=False)
    state = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'استان'}), required=False)
    zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کدپستی'}), required=False)
    # phase2) country = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کشور'}), required=False)

    class Meta:
        model = Profile
        # Used2B
        # fields = ("phone", 'address1', 'address2', 'city', 'state', 'zipcode', 'country',)
        # is
        fields = ('address1', 'address2', 'city', 'state', 'zipcode', ) # phase 2) deleted country


class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'رمز'
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>رمزتان نباید با سایر اطلاعات شما مشابه باشد</li><li>رمزتان باید حداقل دارای 8 کاراکتر باشد</li><li>رمزتان نباید رمز رایجی باشد</li><li>رمزتان نباید تماما عددی باشد</li></ul>'

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'تکرار رمز'
        self.fields['new_password2'].label = ''
        self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>رمز خود را دوباره وارد کنید</small></span>'

# Used2B
# class UpdateUserForm(UserChangeForm):
#     # hide password stuff
#     password = None
#     # get other fields
#     email = forms.EmailField(label="",
#                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}), required=False)
#     first_name = forms.CharField(label="", max_length=100,
#                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}), required=False)
#     last_name = forms.CharField(label="", max_length=100,
#                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}), required=False)
#
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email',)
#
#     def __init__(self, *args, **kwargs):
#         super(UpdateUserForm, self).__init__(*args, **kwargs)
#
#         self.fields['username'].widget.attrs['class'] = 'form-control'
#         self.fields['username'].widget.attrs['placeholder'] = 'User Name'
#         self.fields['username'].label = ''
#         self.fields[
#             'username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

# Used2B
# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=False)
#     first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), required=False)
#     last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required=False)
#
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
#
#     def __init__(self, *args, **kwargs):
#         super(SignUpForm, self).__init__(*args, **kwargs)
#
#         self.fields['username'].widget.attrs['class'] = 'form-control'
#         self.fields['username'].widget.attrs['placeholder'] = 'User Name'
#         self.fields['username'].label = ''
#         self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
#
#         self.fields['password1'].widget.attrs['class'] = 'form-control'
#         self.fields['password1'].widget.attrs['placeholder'] = 'Password'
#         self.fields['password1'].label = ''
#         self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
#
#         self.fields['password2'].widget.attrs['class'] = 'form-control'
#         self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
#         self.fields['password2'].label = ''
#         self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


# is
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError("Passwords don't match")
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


# is
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='You can change your password using this form...<a href=\"../password/\">this form</a>')

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'email', 'first_name', 'last_name', 'password', 'last_login')


# is
class UserChangeFormUser(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'email', 'first_name', 'last_name',)

    def __init__(self, *args, **kwargs):
         super(UserChangeFormUser, self).__init__(*args, **kwargs)

         self.fields['username'].widget.attrs['class'] = 'form-control'
         self.fields['username'].widget.attrs['placeholder'] = 'نام کاربری'
         self.fields['username'].label = 'نام کاربری'

         self.fields['phone_number'].widget.attrs['class'] = 'form-control'
         self.fields['phone_number'].widget.attrs['placeholder'] = 'شماره تلفن'
         self.fields['phone_number'].label = 'شماره تلفن'

         self.fields['email'].widget.attrs['class'] = 'form-control'
         self.fields['email'].widget.attrs['placeholder'] = 'ایمیل'
         self.fields['email'].label = 'ایمیل'

         self.fields['first_name'].widget.attrs['class'] = 'form-control'
         self.fields['first_name'].widget.attrs['placeholder'] = 'نام'
         self.fields['first_name'].label = 'نام'

         self.fields['last_name'].widget.attrs['class'] = 'form-control'
         self.fields['last_name'].widget.attrs['placeholder'] = 'نام خانوادگی'
         self.fields['last_name'].label = 'نام خانوادگی'




# is
class UserRegistrationForm(forms.Form):
    my_username = forms.CharField(max_length=225, label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام کاربری'}), required=True)
    phone_number = forms.CharField(max_length=11, label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'شماره تماس'}), required=True)
    my_email = forms.EmailField()
    first_name = forms.CharField(max_length=225)
    last_name = forms.CharField(max_length=225)

    password = forms.CharField(widget=forms.PasswordInput, validators=[MinLengthValidator(8)])

    def __init__(self, *args, **kwargs):

        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['my_email'].widget.attrs['class'] = 'form-control'
        self.fields['my_email'].widget.attrs['placeholder'] = 'ایمیل'
        self.fields['my_email'].label = ''
        self.fields['my_email'].help_text = '<span class="form-text text-muted"><small></small></span>'

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'نام'
        self.fields['first_name'].label = ''
        self.fields['first_name'].help_text = '<span class="form-text text-muted"><small></small></span>'

        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'نام خانوادگی'
        self.fields['last_name'].label = ''
        self.fields['last_name'].help_text = '<span class="form-text text-muted"><small></small></span>'

        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'رمز'

        self.fields['password'].label = ''
        self.fields['password'].help_text = '<ul class="form-text text-muted small"><li>رمزتان نباید با سایر اطلاعات شما مشابه باشد</li><li>رمزتان باید حداقل دارای 8 کاراکتر باشد</li><li>رمزتان نباید رمز رایجی باشد</li><li>رمزتان نباید تماما عددی باشد</li></ul>'

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This Email Already Exists')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        user = User.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError("Phone Number Already Exists")

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError("Username Already Exists")


# is
class VerifyCodeForm(forms.Form):
    code = forms.IntegerField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Verify Code'}), required=True)
