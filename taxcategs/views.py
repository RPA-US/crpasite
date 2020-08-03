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
    InputFormatSupportedForm,
    KnowledgeSourceForm,
    ReportForm,
    CommentForm,
)
import datetime
from django.contrib.auth.decorators import permission_required
from .forms import ProposalCategoryTermForm

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


from django.db.models.signals import pre_save
from django.dispatch import receiver


# @receiver(pre_save, sender=CategoryTerm)
# def handler(sender, instance, **kwargs):
#     if not instance.subject_init:
#         instance.subject_init = instance.subject_initials()


# class CategoryDetailView(DetailView):
#     model = TaxCateg
#     template_name = "categories/detail.html"

class CategoryDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        # if self.request.user.is_authenticated:
        categoryTerm = get_object_or_404(CategoryTerm, pk=kwargs['pk'])
        # else:
		#     return CategoryTerm.objects.none()
        context = {'categoryTerm': categoryTerm}
        return render(request, 'categories/detail.html', context)

class AddCategoryTermProposalView(CreateView):
    # model = CategoryTerm
    form_class = ProposalCategoryTermForm
    template_name = "categories/create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self, *args, **kwargs):
        initial = super(AddCategoryTermProposalView, self).get_initial(**kwargs)
        initial['term'] = 'My term'
        return initial

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AddCategoryTermProposalView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
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
