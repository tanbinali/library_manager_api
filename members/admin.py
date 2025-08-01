from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Member, BorrowRecord

admin.site.register(Member, UserAdmin)
admin.site.register(BorrowRecord)
