from django.contrib.auth.models import User
from django.db import models

# مدل BMIHistory برای ذخیره تاریخچه BMI دانش‌آموزان
class BMIHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    height = models.FloatField()  # قد دانش‌آموز
    weight = models.FloatField()  # وزن دانش‌آموز
    bmi = models.FloatField()  # شاخص BMI
    date_created = models.DateTimeField(auto_now_add=True)  # زمان ایجاد BMI

    def __str__(self):
        return f"{self.user.username} - {self.bmi}"

# مدل HealthProgram برای ذخیره برنامه‌های غذایی و تمرینی ارسال شده توسط مشاور
class HealthProgram(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    consultant = models.ForeignKey('Consultant', on_delete=models.CASCADE)
    program_text = models.TextField()  # برنامه ارسال شده
    date_assigned = models.DateTimeField(auto_now_add=True)  # زمان ارسال برنامه

    def __str__(self):
        return f"Program for {self.user.username} by {self.consultant.name}"

# مدل Consultant برای ذخیره اطلاعات مشاوران
class Consultant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # نام مشاور
    code = models.CharField(max_length=20, unique=True)  # کد مشاور برای شناسایی
    # شما می‌توانید ویژگی‌های بیشتری برای مشاوران اضافه کنید

    def __str__(self):
        return self.name

    def assign_program(self, student, program_text):
        """ارسال برنامه به دانش‌آموز توسط مشاور"""
        HealthProgram.objects.create(user=student, consultant=self, program_text=program_text)

