from django.contrib import admin
from .models import Transaction, Partner


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction_type', 'amount', 'account', 'date')
    list_filter = ('transaction_type', 'account', 'date')
    search_fields = ('description',)


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


