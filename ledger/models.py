from django.db import models


class Partner(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        INCOME = 'INCOME', 'Income'
        EXPENSE = 'EXPENSE', 'Expense'

    class Account(models.TextChoices):
        PARTNER1 = 'PARTNER1', 'Jouhar'
        PARTNER2 = 'PARTNER2', 'Aleena'
        COMPANY = 'COMPANY', 'Lsofito innovations'

    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    account = models.CharField(max_length=10, choices=Account.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-id']

    def __str__(self) -> str:
        return f"{self.transaction_type} {self.amount} on {self.date} -> {self.account}"


