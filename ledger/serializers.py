from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id',
            'transaction_type',
            'amount',
            'description',
            'date',
            'account',
            'created_at',
        ]


