# fitness/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import BMIHistory, HealthProgram

# فرم ثبت‌نام برای کاربران جدید
class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# فرم ورود برای کاربران
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='نام کاربری', max_length=100)
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)
    consultant_code = forms.CharField(label='کد مشاور (اختیاری)', max_length=20, required=False)


# فرم محاسبه BMI
class BMIForm(forms.Form):
    height = forms.FloatField(label='قد (سانتی‌متر)', min_value=1)
    weight = forms.FloatField(label='وزن (کیلوگرم)', min_value=1)

    def calculate_bmi(self):
        """محاسبه BMI"""
        height_in_meters = self.cleaned_data['height'] / 100
        weight_in_kg = self.cleaned_data['weight']
        bmi = weight_in_kg / (height_in_meters ** 2)
        return round(bmi, 2)

# فرم ارسال برنامه توسط مشاور
class HealthProgramForm(forms.Form):
    program_text = forms.CharField(widget=forms.Textarea, label="متن برنامه", max_length=1000)

    def clean_program_text(self):
        program_text = self.cleaned_data.get('program_text')
        if len(program_text) < 10:
            raise forms.ValidationError("متن برنامه باید حداقل 10 کلمه باشد.")
        return program_text
