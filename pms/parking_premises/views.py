from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import *
from parking_premises.forms import CreatePremiseForm, CreateSlotForm
from parking_premises.models import Premises, Slot, BookParking
from users.mixin import CustomActiveLoginRequiredMixin
from datetime import datetime


# Create your views here.


class PremiseListView(CustomActiveLoginRequiredMixin, ListView):
    model = Premises
    template_name = "premises/premises_list.html"
    context_object_name = "all_premises"
    paginate_by = 10

    def get_queryset(self):
        queryset = Premises.objects.filter(premise_user=self.request.user).active()
        return queryset


class PremiseCreateView(CustomActiveLoginRequiredMixin, CreateView):
    template_name = "premises/premise_create.html"
    form_class = CreatePremiseForm
    success_url = "premises-list"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.premise_user = self.request.user
        instance.save()
        return super(PremiseCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Premises Is Successfully Created.")
        return self.success_url


class PremiseDeleteView(CustomActiveLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        premise_id = kwargs.get("pk")
        premise_obj = Premises.objects.get(id=premise_id)
        if premise_obj:
            premise_obj.delete()
            messages.success(request, f"Premise is deleted successfully.")
        return redirect("parking_premises:premises_list")


class SlotListView(CustomActiveLoginRequiredMixin, ListView):
    model = Slot
    template_name = "premises/slot_list.html"
    context_object_name = "all_slots"
    paginate_by = 10

    def get_queryset(self):
        queryset = Slot.objects.filter(
            premise_slot__premise_user=self.request.user
        ).active()
        return queryset


class SlotCreateView(CustomActiveLoginRequiredMixin, CreateView):
    template_name = "premises/slot_create.html"
    form_class = CreateSlotForm
    success_url = "slot-list"

    def form_valid(self, form):
        form.save()
        return super(SlotCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Slot Is Successfully Created.")
        return self.success_url


class SlotDeleteView(CustomActiveLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        slot_id = kwargs.get("pk")
        slot_obj = Slot.objects.get(id=slot_id)
        if slot_obj:
            slot_obj.delete()
            messages.success(request, f"Slot is deleted successfully.")
        return redirect("parking_premises:slot_list")


class AllSlotView(CustomActiveLoginRequiredMixin, ListView):
    model = Slot
    template_name = "premises/all_slots.html"
    context_object_name = "all_slots"
    paginate_by = 10

    def get_queryset(self):
        vehicle_type = self.request.GET.get("car_type", None)
        start_date = self.request.GET.get("start_date", None)
        end_date = self.request.GET.get("end_date", None)
        self.start_date = ""
        self.end_date = ""

        if start_date and end_date and vehicle_type:
            queryset = Slot.objects.all().active()
            start_date = datetime.strptime(start_date, "%d/%m/%Y %H:%M")
            end_date = datetime.strptime(end_date, "%d/%m/%Y %H:%M")
            booking_slots = BookParking.objects.filter(
                start_time__lte=end_date, end_time__gte=start_date
            ).values_list("slot_book", flat=True)
            self.start_date = str(start_date)
            self.end_date = str(end_date)
            if booking_slots:
                queryset = queryset.exclude(id__in=booking_slots)

            if queryset.count() == 0:
                messages.error(self.request, f"All parking slot is booked.")
        else:
            queryset = Slot.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["start_date"] = self.start_date
        data["end_date"] = self.end_date
        return data


class BookParkingSlotView(CustomActiveLoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        start_date = self.request.POST.get("book_start_date", [])
        end_date = self.request.POST.get("book_end_date", [])
        slot_id = self.request.POST.get("slot_id", [])
        converted_start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        converted_end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
        obj = BookParking.objects.create(
            slot_book_id=slot_id,
            user=request.user,
            start_time=converted_start_date,
            end_time=converted_end_date,
        )
        if obj:
            messages.success(request, f"Slot is Booked successfully.")
        else:
            messages.error(request, f"Slot is not book successfully.")

        return redirect("parking_premises:all_slots")
