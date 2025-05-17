from django.contrib import admin
from .models import BMIHistory, HealthProgram, Consultant, User

# مدیریت BMIHistory
class BMIHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'height', 'weight', 'bmi', 'date_created')
    search_fields = ('user__username', 'bmi')  # امکان جستجو بر اساس نام کاربری یا BMI
    list_filter = ('date_created',)  # فیلتر تاریخ ایجاد
    ordering = ('-date_created',)  # ترتیب بر اساس تاریخ جدیدتر

# مدیریت HealthProgram
class HealthProgramAdmin(admin.ModelAdmin):
    list_display = ('user', 'consultant', 'program_text', 'date_assigned')
    search_fields = ('user__username', 'consultant__name')
    list_filter = ('date_assigned',)
    ordering = ('-date_assigned',)

# مدیریت Consultant
class ConsultantAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'code')  # نمایش نام مشاور، نام کاربری و کد مشاور
    search_fields = ('name', 'code')  # جستجو بر اساس نام مشاور یا کد مشاور
    ordering = ('name',)  # مرتب‌سازی بر اساس نام مشاور

# نمایش مشاوران در مدیریت
admin.site.register(Consultant, ConsultantAdmin)

# ثبت BMIHistory در مدیریت
admin.site.register(BMIHistory, BMIHistoryAdmin)

# ثبت HealthProgram در مدیریت
admin.site.register(HealthProgram, HealthProgramAdmin)

# ثبت User (در صورتی که نیاز به مدیریت خاص دارید)
# اگر شما از User مدیریت پیش‌فرض استفاده می‌کنید، نیاز به ثبت دوباره آن نیست.
# در غیر این صورت، می‌توانید کاربری‌های خاصی برای مدیریت مشاوران اضافه کنید.

