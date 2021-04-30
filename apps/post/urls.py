from django.urls import path
from .views import MyPostList, PostDetail, like, AddComment, FollowingPost, UpdatePost, post_delete, \
    comment_delete, AddPostView, un_like

urlpatterns = [
    path('', MyPostList.as_view(), name="my_post_list"),
    path('add_post/', AddPostView.as_view(), name="add_new_post"),
    path('<int:pk>/', PostDetail.as_view(), name="post_detail"),
    path('<int:pk>/like', like, name="like"),
    path('<int:pk>/unlike', un_like, name="un_like"),
    path('<int:pk>/comment', AddComment.as_view(), name="comment"),
    path('following_post/', FollowingPost.as_view(), name="following_post"),
    path('edit_post/<int:pk>', UpdatePost.as_view(), name='edit_post'),
    path('post_delete/<int:pk>', post_delete, name="post_delete"),
    path('comment_delete/<int:pk>', comment_delete, name="comment_delete"),
]
