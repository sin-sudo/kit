from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator

# home.htmlに使う
class Course(models.Model):
  course_name = models.CharField(max_length = 30)

  def __str__(self):
    return self.course_name

# 課程別のboards.htmlに使う
class Board(models.Model):
  name = models.CharField(max_length = 30)
  description = models.CharField(max_length = 100)
  course = models.ForeignKey(Course, on_delete = models.CASCADE, related_name = 'boards')

  def __str__(self):
    return self.name

  def get_topics_count(self):
    return Topic.objects.filter(board = self).count()
  
  def get_posts_count(self):
    return Post.objects.filter(topic__board = self).count()

  def get_last_post(self):
    return Post.objects.filter(topic__board = self).order_by('-created_at').first()

# トピックを表示するtopics.htmlに使う
class Topic(models.Model):
  subject = models.CharField(max_length=255)
  last_updated = models.DateTimeField(auto_now_add=True)
  board = models.ForeignKey(Board, related_name='topics', on_delete = models.CASCADE)
  starter = models.ForeignKey(User, related_name='topics', on_delete = models.CASCADE)
  views = models.PositiveIntegerField(default=0)

  def __str__(self):
    return self.subject

# 返信一覧を表示するtopic_posts.htmlに使う
class Post(models.Model):
  message = models.TextField(max_length=4000)
  topic = models.ForeignKey(Topic, related_name='posts', on_delete = models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True)
  created_by = models.ForeignKey(User, related_name='posts', on_delete = models.CASCADE)
  updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete = models.CASCADE)

  def __str__(self):
    # このメソッドで30字に切り詰めた文字列をリターンする
    truncated_message = Truncator(self.message)
    return truncated_message.chars(30)