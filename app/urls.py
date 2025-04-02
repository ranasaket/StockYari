from django.urls import path
from . import views

urlpatterns = [
   path('get-data/<int:index_id>/', views.DailyPriceAPIView.as_view(), name='get-data'),
]
