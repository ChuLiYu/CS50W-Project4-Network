from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    created_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    context = models.TextField(max_length=200)


class Following(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )

    followee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followee"
    )

    class Meta:
        unique_together = ("follower", "followee")


class Like(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="liked by")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"{self.creator} likes post {self.post.id}"

    class Meta:
        unique_together = ("creator", "post")


# class Comment(models.Model):
#     creator = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="Commented by")
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     context=models.TextField()
