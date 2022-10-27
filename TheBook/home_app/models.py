from django.db import models
from django.utils import timezone
from login_app.models import CustomUser


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    # slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    likes = models.ManyToManyField(CustomUser, related_name='liked_posts', default=0)

    def total_likes(self):
        return self.likes.count()

    def who_liked(self):
        return self.likes.all()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.SET('User Deleted'), related_name='author_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-publish',)