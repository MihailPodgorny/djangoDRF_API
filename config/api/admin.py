from django.contrib import admin
from .models import Transaction, Wallet


class TransactionAdmin(admin.ModelAdmin):
    fields = ('wallet', 'operation', 'value', 'comment')


class WalletAdmin(admin.ModelAdmin):
    fields = ('name', 'owner', 'balance')


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Wallet, WalletAdmin)

