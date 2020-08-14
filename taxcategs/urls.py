from django.urls import path, re_path
from .views import CategoriesListView, CategoryDetailView, AddInputFormatSupportedView, AddKnowledgeSourceView, AddCommentView, AddCategoryTermProposalView, select_proposal_view, ProposalListView, review_multiple_form, CategoriesListReview, TaxCategoryDetailView, taxonomy_view, ProductNavigateCategoryView, CommentListView, export_taxonomy, CommentDetailView, CategTermsListView
from django.contrib.auth.views import LogoutView

app_name = "taxcategs"

urlpatterns = [
    path('listview/', CategoriesListView.as_view(), name="ul_taxonomy"),
    path('navigate/', taxonomy_view, name="categoryterm_list"),
    path('navigate/<int:pk>/', ProductNavigateCategoryView.as_view(), name="product_categoryterm_list"),
    path('view/<int:pk>/', CategoryDetailView.as_view(), name="categoryterm_detail"),
    path('detail/<int:pk>/', TaxCategoryDetailView.as_view(), name="taxcategory_detail"),
    path('review/<int:id>/', review_multiple_form, name="review"),
    path('terms/<int:pk>/', CategTermsListView.as_view(), name="terms"),
]

urlpatterns += [   
    path('select/', select_proposal_view, name='categoryterm_create'),
    path('proposal/', AddCategoryTermProposalView.as_view(), name='categoryterm_proposal'),
    re_path(r'^myproposals/(?:(?P<status>\d)/)?$', ProposalListView.as_view(), name='categoryterm_myproposal'),
    path('input/', AddInputFormatSupportedView.as_view(), name='inputformatsupported_create'),
    path('knowledgesource/', AddKnowledgeSourceView.as_view(), name='knowledgesource_create'),
    re_path(r'^comment/(?:(?P<categterm>\d)/)?$', AddCommentView.as_view(), name='comment_create'),
    path('comment_detail/<int:pk>/', CommentDetailView.as_view(), name="comment_detail"),
    re_path(r'^comment/list/(?:(?P<mine>\d||<pk>\d)/)?$', CommentListView.as_view(), name='comment_list'),
    path('export/', export_taxonomy, name='export'),
    re_path(r'^reviewproposals/(?:(?P<status>\d)/)?$', CategoriesListReview.as_view(), name='categoryterm_proposalreview'),
]