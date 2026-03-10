from django import template

register = template.Library()

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
