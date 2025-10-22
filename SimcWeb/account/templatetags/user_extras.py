from django import template

register = template.Library()

@register.filter
def iniciais(nome):
    """
    Retorna as iniciais de um nome (ex: Nathalia Mariano -> NM)
    """
    if not nome:
        return ""
    partes = nome.strip().split()
    iniciais = "".join([parte[0].upper() for parte in partes[:2]])
    return iniciais