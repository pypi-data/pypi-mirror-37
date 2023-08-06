from django.urls import path

from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.BlogHomeView.as_view(), name="home"),
    path('new/', views.NewBlogView.as_view(), name="new"),
    path('<uuid:uuid>/edit/', views.BlogEditView.as_view(), name="edit"),
    path('drafts/', views.BlogDraftView.as_view(), name="drafts"),
    path('<slug:slug>/', views.BlogReadView.as_view(), name="read"),
    path('<uuid:uuid>/publish/', views.BlogPublishView.as_view(), name="publish"),
    path('<uuid:uuid>/delete/', views.BlogDeleteView.as_view(), name="delete"),
]