from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from api.forms import SignUpForm, ProfileForm
from .models import Subscription
from django.contrib.auth.models import User

# Sign Up View
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'commons/signup.html'

# Edit Profile View
class ProfileView(UpdateView):
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('home')
    template_name = 'commons/profile.html'

# Create your views here.
def subscription_list(request):
    subscriptions = Subscription.public.all()
    context = {'subscriptions': subscriptions}
    return render(request, 'api/subscription_list.html', context)

def subscription_user(request, username):
    user = get_object_or_404(User, username=username)
    if request.user == user:
        subscriptions = user.subscriptions.all()
    else:
        subscriptions = Subscription.public.filter(owner__username=username)
    context = {'subscriptions': subscriptions, 'owner': user}
    return render(request, 'api/subscription_user.html', context)