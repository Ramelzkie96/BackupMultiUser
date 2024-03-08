from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, AdminPasswordChangeForm
from .models import User
from .forms import SignUpForm

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class MyUserAdmin(BaseUserAdmin):
    form = MyUserChangeForm
    add_form = SignUpForm
    change_password_form = AdminPasswordChangeForm

    list_display = ('username', 'email', 'is_admin', 'is_employee', 'is_customer')
    list_filter = ('is_admin', 'is_employee', 'is_customer')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_admin', 'is_employee', 'is_customer')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_admin', 'is_employee', 'is_customer'),
        }),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)

    def change_user_password(self, request, id, form_url=''):
        user = self.get_object(request, id)
        if user is not None:
            if request.method == 'POST':
                form = self.change_password_form(user, request.POST)
                if form.is_valid():
                    form.save()
            else:
                form = self.change_password_form(user)
            return self.render_change_form(request, form, change=True, obj=user, form_url=form_url)

admin.site.register(User, MyUserAdmin)
