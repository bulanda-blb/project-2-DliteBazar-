from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user-management/', views.user_management, name='user_management'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('deactivate-user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('activate-user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('image-management/', views.image_management, name='image_management'),
    path('deactivate/<int:image_id>/', views.deactivate_image, name='deactivate_image'),
    path('activate/<int:image_id>/', views.activate_image, name='activate_image'),
    path('withdrawals/', views.withdrawal_requests, name="withdrawal_requests"),
    path('approve/<int:request_id>/', views.approve_withdrawal, name="approve_withdrawal"),
    path('reject/<int:request_id>/', views.reject_withdrawal, name="reject_withdrawal"),
    path('complaints-management/', views.complaints_section, name="complaints_section"),
    path('support-tickets/<int:ticket_id>/', views.ticket_details, name='ticket_details'),
    path('user-verification-requests/',views.user_verification_requests, name='user_verification_requests'),
    path('accepted_document/<int:verification_id>/', views.accepted_document, name='accepted_document'),
    path('rejected_document/<int:verification_id>/', views.rejected_document, name='rejected_document'),
    path('contact-us/', views.contact_us_data, name='contact_us'),
    path('send_email/<int:contact_id>/', views.send_email, name='send_email'),
]




