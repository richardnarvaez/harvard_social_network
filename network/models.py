from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    image_url = models.CharField(max_length=500, default='https://cdn.dribbble.com/users/72948/screenshots/1631127/cell311.png')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    target = models.ForeignKey('User', on_delete=models.CASCADE, related_name='folowers')
    follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='targets')

class Post(models.Model):
    content = models.CharField(max_length=255)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='author')
    date = models.DateTimeField(default=datetime.now())
    liked = models.ManyToManyField('User', default=None, blank=True, related_name='post_likes')

    @property
    def num_likes(self):
        return self.liked.all().count()


class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)


    def __str__(self):
        return str(self.post)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="commented by")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(blank=False)
    likes = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True, null=False, blank=True, verbose_name="commented on")

    # Model naming
    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"
        ordering = ["date"]

    def __str__(self):
        return f"Comment {self.id} made by {self.user} on post {self.post_id} on {self.date.strftime('%d %b %Y %H:%M:%S')}"





