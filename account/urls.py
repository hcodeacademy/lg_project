from django.contrib import admin
from django.urls import path
from. import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'account'

urlpatterns = [
    path('', views.index, name="homepage"),
    path('account/form/', views.user_form_view, name="user_form"),
    path('account/detail/<str:user_id>/', views.user_detail_view, name='user-detail'),
    path('account/detail/<str:user_id>/download/<str:name>', views.generate_pdf, name='download'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
