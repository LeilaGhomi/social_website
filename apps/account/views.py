from django.contrib import messages, auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, RedirectView, UpdateView
from apps.account.form import AccountCreationForm, UserUpdateForm
from apps.account.models import User, Following, FriendRequest
from .helper import get_random_otp, send_otp, check_otp_expiration
from .tokens import account_activation_token


class RegisterView(CreateView):
    form_class = AccountCreationForm
    template_name = 'account/register_user.html'

    def post(self, request, **kwargs):
        form = AccountCreationForm(request.POST, request.FILES or None)
        if request.POST.get('reg_type') == 'email' and request.POST.get('email') == '':
            messages.error(request, 'Enter your email address')
            return HttpResponseRedirect(reverse('register'))
        elif form['reg_type'] == 'sms' and request.POST.get('phone_number') == '':
            messages.error(request, 'Enter your phone number')
            return HttpResponseRedirect(reverse('register'))
        elif request.POST.get('reg_type') == 'email' and User.objects.filter(email=request.POST.get('email')):
            user = User.objects.get(email=request.POST.get('email'))
            if user.is_active is True:
                messages.error(request, 'There is already an account with this email address! ')
            else:
                user.delete()
                messages.error(request, 'Your previous account deactivated for activate Try again!')
            return HttpResponseRedirect(reverse('register'))
        elif request.POST.get('reg_type') == 'sms' and User.objects.filter(
                phone_number=request.POST.get('phone_number')):
            user = User.objects.get(phone_number=request.POST.get('phone_number'))
            if user.is_active is True:
                messages.error(request, 'There is already an account with this phone number! ')
            else:
                user.delete()
                messages.error(request, 'Your previous account deactivated for activate Try again!')
            return HttpResponseRedirect(reverse('register'))
        else:
            if form.is_valid():

                user = form.save(commit=False)
                if user.reg_type == 'email':
                    user.is_active = False
                    user.save()
                    current_site = get_current_site(request)
                    mail_subject = 'Activate your account.'
                    message = render_to_string('account/acc_active_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                        'token': account_activation_token.make_token(user),
                    })
                    to_email = form.cleaned_data.get('email')
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    email.send()
                    return HttpResponse('Please confirm your email address to complete the registration')
                else:
                    try:
                        mobile = request.POST.get('phone_number')
                        if User.objects.get(phone_number=mobile):
                            user = User.objects.get(phone_number=mobile)
                            otp = get_random_otp()
                            # send_otp(mobile, otp) ## send otp
                            print(otp)
                            user.otp = otp  # save otp
                            user.save()
                            request.session['user_mobile'] = user.mobile
                            return HttpResponseRedirect(reverse('verify'))
                        else:
                            return HttpResponse('phone number is empty')

                    except User.DoesNotExist:
                        mobile = request.POST.get('phone_number')
                        otp = get_random_otp()
                        send_otp(mobile, otp)
                        print(otp)
                        user.otp = otp
                        user.is_active = False
                        user.save()
                        request.session['user_mobile'] = user.phone_number
                        return HttpResponseRedirect(reverse('verify'))

            else:
                form = AccountCreationForm
                if request.POST.get('password1') != request.POST.get('password2'):
                    messages.error(request, 'password mis mach')
                messages.error(request, 'password is too common')
            return render(request, 'account/register_user.html', {'form': form})


def verify(request):
    try:
        mobile = request.session.get('user_mobile')
        if mobile is None:
            user = User.objects.get(phone_number=mobile)
            user.delete()
            return HttpResponse('phone number is empty')

        user = User.objects.get(phone_number=mobile)
        if request.method == "POST":

            # check otp expiration
            if not check_otp_expiration(user.phone_number):
                messages.error(request, "OTP is expired, please try again.")
                return HttpResponseRedirect(reverse('register'))

            if user.otp != int(request.POST.get('otp')):
                messages.error(request, "OTP is incorrect.")
                return HttpResponseRedirect(reverse('verify'))

            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('profile'))

        return render(request, 'account/verify.html', {'mobile': mobile})

    except User.DoesNotExist:
        messages.error(request, "Error accorded, try again.")
        return HttpResponseRedirect(reverse('register'))


class ActivateView(View):
    def get(self, request, uidb64, token):

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('profile'))
        else:
            return HttpResponse('Activation link is invalid!')


class UserName(View):
    """
    To display each account's name in their profile
    """

    def get(self, request):
        username = User.username
        return render(request, 'account/profile.html', {'username': username})


class UserList(ListView):
    """
        show list of users
    """
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserDetail(DetailView):
    """
        show detail of users
    """
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Search(View):
    """
    The account can search among other users
    """

    def get(self, request):
        search_text = request.GET.get('search_text')
        users = None
        results = User.objects.exclude(id=request.user.id,
                                       is_superuser=True)  # name of the active account and admins are not displayed in the list
        if search_text:
            users = User.objects.filter(username__icontains=search_text)
        return render(request, 'account/search.html', {'users': users, "results": results})


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class FollowersList(LoginRequiredMixin, View):
    """
    show list of followers for login user
    """

    def get(self, request):
        person = User.objects.get(id=request.user.id)
        users = person.follower.all()
        context = {'users': users}
        return render(request, 'account/follower_list.html', context)


class FollowingList(View):
    """
   show list of followings for login user
    """

    def get(self, request):
        person = User.objects.get(id=request.user.id)
        users = person.followed.all()
        context = {'users': users}
        return render(request, 'account/followed_list.html', context)


class UpdateUser(UpdateView):
    """
    edit user profile by login user
    """
    model = User
    form_class = UserUpdateForm
    success_url = '/profile/'
    template_name = 'account/edit_user.html'


@login_required
def send_friend_request(request, user_id):
    """
    send friend request from login user to other users
    """
    from_user = request.user
    to_user = User.objects.get(id=user_id)
    friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
    if created:
        messages.error(request, "Request send...")
        return HttpResponseRedirect(reverse('profile'))
    else:
        messages.error(request, "Request was already sent!")
        return HttpResponseRedirect(reverse('profile'))


@login_required
def accept_friend_request(request, request_id):
    """
        accept friend request by login user
    """
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        to_user = friend_request.to_user
        from_user = friend_request.from_user
        following = Following.objects.filter(user=from_user, follower=to_user)
        followers = Following.objects.filter(user=to_user, followed=from_user)
        is_following = True if following else False
        is_follower = True if followers else False

        if not is_following:
            Following.follow(from_user, to_user)

        if not is_follower:
            Following.follow_back(to_user, from_user)
        messages.error(request, "Request accepted")
        return HttpResponseRedirect(reverse('profile'))
    else:
        messages.error(request, "Request not accepted")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_friend_request(request, request_id):
    """
            Delete friend request by login user
        """
    friend_request = FriendRequest.objects.get(id=request_id)
    friend_request.delete()
    messages.error(request, "Request deleted!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class RequestList(View):
    """
    show list of persons that request to login user
    """

    def get(self, request):
        person = User.objects.get(id=request.user.id)
        users = person.to_user.all()
        context = {'users': users}
        return render(request, 'account/requests.html', context)
