from django import template
from jalali_date import date2jalali, datetime2jalali

register = template.Library()


@register.filter(name='cut')
def cut(value, arg):
    return value.replace(arg, '')


@register.filter(name='show_jalali_date')
def show_jalali_date(value):
    return date2jalali(value)


@register.filter(name='three_digits_currency')
def three_digits_currency(value: int):
    return '{:,}'.format(value) + ' تومان'


@register.filter(name='make_it_range')
def make_it_range(value: int):
    return range(value)


@register.simple_tag
def multiply(quantity, price, *args, **kwargs):
    return three_digits_currency(quantity * price)


@register.filter(name='make_it_month')
def make_it_month(value):
    date = str(date2jalali(value))
    date = date.split('-')[1]
    if date[0] == '0':
        date = date.replace('0', '')
    return date


@register.filter(name='make_it_year')
def make_it_year(value):
    date = str(date2jalali(value))
    return date.split('-')[0]


@register.filter(name='name_of_month')
def name_of_month(value):
    month_list = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'ابان', 'اذر', 'دی', 'بهمن', 'اسفند']
    date = str(date2jalali(value))
    date = date.split('-')[1]
    return month_list[int(date)-1]