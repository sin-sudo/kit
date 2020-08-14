from django.urls import path

from .views import home, board, topic, new_topic, topic_posts, topic_reply, PostUpdateView

urlpatterns = [
    path('', home, name="home"),
    # 課程別のboardを表示するためにはcourseのpkが必要（boardのpkは必要ない）
    path('course/<int:pk>', board, name="board"),
    path('course/<int:pk>/board/<int:board_pk>', topic, name="topic"),
    # 新しいトピックを追加する為のビューを追加
    path('course/<int:pk>/board/<int:board_pk>/new', new_topic, name="new_topic"),
    path('course/<int:pk>/board/<int:board_pk>/topic/<int:topic_pk>', topic_posts, name="topic_posts"),
    path('course/<int:pk>/board/<int:board_pk>/topic/<int:topic_pk>/reply', topic_reply, name="topic_reply"),
    path('course/<int:pk>/board/<int:board_pk>/topic/<int:topic_pk>/post/<int:post_pk>/edit/', PostUpdateView.as_view(), name="edit_post"),
]
