from django.urls import path, re_path
from .views import CategoriesListView, CategoryDetailView, ReviewCategoryTermProposalView, AddInputFormatSupportedView, AddKnowledgeSourceView, AddReportView, AddCommentView, AddCategoryTermProposalView, select_proposal_view, ReviewCategoryTermProposalView, ProposalListView, review_multiple_form, CategoriesListReview, TaxCategoryDetailView, taxonomy_view, ProductNavigateCategoryView
from django.contrib.auth.views import LogoutView

app_name = "taxcategs"

urlpatterns = [
    path('listview/', CategoriesListView.as_view(), name="animated_taxonomy"),
    path('navigate/', taxonomy_view, name="categoryterm_list"),
    path('navigate/<int:pk>/', ProductNavigateCategoryView.as_view(), name="product_categoryterm_list"),
    path('view/<int:pk>/', CategoryDetailView.as_view(), name="categoryterm_detail"),
    path('detail/<int:pk>/', TaxCategoryDetailView.as_view(), name="taxcategory_detail"),
    path('review/<int:id>/', review_multiple_form, name="review"),
]

urlpatterns += [   
    path('select/', select_proposal_view, name='categoryterm_create'),
    path('proposal/', AddCategoryTermProposalView.as_view(), name='categoryterm_proposal'),
    re_path(r'^myproposals/(?:(?P<status>\d)/)?$', ProposalListView.as_view(), name='categoryterm_myproposal'),
    path('input/', AddInputFormatSupportedView.as_view(), name='inputformatsupported_create'),
    path('knowledgesource/', AddKnowledgeSourceView.as_view(), name='knowledgesource_create'),
    path('report/', AddReportView.as_view(), name='report_create'),
    path('comment/', AddCommentView.as_view(), name='comment_create'),
    path('edit/', ReviewCategoryTermProposalView.as_view(), name='categoryterm_edit'),
    re_path(r'^reviewproposals/(?:(?P<status>\d)/)?$', CategoriesListReview.as_view(), name='categoryterm_proposalreview'),
]