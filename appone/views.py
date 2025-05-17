from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import SignUpForm, BMIForm
from .models import BMIHistory, HealthProgram, Consultant, User
from .decorators import consultant_required
from django.contrib.auth import logout


# ثبت‌نام کاربر
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


# ورود کاربر
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        consultant_code = request.POST.get('consultant_code')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # اگر کد مشاور وارد شده باشد، بررسی می‌کنیم که این کد معتبر باشد
            if consultant_code:
                try:
                    consultant = Consultant.objects.get(code=consultant_code)
                    user.consultant = consultant  # اضافه کردن مشاور به کاربر
                    user.save()
                except Consultant.DoesNotExist:
                    # کد مشاور نامعتبر است، می‌توانید پیامی به کاربر نمایش دهید.
                    pass

            login(request, user)
            return redirect('home')
        else:
            # ورود ناموفق
            return render(request, 'login.html', {'error': 'نام کاربری یا رمز عبور اشتباه است'})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



# صفحه اصلی و محاسبه BMI
def home(request):
    bmi_result = None
    if request.method == 'POST':
        form = BMIForm(request.POST)
        if form.is_valid():
            height_in_meters = form.cleaned_data['height'] / 100
            weight_in_kg = form.cleaned_data['weight']
            bmi = weight_in_kg / (height_in_meters ** 2)
            bmi_result = round(bmi, 2)

            # ذخیره BMI در تاریخچه
            BMIHistory.objects.create(user=request.user, height=form.cleaned_data['height'],
                                      weight=form.cleaned_data['weight'], bmi=bmi_result)
    else:
        form = BMIForm()
    return render(request, 'home.html', {'form': form, 'bmi_result': bmi_result})


# صفحه پروفایل دانش‌آموز
@login_required
def profile(request):
    bmi_history = BMIHistory.objects.filter(user=request.user)
    health_programs = HealthProgram.objects.filter(user=request.user)
    return render(request, 'profile.html', {'bmi_history': bmi_history, 'health_programs': health_programs})


# حذف BMI از تاریخچه
@login_required
def delete_bmi(request, bmi_id):
    bmi_record = get_object_or_404(BMIHistory, id=bmi_id, user=request.user)
    if request.method == "POST":
        bmi_record.delete()
        return redirect('profile')
    return render(request, 'confirm_delete.html', {'bmi_record': bmi_record})


# صفحه داشبورد مشاور
@consultant_required
def consultant_dashboard(request):
    students = User.objects.all()
    return render(request, 'consultant_dashboard.html', {'students': students})


# ارسال برنامه به دانش‌آموز
@consultant_required
def assign_program(request, student_id):
    student = get_object_or_404(User, id=student_id)
    if request.method == 'POST':
        program_text = request.POST.get('program_text')
        consultant = request.user.consultant
        HealthProgram.objects.create(user=student, consultant=consultant, program_text=program_text)
        return redirect('consultant_dashboard')
    return render(request, 'assign_program.html', {'student': student})


# صفحه پروفایل مشاور
@login_required
@consultant_required
def consultant_profile(request):
    consultant = request.user.consultant
    health_programs = HealthProgram.objects.filter(consultant=consultant)
    return render(request, 'consultant_profile.html', {'consultant': consultant, 'health_programs': health_programs})


# مدیریت دانش‌آموزان توسط مشاور
@consultant_required
def manage_students(request):
    students = User.objects.all()
    return render(request, 'manage_students.html', {'students': students})


# خروج از سیستم
def logout_view(request):
    logout(request)
    return redirect('home')  # پس از خروج کاربر به صفحه اصلی هدایت می‌شود
