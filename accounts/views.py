from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login
from .forms import RegisterForm, LoginForm, GuestForm
from django.views.generic import DetailView
from .models import GuestEmail
from django.utils.http import is_safe_url
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy

User = get_user_model()


def register_page(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        data = form.cleaned_data
        role = data.get("role")
        # Checking: user cannot register as Reviewer
        if role == "2" or role == "3":
            password = data.get("password")
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            email = data.get("email")
            new_user = User.objects.create_user(
                email, password, first_name, last_name, int(role)
            )
        else:
            new_user = None
        if new_user is not None:
            messages.success(request, "Created User.")
            return redirect("accounts:login")

        messages.warning(request, "Create Error !")

    context = {"form": form}

    return render(request, "accounts/register.html", context)


def register_page_reviewer(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        data = form.cleaned_data
        # Checking: user cannot create a Reviewer account, only Reviewers can create others Reviewers accounts
        if request.user.is_authenticated and (request.user.role == 1):
            password = data.get("password")
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            email = data.get("email")
            role = "1"
            new_user = User.objects.create_user(
                email, password, first_name, last_name, int(role)
            )
        else:
            new_user = None
        if new_user is not None:
            messages.success(request, "Reviewer created.")
            return redirect("accounts:reviewer_register")

        messages.warning(request, "Create Error !")

    context = {"form": form}

    return render(request, "accounts/register_reviewer.html", context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect("home_url")

    form = LoginForm(request.POST or None)
    context = {"form": form}
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None

    if form.is_valid():
        data = form.cleaned_data
        email = data.get("email")
        password = data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session["guest_email_id"]
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("home_url")
        else:
            messages.warning(request, "Credentials error.")

    return render(request, "accounts/login.html", context)


def guest_register_view(request):
    if request.user.is_authenticated:
        return redirect("carts:home")

    form = GuestForm(request.POST or None)
    context = {"form": form}
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None

    if form.is_valid():
        data = form.cleaned_data
        email = data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session["guest_email_id"] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("home_url")

    return render(request, "accounts/login.html", context)

 
class AccountDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        roles = {"1":"Reviewer","2":"Provider","3":"Developer","4":"Administrador"}
        if self.request.user.is_authenticated:
            user = get_object_or_404(User, pk=request.user.pk)
        else:
            user = None
        rol = roles.get(str(user.role))
        context = {'user': user, 'rol': rol}
        return render(request, 'accounts/detail.html', context)


def destroy(request):
    User.objects.filter(pk=request.user.id).update(active=False)
    messages.warning(request, "Deleted User.")
    return HttpResponseRedirect(reverse_lazy('accounts:logout')) 