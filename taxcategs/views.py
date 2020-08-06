from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, FormView, DeleteView
from .models import (
    TaxCateg,
    CategoryTerm,
    InputFormatSupported,
    KnowledgeSource,
    Report,
    Comment,
)
from taxcategs.forms import (
    ProposalCategoryTermForm,
    ProposalReviewForm,
    InputFormatSupportedForm,
    KnowledgeSourceForm,
    ReportForm,
    CommentForm,
)
import datetime
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required
from .forms import ProposalCategoryTermForm
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your views here.
class CategoriesListView(ListView):
    model = TaxCateg
    queryset = TaxCateg.objects.all()
    paginate_by = 50
    template_name = "categories/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categTerms"] = CategoryTerm.objects.filter(
            active=True, is_tax_categ=True
        ).all()
        return context


class ProposalListView(ListView):
    model = CategoryTerm
    template_name = 'categories/user-proposal-list.html'
    context_object_name = 'proposals'
    paginate_by = 10
    ordering = ['-created_at']
    def get_queryset(self):
        return CategoryTerm.objects.filter(user=self.request.user, active=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["activeCategTerms"] = CategoryTerm.objects.filter(
            active=True, user=self.request.user
        ).all()
        context["taxCategTerms"] = CategoryTerm.objects.filter(
            active=True, user=self.request.user, is_tax_categ=True
        ).all()
        return context


class CategoriesAcceptedListView(ListView):
    model = CategoryTerm
    queryset = CategoryTerm.objects.filter(active=True)
    paginate_by = 5
    template_name = "categories/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Accepted proposals"
        return context



class CategoryDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        # if self.request.user.is_authenticated:
        categoryTerm = get_object_or_404(CategoryTerm, pk=kwargs['pk'])
        # else:
		#     return CategoryTerm.objects.none()
        context = {'categoryTerm': categoryTerm}
        return render(request, 'categories/detail.html', context)

class AddCategoryTermProposalView(CreateView):
    model = CategoryTerm
    form_class = ProposalCategoryTermForm
    template_name = "categories/create.html"

    def form_valid(self, form):
        # self.object = form.save(commit=False)
        # self.object.user = self.request.user
        # self.object.formats_supported.set(None)
        # saved = self.object.save()
        form.cleaned_data.update({'active': False})
        form.cleaned_data.update({'is_tax_categ': False})
        if form.taxcategdecision == '1':
            form.cleaned_data.update({'substitute_tax_categ': True})
        else:
            form.cleaned_data.update({'substitute_tax_categ': False})
        self.object = CategoryTerm.create(self, form.cleaned_data)
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self, *args, **kwargs):
        initial = super(AddCategoryTermProposalView, self).get_initial(**kwargs)
        # initial['term'] = 'My term'
        return initial

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AddCategoryTermProposalView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        kwargs['taxcategdecision'] = self.request.GET["taxcateg"]
        return kwargs

    # fields = '__all__'
    # fields = ('title', 'body')

    # def get(self, request, *args, **kwargs):
    #     context = {'form': ProposalCategoryTermForm()}
    #     return render(request, 'books/cat_term-create.html', context)

    # def post(self, request, *args, **kwargs):
    #     form = ProposalCategoryTermForm(request.POST)
    #     if form.is_valid():
    #         cat_term = form.save()
    #         cat_term.creator = request.user
    #         cat_term.save()
    #         return HttpResponseRedirect(reverse_lazy('categories:categoryterm_list', args=[cat_term.id]))
    #     return render(request, 'categories/create.html', {'form': form})

class ReviewCategoryTermProposalView(FormView):
    model = CategoryTerm
    form_class = ProposalCategoryTermForm
    template_name = "categories/edit.html"
    # fields = '__all__'
    # fields = ('title', 'body')

class AddInputFormatSupportedView(CreateView):
    model = InputFormatSupported
    form_class = InputFormatSupportedForm
    template_name = "categories/create-inputformat.html"


class AddKnowledgeSourceView(CreateView):
    model = KnowledgeSource
    form_class = KnowledgeSourceForm
    template_name = "categories/create-source.html"

class AddReportView(CreateView):
    model = Report
    form_class = ReportForm
    template_name = "categories/create-report.html"


class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "categories/create-comment.html"

class CategoriesRefusedListView(ListView):
    queryset = CategoryTerm.objects.filter(decision='KO').all()
    paginate_by = 5
    template_name = "categories/list.html"

class CategoriesToReviewListView(ListView):
    # Blog.objects.exclude(
    # entry__in=Entry.objects.filter(
    #     headline__contains='Lennon',
    #     pub_date__year=2008,
    # ),
    # )
    # subs = Report.objects.all()
    # locs = []
    # for sub in subs:
    #     locs.append(Location.objects.get(id=sub.location_id, is_active=True))
    # queryset = locs
    queryset = CategoryTerm.objects.filter(active=False, decision__isnull=True)#exclude(decision__exact="")
    paginate_by = 5
    template_name = "categories/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Proposals for review"
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Refused proposals"
        return context

def multiple_forms(request):
    if request.method == 'POST':
        report_form = ReportForm(request.POST)
        category_term_form = ProposalReviewForm(request.POST)
        if report_form.is_valid() or category_term_form.is_valid():
            # Do the needful
            return HttpResponseRedirect(reverse('taxcategs:proposalsToReview') )
    else:
        report_form = ReportForm()
        category_term_form = ProposalReviewForm()

    context = {
        'report_form': report_form,
        'category_term_form': category_term_form,
    }

    return render(request, 'categories/create-report.html', context)

def select_proposal_view(request):
    return render(request, "categories/proposal.html")



def accept_proposal(request):
    form = ProposalReviewForm(request.POST or None)

    if form.is_valid():
        data = form.cleaned_data
        role = data.get("role")
        # Checking: user cannot register as Reviewer
        if role == "1":
            term = data.get("term")
            description = data.get("description")
            formats_supported = data.get("formats_supported")
            categoryChars = data.get("categoryChars")
            new_user = User.objects.create_user(
                categoryChars, term, description, formats_supported, int(role)
            )
        else:
            new_user = None
        if new_user is not None:
            messages.success(request, "Created User.")
            return redirect("accounts:login")

        messages.warning(request, "Create Error !")

    context = {"form": form}

    return render(request, "accounts/register.html", context)

    def listing(request):
        contact_list = Contact.objects.all()
        paginator = Paginator(contact_list, 25) # Show 25 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'list.html', {'page_obj': page_obj})