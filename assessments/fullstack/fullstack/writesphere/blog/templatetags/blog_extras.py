from django import template
from django.db.models import Sum

register = template.Library()

@register.filter
def total_views(posts):
    """Calculate total views for a queryset of posts"""
    return posts.aggregate(total_views=Sum('views_count'))['total_views'] or 0

@register.filter
def status_color(status):
    """Return bootstrap color class based on post status"""
    colors = {
        'published': 'success',
        'draft': 'secondary',
        'archived': 'danger'
    }
    return colors.get(status, 'secondary')

@register.filter
def role_color(role):
    """Return bootstrap color class based on user role"""
    colors = {
        'admin': 'danger',
        'author': 'primary',
        'reader': 'info'
    }
    return colors.get(role, 'secondary')
