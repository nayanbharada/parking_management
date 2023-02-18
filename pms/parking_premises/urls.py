from django.urls import path
from . import views

app_name = "parking_premises"

urlpatterns = [
    path("premises-list", views.PremiseListView.as_view(), name="premises_list"),
    path("premises-create", views.PremiseCreateView.as_view(), name="premises_create"),
    path("premises-delete/<int:pk>/", views.PremiseDeleteView.as_view(), name="premises_delete"),
    path("slot-list", views.SlotListView.as_view(), name="slot_list"),
    path("slot-create", views.SlotCreateView.as_view(), name="slot_create"),
    path("slot-delete/<int:pk>/", views.SlotDeleteView.as_view(), name="slot_delete"),
    path('all_slots', views.AllSlotView.as_view(), name="all_slots"),
    path('book_parking_slot/', views.BookParkingSlotView.as_view(), name='book_parking_slot')

]
