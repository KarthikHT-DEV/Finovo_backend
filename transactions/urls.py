from django.urls import path
from django.http import HttpResponse
from .views import (
    DashboardView, AnalyticsView, CategoryListView, 
    TransactionListCreateView, BudgetView, TransactionDetailView,
    TransactionFavoriteView, TransactionUnfavoriteView,
    NotificationListView, NotificationReadView,
    NotificationStarView, NotificationClearView, NotificationBulkDeleteView,
)

urlpatterns = [
    path('hello/',       lambda r: HttpResponse("HELLO TXN"), name='hello-txn'),
    path('dashboard/',   DashboardView.as_view(),             name='dashboard'),
    path('analytics/',   AnalyticsView.as_view(),             name='analytics'),
    path('categories/',  CategoryListView.as_view(),          name='category-list'),
    path('budgets/',     BudgetView.as_view(),                name='budgets'),
    path('notifications/', NotificationListView.as_view(),    name='notification-list'),
    path('notifications/read/', NotificationReadView.as_view(), name='notification-read'),
    path('notifications/clear/', NotificationClearView.as_view(), name='notification-clear'),
    path('notifications/bulk-delete/', NotificationBulkDeleteView.as_view(), name='notification-bulk-delete'),
    path('notifications/<int:pk>/star/', NotificationStarView.as_view(), name='notification-star'),
    path('<int:pk>/favorite/', TransactionFavoriteView.as_view(), name='transaction-favorite'),
    path('<int:pk>/unfavorite/', TransactionUnfavoriteView.as_view(), name='transaction-unfavorite'),
    path('<int:pk>/',    TransactionDetailView.as_view(),     name='transaction-detail'),
    path('',             TransactionListCreateView.as_view(), name='transaction-list-create'),
]
