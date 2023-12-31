
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.socialaccount.urls')),

    path('',views.home,name='home'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('collaboration/',views.collaboration,name='collaboration'),
    path('contact/',views.contact, name='contact'),
    path('collaboration/',views.collaboration, name='collaboration'),
    path('success_submission/',views.success_submission, name='success_submission'),
    path('investment/',views.investment, name='investment'),
    path('investment_product/',views.investment_product, name='investment_product'),
    path('investment/<int:investment_id>/add_to_favorite/', views.add_to_favorite, name='add_to_favorite'),
    path('remove_from_favorite/<int:investment_id>/', views.remove_from_favorite, name='remove_from_favorite'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('product/<int:subfield_item_id>/', views.product_detail, name='product_detail'),
    path('categories/', views.display_categories, name='display_categories'),
    path('search/',views.search_view, name='search_view'),
    path('about_us/', views.about_us, name='about_us'),

    path('order_product/<int:product_id>/',views.order_product, name='order_product'),
    path('order_investment/<int:investment_id>/',views.order_investment, name='order_investment'),
    path('job-application/',views.job_application_form, name='job_application_form'),
    path('job-application/success/', views.job_application_success, name='job_application_success'),
    path('product_assistance/',views.product_assistance, name='product_assistance'),
    path('assistance_successful/',views.assistance_successful, name='assistance_successful'),



 
     # <<----- AUTHENTICATIN ----->>
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    

     # <<----- RESET PASSWORD BY EMAIL ----->>
    path('reset_password/', auth_views.PasswordResetView.as_view
         (template_name='auth/reset_password.html')
         ,name='reset_password'),


    path('reset-password_sent/', auth_views.PasswordResetDoneView.as_view
         (template_name='auth/password_reset_sent.html')
         ,name='password_reset_done'),


    path('reset-password_complete/', auth_views.PasswordResetCompleteView.as_view
         (template_name='auth/change_password_done.html')
         ,name='password_reset_complete'),


    path('reset/uidb64/<token>',auth_views.PasswordResetConfirmView.as_view
          (template_name='auth/change_password_done.html')
         ,name='password_reset_confirm'),


]




urlpatterns += static(settings.STATIC_URL , document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)