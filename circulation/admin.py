from django.contrib import admin
from circulation.models import Loan, Reservation

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display  = ("book", "borrower", "borrowed_at", "due_date", "returned_at")
    list_filter   = ("due_date", "returned_at")
    search_fields = ("book__title", "borrower__username")

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display  = ("book", "requester", "created_at", "fulfilled")
    list_filter   = ("fulfilled",)
    search_fields = ("book__title", "requester__username")
