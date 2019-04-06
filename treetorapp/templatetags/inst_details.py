from django import template
register = template.Library()

@register.filter(name='det_on_name')
def det_on_name(value):

    print("sasdasfzsdgmslhwo;ihiats;oih ")
    print(value)
    details = 8
    return details
