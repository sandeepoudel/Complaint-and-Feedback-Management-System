
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import complaint_list, home_view, login_view, signup_view, logout_view, submit_complaint, complaint_detail

urlpatterns = [
    path("", home_view, name="home"),
    path("signup/", signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name="logout"),

    path('complaints/', complaint_list, name='complaint_list'),
    path('complaints/<int:pk>/', complaint_detail, name='complaint_detail'),
    path('complaints/submit/', submit_complaint, name='submit_complaint'),
]
urlpatterns += static(settings.MEDIA_URL, 
                      document_root=settings.MEDIA_ROOT)