from django.urls import path
from .views import CategoriesListView, CategoryDetailView, ReviewCategoryTermProposalView, AddInputFormatSupportedView, AddKnowledgeSourceView, AddReportView, AddCommentView, AddCategoryTermProposalView, select_proposal_view, ReviewCategoryTermProposalView, ProposalListView, CategoriesToReviewListView, CategoriesAcceptedListView, CategoriesRefusedListView
from django.contrib.auth.views import LogoutView

app_name = "taxcategs"

urlpatterns = [
    path('navigate/', CategoriesListView.as_view(), name="categoryterm_list"),
    path('view/<int:pk>/', CategoryDetailView.as_view(), name="categoryterm_detail"),
    path('review/', ReviewCategoryTermProposalView.as_view(), name="review"),
]

urlpatterns += [   
    path('select/', select_proposal_view, name='categoryterm_create'),
    path('proposal/', AddCategoryTermProposalView.as_view(), name='categoryterm_proposal'),
    path('myproposals/', ProposalListView.as_view(), name='categoryterm_myproposal'),
    path('proposalsToReview/', CategoriesToReviewListView.as_view(), name='categoryterm_proposalreview'),
    path('acceptedProposals/', CategoriesAcceptedListView.as_view(), name='categoryterm_proposalaccepted'),
    path('refusedProposals/', CategoriesRefusedListView.as_view(), name='categoryterm_proposalrefused'),
    path('input/', AddInputFormatSupportedView.as_view(), name='inputformatsupported_create'),
    path('knowledgesource/', AddKnowledgeSourceView.as_view(), name='knowledgesource_create'),
    path('report/', AddReportView.as_view(), name='report_create'),
    path('comment/', AddCommentView.as_view(), name='comment_create'),
    path('edit/', ReviewCategoryTermProposalView.as_view(), name='categoryterm_edit'),
]