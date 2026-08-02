from django.urls import path, include

from . import views

from rest_framework.routers import DefaultRouter

router: DefaultRouter = DefaultRouter()
router.register(r'tables', views.BookingViewSet)

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name="about"),
   path('menu/', views.menu, name='menu'),
    path('menu_item/<int:pk>/', views.display_menu_item, name='menu_item'),
    path('bookings/', views.bookings, name="bookings"),
    path('book/', views.book, name='book'),
    # API paths
    path('menu/<int:pk>', views.SingleMenuItemView.as_view(), name='menu-item'),
    path('booking/', include(router.urls)),
]

