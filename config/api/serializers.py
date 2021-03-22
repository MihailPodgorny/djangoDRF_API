from rest_framework.serializers import ModelSerializer

from .models import Wallet, Transaction


class WalletSerializer(ModelSerializer):
    """ При методах PUT и PATCH из сериализатора удаляется поле balance"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'view' in self.context and self.context['view'].action in ['update', 'partial_update']:
            self.fields.pop('balance', None)

    class Meta:
        model = Wallet
        fields = ['id', 'name', 'owner', 'balance']


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'wallet', 'operation', 'value', 'comment']
