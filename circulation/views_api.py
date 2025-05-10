from rest_framework import viewsets, permissions
from circulation.models import Loan, Reservation
from circulation.serializers import LoanSerializer, ReservationSerializer
from api.permissions import IsLibrarianOrAdmin, IsOwnerOrStaff
from rest_framework import mixins

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsLibrarianOrAdmin | IsOwnerOrStaff]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.groups.filter(name__in=["Bibliotecario", "Admin"]).exists():
            return qs
        return qs.filter(borrower=self.request.user)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        # Bibliotecario o Admin pueden ver todas
        if self.request.user.groups.filter(name__in=["Bibliotecario", "Admin"]).exists():
            return qs
        # Cliente → sólo sus reservas
        return qs.filter(requester=self.request.user)


