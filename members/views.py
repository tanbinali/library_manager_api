from rest_framework import viewsets
from .models import Member, BorrowRecord
from .serializers import MemberSerializer, BorrowRecordSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    filterset_fields = ['username', 'email']
    
class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
    filterset_fields = ['member', 'book', 'return_date']
