import django_filters
from django import forms
from .models import Post, Author

class PostFilter(django_filters.FilterSet):
    author = django_filters.ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label="Имя автора",
        empty_label="Любой"
    )
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label="Название"
    )
    create_date = django_filters.DateFilter(
        field_name='created_at',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Позже указанной даты',
        lookup_expr='gt'
    )

    class Meta:
        model = Post
        fields = ['title', 'create_date']



