from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Permite acessar dicionário pelo template: {{ dict|get_item:'chave' }}"""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None
