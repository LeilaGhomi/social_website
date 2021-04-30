from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic.base import View


class LoginView(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        next = request.GET.get('next')
        username = request.POST.get("username")
        password = request.POST.get("password")
        is_logout = request.POST.get("logout")
        message = ''
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user:
                    login(request, user)
                    message = 'login was successful'
                    if next:
                        return redirect(next)
            else:
                message = 'username or password is wrong'
                return render(request, 'index.html', {'message': message})
        elif not username and password:
            message = 'username or password is empty'
            return render(request, 'index.html', {'message': message})
        elif is_logout:
            logout(request)
            # message = 'Logout successful'
        # return render(request, 'account/profile.html', {'message': message})
        return redirect('profile')
