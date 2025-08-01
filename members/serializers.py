from rest_framework import serializers
from .models import Member, BorrowRecord
from books.models import Book

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'username', 'email', 'membership_date']

class BorrowRecordSerializer(serializers.ModelSerializer):
    member = serializers.StringRelatedField(read_only=True)
    member_id = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all(), write_only=True, source='member')
    book = serializers.StringRelatedField(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), write_only=True, source='book')

    class Meta:
        model = BorrowRecord
        fields = ['id', 'book', 'book_id', 'member', 'member_id', 'borrow_date', 'return_date']

    def create(self, validated_data):
        book = validated_data['book']
        if not book.availability:
            raise serializers.ValidationError({'error': 'Book is not available'})
        book.availability = False
        book.save()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return_date = validated_data.get('return_date')
        if return_date and not instance.return_date:
            instance.book.availability = True
            instance.book.save()
        return super().update(instance, validated_data)


