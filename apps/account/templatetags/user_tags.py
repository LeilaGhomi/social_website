from django import template

from apps.account.models import User, FriendRequest

register = template.Library()


@register.simple_tag(name='follower_cnt')
def count_follower(request):
    # Count followers
    user = User.objects.get(id=request.user.id)
    return user.follower.count()


@register.simple_tag(name='following_cnt')
def count_followed(request):
    # Count followings
    account = User.objects.get(id=request.user.id)
    return account.followed.count()\


@register.simple_tag(name='r_cnt')
def count_request(request):
    # Count requests
    requests = FriendRequest.objects.filter(to_user=request.user.id)
    return requests.count()
