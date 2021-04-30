from django import template
from ..models import Post

register = template.Library()


@register.simple_tag(name='p_cnt')
def count_post(pk):
    # count posts of user
    return Post.objects.filter(account_id=pk).count()


@register.simple_tag(name='l_cnt')
def count_like(pk):
    # count likes of post
    post = Post.objects.get(pk=pk)
    return post.like_set.count()


@register.simple_tag(name='c_cnt')
def count_comment(pk):
    # count comments of post
    post = Post.objects.get(pk=pk)
    return post.comment_set.count()


@register.inclusion_tag('post/post_comments.html')
def show_comments(pk, user):
    # show comment of post
    post = Post.objects.get(pk=pk)
    comments = post.comment_set.all()
    return {'comments': comments, 'user': user, 'post': post}


@register.inclusion_tag('post/user_post.html')
def user_post(user):
    # show post of user
    posts = user.post_set.all()
    return {'posts': posts}


@register.filter(name='l_ch')
def like_check(post, user):
    # check that user like this post or not
    like = post.like_set.filter(user_id=user)
    if len(like):
        return False
    return True
