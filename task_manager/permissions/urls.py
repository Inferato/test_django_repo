from django.urls import path
from permissions.views import list_users, manage_permissions, tags_page


urlpatterns = [
    path('user-list/', list_users, name='user_list'),
    path('manage-permissions/<int:user_id>/', manage_permissions, name='manage_permissions'),
    path('tags/', tags_page, name='tags_page')
]