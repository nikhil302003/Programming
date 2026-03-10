from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import path
from django.template.response import TemplateResponse
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'date_joined', 'last_login', 'reset_password_button')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'bio', 'profile_picture', 'website', 'twitter_handle')}),
        (_('Permissions'), {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('date_joined', 'last_login')
    
    actions = ['reset_password']
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:user_id>/reset-password/', self.admin_site.admin_view(self.reset_password_view), name='auth_user_reset_password'),
        ]
        return custom_urls + urls
    
    def reset_password(self, request, queryset):
        """Admin action to reset passwords for selected users"""
        count = queryset.count()
        # Set a temporary password for all selected users
        for user in queryset:
            user.set_password('temp123456')
            user.save()
        
        self.message_user(request, f'Password reset to "temp123456" for {count} user(s). Users should change this on first login.', messages.WARNING)
    
    reset_password.short_description = 'Reset selected users passwords to "temp123456"'
    
    def reset_password_button(self, obj):
        """Add a reset password button to each user row"""
        from django.urls import reverse
        from django.utils.safestring import mark_safe
        url = reverse('admin:auth_user_reset_password', args=[obj.pk])
        return mark_safe(f'<a href="{url}" class="button">Reset Password</a>')
    
    reset_password_button.short_description = 'Reset Password'
    reset_password_button.allow_tags = True
    
    def reset_password_view(self, request, user_id):
        """Individual user password reset view"""
        user = get_object_or_404(User, pk=user_id)
        
        if request.method == 'POST':
            form = AdminPasswordChangeForm(user, request.POST)
            if form.is_valid():
                form.save()
                self.message_user(request, f'Password for {user.username} has been changed successfully.', messages.SUCCESS)
                return redirect('admin:auth_user_changelist')
        else:
            form = AdminPasswordChangeForm(user)
        
        context = {
            **self.admin_site.each_context(request),
            'title': f'Change password: {user.username}',
            'form': form,
            'user': user,
            'opts': self.model._meta,
            'is_popup': False,
            'save_as': False,
            'has_change_permission': True,
            'has_add_permission': False,
            'has_delete_permission': False,
        }
        
        return TemplateResponse(request, 'admin/auth/user/change_password.html', context)
