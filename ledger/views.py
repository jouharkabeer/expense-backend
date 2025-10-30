from datetime import date as date_class
from decimal import Decimal

from django.db.models import Sum, Case, When, F, DecimalField
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        tx_type = self.request.query_params.get('type')
        if tx_type in ('INCOME', 'EXPENSE'):
            qs = qs.filter(transaction_type=tx_type)
        return qs


@api_view(['GET'])
def summary(request):
    # Compute totals
    income_total = (
        Transaction.objects.filter(transaction_type='INCOME').aggregate(total=Sum('amount'))['total']
        or Decimal('0')
    )
    expense_total = (
        Transaction.objects.filter(transaction_type='EXPENSE').aggregate(total=Sum('amount'))['total']
        or Decimal('0')
    )

    # Account balances (partners and company)
    def account_balance(account_code: str) -> Decimal:
        agg = Transaction.objects.filter(account=account_code).aggregate(
            inc=Sum(Case(When(transaction_type='INCOME', then=F('amount')), output_field=DecimalField())),
            exp=Sum(Case(When(transaction_type='EXPENSE', then=F('amount')), output_field=DecimalField())),
        )
        inc = agg['inc'] or Decimal('0')
        exp = agg['exp'] or Decimal('0')
        return inc - exp

    partner1 = account_balance('PARTNER1')
    partner2 = account_balance('PARTNER2')
    company = account_balance('COMPANY')

    total_balance = partner1 + partner2 + company

    return Response(
        {
            'income_total': str(income_total),
            'expense_total': str(expense_total),
            'total_balance': str(total_balance),
            'partner1_balance': str(partner1),
            'partner2_balance': str(partner2),
            'company_balance': str(company),
            'today': date_class.today().isoformat(),
        }
    )


