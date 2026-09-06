from django.contrib import admin
from .models import (Collection, Product, Customer, Order,
                     Profile, Blog, ProductCode, Comment, Festival, InstagramPost)
# Used2B
# from django.contrib.auth.models import User
# is
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User, OtpCode
from django.contrib.auth.models import Group

admin.site.register(ProductCode)
admin.site.register(Festival)
admin.site.register(InstagramPost)


class CommentAdmin(admin.ModelAdmin):
    list_filter = ("confirmed",)

admin.site.register(Comment, CommentAdmin)



class ProductInline(admin.TabularInline):
    model = Product
    fields = ('name',)  # show only product name
    readonly_fields = ('name',)  # make it uneditable in inline
    extra = 0
    show_change_link = True  # makes the name clickable (links to product edit page)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_available', 'pub_date')
    inlines = [ProductInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'collection', 'price', 'is_available', 'pub_date')
    list_filter = ('collection', 'is_available')
admin.site.register(Customer)
admin.site.register(Order)


class ProfileInline(admin.StackedInline):
    model = Profile


# Used2B
# class UserAdmin(admin.ModelAdmin):
#     model = User
#     fields = ['username', 'first_name', 'last_name', 'email']
#     inlines = [ProfileInline]
#
#
# admin.site.unregister(User)
#
#
# admin.site.register(User, UserAdmin)


# is
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    model = User
    inlines = [ProfileInline]
    list_display = ("username", 'phone_number', 'first_name', 'last_name', 'email')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('username', 'phone_number', 'email', 'first_name', 'last_name', 'password')}),
        ('permissions', {'fields': ('is_admin', 'last_login')})
    )

    add_fieldsets = (
        (None, {'fields': ('username', 'phone_number', 'email', 'first_name', 'last_name', 'password1', 'password2')}),
    )

    search_fields = ('username', 'phone_number')
    ordering = ("username",)
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Blog)



@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')