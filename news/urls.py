from django.urls import path
from news.views import PostList, PostDetail, PostCreate, PostSearch, PostUpdate, PostDelete


urlpatterns = [
   path('', PostList.as_view(), name='posts_list'),
   path('create/', PostCreate.as_view()),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('<int:pk>/edit', PostUpdate.as_view(), name='post_edit'),
   path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
]
