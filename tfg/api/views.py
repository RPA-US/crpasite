from django.shortcuts import redirect, render, get_object_or_404
from .models import Subscription
from django.contrib.auth.models import User

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