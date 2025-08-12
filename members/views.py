from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.models import Group

from .models import Member, BorrowRecord
from .serializers import MemberSerializer, BorrowRecordSerializer
from api.permissions import IsLibrarianGroupOnly, IsMemberGroupOnly


class MemberViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing library members.

    Permissions:
    - Only users in the 'Librarian' group can access this.
    """
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

    @swagger_auto_schema(
        operation_summary="List members",
        operation_description="Retrieve a list of all members filtered by username or email.",
        responses={200: MemberSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve member",
        operation_description="Get details of a specific member by ID.",
        responses={200: MemberSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create member",
        operation_description="Create a new member (librarians only).",
        request_body=MemberSerializer,
        responses={201: MemberSerializer()},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update member",
        operation_description="Fully update a member (librarians only).",
        request_body=MemberSerializer,
        responses={200: MemberSerializer()},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update member",
        operation_description="Partially update a member (librarians only).",
        request_body=MemberSerializer,
        responses={200: MemberSerializer()},
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete member",
        operation_description="Delete a member (librarians only).",
        responses={204: 'No Content'},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class BorrowRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing borrow records.

    Permissions:
    - Librarians and Admins have full CRUD access.
    - Members can retrieve their own active borrow records via `/records/mine/`.
    """
    queryset = BorrowRecord.objects.select_related('member', 'book').all()
    serializer_class = BorrowRecordSerializer
    permission_classes = [IsLibrarianGroupOnly]

    @swagger_auto_schema(
        operation_summary="List borrow records",
        operation_description="Retrieve a list of all borrow records.",
        responses={200: BorrowRecordSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve borrow record",
        operation_description="Get details of a specific borrow record by ID.",
        responses={200: BorrowRecordSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create borrow record",
        operation_description="Create a new borrow record (librarians only).",
        request_body=BorrowRecordSerializer,
        responses={201: BorrowRecordSerializer()},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update borrow record",
        operation_description="Fully update a borrow record (librarians only).",
        request_body=BorrowRecordSerializer,
        responses={200: BorrowRecordSerializer()},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update borrow record",
        operation_description="Partially update a borrow record (librarians only).",
        request_body=BorrowRecordSerializer,
        responses={200: BorrowRecordSerializer()},
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete borrow record",
        operation_description="Delete a borrow record (librarians only).",
        responses={204: 'No Content'},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        method='get',
        operation_summary="List active borrow records for current member",
        operation_description=(
            "Retrieve all active borrow records where the logged-in user is the member "
            "and the book has not yet been returned."
        ),
        responses={200: BorrowRecordSerializer(many=True)},
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsMemberGroupOnly])
    def mine(self, request):
        records = BorrowRecord.objects.filter(
            member=request.user,
            returned_at__isnull=True
        ).select_related('book')
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)
