from django.db.utils import IntegrityError
from .models import Like, Post, User
from typing import Optional


def toggle_like(like_author: str, liked_post: int) -> Optional[Like]:

    user = User.objects.get(username=like_author)
    post = Post.objects.get(pk=liked_post)

    try:
        return Like.objects.create(creator=user, post=post)
    except IntegrityError:
        Like.objects.get(creator=user, post=post).delete()


def count_likes(post_id: int) -> int:
    post = Post.objects.get(pk=post_id)
    return post.likes.all().count()
