from django import template
register = template.Library()


@register.filter('reportkey')
def reportkey(dict_data, key):
    if key in dict_data:
        return dict_data.get(key)


@register.filter('absolute')
def absolute(data):
    return abs(2*data)


@register.filter('hundredminus')
def hundredminus(data):
    return 100-data


@register.filter('twice')
def twice(data):
    return data*2
