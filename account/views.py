from django.shortcuts import render, redirect
from django.contrib.auth import (authenticate, get_user_model, login, logout)
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .forms import *
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from actions.models import Action
from actions.utils import create_action


User = get_user_model()


def index(request):
    return render(request, 'index.html')


def user_login(request):
    context = {}
    login_form = LoginForm(request.POST or None)
    context['login_form'] = login_form
    if login_form.is_valid():
        username = login_form.cleaned_data.get('username', '')
        password = login_form.cleaned_data.get('password', '')

        user = User.objects.filter(
            Q(username__iexact = username) |
            Q(email__iexact = username)
        ).distinct()

        if not user.exists() and user.count() != 1:
            login_message = 'This user does not exist'
            context['login_message'] = login_message
            return render(request, 'registration/login.html', context)

        user = user.first()

        if not user.check_password(password):

            login_message = 'Incorrect password'
            context['login_message'] = login_message
            return render(request, 'registration/login.html', context)

        login(request, user, backend = 'django.contrib.auth.backends.ModelBackend')
        return redirect('dashboard')
    return render(request, "registration/login.html", context)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit = False)
            new_user.set_password(user_form.cleaned_data['password'])
            Profile.objects.create(user=new_user)
            create_action(new_user, 'has_created_account')
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user' : new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'user_form': user_form})


def logout_view(request):
    logout(request)
    return render(request, 'registration/logged_out.html')


@login_required
def dashboard(request):
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',
                                                       flat=True)
    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]

    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard',
                   'actions': actions})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance = request.user, data = request.POST)
        profile_form = ProfileEditForm(instance = request.user.profile,
                                       data = request.POST,
                                       files = request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile update successfully')
        else:
            messages.error(request, 'Error')
    else:
        user_form = UserEditForm(instance = request.user)
        profile_form = ProfileEditForm(instance = request.user.profile)

    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form':profile_form})

@login_required
def user_list(request):
    users = User.objects.filter(is_active = True)
    return render(request,
                  'account/user/list.html',
                  {'section': 'people', 'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request,
                  'account/user/detail.html',
                  {'section': 'people', 'user': user})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
                create_action(request.user, 'is_following', user)
                # create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})



# def user_login(request):
#     username = request.POST.get('username','')
#     password = request.POST.get('password', '')
#     user = authenticate(username = username, password = password)
#
#
#     if user is not None:
#         if user.is_active:
#             login(request, user)
#             return HttpResponse('Authenticated successfully')
#         else:
#             return HttpResponse('Disabled account')
#     else:
#         return HttpResponse('Invalid login')
