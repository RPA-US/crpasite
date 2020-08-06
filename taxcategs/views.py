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
from django.core.exceptions import ValidationError
from django.contrib import messages
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

# TODO
class CategoriesListView(ListView):
    model = TaxCateg
    template_name = "categories/taxcategs.html"
    paginate_by = 50

    def get_queryset(self):
        return TaxCateg.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categTerms"] = CategoryTerm.objects.filter(
            active=True, is_tax_categ=True
        )
        return context


class ProposalListView(ListView):
    model = CategoryTerm
    template_name = "categories/user-proposal-list.html"
    context_object_name = "proposals"
    paginate_by = 10
    ordering = ["-created_at"]

    def get_queryset(self):
        status = self.request.GET.get("status", None)
        if status and status == "1":
            q = CategoryTerm.objects.filter(user=self.request.user, active=False)
        elif status == "3":
            q = CategoryTerm.objects.filter(active=True, user=self.request.user, is_tax_categ=True)
        else:
            q = CategoryTerm.objects.filter(active=True, user=self.request.user, is_tax_categ=False)
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = self.request.GET.get("status", None)
        if status and status == "1":
            c = "Pending"
        elif status == "3":
            c = "Accepted: Taxonomic categories"
        else:
            c = "Accepted: Category terms"
        context["status"] = c
        return context



class CategoryDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        # if self.request.user.is_authenticated:
        categoryTerm = get_object_or_404(CategoryTerm, pk=kwargs["pk"])
        # else:
        #     return CategoryTerm.objects.none()
        context = {"categoryTerm": categoryTerm}
        return render(request, "categories/detail.html", context)


class AddCategoryTermProposalView(CreateView):
    model = CategoryTerm
    form_class = ProposalCategoryTermForm
    template_name = "categories/create.html"

    def form_valid(self, form):
        # self.object = form.save(commit=False)
        # self.object.user = self.request.user
        # self.object.formats_supported.set(None)
        # saved = self.object.save()
        form.cleaned_data.update({"active": False})
        form.cleaned_data.update({"is_tax_categ": False})
        if form.taxcategdecision == "1":
            form.cleaned_data.update({"substitute_tax_categ": True})
        else:
            form.cleaned_data.update({"substitute_tax_categ": False})
        self.object = CategoryTerm.create(self, form.cleaned_data)
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self, *args, **kwargs):
        initial = super(AddCategoryTermProposalView, self).get_initial(**kwargs)
        # initial['term'] = 'My term'
        return initial

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AddCategoryTermProposalView, self).get_form_kwargs(
            *args, **kwargs
        )
        kwargs["user"] = self.request.user
        kwargs["taxcategdecision"] = self.request.GET["taxcateg"]
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


# TODO
class ReviewCategoryTermProposalView(FormView):
    model = CategoryTerm
    form_class = ProposalCategoryTermForm
    template_name = "categories/edit.html"
    # fields = '__all__'
    # fields = ('title', 'body')

# TODO
class AddInputFormatSupportedView(CreateView):
    model = InputFormatSupported
    form_class = InputFormatSupportedForm
    template_name = "categories/create-inputformat.html"

# TODO
class AddKnowledgeSourceView(CreateView):
    model = KnowledgeSource
    form_class = KnowledgeSourceForm
    template_name = "categories/create-source.html"

# TODO
class AddReportView(CreateView):
    model = Report
    form_class = ReportForm
    template_name = "categories/create-report.html"

# TODO
class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "categories/create-comment.html"

class CategoriesListReview(ListView):
    model = CategoryTerm
    template_name = "categories/list.html"
    context_object_name = "proposals"
    paginate_by = 5
    ordering = ["-created_at"]

    def get_queryset(self):
        status = self.request.GET.get("status", None)
        if status and status == "1":
            q = CategoryTerm.objects.filter(active=True) # ACCEPTED
        elif status == "2":
            q = CategoryTerm.objects.filter(decision="2") #REJECTED
        else:
            q =  CategoryTerm.objects.filter(active=False, decision__exact="")  # exclude(decision__exact="") # PENDING
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = self.request.GET.get("status", None)
        if status and status == "1":
            c = "Accepted proposals"
        elif status == "2":
            c = "Rejected proposals"
        else:
            c = "Proposals for review"
        context["status"] = c
        return context

def review_multiple_form(request, id):
    categterm = CategoryTerm.objects.get(pk=id)
    if request.method == "POST":
        category_term_form = ProposalReviewForm(request.POST)
        report_form = ReportForm(request.POST)
        if report_form.is_valid() and category_term_form.is_valid():
            if (not request.user.is_authenticated) or request.user.role != 1:
                raise ValidationError("Reviewer must be authenticated.")
            categterm_validated_data = category_term_form.cleaned_data
            rep_validated_data = report_form.cleaned_data
            res = rep_validated_data.get("result")
            categterm.description = categterm_validated_data.get("description")
            categterm.categoryChars = categterm_validated_data.get("categoryChars")
            desc = categterm_validated_data.get("decision")
            if desc == "1" or desc == "2":
                context = {
                    "report_form": report_form,
                    "category_term_form": category_term_form,
                }
                if not res:
                    messages.warning(request, "If the proposal has been accepted it must have a result of that acceptance")
                    return render(request, "categories/create-report.html", context)
                if res == "3" or res == "4":
                    if not categterm.substitute_tax_categ:
                        messages.warning(request, "Cannot save a proposal as a taxonomy category if it was not registered that way by its author")
                        return render(request, "categories/create-report.html", context)
                    categterm.active = True
                    categterm.is_tax_categ = True
                elif res == "1" or res == "2":
                    categterm.active = True
                    categterm.is_tax_categ = False
            else:
                if res:
                    raise ValidationError("The report cannot have a reason for acceptance if the proposal has been rejected")

            categterm.save()
            rep_validated_data.update({"categ_term": categterm})
            rep_validated_data.update({"review_user": request.user})
            saved_rep = Report.objects.create(**rep_validated_data)

            return HttpResponseRedirect(reverse("taxcategs:categoryterm_proposalreview"))
    else:
        category_term_form = ProposalReviewForm(instance=categterm)
        report_form = ReportForm()
        
    context = {
        "reptaxcateg": categterm.substitute_tax_categ,
        "report_form": report_form,
        "category_term_form": category_term_form,
    }

    return render(request, "categories/create-report.html", context)


def select_proposal_view(request):
    return render(request, "categories/proposal.html")


def listing(request):
    contact_list = Contact.objects.all()
    paginator = Paginator(contact_list, 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "list.html", {"page_obj": page_obj})

