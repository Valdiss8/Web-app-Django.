from django import template

register = template.Library()

@register.filter
def index_even(value, my_list):
    for index in range(len(my_list)):
        if value == my_list[index]:
            if index % 2 == 0:
                return True
            else:
                return False



