from django import template

register = template.Library()

'😀 😐 🫩'

@register.filter
def emoji(value):
    if value == 0:
        return '😐'
    elif value > 0:
        return '😀'
    else:
        return '🫩'

bad_words = ['плохое', 'запрещённое', 'грубое']

@register.filter
def censor(value):
    if not isinstance(value, str):
        return value

    result = value
    for word in bad_words:
        import re
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        replacement = '*' * len(word)
        result = pattern.sub(replacement, result)
    return result