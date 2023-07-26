from django.urls import path
from django.views.decorators.cache import cache_page
from news.views import PostList, PostDetail, PostCreate, PostSearch, PostUpdate, PostDelete


urlpatterns = [
   path('', cache_page(60)(PostList.as_view()), name='posts_list'),
   path('create/', PostCreate.as_view()),
   path('search/', cache_page(300)(PostSearch.as_view()), name='post_search'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('<int:pk>/edit', PostUpdate.as_view(), name='post_edit'),
   path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
]
