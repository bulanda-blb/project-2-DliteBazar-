from django.urls import path
from . import views


urlpatterns = [
    path('', views.profile_page, name = 'profile_page'),
    path('edit_image/<int:image_id>/', views.edit_image_details, name='edit_image'),
    path('checkout/<int:image_id>/', views.checkout, name='checkout'),
    path('view-purchased-image-details/<int:purchased_id>/', views.purchased_image_details, name='purchased_image_details'),
    path('view-sold-image-details/<int:sold_id>/', views.sold_image_details, name='sold_image_details'),
    path('verify-accout', views.user_verification_centre, name = 'user_verification' ),
    path('notification-centre', views.notifications, name="notifications"),
    path('toggle-email-notification/', views.toggle_email_notification, name='toggle_email_notification'),
    path('tansactions-details', views.transactions, name="transactions"),
    path('complaint-solved/<int:ticket_id>/', views.complaint_solved, name='complaint_solved'),
    
         
    
]

