from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, ArticleCreate, ChoosePostType


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostsList.as_view(), name='post_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('create/', PostCreate.as_view()),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   path('choose/', ChoosePostType.as_view(), name='choose_post_type'),
]
