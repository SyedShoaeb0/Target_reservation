from django.urls import path
from authentication import views as auth_views

urlpatterns = [
    path('login/', auth_views.login_view, name='login_view'),
    path('logout/', auth_views.logout_user, name='logout'),
    path('register/', auth_views.register, name='register'),
    path('book_target/', auth_views.book_target, name='book_target'),
    path('release_target/', auth_views.release_target, name='release_target'),  # New URL for releasing targets
    # Other URL patterns for your application
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)