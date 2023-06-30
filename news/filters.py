from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateFilter, DateFromToRangeFilter
from django import forms

from news.models import Author, Category


class DateInput(forms.DateInput):
    input_type = 'date'


class PostFilter(FilterSet):
    author = ModelChoiceFilter(field_name='author',
                               label='Автор',
                               empty_label='Все авторы',
                               queryset=Author.objects.all(),)
    name = CharFilter(field_name='name', lookup_expr='contains', label='Наименование')
    datetime_in = DateFilter(field_name='datetime_in', lookup_expr='gt', label='Дата публикации', widget=DateInput)
    category = ModelChoiceFilter(field_name='category',
                                 label='Категория',
                                 empty_label='Все категории',
                                 queryset=Category.objects.all())
