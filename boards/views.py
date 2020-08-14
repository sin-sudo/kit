from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.db.models import Count
from django.views.generic import UpdateView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Course, Board, Topic, Post
from .forms import NewTopicForm, ReplyTopicForm


def home(request):
  courses = Course.objects.all()
  return render(request, 'home.html', {'courses':courses})

def board(request, pk):
  course = get_object_or_404(Course, pk=pk)
  return render(request, 'board.html', {'course':course})

def topic(request, pk, board_pk):
  board = get_object_or_404(Board, course__pk=pk, pk=board_pk)
  # annotateは別のモデルから別のモデルのある値を取得するための関数
  topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts')-1)
  return render(request, 'topics.html', {'board':board, 'topics':topics})

@login_required
def new_topic(request, pk, board_pk):
  board = get_object_or_404(Board, course__pk=pk, pk=board_pk)
  # 今はログイン機能を実装していないのでとりあえずfirst()
  # user = User.objects.first()
  user = request.user

  if request.method == 'POST':
    form = NewTopicForm(request.POST)
    if form.is_valid():
      # この時点ではまだデータベースに保存されない
      topic = form.save(commit=False)
      topic.board = board
      topic.starter = user
      # ここでやっと保存される？
      topic.save()
      post = Post.objects.create(
        message = form.cleaned_data.get('message'),
        topic = topic,
        created_by = user
      )
      return redirect('topic', pk=pk, board_pk=board_pk)
  else:
    form = NewTopicForm()
    # formも辞書として渡す
  return render(request, 'new_topic.html', {'board':board,'form':form})

def topic_posts(request, pk, board_pk, topic_pk):
  topic = get_object_or_404(Topic, pk=topic_pk, board__pk=board_pk, board__course__pk=pk)
  topic.views += 1
  topic.save()
  return render(request, 'topic_posts.html', {'topic':topic})

@login_required
def topic_reply(request, pk, board_pk, topic_pk):
  topic = get_object_or_404(Topic, pk=topic_pk, board__pk=board_pk, board__course__pk=pk)

  user = request.user

  if request.method == 'POST':
    form = ReplyTopicForm(request.POST)
    if form.is_valid():
      # messageに関してはこの中に含まれている？
      post = form.save(commit=False)
      post.topic = topic
      post.created_by = request.user
      post.save()

      # 返信があった時にlast_updatedが更新されるように
      topic.last_updated = timezone.now()
      topic.save()
    return render(request, 'topic_posts.html', {'topic':topic})
  else:
    form = ReplyTopicForm()
    return render(request, 'topic_reply.html', {'topic':topic, 'form':form} )


class PostUpdateView(UpdateView):
  model = Post
  template_name = 'edit_post.html'
  fields = ('message',)
  # URLConfのpkを指定する
  pk_url_kwarg = 'post_pk'
  # テンプレート側で参照する変数名
  context_object_name = 'post'

  def get_queryset(self):
    # これは何を継承している？
    queryset = super().get_queryset()
    # ログインしているユーザによるpostのクエリセットを取得している
    # デフォルトではallですべてのクエリセットを取得している
    return queryset.filter(created_by=self.request.user)
  
  def form_valid(self, form):
    post = form.save(commit=False)
    post.updated_by = self.request.user
    post.updated_at = timezone.now()
    post.save()
    return redirect('topic_posts', pk=post.topic.board.course.pk, board_pk=post.topic.board.pk, topic_pk=post.topic.pk)


# シンプルな書き方
# def new_post(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('post_list')
#     else:
#         form = PostForm()
#     return render(request, 'new_post.html', {'form': form})

