# coding=utf-8

from django.contrib import admin
from .models import Member

# Register your models here.


class MemberAdmin(admin.ModelAdmin):
    list_display = 'username', 'password'

    # def save_model(self, request, obj, form, change):
    #     user = str(obj).split(':')
    #     if change:
    #         memberManager.change_password(user)
    #         obj.save()
    #     else:
    #         if memberManager.exist(user[0]) != -1:
    #             print "username" + user[0] + "has existed"
    #         else:
    #             memberManager.store_members(user)
    #             obj.save()
    #
    # def delete_model(self, request, obj):
    #     username = str(obj).split(':')[0]
    #     obj.delete()
    #     memberManager.delete_members(username)


admin.site.register(Member, MemberAdmin)
