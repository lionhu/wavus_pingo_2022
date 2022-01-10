from django import template

register = template.Library()  # Djangoのテンプレートタグライブラリ


# カスタムフィルタとして登録する
@register.filter
def orderpluarl(value):
    if value == 1:
        return str(value) + " order"
    else:
        return str(value) + " orders"


@register.filter
def shorten_id(value):
    return str(value)[-8:-1]

@register.filter
def absolute_imageurl(value):
    return "https://online.nichiei.services{}".format(value)


# カスタムタグとして登録する
@register.simple_tag
def multiply6(value1, value2):
    return value1 * value2
