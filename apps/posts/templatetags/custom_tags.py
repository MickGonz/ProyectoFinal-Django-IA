from django import template
register = template.Library()

@register.filter
def has_group(user, group_name):
    """
    Verifica si el usuario pertenece a un grupo específico.
    """
    return user.groups.filter(name=group_name).exists()