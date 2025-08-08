from rest_framework import viewsets
from .models import Member, BorrowRecord
from .serializers import MemberSerializer, BorrowRecordSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsLibrarianGroupOnly, IsMemberGroupOnly
from django.contrib.auth.models import Group

class MemberViewSet(viewsets.ModelViewSet):
    serializer_class = MemberSerializer
    filterset_fields = ['username', 'email']
    permission_classes = [IsLibrarianGroupOnly]

    def get_member_group(self):
        if not hasattr(self, '_member_group'):
            self._member_group = Group.objects.get(name="Member")
        return self._member_group

    def get_queryset(self):
        member_group = self.get_member_group()
        return Member.objects.filter(groups=member_group)

class BorrowRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing borrow records.

    Permissions:
    - Admins have full access.
    - Librarians can access full CRUD operations.

    Actions:
    - mine (GET): Members can retrieve their own active borrow records.

    Usage:
    - /records/mine/ returns borrow records where the logged-in user is the member and book is not returned.
    """
    queryset = BorrowRecord.objects.select_related('member', 'book').all()
    serializer_class = BorrowRecordSerializer
    permission_classes = [IsLibrarianGroupOnly]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsMemberGroupOnly])
    def mine(self, request):
        """
        Retrieve active borrow records for the logged-in member.

        Returns a list of borrow records where:
        - member is the logged-in user
        - returned_at is null (book not yet returned)
        """
        records = BorrowRecord.objects.filter(
            member=request.user,
            returned_at__isnull=True
        ).select_related('book')
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)
